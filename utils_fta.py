from itertools import product


def generate_bit_combinations(n):
    # Use itertools.product to generate all combinations of 0 and 1 for the given length
    bit_combinations = list(product("01", repeat=n))
    # Convert the tuples to strings
    bit_combinations = [''.join(bits) for bits in bit_combinations]
    return bit_combinations


def fault_sorter(element):
    parts = element.split('_')
    wire_part = parts[0][1:]

    if len(parts) == 2:
        fan_part = "-1"
        stuck_part = parts[1]
    else:
        fan_part = parts[1]
        stuck_part = parts[2]

    return int(wire_part), int(fan_part), stuck_part


def create_fault_table(input_values, all_discovered_faults, all_faults):
    fault_table = []
    # Create a 2D table where each row corresponds to an input vector, and columns indicate discovered elements
    for binary, output in zip(input_values, all_discovered_faults):
        row = [1 if element in output else 0 for element in all_faults]
        fault_table.append([binary] + row)
    # Add header row
    fault_table = [["-"] + all_faults] + fault_table
    return fault_table


def find_cols_index(fault_table, row_index):
    cols_index = [index for index, value in enumerate(fault_table[row_index]) if value == 1]
    return cols_index


def find_essential(fault_table):
    for col_index in range(1, len(fault_table[0])):
        # Calculate the sum of elements in the current column
        col_sum = sum(row[col_index] for row in fault_table[1:])
        if col_sum == 1:
            # Find the corresponding row index and add it to the list of rows to be removed
            row_index = [i for i, value in enumerate(fault_table[1:]) if value[col_index] == 1][0] + 1
            cols_index = find_cols_index(fault_table, row_index)
            return row_index, cols_index
    return None


def find_needed(fault_table):
    max_sum = float('-inf')
    row_max_sum_index = None
    for row_index, row in enumerate(fault_table[1:], start=1):
        row_sum = sum(row[1:])
        if row_sum > max_sum:
            max_sum = row_sum
            row_max_sum_index = row_index
    if max_sum < 1:
        return None
    cols_index = find_cols_index(fault_table, row_max_sum_index)
    return row_max_sum_index, cols_index


def prune_table(fault_table, row_index, cols_index):
    new_fault_table = [
        [fault_table[i][j] for j in range(len(fault_table[i])) if j not in cols_index]
        for i in range(len(fault_table)) if i not in [row_index]
    ]
    return new_fault_table


def prune_iterator(fault_table, finder, verbose=0):
    finder_tests = []
    new_fault_table = fault_table
    while True:
        finder_out = finder(new_fault_table)

        if finder_out is None:
            if verbose:
                print_table(new_fault_table[1:])
            return finder_tests, new_fault_table

        row_index, cols_index = finder_out
        finder_test = new_fault_table[row_index][0]
        finder_tests.append(finder_test)

        if verbose:
            print_table(new_fault_table[1:])
            print(f"Test: {finder_test}")
            print(f"Row Num: {row_index}")
            print(f"Cols Num: {cols_index}")
            print("-" * 10)

        new_fault_table = prune_table(new_fault_table, row_index, cols_index)


def print_table(fault_table):
    for row in fault_table:
        print(row)
