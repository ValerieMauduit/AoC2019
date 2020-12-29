def incoder(opcodes):
    n = 0
    while n <= len(opcodes):
        code = opcodes[n]
        if code == 1:
            opcodes[opcodes[n + 3]] = opcodes[opcodes[n + 1]] + opcodes[opcodes[n + 2]]
        elif code == 2:
            opcodes[opcodes[n + 3]] = opcodes[opcodes[n + 1]] * opcodes[opcodes[n + 2]]
        elif code == 99:
            n = len(opcodes)
        else:
            n = len(opcodes)
        n += 4

    return opcodes