
from string import ascii_lowercase
from sys import argv
from typing import List, Set, Tuple, Dict

#############################################################
# PASSWORD RULES
# 1. One increasing straight of at least 3 letters (abc, efg)
# 2. No i, o, l
# 3. At least two different pairs of letters (aa, ee, zz)

# Password incrementing basicaly works like an odometer
# but with letters instead of numbers
#############################################################


# -----------------------------------------------------------
# Check validity of password
# -----------------------------------------------------------

def has_no_illegal_vals(pw: str) -> bool:
    return all(ch not in 'iol' for ch in pw)


def has_straight(pw: str, lower_case_letters: str = ascii_lowercase) -> bool:
    for i in range(len(pw) - 2):
        three_chars = pw[i:(i+3)]
        if three_chars in lower_case_letters:
            return True
    return False


def has_two_pairs(pw: str) -> bool:
    pairs = 0
    for i in range(len(pw) - 1):
        if pw[i] == pw[i+1]:
            pairs += 1
            i += 2
        else:
            i += 1
    
    return pairs >= 2

def has_two_pairs(pw: str) -> bool:
    # Make all possible pairs
    poss_pairs = [ch1 + ch2 for ch1, ch2 in zip(ascii_lowercase, ascii_lowercase)]

    pairs = []
    for p in poss_pairs:
        if p in pw:
            pairs.append(p)
    
    return len(pairs) >= 2


def is_valid(pw: str) -> bool:
    return (
        has_no_illegal_vals(pw) and
        has_straight(pw) and
        has_two_pairs(pw)
    )


# -----------------------------------------------------------
# Increment password, ignoring the rules
# Plan to increment, check validity. 
# If good, done. If not, roll again.
# This is not efficient but the password isn't very long...
# -----------------------------------------------------------

def roll_password(pw: str) -> str:
    letters = list(ascii_lowercase)
    mapped_numbers = list(range(26))

    char_to_dig : Dict[str, int] = dict(zip(letters, mapped_numbers))
    dig_to_char : Dict[int, str] = dict(zip(mapped_numbers, letters))

    forbidden_digs = [char_to_dig[ch] for ch in 'iol']
    
    pw_as_ints = [char_to_dig[ch] for ch in pw]

    i = len(pw_as_ints) - 1     # Start at the right
    while i>= 0:
        pw_as_ints[i] += 1
        if pw_as_ints[i] == 26:
            pw_as_ints[i] = 0   # roll back to 'a'
            i -= 1      # move to next i (left)
            continue

        if pw_as_ints[i] in forbidden_digs:
            pw_as_ints[i] += 1
            for v in range(i + 1, len(pw_as_ints)):
                pw_as_ints[v] = 0   # reset all values after illegal val to 0
            break
        else:
            break   # No rollover or forbidden - might break straight and pair rules but ok for now

    return ''.join([dig_to_char[d] for d in pw_as_ints])


def next_good_password(pw: str) -> str:
    curr_pw = pw
    while True:
        curr_pw = roll_password(curr_pw)
        if is_valid(curr_pw):
            return curr_pw


if __name__ == "__main__":
    # My input = vzbxxyzz
    input_str = argv[1]
    
    part1_pass = next_good_password(input_str)

    print("Part 1 next password :", part1_pass)
    print("Part 2 next next password:", next_good_password(part1_pass))
