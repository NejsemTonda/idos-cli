from dataclasses import dataclass

@dataclass
class Transport:
    name: str
    when: str
    f: str
    finish: str
    t: str
    
    def __repr__(self):
        raise NotImplementedError("repr for Tranport was not implemented")


class Connection:
    def __init__(self, transports: list[Transport]):
        self.transports = transports
        # TODO

    def __repr__(self):
        raise NotImplementedError("repr for Connection was not implemented")
 
