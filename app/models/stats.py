from dataclasses import dataclass, asdict
from app.helpers.file import read_json, write_json

@dataclass
class Metric:
    processed: int = 0
    success: int = 0
    failed: int = 0

@dataclass
class AppStats:
    metrics: Metric
    last_file: str = "-"
    last_error: str = "-"

    @classmethod
    def load(cls, file_path: str) -> "AppStats":
        stats_data = read_json(file_path)

        if not stats_data:
            return cls(metrics=Metric())

        raw_metrics = stats_data.get("metrics", {})
        metric_obj = Metric(
            processed=raw_metrics.get("processed", 0),
            success=raw_metrics.get("success", 0),
            failed=raw_metrics.get("failed", 0)
        )

        return cls(
            metrics=metric_obj,
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
        self.last_file = file_name,
        self.last_error = str(error)
        self.save(file_path)

    def save(self, file_path: str):
        write_json(file_path, asdict(self))