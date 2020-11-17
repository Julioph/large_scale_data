

def encode_list(s_list):
    """Generator object."""
    """Yields the count of each item in the list"""
    # if same as before: yield +1
    # if new, yield one
    i = 0
    while i <= len(s_list)-1:
        count = 1

        if i == len(s_list)-1:
            yield [s_list[i],count]
            return

        while s_list[i] == s_list[i + 1]:
            count += 1
            i += 1
        yield [s_list[i],count]
        i += 1


def create_list(s_list):
    """Main function"""
    """Returns the run-length encoded list"""
    encoded_list = []
    for j in encode_list(s_list):
        encoded_list.append(j)

    # print(encoded_list)
    return encoded_list


# The following is called if you execute the script from the commandline
# e.g. with python solution.py
if __name__ == "__main__":
    # create_list([1, 1, 1, 2, 3, 3, 4, 4, 5, 1, 1, 7, 5])
    assert create_list([1, 1, 1, 2, 3, 3, 4, 4, 5, 1,1,7,5]) == [[1, 3], [2, 1], [3, 2], [4, 2], [5, 1], [1, 2], [7, 1], [5, 1]]
