"""
Problem 5

A nice string is one with all of the following properties:

It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
"""

# Part 1: How many strings are nice?

raw_input = open('05_input.txt', 'r').readlines()


def check_vowels(string_to_check, num_vow=3):
    vowels_good = False
    vowels = set(('a', 'e', 'i', 'o', 'u'))
    vowel_count = 0
    for s in string_to_check:
        if s in vowels:
            vowel_count += 1
    if vowel_count > 2:
        vowels_good = True
    return vowels_good


def check_repeats(string_to_check, repeated_times=2):
    unique_letters_to_check =list(set(list(string_to_check)))
    repeats_good = False
    repeated_list = []
    for letter in unique_letters_to_check:
        repeated = letter * repeated_times
        if repeated in string_to_check:
            repeats_good = True
            repeated_list.append(repeated)
    return repeats_good, repeated_list


def check_forbidden_strings(string_to_check, forbidden=['ab', 'cd', 'pq', 'xy']):
    forbidden_good = True
    for pair in forbidden:
        if pair in string_to_check:
            forbidden_good = False
    return forbidden_good


def string_is_nice(string_to_check, n_vowels=3, repeat_times=2, forbidden=['ab', 'cd', 'pq', 'xy']):
    vowels = check_vowels(string_to_check, n_vowels)
    repeats = check_repeats(string_to_check, repeat_times)
    forbidden_strings = check_forbidden_strings(string_to_check, forbidden)
    return vowels and repeats[0] and forbidden_strings


nice = []
for string in raw_input:
    nice.append(string_is_nice(string))

print(f"Part 1: There are {sum(nice)} nice strings.")

"""
Part 2
Now, a nice string is one with all of the following properties:

It contains a pair of any two letters that appears at least twice in the string without overlapping, 
like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
It contains at least one letter which repeats with exactly one letter between them, 
like xyx, abcdefeghi (efe), or even aaa.
"""


def skip_match(string_to_check):
    skip_match_good = False
    for i in range(len(string_to_check) - 2):
        if string_to_check[i] == string_to_check[i+2]:
            skip_match_good = True
    return skip_match_good


def pair_repeat(string_to_check):
    pair_good = False
    for i in range(len(string_to_check) - 1):
        pair = string_to_check[i:i+2]
        if string_to_check.count(pair) > 1:
            pair_good = True
    return pair_good


def string_is_nice_again(string_to_check):
    skip_good = skip_match(string_to_check)
    pairs_good = pair_repeat(string_to_check)
    return skip_good and pairs_good


nice2 = []
for t in raw_input:
    nice2.append(string_is_nice_again(t))

print(f"With new rules, there are {sum(nice2)} nice strings.")

