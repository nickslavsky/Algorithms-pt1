def sort_and_count(input_list):
    n = len(input_list)
    if n < 2:
        return (input_list, 0)
    else:
        left_sorted, left_count = sort_and_count(input_list[:n//2])
        right_sorted, right_count = sort_and_count(input_list[n//2:])
        parent_sorted, split_count = merge_and_count_split_inv(left_sorted, right_sorted)
    return parent_sorted, left_count+right_count+split_count

def merge_and_count_split_inv(left, right):
    temp = []
    split_count = 0
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            temp.append(left[i])
            i += 1
        else:
            temp.append(right[j])
            split_count += len(left)-i
            j += 1
    temp += left[i:]
    temp += right[j:]
    return temp, split_count

if __name__ == '__main__':
    a = []
    with open('IntegerArray.txt') as file:
        for line in file:
            a.append(int(line))
    sorted_list, count = sort_and_count(a)
    print(count)
    
