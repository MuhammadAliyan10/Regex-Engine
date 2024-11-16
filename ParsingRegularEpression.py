def parseSplit(r, idx):
    idx, prev = parseConcat(r, idx)
    while idx < len(r):
        if r[idx] == ')':  # Exit on closing parenthesis
            break
        assert r[idx] == "|", "Expected '|' but found something else"
        idx, node = parseConcat(r, idx + 1)
        prev = ('split', prev, node) 
    return idx, prev


def parseConcat(r, idx):
    prev = None
    while idx < len(r):
        if r[idx] in "|)": 
            break
        idx, node = parseNode(r, idx)
        if prev is None:
            prev = node
        else:
            prev = ('cat', prev, node)  
    return idx, prev


def parseNode(r, idx):
    ch = r[idx]
    idx += 1
    assert ch not in "|)", "Unexpected character in node"
    if ch == "(":
        idx, node = parseSplit(r, idx)
        if idx < len(r) and r[idx] == ")": 
            idx += 1
        else:
            raise Exception("Unbalanced Parenthesis")
    elif ch == '.':
        node = 'dot'
    elif ch in "*+{":  
        raise Exception("Nothing to repeat")
    else:
        node = ch
    idx, node = parsePostfix(r, idx, node)
    return idx, node


def parsePostfix(r, idx, node):
    if idx == len(r) or r[idx] not in "*+{":
        return idx, node  
    ch = r[idx]
    idx += 1
    if ch == "*":
        rMin, rMax = 0, float('inf')
    elif ch == "+":
        rMin, rMax = 1, float('inf')
    elif ch == "{":  
        idx, rMin = parseInt(r, idx)
        if rMin is None:
            raise Exception("Expected Integer")
        rMax = rMin
        if idx < len(r) and r[idx] == ",":
            idx, rMax = parseInt(r, idx + 1)
            rMax = rMax if rMax is not None else float('inf')
        if idx < len(r) and r[idx] == "}":
            idx += 1
        else:
            raise Exception("Unbalanced brace")
    else:
        raise Exception(f"Unexpected postfix operator '{ch}'")
    if rMin > rMax:
        raise Exception("Minimum repetitions cannot be greater than maximum")
    node = ('repeat', node, rMin, rMax)
    return idx, node


def parseInt(r, idx):
    start = idx
    while idx < len(r) and r[idx].isdigit():
        idx += 1
    return idx, int(r[start:idx]) if start != idx else None


def reParse(r):
    if not r:
        return None
    idx, node = parseSplit(r, 0)
    if idx != len(r): 
        raise Exception("Unexpected character at the end")
    return node


# Tests
assert reParse("") is None
assert reParse(".") == "dot"
assert reParse("a") == "a"
assert reParse("ab") == ('cat', 'a', 'b')
assert reParse("a|b") == ('split', 'a', 'b')
assert reParse("a+") == ('repeat', 'a', 1, float('inf'))
assert reParse("a{3,6}") == ('repeat', 'a', 3, 6)
assert reParse("a|bc") == ('split', 'a', ('cat', 'b', 'c'))
assert reParse("ab|c") == ('split', ('cat', 'a', 'b'), 'c')
assert reParse("(a|b)c") == ('cat', ('split', 'a', 'b'), 'c')

