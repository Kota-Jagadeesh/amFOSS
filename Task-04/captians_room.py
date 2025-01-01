#Input 
K=int(input())
room_numbers=list(map(int,input().split()))
#Using a formula to find the Captain's room
unique_room=set(room_numbers)
captains_room=(sum(unique_room)*K-sum(room_numbers))//(K - 1)
# Output 
print(captains_room)
