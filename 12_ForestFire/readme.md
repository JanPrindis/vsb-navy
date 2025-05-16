# TASK 12 - Forest Fire

Cílem úkolu bylo vytvořit buněčný automat, který bude simulovat požár lesu. 

---
## Postup
- Vytvoří se matice reprezentující mapu, kde každá buňka bude s pravěpodobností 50 % (`density`) strom, nebo prázdné.
- Poté se spustí simulace.
- Každý tick simulace:
  - Pokud je aktuální buňka _**prázdná**_
    - S pravděpodobností 5 % (`p`) se přemění na strom, jinak zůstane prázdná
  - Pokud je aktuální buňka _**ohořelý strom**_
    - Přemění se na prázdnou buňku
  - Pokud aktuální buňka _**hoří**_
    - Přemění se na ohořelou
  - Pokud je buňka _**strom**_
    - Pokud hoří jeden ze stromů v sousedství (definováno podle `neighborhood`), tak začně hořet
    - Pokud žádný ze sousedů nehoří
      - S pravděpodobností 0.1 % dojde k samovznícení
      - Jinak zůstává stromem

---

## Sousedství
- Lze nastavit 2 typy sousedství podle parametru předaného v konstruktoru třídy
  - _**Von Neumann**_ - Sousedi se počítají pouze nahoře, dole, vlevo a vpravo
  - _**Moore**_ - Navíc obsahuje diagonální sousedy

## Výstup
- Po zavolání metody `run` se spustí simulace prostředí.
- Pro lepší vizualizaci obou voleb sousedů se po spuštění mainu vytvoří separátní instance pro každého z nich.

![](./result.gif)

(Výstup skriptu, [Imgur link na gif](https://imgur.com/a/niE6fGn))
