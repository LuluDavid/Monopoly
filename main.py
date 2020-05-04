# This is an attempt to recreate the game Monopoly, because we do not want to pay
# for it on Steam, and mostly because we are very bored during this quarantine.

import json
import random
from src.classes import User, Board, Street, Box, Game



def initGame():

    with open("boxes.json") as boxes_file:
        json_boxes = json.loads(boxes_file.read())

    boxes = []

    for box in json_boxes:
        if json_boxes[box]["type"] == "street":
            boxes.append(
                Street(
                    int(box), 
                    json_boxes[box]["type"], 
                    json_boxes[box]["name"], 
                    json_boxes[box]["price"], 
                    json_boxes[box]["rent"], 
                    json_boxes[box]["color"]
                )
            )
        else:
            boxes.append(
                Box(
                    int(box),
                    json_boxes[box]["type"],
                    json_boxes[box]["name"]
                )
            )
    return Board(boxes)
    
def initPlayers():    #beginning of the game only
    playersNumber = input("Combien y a-t-il de joueurs ?")
    while (int(playersNumber)<=1):
        playersNumber = input("Le jeu doit comporter au minimum 2 joueurs. Combien y a-t-il de joueurs ? ")
    L=[]     #list with all the names of the players
    for i in range(int(playersNumber)):
        player = input("Quel est le nom du joueur"+str(i+1)+" ?")
        L.append(User(player))
    return L
    
def orderOfPlayers(L):
    input("Bienvenue à tous dans cette super partie de Monopoly, nous avons tout d'abord tirer au sort l'ordre de jeu des différents joueurs")
    random.shuffle(listOfPlayers)
    n=len(listOfPlayers)
    for i in range(n):
        print("Le joueur "+str(i+1)+" est "+listOfPlayers[i].name)
    return listOfPlayers
    
    
def actualizePosition(order, i, dice):
    oldPosition = order[i].position
    if (oldPosition+dice < 40):
        order[i].position = oldPosition + dice
    else :
        order[i].position = (oldPosition+dice-40)
        
        
def buyAStreetOrNot(player):
    pos = player.position
    case=board.boxes[pos]
    if (case.box_type == "street"):
        price = case.price[0]
        if (case.owner == None  and player.money>=price):
            choice = input("Cette propriété est libre, son prix est de "+str(price)+" euros. Voulez-vous l'acheter ? (Il vous reste "+str(player.money)+ " euros)")
            if (choice.lower() == "oui".lower()):
                player.goods.append(board.boxes[pos])
                board.boxes[pos].owner = player
                player.money = player.money - price
                input("Vous venez d'acheter la propriété "+ str(case.name) +". Il vous reste "+str(player.money)+ " euros.")
            else : 
                input("Vous avez décider de ne pas acheter, vous avez toujours "+str(player.money)+" euros.")
        else : 
            if (case.owner == None and player.money<price):
                input("Cette propriété est libre, malheureusement vous n'avez pas assez d'argent pour l'acheter. Il vous reste "+ str(player.money) +" euros et le prix est de "+str(price) + " euros.")
            else :      #the street belongs to someone
                ownerName = case.owner.name
                if (case.owner == player):
                    input("Cette propriété vous appartient. Vous ne pouvez rien faire")
                else:
                    rent = case.rent[0]
                    print("Cette propriété appartient à "+ownerName+", vous lui devez "+str(rent)+" euros.")
                    player.money = player.money - rent
                    print("Il vous reste "+str(player.money)+" euros.")
                    case.owner.money = case.owner.money + rent
                    input(""+ownerName+" gagne "+str(rent)+" euros, il lui reste "+str(case.owner.money)+" euros.")
    else:
        input("ce n'est pas une rue, pour l'instant vous ne pouvez pas l'acheter.")
                
    
    
def turn(order):                         #one turn
    numberOfPlayers = len(order)
    for i in range(numberOfPlayers):
        dice=random.randint(2,12)
        print(""+order[i].name+", tu as fait "+ str(dice))
        actualizePosition(order,i,dice)
        pos = order[i].position
        playerStreetPosition = board.boxes[pos].name
        input("Tu es sur la case : " + playerStreetPosition)
        buyAStreetOrNot(order[i])
    for player in order:
        if (player.money <0):
            input(""+ player.name+ ", tu as perdu! Tu n'as plus d'argent.")
            order.remove(player)
    return order
    
    
    


if __name__ == "__main__":
    board = initGame()
    #for box in board.boxes:
        #print("{} - TYPE : {} \t\t NAME : {}".format(box.index, box.box_type, box.name))
    listOfPlayers = initPlayers()
    numberOfPlayers = len(listOfPlayers)
    order = orderOfPlayers(listOfPlayers)
    while len(order)>=2:
        order = turn(order)
    print(""+order[0].name+"!! TU AS GAGNE !!!!!!")
    
        
    

































