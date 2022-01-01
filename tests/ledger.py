from distributed_structures.ledger import ledger

l = ledger()
# b = l.add("test")
# b = l.add("2")

# for n in range(1000):
#     l.add( 46 * (n + 101) )

print(sum(l))