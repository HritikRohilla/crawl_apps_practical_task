def find_number(number_list, n):
    # Calculate the sum of integers from 1 to n
    total_sum = n * (n + 1) / 2
    
    # Calculate the sum of elements in the given list
    arr_sum = sum(number_list)
    
    # Find the missing number
    missing_number = int(total_sum) - arr_sum
    return missing_number

# Example list and value of n
number_list = [4, 5, 3, 2, 8, 1, 6, 9, 10, 15, 12, 11, 14, 13]
total_value_to_present = 15

# Find and priint the missing number
print("Missing number:", find_number(number_list, total_value_to_present))