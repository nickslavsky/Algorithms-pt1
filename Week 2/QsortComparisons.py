def quick_sort_and_comp_count(input_list, left, right):
    if right - left < 2:
        return 0
    p = choose_median(input_list, left, right)
    split = partition(input_list, left, p, right)
    comp_count = right - left - 1
    comp_count += quick_sort_and_comp_count(input_list, left, split)
    comp_count += quick_sort_and_comp_count(input_list, split + 1, right)
    return comp_count


def partition(input_list, left, p, right):
    if p != left:  # Assume pivot    =    1
        input_list[p], input_list[left] = input_list[left], input_list[p]
    pivot = input_list[left]
    i = left + 1
    j = left + 1
    while j < right:
        if input_list[j] < pivot:
            input_list[i], input_list[j] = input_list[j], input_list[i]
            i += 1
        j += 1
    input_list[left], input_list[i - 1] = input_list[i - 1], input_list[left]
    return i - 1


def choose_first(input_list, left, right):
    return left


def choose_last(input_list, left, right):
    return right - 1


def choose_median(input_list, left, right):
    candidates = [left,  right - 1, left + (right - left - 1) // 2]
    return sorted(candidates, key=lambda idx: input_list[idx])[1]


if __name__ == '__main__':
    with open('QuickSort.txt') as file:
        a = [int(line) for line in file]
    count = quick_sort_and_comp_count(a, 0, len(a))
    print(count)
