def read_number_pairs(filename):
    """
    Read pairs of numbers from a file.
    
    Args:
    - filename (str): The path to the file to read.
    
    Returns:
    - list of tuple: A list of tuples where each tuple contains a pair of numbers.
    """
    number_pairs = []

    # Open the file for reading
    with open(filename, 'r') as f:
        # Loop through each line in the file
        for line in f:
            # Split the line by spaces to get the two numbers
            num1, num2 = map(int, line.split())
            
            # Append the numbers as a tuple to the list
            number_pairs.append((num1, num2))
    
    return number_pairs

# Example usage
pairs = read_number_pairs('input.txt')
print(pairs)
