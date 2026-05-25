from datetime import datetime
from decimal import Decimal

class Transaction:
    def __init__(
        self,
        account_id: str,
        date: str,
        amount: float,
        name: str,
        description: str = None,
        notes: str = None,
        currency: str = None,
        category_id: str = None,
        merchant_id: str = None,
        nature: str = "expense",
        tag_ids: list[str] = None
    ):
        self.account_id = account_id
        self.date = date #YYYY-MM-DD
        self.amount = amount
        self.name = name
        self.description = description
        self.notes = notes
        self.currency = currency
        self.category_id = category_id
        self.merchant_id = merchant_id
        self.nature = nature
        self.tag_ids = tag_ids or []

    def to_json(self):
        data = {
            "account_id": self.account_id,
            "date": self.date,
            "amount": self.amount,
            "name": self.name,
            "nature": self.nature,
        }

        if self.description:
            data["description"] = self.description
        if self.notes:
            data["notes"] = self.notes
        if self.currency:
            data["currency"] = self.currency
        if self.category_id:
            data["category_id"] = self.category_id
        if self.merchant_id:
            data["merchant_id"] = self.merchant_id
        if self.tag_ids:
            data["tag_ids"] = self.tag_ids

        return data
    
    @classmethod
    def from_ofx_data(cls, sure_account_id, data):
        txn_date = data.get("date")

        if isinstance(txn_date, datetime):
            txn_date = txn_date.date().isoformat()
        
        txn_amount = data.get("amount")
        if isinstance(txn_amount, Decimal):
            txn_amount = float(txn_amount)
        
        txn_description = data.get("description") or data.get("payee") or "Transaction"
        txn_nature = "income" if data.get("type") == "credit" else "expense"

        transaction = Transaction(
            account_id=sure_account_id,
            date=txn_date,
            amount=txn_amount,
            name=txn_description,
            description=txn_description,
            nature=txn_nature,
            currency=data.get("currency")
        )

        return transaction

