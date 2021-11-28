arr = []
f = open('account_data_example.txt')
for x in f:
    arr.append(f"{x.rstrip().split(', ')[0]}:{x.rstrip().split(', ')[1]}")
print(arr)
print("B91302781:RK5kA1" in arr)