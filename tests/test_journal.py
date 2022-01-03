from distributed_structures.journal_block import journal_block
from distributed_structures.journal import journal
from distributed_structures.subroutines import hash_string
from json import dumps

def test_journal_block_creation():
    jb = journal_block()
    jb.value = 1
    assert type(1) == jb.type
    block_dict = {
        'body': {
            'value': 1,
            'type': 'int'
        },
        'next': None
    }
    assert jb.digest() == hash_string(dumps(block_dict))

def test_journal():
    j = journal()
    print(j)

if __name__ == "__main__":
    test_journal_block_creation()
    test_journal()