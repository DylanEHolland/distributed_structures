from datetime import datetime
from distributed_structures.subroutines import hash_string, type_to_string
from distributed_structures.common import types
from json import dumps, loads

class journal_block:
    # Blocks need to store a single value, the values type and what comes after it (if applicable)
    def __init__(self, **args):
        self.previous = None
        self.next = None
        self.value = None
        self.type = type(None)
        if 'from_dict' in args:
            print("Loading block")
        else:
            self.timestamp = datetime.now()
    
    def __str__(self):
        return f"<{self.digest()}>"
    
    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)
        if key == "value":
            object.__setattr__(self, 'type', type(value))
    
    def data_digest(self):
        return hash_string(self.serialize(data_only=True))

    def digest(self):
        return hash_string(self.serialize())
    
    def to_dict(self):
        return {
            'body': {
                'value': self.value,
                'type': self.type
            },
            'previous': self.previous,
            'next': self.next
        }

    def serialize(self, data_only = False):
        data = self.to_dict()
        b_type = data['body']['type']
        data['body']['type'] = type_to_string(b_type)

        if data_only:
            del data['previous']
            del data['next']

        return dumps(data)