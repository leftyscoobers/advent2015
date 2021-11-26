"""
Problem 4: Find the lowest number appended to the input that produces an md5 hash that starts with five zeros...
"""

import hashlib

input = 'iwrupvqb'


def test_for_zeros(hex_string, num_zeros=5):
    return hex_string[:num_zeros] == '0' * num_zeros

# I don't know much about this so start with brute force... :-\
def find_lowest_int(input_string, zeros=5):
    found_answer = False
    integer = 0
    while not found_answer:
        integer += 1
        if integer % 10000 == 0:
            print(integer)
        full_string = input_string + str(integer)
        encoded = hashlib.md5(full_string.encode())
        found_answer = test_for_zeros(encoded.hexdigest(), num_zeros=zeros)
    return integer

pt1_int = find_lowest_int(input, 5)
print(f"Lowest integer is {pt1_int}")

# Part 2: now do the same but with 6 zeros...
pt2_int = find_lowest_int(input, 6)
print(f"Lowest integer is {pt2_int}")