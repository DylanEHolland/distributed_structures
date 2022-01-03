class distributed_list:
    def __init__(self, **args):
        is_node = args.get('is_node')
        if is_node:
            print("This is not just a simple list")
        print("mfw")
        