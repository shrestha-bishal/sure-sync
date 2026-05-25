from parsers.ofx_parser import OfxParser
from parsers.account_mapping_parser import AccountMappingParser

class Parser:
    def __init__(self):
        self.parsers = {
            "ofx": OfxParser(),
            "yml": AccountMappingParser()
        }

    def parse(self, file_path):
        extension = file_path.lower().split(".")[-1]

        parser = self.parsers.get(extension)

        if not parser:
            raise ValueError(f"No parser available for .{extension} files")
        
        return parser.parse(file_path)