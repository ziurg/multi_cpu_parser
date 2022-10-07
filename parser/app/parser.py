from dataclasses import dataclass
from typing import Dict, List, Optional


def coroutine(func):
    """
    Wrapper fonction to avoid initialisation
    of generator function (no need to call
    the next method before to get values).
    """

    def starter(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen

    return starter


@dataclass
class Parser:
    nodes: Optional[Dict[int, List[float]]] = None
    elements: Optional[Dict[int, List[int]]] = None

    def __post_init__(self):
        self.nodes = {}
        self.elements = {}

    def read(self, filepath: str) -> str:
        prs = self.parse()
        with open(filepath) as f:
            lines = f.readlines()
            for line in lines:
                prs.send(line)

    @coroutine
    def parseNodes(self):
        """Parsing line containing node informations.

        The node informations should be provided in the
        following format :
        .NOE I 12 X 1.32 Y -0.23 Z 0. ATT 1
        """
        while True:
            line = yield
            sline = (l for l in line.split() if l != ".NOE")
            dline = dict(zip(sline, sline))
            self.nodes[int(dline["I"])] = [
                float(v) for v in [dline["X"], dline["Y"], dline["Z"]]
            ]

    @coroutine
    def parseElements(self):
        """Parsing line containing element informations.

        The element informations should be provided in the
        following format :
        .MAI I 11 N 13 12 11 14 ATT 2
        """
        while True:
            line = yield
            try:
                sline = line.split()
                self.elements[int(sline[2])] = [int(v) for v in sline[4:8]]
            except:
                pass

    @coroutine
    def parse(self):
        nodes = self.parseNodes()
        elements = self.parseElements()
        #
        while True:
            line = yield
            if line.startswith(".NOE"):
                nodes.send(line)
            elif line.startswith(".MAI"):
                elements.send(line)

    def get_nodes(self) -> Dict[int, List[float]]:
        return self.nodes

    def get_elements(self) -> Dict[int, List[int]]:
        return self.elements
