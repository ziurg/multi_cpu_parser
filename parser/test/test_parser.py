from app.parser import Parser


def test_parse_get_nodes():
    p = Parser()
    nodes = {1: [1.2, -4.5, 0.0], 2: [6.7, 0.0, -8.9]}
    p.nodes = nodes
    assert p.get_nodes() == nodes


def test_parse_get_elements():
    p = Parser()
    elements = {1: [2, 3, 4], 2: [5, 6, 7, 8]}
    p.elements = elements
    assert p.get_elements() == elements


def test_node_parser():
    p = Parser()
    parser_nodes = p.parseNodes()
    line = ".NOE I 12 X 1.32 Y -0.23 Z 0. ATT 1"
    parser_nodes.send(line)
    nodes = p.get_nodes()
    assert nodes == {12: [1.32, -0.23, 0.0]}


def test_element_parser():
    p = Parser()
    parser_elements = p.parseElements()
    line = ".MAI I 11 N 13 12 11 14 ATT 2"
    parser_elements.send(line)
    elements = p.get_elements()
    assert elements == {11: [13, 12, 11, 14]}


def test_parser():
    with open("example.txt", "w") as f:
        f.write(".NOE I 12 X 1.32 Y -0.23 Z 0. ATT 1\n")
        f.write(".MAI I 11 N 13 12 11 14 ATT 2\n")
    p = Parser()
    p.read("example.txt")
    nodes = p.get_nodes()
    assert nodes == {12: [1.32, -0.23, 0.0]}
    elements = p.get_elements()
    assert elements == {11: [13, 12, 11, 14]}
