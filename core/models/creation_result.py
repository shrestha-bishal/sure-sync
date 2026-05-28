from dataclasses import dataclass

@dataclass
class CreationResult:
    is_successful: bool
    is_duplicate: bool
    message: str = ""