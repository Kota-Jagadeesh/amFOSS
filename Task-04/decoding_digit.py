# Input string
S = input()

# Initialize a list of 10 zeros for the digits 0 through 9
digit_count = [0] * 10

#Iterate through each character in the string
for char in S:
    #Check if the character is a digit
    if char.isdigit():
        #Increment the count of the digit
        digit_count[int(char)] += 1
#Print the frequency of each digit separated by spaces
print(' '.join(map(str, digit_count)))
