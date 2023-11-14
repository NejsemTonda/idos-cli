from dataclasses import dataclass

@dataclass
class Transport:
    name: str
    when: str
    f: str
    finish: str
    t: str
    
    def __repr__(self):
        return f"{self.name}\n  {self.when} {self.f} \n  {self.finish} {self.t}" 


class Connection:
    def __init__(self, transports: list[Transport]):
        assert len(transports) > 0, "no transports in connection"
        self.transports = transports
        self.start = transports[0].when
        self.finish = transports[-1].finish

    def __repr__(self):
        ts = []
        for t in self.transports:
            for line in repr(t).split("\n"):
                ts.append(line)

        l = len(max(ts, key=lambda x: len(x)))+1
        times = f"{self.start} --> {self.finish}"
        l = max(l, len(times)+3)
 
        ret = f"|-- {times} " + "-"*(l - len(times)-3) + "|\n"
        ts =[f"| {t}" + " "*(l-len(t)) + "|" for t in ts]
        ret += "\n".join(ts)
        ret += "\n|-" + "-"*l+"|"

        return ret
