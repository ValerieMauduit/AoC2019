# --- Day 4: Secure Container ---

# First star:
# You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password
# on a sticky note, but someone threw it out.
# However, they do remember a few key facts about the password:
# - It is a six-digit number.
# - The value is within the range given in your puzzle input.
# - Two adjacent digits are the same (like 22 in 122345).
# - Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or
# 135679).
# How many different passwords within the range given in your puzzle input meet these criteria?
# Your puzzle input is 387638-919123.

# Second star:
# An Elf just remembered one more important detail: **the two adjacent matching digits are not part of a larger group of
# matching digits**.
# How many different passwords within the range given in your puzzle input meet all of the criteria?

def run(star):
    if star == 1:
        nbpswd = 0
        for n in range(387638, 919123 + 1):
            pwd = str(n)
            modif = '0' + pwd[:5]
            if any([l1 == l2 for (l1, l2) in zip(pwd, modif)]):
                if all([int(l1) >= int(l2) for (l1, l2) in zip(pwd, modif)]):
                    nbpswd += 1
        print(f'Star {star} - There are {nbpswd} different passwords in the range')
        return nbpswd

    elif star == 2:
        nbpswd = 0
        for n in range(387638, 919123 + 1):
            pwd = str(n)
            modif = '0' + pwd[:5]
            if any([l1 == l2 for (l1, l2) in zip(pwd, modif)]):
                if all([int(l1) >= int(l2) for (l1, l2) in zip(pwd, modif)]):
                    modif = pwd + '0'
                    diffs = [1] + [int(modif[n]) - int(modif[n - 1]) for n in range(1, 6)] + [1]
                    if any([((diffs[n] == 0) & (diffs[n - 1] >= 1) & (diffs[n + 1] >= 1)) for n in range(1, 6)]):
                        nbpswd += 1

        print(f'Star {star} - There are {nbpswd} different passwords in the range')
        return nbpswd

    else:
        raise Exception('Star number must be either 1 or 2.')
