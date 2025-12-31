import yaml

class AccountMappingParser:
    def parse(self, file_path):
        # Extract account mappings
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
            return data.get("accounts", {})