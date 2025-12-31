from ofxparse import OfxParser as OfxLibParser

class OfxParser:
    def parse(self, file_path):
        with open(file_path) as f:
            ofx = OfxLibParser.parse(f)

        data = []
        for account in ofx.accounts:
            for transaction in account.statement.transactions:
                data.append({
                    "bank_id":account.bank_id,
                    "account_id": account.account_id,
                    "transaction_id": transaction.id,
                    "type": transaction.type,
                    "date": transaction.date,
                    "amount": transaction.amount,
                    "description": transaction.memo,
                    "payee": getattr(transaction, "payee", None),
                })
        return data