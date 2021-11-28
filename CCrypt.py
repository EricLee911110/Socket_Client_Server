a = "RK5kA1"
crypted = ""
for x in a:
    if x.isupper():
        crypted += chr((((ord(x) - 2) -65) %26) +65) 
    elif x.islower():
        crypted += chr((((ord(x) -2) -97) %26) +97)
    else:
        crypted += chr((((ord(x) -2) -48) %10) +48)

print(crypted)



