
class Mortal:
    """
    Represents a mortal(person, individual, etc Immortals not allowed),
    holds name, socket client, and IP address
    """

    def __init__(self, client_addr, client):
        self.client_addr = client_addr
        self.client = client
        self.name = None


    def set_name(self,name):
        """
        sets the name for the mortal
        :param name: str
        :return: None
        """
        self.name = name

    def __repr__(self):
        return f"Mortal({self.client},{self.client_addr})"
