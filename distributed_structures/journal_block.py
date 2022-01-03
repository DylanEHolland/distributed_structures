from datetime import datetime

class journal_block:
    # Blocks need to store a single value, the values type and what comes after it (if applicable)

    def __init__(self, **args):
        if 'from_dict' in args:
            print("Loading block")
        else:
            self.timestamp = datetime.now()
    
    def __str__(self):
        return "<>"
    
    def digest(self):
        return "FFF"