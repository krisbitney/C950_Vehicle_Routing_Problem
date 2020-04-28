class Destination:

    def __init__(self, lid, name, address):
        self.lid = lid
        self.name = name
        self.address = address

    def __eq__(self, other):
        return (self.lid == other.lid and
                self.name == other.name and
                self.address == other.address)

    def __hash__(self):
        hash_code = 1
        hash_code = 31 * hash_code + hash(self.lid)
        hash_code = 31 * hash_code + hash(self.name)
        hash_code = 31 * hash_code + hash(self.address)
        return hash_code

    def __repr__(self):
        return ("Destination(" +
                self.lid + ", " +
                self.name + ", " +
                self.address + ")")
