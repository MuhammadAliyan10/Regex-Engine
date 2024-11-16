
def reParse(r):
    idx, node = parseSplit(r, 0)
    if idx != len(r):
        raise Exception("Unexpected ')'")
    return node


assert reParse("") is None
assert reParse(".") == "dot"
assert reParse("a") == "a"
assert reParse("ab") == ('cat', 'a', 'b')
assert reParse("a|b") == ('split', 'a', 'b')
assert reParse("a+")  == ('repeat', 'a', 1, float('inf'))
assert reParse("a{3,6}") == ('repeat', 'a', 3, 6)
assert reParse("a|bc") == ('split', 'a', ('cat', 'b', 'c'))


def parseSplit(r,idx):
    idx, prev = parseConcat(r, idx)
    while idx < len(r):
        if r[idx] == ')':
            break
        assert r[idx] == "|", "BUG"
        idx,node = parseConcat(r, idx + 1)
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
    
    def parseNode(r,idx):
        ch = r[idx]
        idx += 1
        assert ch not in "|)"
        if ch == "(":
            idx, node = parseSplit(r,idx)
            if idx < len(r) and r[idx] == ")":
                idx += 1
            else:
                raise Exception("Unbalanced Parenthesis")
        elif ch == '.':
            node = 'dot'
        elif ch == '*+{':
            raise Exception("Nothing to repeat")
        else:
            node = ch
        idx, node = parsePostfix(r, idx, node)
        return idx, node
    
    def parsePostfix(r,idx,node):
        if idx == len(r) or r[idx] == "*+{":
            return idx, node
        ch = r[idx]
        idx += 1
        if ch == "*":
            rMin, rMax = 0, float('inf')
        elif ch == "+":
            rMin, rMax = 1, float('inf')
        else:
            idx, i = parseInt(r,idx)
            if i in None:
                raise Exception("Expected Integer")
            rMin =  rMax = i
            if idx < len(r) and r[idx] == ",":
                idx, j = parseInt(r, idx + 1)
                rMax = j if (j is not None) else float('inf')
            if idx < len(r) and r[idx] == "}":
                idx += 1
            else:
                raise Exception("Unbalance brace")
        if rMin > rMax:
            raise Exception("Min repeat is greater then Max repeat")
        node = ('repeat',node, rMin, rMax)
        return idx, node
    
    def parseInt(r, idx):
        save = idx
        while idx < len(r) and r[idx].isdigit():
            idx += 1
        return idx, int(r[idx:save]) if save != idx else None
    

        




