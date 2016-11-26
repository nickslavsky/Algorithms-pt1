import logging
import sys


def two_sum_sorting(numbers_set, range_start, range_end):
    logger.info('Started function that uses sorting')
    numbers_sorted = sorted(numbers_set)
    logger.info('Done sorting')
    start = 0
    end = len(numbers_set) - 1
    result = set()

    logger.info('Entering main while loop')
    while start < end:
        tmp = numbers_sorted[start] + numbers_sorted[end]
        if tmp > range_end:
            end -= 1
        elif tmp < range_start:
            start += 1
        else:
            result.add(tmp)
            for i in range(start + 1, end):
                t = numbers_sorted[i] + numbers_sorted[end]
                if check_in_range(t, range_start, range_end):
                    result.add(t)
                else:
                    break
            end -= 1
    logger.info('Done looping')  # approx 1.6s
    return len(result)


def two_sum_hash(numbers_set, range_start, range_end):
    logger.info('Started function that uses set lookup')
    result = set()
    for i in range(range_start, range_end):
        for n in numbers_set:
            if i - n in numbers_set and i - n != n:
                result.add(i)
    logger.info('Finished set lookup')  # more than 60min
    return len(result)


def check_in_range(number, range_start, range_end):
    if range_start < number < range_end:
        return True
    else:
        return False


if __name__ == '__main__':
    # initialize logging to console
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(name)s %(levelname)s %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    # actual start
    logger.info('Program started')
    nums = set()
    # load data
    with open('algo1-programming_prob-2sum.txt') as data:
        for line in data:
            raw = line.strip()
            if raw:
                i = int(raw)
                nums.add(i)
    logger.info('Data loaded from file')
    print(two_sum_sorting(nums, -10000, 10000))
    # print(two_sum_hash(nums, -10000, 10000))
    logger.info('Program end')
