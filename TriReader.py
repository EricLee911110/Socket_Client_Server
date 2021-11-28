arr = []
f = open('traingle_data_example.txt') 
for x in f:
    arr.append(x.rstrip())
print(arr)
print(arr[1])

def person(name):
    name = name
    happy(name)

def happy(name):
    name = name
    print(f"{name} is happy!")

person("Eric")