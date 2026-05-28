from dataclasses import dataclass, asdict, field
from core.helpers.file import read_json, write_json
from typing import List
from datetime import datetime

@dataclass
class Metric:
    processed: int = 0
    success: int = 0
    failed: int = 0

@dataclass
class Account:
    bank_name: str = "Unknown Bank"
    account_name: str = "Unnamed Account"
    account_num: str | None = None
    last_transaction: datetime | None = "-"
    last_sync: datetime | None = "-"

@dataclass
class AppStats:
    metrics: Metric = field(default_factory=Metric)
    accounts: List[Account] = field(default_factory=list)
    last_file: str = "-"
    last_error: str = "-"

    @classmethod
    def load(cls, file_path: str, valid_mappings: dict | None = None) -> "AppStats":
        stats_data = read_json(file_path) or {}

        # metrics
        raw_metrics = stats_data.get("metrics", {})
        metric_obj = Metric(
            processed=raw_metrics.get("processed", 0),
            success=raw_metrics.get("success", 0),
            failed=raw_metrics.get("failed", 0)
        )

        # accounts
        raw_accounts = stats_data.get("accounts", [])
        accounts: List[Account] = []

        if valid_mappings is not None:
            historical_map = {}
            if isinstance(raw_accounts, list):
                for acc in raw_accounts:
                    if isinstance(acc, dict) and acc.get("account_num"):
                        historical_map[acc.get("account_num")] = acc

            for ofx_key, mapping in valid_mappings.items():
                account_num = "xxxx"

                if ":" in ofx_key:
                    parts = ofx_key.split(":", 1)
                    raw_num = parts[1] if parts[1] else ""
                    account_num += raw_num[-4:] if len(raw_num) >=4 else raw_num
                else:
                    account_num += ofx_key[-4:] if len(ofx_key) >= 4 else ofx_key

                account_obj = Account(
                    bank_name=mapping.bank_name or "Unknown Bank",
                    account_name=mapping.account_name or "Unnamed Account",
                    account_num=account_num
                )

                accounts.append(account_obj)
        else:
            for acc in raw_accounts:
                accounts.append(Account(
                    bank_name=acc.get("bank_name", "Unknown Bank"),
                    account_name=acc.get("account_name", "Unnamed Account"),
                    account_num=acc.get("account_num"),
                    last_transaction=acc.get("last_transaction", "-"),
                    last_sync=acc.get("last_sync", "-")
                ))

        return cls(
            metrics=metric_obj,
            accounts=accounts,
            last_file=stats_data.get("last_file", "-"),
            last_error=stats_data.get("last_error", "-")
        )         

    def on_success(self, file_name: str, file_path: str):
        self.metrics.processed += 1
        self.metrics.success += 1
        self.last_file = file_name
        self.last_error = "-"
        self.save(file_path)

    def on_failure(self, file_name: str, error: Exception, file_path: str):
        self.metrics.processed += 1
        self.metrics.failed += 1
        self.last_file = file_name
        self.last_error = str(error)
        self.save(file_path)

    def save(self, file_path: str):
        write_json(file_path, asdict(self))