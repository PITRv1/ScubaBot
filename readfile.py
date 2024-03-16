
def LoadPositionsFromFile():
    gyongyok = open("gyongyok.txt") # gyongyok.txt megnyitása
    sorok = gyongyok.readlines() # gyongyok.txt kiolvasása

    gyongyok.close() # gyongyok.txt bezárása
    sorok.pop(0) # Legelső sor eltávolítása (x;y;z;e; sor)

    positions = [] # Rendezett pozicíók listája

    for i in range(len(sorok)):
        sor = sorok[i].split(";") # Elemek poziciójának és értéküknek eltárolása egy listába -> ["x", "y", "z", "e"]
        sor = sor[:-1] # "\n" elem eltávolítsa a listából
        positions.append(sor) # Rendezett poziciók hozzáadása a listához

    return positions # Rendezett pozició lista visszaadása

print(LoadPositionsFromFile())