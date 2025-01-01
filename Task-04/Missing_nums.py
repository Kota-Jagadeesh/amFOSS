# Input
n = int(input())  # Size of the first list
A = list(map(int, input().split()))  # First list
m = int(input())  # Size of the second list
B = list(map(int, input().split()))  # Second list

# Count frequencies of numbers in A and B
from collections import Counter
count_A = Counter(A)
count_B = Counter(B)

# Find missing numbers
missing = []
for num in count_B:
    # Check if the count in B is greater than the count in A
    if count_B[num] > count_A.get(num, 0):
        missing.append(num)

# Sort the missing numbers
missing = sorted(missing)

# Output
print(*missing)
