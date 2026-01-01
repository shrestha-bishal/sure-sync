from helpers.logger import log
import re
from models.transaction import Transaction

class TransactionsClient:
    def __init__(self, base_client):
        self.base = base_client

    def list(self, params=None):
        return self.base.get("/transactions", params=params)

    def parse_amount(self, amount_str):
        # Remove currency symbols and delimiters, handle both "." and "," as decimal separators
        # Example: "$1,234.56" -> 1234.56, "1.234,56 €" -> 1234.56
        cleaned = re.sub(r'[^\d,.\-]', '', amount_str)
        # If both ',' and '.' present, assume ',' is thousands and '.' is decimal (US style)
        if ',' in cleaned and '.' in cleaned:
            if cleaned.find(',') < cleaned.find('.'):
                cleaned = cleaned.replace(',', '')
            else:
                cleaned = cleaned.replace('.', '').replace(',', '.')
        # If only ',' present, treat as decimal (EU style)
        elif ',' in cleaned:
            cleaned = cleaned.replace(',', '.')
        try:
            return float(cleaned)
        except ValueError:
            return None

    def exists(self, transaction: Transaction) -> bool:
        amount = float(transaction.amount)
        if transaction.nature == "income" and amount > 0:
            amount = -amount
        elif transaction.nature == "expense" and amount < 0:
            amount = abs(amount)

        params = {
            "account_id": transaction.account_id,
            "start_date": transaction.date,
            "end_date": transaction.date,
            "min_amount": amount,
            "max_amount": amount,
            "type": transaction.nature,
            "per_page": 100,
        }

        if transaction.name:
            params["search"] = transaction.name

        def normalize_name(name):
            return (name or "").strip().lower()

        page = 1
        while True:
            params["page"] = page
            response = self.list(params=params)
            transactions = response.get("transactions", [])

            for existing in transactions:
                existing_amount = self.parse_amount(existing.get("amount", ""))
                if (
                    normalize_name(existing.get("name")) == normalize_name(transaction.name)
                    and existing.get("currency").upper() == transaction.currency.upper()
                    and existing_amount is not None
                    and abs(existing_amount - float(transaction.amount)) < 0.01
                ):
                    return True
                
            if len(transactions) < params["per_page"]:
                break

            page += 1
        return False
    
    def create(self, transaction: Transaction):
        required = [transaction.account_id, transaction.date, transaction.amount, transaction.name]
        if not all(required):
            log(f"[ERROR] Missing required transaction fields: {required}")
            raise ValueError("Missing required transaction fields")
        
        # checking if the transaction exists
        if self.exists(transaction):
            log(
                f"[DUPLICATE] Transaction skipped | "
                f"Account: {transaction.account_id} | "
                f"Date: {transaction.date} | "
                f"Amount: {transaction.amount:.2f} {transaction.currency} | "
                f"Name: {transaction.name} | "
                f"Nature: {transaction.nature}"
            )

            return None

        payload = {"transaction": transaction.to_json()}
        log(
            f"[CREATE] Creating transaction | "
            f"Account: {transaction.account_id} | "
            f"Date: {transaction.date} | "
            f"Amount: {transaction.amount:.2f} {transaction.currency} | "
            f"Name: {transaction.name} | "
            f"Nature: {transaction.nature}"
        )

        response = self.base.post("/transactions", json=payload)
        log(f"Transaction created: {response}")
        return response.get("transaction", response)
