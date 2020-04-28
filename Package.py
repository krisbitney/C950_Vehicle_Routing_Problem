class Package:
    """
    The Package class holds package data
    """

    def __init__(self, pid, lid, address, city, state, zip_code, weight, deadline, status):
        self.pid = pid
        self.lid = lid
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.weight = weight
        self.deadline = deadline
        self.status = status

    def __eq__(self, other):
        return (self.pid == other.pid and
                self.lid == other.lid and
                self.weight == other.weight)

    def __hash__(self):
        hash_code = 1
        hash_code = 31 * hash_code + hash(self.pid)
        hash_code = 31 * hash_code + hash(self.lid)
        return hash_code

    def __repr__(self):
        return ("Package(" +
                self.pid + ", " +
                self.lid + ", " +
                self.address + ", " +
                self.city + ", " +
                self.state + ", " +
                self.zip_code + ", " +
                self.weight + ", " +
                self.deadline + ", " +
                self.status + ")")
