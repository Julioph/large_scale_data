def sublist(s_list):
    """
    Returns all the sub-lists (with ascending order)
    of input list  by using generators
    """

    k = 0
    while k <= len(s_list) - 1:
        i = k
        sublist = list()
        sublist.append(s_list[i])
        while i != len(s_list) - 1 and (s_list[i + 1] >= s_list[i]): #or s_list[i + 1] == s_list[i] + 1):
            sublist.append(s_list[i + 1])
            i += 1
        k = i + 1
        yield sublist


def find_commons(a, b):
    return [item for item in a if item in b]


def longest_common_list(s_list):
    """
    Create the longest_common_list function which returns
    the common longest sublist between s_list and its reverse
    """

    a = sorted(sublist(s_list), key=len, reverse=True)
    b = sorted(sublist(s_list[::-1]), key=len, reverse=True)

    # x = list()
    # for item in a: #doesn't matter which because it is sorted by length
    #     for item2 in b:
    #         f = find_commons(item, item2)
    #         if len(f) != 0:
    #             x.append(f)
    #
    # print(max(x, key=len))

    return max([find_commons(item, item2) for item in a for item2 in b], key=len)


if __name__ == "__main__":
    # print(longest_common_list([1, 1, 2, 3, 0, 0, 3, 4, 5, 7, 1, 3, 2, 1, 1, 2]))
    #Tests:
    # [4, 3, 7, 8, 9, 2, 3, 4, 0, 1, 1, 1, 2, 3, 4, 5, 6, 3]
    # [11, 10, 9, 8, 7, 1, 1, 2, 0, 2, 1, 1]
    # [1,2,3,4,0,7,1,6,3,2,1]
    # [2,3,4,0,7,1,6,3,2,1]
    # [11, 10, 9, 8, 7, 1, 1, 2, 0, 2, 1, 1]
    # [1, 1, 2, 0, 2, 1, 1, 7, 8, 9, 10, 11]
    # [1, 2, 3, 4, 3, 2, 1, 0, 7, 1, 6]
    assert longest_common_list([1, 1, 2, 3, 0, 0, 3, 4, 5, 7, 1, 3, 2, 1, 1, 2]) == [1, 1, 2, 3]
