#Player VS Computer Python Tic-Tac-Toe
#Gruppe 13

import random

# generiert ein Spielfeld in einem Array und gibt dieses zurück.
def genGrid():
    grid = []
    for row in range(3):
        grid.append([' ']*3)
    return grid


# Zeigt das Spielfeld mit den x und y Achsenwerten auf der Konsole an.
def printGrid(grid):
    colNumbers = "  "
    for colNum in range(3):
        colNumbers += str(colNum + 1) + "   "
    print(colNumbers)
    for index, row in enumerate(grid):
        rowOutput = str(index + 1) + " "
        for cellNum,cell in enumerate(row):
            rowOutput += cell + " | "
        print(rowOutput)

#Zug von Spieler X durchführen. 
#Übergeben wird das derzeitige Grid.
#Es wird überprüft, ob die Usereingabe im möglichen Bereich liegt und nicht bereits belegt ist. 
#Wenn das der Fall ist, wird der Input als X und Y Koordinate (guessX und guessY) returned.
def userInput(grid):
    while True:
        try:
            guess = input("Bitte die Koordinaten für den nächsten Zug eingeben. <x,y>: ") #nimmt den Input und übergibt ihn einer Variable, welche dann gesplittet wird
            guess = guess.split(',')
            guessX = int(guess[1])
            guessY = int(guess[0])
            if not (guessX > 0 and guessX <= 3) and (guessY > 0 and guessY <= 3): #ArrayBereich definieren, um im Spielfeld zu bleiben
                print("Maximale Koordinaten sind  " + str(3)) #Werte wenn nicht im Arraybereich
            elif grid[guessX - 1][guessY - 1] != " ":
                print("Die ausgewählte Zelle ist bereits belegt.") #Wenn die Zelle schon belegt ist
            else:
                break
        except:
            print("Beide Koordinaten müssen Integer sein: x,y") #Es müssen Integer eingegeben werden (Fehlerbehandlung)

    grid[guessX - 1][guessY - 1] = "X"
    return guessX, guessY

# Gewinnmöglichkeiten abdecken, Waagerecht, Senkrecht und Diagonal.
def winCheck(grid, player):
    return (
        (grid[0][0] == player and grid[1][0] == player and grid[2][0] == player) or # Waagerecht oberste Zeile
        (grid[0][1] == player and grid[1][1] == player and grid[2][1] == player) or # Waagerecht mittlere Zeile
        (grid[0][2] == player and grid[1][2] == player and grid[2][2] == player) or # Waagerecht unterste Zeile

        (grid[0][0] == player and grid[0][1] == player and grid[0][2] == player) or # Senkrecht linke spalte
        (grid[1][0] == player and grid[1][1] == player and grid[1][2] == player) or # Senkrecht mittlere spalte
        (grid[2][0] == player and grid[2][1] == player and grid[2][2] == player) or # Senkrecht rechte spalte

        (grid[0][0] == player and grid[1][1] == player and grid[2][2] == player) or # diagonal
        (grid[2][0] == player and grid[1][1] == player and grid[0][2] == player)    # diagonal
    )

# Kopiert das gegebene Array und gibt dieses dann zurück.
def copyGrid(grid):
    copy = []
    for index,row in enumerate(grid):
        copy.append([])
        for cell in row:
            copy[index].append(cell)
    return copy


#Berechnet den Zug des Computers. Es wird in Reihenfolge geprüft und ausgeführt ob:
#Der Computer gewinnen kann -> jenes Feld wird ausgewählt, um zu gewinnen.
#Der Spieler gewinnen kann -> jenes Feld wird ausgewählt, um den Spieler zu blockieren.
#Eine Ecke frei ist -> eine freie Ecke wird ausgewählt.
#Die Mitte frei ist -> die Mitte wird ausgewählt.
#Ansonsten -> ein freies Feld wird ausgewählt.
#Am Ende jeder Option wird das ganze als als X und Y Koordinate (rowNum und cellNum) returned.
#returned none wenn keine Option eintritt.

def aiTurn(grid):
    #Überprüft ob der Computer gewinnen kann.
    #Vergleicht alle möglichen Züge mit einem duplizierten Array um zu prüfen, ob KI gewinnen kann.
    for rowNum in range(0,3):
        for cellNum in range(0,3):
            copy = copyGrid(grid)
            if copy[rowNum][cellNum] == " ":
                copy[rowNum][cellNum] = "O"
                if winCheck(copy, "O"):
                    return rowNum, cellNum

    #Blockiert den Spieler, falls er im nächsten Zug gewinnen könnte.
    #Vergleicht alle möglichen Züge mit einem duplizierten Array, um zu überprüfen, ob der Spieler gewinnen kann, um ihn dann zu blocken.
    for rowNum in range(0,3):
        for cellNum in range(0,3):
            copy = copyGrid(grid)
            if copy[rowNum][cellNum] == " ":
                copy[rowNum][cellNum] = "X"
                if winCheck(copy, "X"):
                    return rowNum, cellNum

    #Prüft ob die Ecken frei sind, wenn ja wird eine ausgewählte Ecke gesetzt.
    possibleMoves = []
    if grid[0][0] == " ":
        possibleMoves.append([0,0])
    if grid[2][0] == " ":
        possibleMoves.append([2,0])
    if grid[0][2] == " ":
        possibleMoves.append([0,2])
    if grid[2][2] == " ":
        possibleMoves.append([2,2])

    if len(possibleMoves) > 0:
        move = random.choice(possibleMoves)
        return move[0], move[1]

    # Prüft ob die goldene Mitte noch verfügbar ist.
    if grid[1][1] == " ":
        return 1,1

    # Ansonsten eine andere freie Möglichkeit wählen.
    possibleMoves = []
    if grid[1][0] == " ":
        possibleMoves.append([1,0])
    elif grid[2][1] == " ":
        possibleMoves.append([2,1])
    elif grid[1][2] == " ":
        possibleMoves.append([1,2])
    elif grid[0][1] == " ":
        possibleMoves.append([0,1])

    if len(possibleMoves) > 0:
        move = random.choice(possibleMoves)
        return move[0], move[1]

    # Wenn keine Rückgabe vorhanden ist.
    return None

#Main Methode die das Spiel ausführt indem es alle Methoden aufruft.
if __name__ == "__main__":

    grid = genGrid() #Generiert das Spielfeld
    printGrid(grid) #Zeigt das Spielfeld an

    count = 0 #Zählerstand
    while not winCheck(grid, "X") and not winCheck(grid, "O"):  #Schleife bis der Spieler oder die KI gewonnen hat.
        if count >= 9:  # Wenn 9 Züge vorbei sind, endet das Spiel automatisch. Es wird die while-Schleife gebreakt.
            break
        count += 1 #inkrementieren des Zählers, steht für Zug +1.
        print("\n")

        #Userinput bekommen, dem Spielfeld hinzufügen und das neue Spielfeld wieder ausgeben.
        userInput(grid)
        printGrid(grid)


        if not winCheck(grid, "X"):    #Prüfe ob Spieler X im letzten Zug gewonnen hat oder nicht, wenn nicht ist die KI am Zug.
            if count >= 9:  # Wenn 9 Züge vorbei sind, endet das Spiel automatisch. Es wird die while-Schleife gebreakt.
                break
            count += 1 #inkrementieren des Zählers, steht für Zug +1.
            print("\n")

            print("KI is am Zug...")
            aiRow, aiCol = aiTurn(grid)     # berechnet den nächst bestmöglichsten Zug.
            grid[aiRow][aiCol] = "O"    # Spielzug eintragen.
            printGrid(grid)     # Neues Spielfeld ausgeben.
        else:
            break       # Spieler X hat bereits gewonnen.

    #Finales Prüfen des Spielfeldes und Gewinnerkrönung.
    if winCheck(grid, "X"):
        print("Du hast gewonnen, Champ!")
    elif winCheck(grid, "O"):
        print("KI hat gewonnen!")
    else:
        print("Unentschieden!")