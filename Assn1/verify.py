def check_coverage(selected_rows, configuration, t):
    # Assuming configuration is a list of lists, where each sub-list is a row of configurations
    # and t is the level of interaction coverage required
    from itertools import combinations
    
    # Generate all t-combinations of column indices
    column_combinations = combinations(range(len(configuration[0])), t)
    # Initialize dictionary to track coverage of each t-combination
    coverage = {comb: set() for comb in column_combinations}
    
    # Iterate over each combination of columns
    for comb in coverage:
        # Check each selected row
        for row in selected_rows:
            # Create a tuple of values in the selected columns for this row
            value_tuple = tuple(configuration[row][i] for i in comb)
            # Add this tuple to the set for the combination
            coverage[comb].add(value_tuple)
    
    # Check if all combinations are fully covered
    for comb, values in coverage.items():
        if len(values) < V**t:  # V is the number of possible values per variable
            return False, coverage
    return True, coverage

# Usage example
selected_rows = [1, 12, 17, 18, 32, 35, 36, 37, 47, 49, 54, 67, 80]
is_covered, detailed_coverage = check_coverage(selected_rows, configuration, T)
print("Is fully covered:", is_covered)
if not is_covered:
    print("Coverage details for debugging:", detailed_coverage)
