import sys
import random

# if str(input("Do you wish to generate new gems?\nAnwser here: ")) == "yes":

open('gems.txt', 'w').close()
    
f = open('gems.txt', 'w')

f.write("x;y;z;e;\n")

for i in range(99):
        
    f.write(f"{random.randint(1, 100)};{random.randint(1, 100)};10;{random.randint(1, 9)};\n")
        
f.write(f"{random.randint(1, 100)};{random.randint(1, 100)};10;{random.randint(1, 9)};")

print("Done")

f.close()