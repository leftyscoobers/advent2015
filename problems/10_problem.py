from itertools import groupby

def read_and_say(start_str: str, n: int = 1) -> str:
    """
    Take the input string and output new read-string.
    Example: '1211' -> one 1, one 2, two 1s = '111221'
    """

    curr_string = start_str
    count = 0
    while count < n:
        new_string = ''.join([str(sum(1 for _ in group)) + char for char, group in groupby(curr_string)])
        count += 1
        curr_string = new_string

    return curr_string


if __name__ == "__main__":
    input_str = '3113322113'

    print("Part 1 length of result after x40 :", len(read_and_say(input_str, n=40)))
    print("Part 2 length of result after x50 :", len(read_and_say(input_str, n=50)))