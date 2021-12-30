from datetime import datetime
from json import dumps, loads
from hashlib import new
from base64 import b64encode

class block:
    value = None
    next = None
    timestamp = None
    
    def __init__(self, **data):
        if not len(data):
            self.timestamp = datetime.now()
            self.next = None
            
    def __str__(self):
        return f"<{self.hash()}>"
    
    def hash(self):
        buffer = self.serialize(no_next=True)
        hasher = new('md5')
        hasher.update(buffer.encode())
        buffer = hasher.hexdigest()
        
        return buffer
    
    def serialize(self, no_next=False):
        buffer = self.to_dict()
        buffer['timestamp'] = buffer['timestamp'].isoformat()
        if no_next:
            del buffer['next']
        
        return dumps(buffer)
    
    def from_serialized(self, serialized):
        node = loads(serialized)
        self.timestamp = datetime.fromisoformat(node['timestamp'])
        self.next = node['next']
        self.value = node['body']['value']
        
        return self
    
    def to_dict(self):
        return {
            'timestamp': self.timestamp,
            'next': self.next,
            'body': {
                'value': self.value                
            }
        }