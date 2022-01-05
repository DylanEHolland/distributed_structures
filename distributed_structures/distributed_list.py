from distributed_structures.journal import journal

class distributed_list:
    is_node = None
    journal = None

    def __init__(self, **args):
        is_node = args.get('is_node')
        if is_node:
            print("This is not just a simple list")
            self.is_node = True
            self.journal = journal()
        else:
            self.is_node = False

    def __str__(self):
        return "[]"

    def append(self, item):
        pass