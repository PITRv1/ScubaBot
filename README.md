<p align="center">
    <img src="https://github.com/PITRv1/ScubaBot/assets/159771306/1cae5473-d150-4c05-9bd2-a19618c527dc" style="width:300px; "/>
</p>

> [!IMPORTANT]
> Amennyiben lehetséges a program futtatása közben vegye fel a hangerőt a jobb élmény elérése érdekében.
> 
> Az összeszedett pontok értékét megtalálja a pontok.txt-ben.

## TELEPÍTÉS

Töltse le a python minimum 3.12-es verzióját: [Python 3.12.2](https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe)

Amint feltelepítette a Python-t, a következő paranccsal töltse le a szükséges könyvtárakat:
```
pip install customtkinter moviepy pillow configparser ursina
```

## RÖVID ISMERTETŐ
Kaptál egy új munkát egy Sea Corp. nevezetű cégnél. A te feladatod kezelni M.I.C.H.A.E.L.-t, a búvárrobotot egy régi számítógépről és egy még régebbi operációs rendszer segítségével.

<p align="center">
    <img src="https://github.com/PITRv1/ScubaBot/assets/159771306/c6da00b1-7dcf-4a1f-bf43-ef91d7eec8a7" style="width:300px; "/>
</p>

## ÚTMUTATÓ
Lépjen be a program mappájába. Nyissa meg a _**main.py**_-t. Ez a program fogja emulálni a Sea OS-t.

<p align="center">
    <img src="https://github.com/PITRv1/ScubaBot/assets/159771306/fbf3b679-acaf-41dd-945e-4a3b7db5a2ca" style="width:400px; "/>
</p>
<p align="center">
    <img src="https://github.com/PITRv1/ScubaBot/assets/159771306/fefa9293-afa1-4ca4-b927-04ab3cacb4b8" style="width:1920px; "/>
</p>

Ha mind ez sikerült, akkor látni fog 2 darab ikont az asztal bal felső sarkában.
- **sysfo.run**: Ebben a programban találja meg a készítőket.

<p align="left">
    <img src="https://github.com/PITRv1/ScubaBot/assets/159771306/9214bd5d-fb8f-4230-9ba9-dfe1dcab2754" style="width:200px; "/>
</p>

- **buvar.run**: Ezzel a programmal tud csatlakozni M.I.C.H.E.A.L.-höz.

<p align="left">
    <img src="https://github.com/PITRv1/ScubaBot/assets/159771306/1efbd075-3d00-4c47-bcfd-0058499b0aa1" style="width:200px; "/>
</p>

---

1. Adja meg a fájlt, amely tartalmazza a gyöngyök pozicióját.
> [!NOTE]
> Figyeljen arra, hogyha a fájl eleje tartalmaz betűket, akkor kapcsolja be az **Első sor törlése** opciót, valamint ügyeljen arra, hogy a fájlban ne legyenek felesleges szóközök és sorok.

![Screenshot 2024-04-03 203150](https://github.com/PITRv1/ScubaBot/assets/159771306/51d912dc-b2e7-459f-b68a-70d1e6820c55)

---

2. Állítsa be a medencét tetszőleges méretre vagy hagyja a minimum értékeken.
![Screenshot 2024-04-03 203804](https://github.com/PITRv1/ScubaBot/assets/159771306/7f65afd8-c4f6-4ee7-863b-4b9e17bab764)

---

3. Adja meg az időt, sebességet és amennyiben szeretne belsőnézetes módot, pipálja be a dobozt.
![Screenshot 2024-04-03 204031](https://github.com/PITRv1/ScubaBot/assets/159771306/b18075f5-2956-47e5-be47-998d436f26a7)

---

4. Amennyiben van ideje, nézze végig az animációkat.
![Screenshot 2024-04-03 204247](https://github.com/PITRv1/ScubaBot/assets/159771306/2bfaff62-67aa-4924-acc5-50f270897947)

---

5. A _**buvar.run**_ program majd automatikusan bezárja magát és elindítja a 3D-s környzetet.
- Kamera forgatása
   - W: felfele
   - S: lefele
   - A: balra
   - D: jobbra

- Kamera mozgása
   - LEFT CTRL: lefele
   - SPACE: felfele
   - GÖRGŐ FEL: közelítés
   - GÖRGŐ LE:  távolodás

---

> [!NOTE]
> ![Screenshot 2024-04-03 205549](https://github.com/PITRv1/ScubaBot/assets/159771306/51142a55-81fa-4d63-8a9a-b654377564ff)
> 
> A start gombra kattintva meg tudja nyitni a start menüt, ahol be tudja zárni a Sea OS-t.

---
## ALGORITMUS LEÍRÁSA:
