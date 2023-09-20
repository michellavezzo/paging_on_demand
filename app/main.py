# Open the file for reading
with open('input.txt', 'r') as f:
    # Initialize an empty list to store the number pairs
    number_pairs = []
    
    # Loop through each line in the file
    for line in f:
        # Split the line by spaces to get the two numbers
        num1, num2 = map(int, line.split())
        
        # Append the numbers as a tuple to the list
        number_pairs.append((num1, num2))

# Print the pairs
for pair in number_pairs:
    print(pair[0], pair[1])