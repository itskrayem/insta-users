import itertools

# Define the characters to be used in combinations
characters = "abcdefghijklmnopqrstuvwxyz0123456789._"

# Generate all combinations of 3 characters
combinations = itertools.product(characters, repeat=4)

# Write combinations to a text file
with open("combinations.txt", "w") as file:
    for combo in combinations:
        file.write("".join(combo) + "\n")

print("Combinations generated and saved to 'combinations.txt'")
