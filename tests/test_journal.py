from distributed_structures.journal_block import journal_block
from distributed_structures.journal import journal
from distributed_structures.subroutines import hash_string
from json import dumps
from os.path import exists, isfile

def test_journal_block_creation():
    jb = journal_block()
    jb.value = 1
    assert type(1) == jb.type

def test_journal():
    j = journal()
    assert isinstance(j, journal)
    assert j.size() == 0
    for n in range(10):
        jb = journal_block()
        jb.value = n
        j.entry(jb)
    assert j.size() == 10
    return j

def test_journal_write(j):
    j.write()
    assert exists(j.journal_dir)

def test_journal_read(j):
    journal_dir = f"/tmp/journal-{j.uuid}"
    new_j = journal(from_dir=journal_dir)


if __name__ == "__main__":
    test_journal_block_creation()
    j = test_journal()
    test_journal_write(j)
    test_journal_read(j)