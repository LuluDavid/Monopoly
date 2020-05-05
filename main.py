# This is an attempt to recreate the game Monopoly, because we do not want to pay
# for it on Steam, and mostly because we are very bored during this quarantine.

import json
import random
from src.classes import User, Board, Street, Box, Game, Station

def main():
    #for box in board.boxes:
        #print("{} - TYPE : {} \t\t NAME : {}".format(box.index, box.box_type, box.name))
    listOfPlayers = initPlayers()    
    numberOfPlayers = len(listOfPlayers)
    order = orderOfPlayers(listOfPlayers)
    while len(order)>=2:
        order = turn(order)
    print(""+order[0].name+"!! TU AS GAGNE !!!!!!")
    
    
    
##Initialize Game

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
            if json_boxes[box]["type"] == "station":
                boxes.append(
                    Station(
                        int(box),
                        json_boxes[box]["type"], 
                        json_boxes[box]["name"], 
                        json_boxes[box]["price"]
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

    """Define the beginning of the game : how many players and what are their names"""
    
    playersNumber = input("Combien y a-t-il de joueurs ?")
    while (int(playersNumber)<=1):
        playersNumber = input("Le jeu doit comporter au minimum 2 joueurs. Combien y a-t-il de joueurs ? ")
    L=[]     #list with all the names of the players
    for i in range(int(playersNumber)):
        player = input("Quel est le nom du joueur"+str(i+1)+" ?")
        L.append(User(player))
    return L
    
    
    
def orderOfPlayers(L):
    
    """After initPlayers(), we choose randomly what is the order of play"""
    
    input("Bienvenue à tous dans cette super partie de Monopoly, nous avons tout d'abord tirer au sort l'ordre de jeu des différents joueurs")
    random.shuffle(L)
    n=len(L)
    for i in range(n):
        print("Le joueur "+str(i+1)+" est "+L[i].name)
    return L
    

##Game

def launchDices():
    dice1 = random.randint(1,6)
    dice2 = random.randint(1,6)
    return [dice1,dice2]
    
    
def actualizePosition(player):
    
    """
    Find the new position of the player after rolling dices
    Check that the player is not in jail, otherwise he can not move
    """
    
    oldPosition = player.getPosition()
    prison = player.getInPrison()
    dices = launchDices()
    totalDices = dices[0]+dices[1]
    prisonTurn = player.getPrisonTurn()
    if (prison == False):
        input(""+player.name+", tu as fait "+str(totalDices))
        if (oldPosition+totalDices < 40):
            player.setPosition(oldPosition + totalDices)
        else :
            player.setPosition(oldPosition+totalDices-40)
    else : 
        isInJail(player)
        
        

def playerHasAllColorStreets(player, positionOfStreet):
    
    """
    Check if a player has all the streets of the same color that the box on 'positionOfStreet'
    Example :chloe = User("Chloé"), position=39, 
    return True if chloe has box 39 (Rue de la paix) and 37 (champs elysées) which are dark-blue
    """
    streetColor = board.getBox(positionOfStreet).getColor()
    if (streetColor == "pink" or streetColor=="dark-blue"):
        count = 0
        n=len(player.getGoods())
        for i in range(n):
            if (player.getGoods()[i].getColor() == streetColor):
                count = count +1 
        if (count == 2):
            return True
        else: 
            return False
    else: 
        count = 0
        n=len(player.getGoods())
        for i in range(n):
            if (player.getGoods()[i].color == streetColor):
                count = count +1 
        if (count == 3):
            return True
        else:
            return False
            
            
def putHomes(player): #TODO : verify that owner has enough money to pay for houses 
    
    """
    function to allow or not the player to add houses on the box (max houses is 5)
    check 1 : does the player has all the properties of the same color ? 
    check 2 : can we still add more houses ? (if already 5 houses, we can't)
    """
    
    position = player.getPosition()
    numberOfHomes = board.getBox(position).getHome()
    priceOfHome = board.getBox(position).getPrice()[1]
    houseAvailable = 5-numberOfHomes
    if (playerHasAllColorStreets(player, player.position) == True):
        if (houseAvailable != 0):
            choice = input("Vous pouvez placer "+str(houseAvailable)+" maison(s) sur cette propriété, une maison coûte "+ str(priceOfHome)+"€. Souhaitez-vous construire ?")
            if(choice.lower() == "oui".lower()):
                nbOfHouses = input("Combien de maison souhaitez-vous construire ?")
                while (int(nbOfHouses) > houseAvailable):
                    nbOfHouses = input("Vous pouvez construire maximum "+str(houseAvailable)+" maisons, combien souhaitez-vous en construire ?")
                board.getBox(position).setHomes(board.getBox(position).getHome() + int(nbOfHouses))
                player.LooseMoney(priceOfHome*int(nbOfHouses))
                input("Vous avez construit" +str(nbOfHouses) + " maisons. Il vous reste " + str(player.money) + "€")
            else:
                input("Vous avez choisi de ne pas construire de maison")
            
                
    
    
    

##Jail


def goToJail(player):
    
    """The player went on the box 'go to jail', he is sent to jail which is in position 10"""
    
    input("Vous allez directement en prison sans passer par la case départ")
    player.setPosition(10)
    player.setInPrison(True)
    player.setPrisonTurn(0)
    
    
    
def jail_chooseToPay(player):
    
    """The player who is in jail chose to get out by paying 50€"""
    
    print("Vous avez décidé de payer 50€, vous n'êtes plus en prison")
    player.LooseMoney(50)
    player.setInPrison(False)
    player.setPrisonTurn(None)
    input("il vous reste "+str(player.getMoney())+"€")
    actualizePosition(player)
    
            
            
def jail_chooseDouble(player):
    
    """The player in jail chose not to pay or had not enough money to pay, so he has to make a double to get        out"""
    
    dices=launchDices()
    if (dices[0] == dices[1]):
        input("Bravo, vous avez fait un double "+str(dices[0])+". Vous êtes sortis de prison et avancez de "+str(2*dices[0])+"")
        player.setPosition(10+2*dices[0])
        player.setInPrison(False)
        player.setPrisonTurn(None)
    else : 
        input("Vous avez fait "+str(dices[0])+" et "+str(dices[1])+". Ce n'est pas un double vous ne sortez pas de prison")
        player.setPrisonTurn(player.getPrisonTurn()+1)       #one turn more in jail

      
def isInJail(player):
    
    """
    The player is in jail,
    case 1 : he is in prison for less than 3 turns so he has to choose between paying or make a double
    case 2 : it's been 3 turns in prison so he gets out of jail and returns to normal game 
    """
    
    turnInPrison = player.getPrisonTurn()    #how many turns since player is in jail ? 
    if (turnInPrison < 3 ):
        if (player.getMoney()>=50):
            choice = input(""+player.getUserName()+", vous avez 2 options, la première est de payer 50€ pour sortir de prison. La deuxième est d'essayer de faire des doubles, vous sortirez automatiquement au bout de 3 tours. Rq : vous pouvez payer 50 euros à chaque tour. Choisissez 1 ou 2")
            while (choice != "1" and choice !="2"):
                choice = input("Vous devez choisir 1 ou 2. 1=payer 50€, 2=attendre 3 tours en tentant de faire un double")
            if (choice == "1"):
                jail_chooseToPay(player)
            else:
                print("Vous avez choisi d'essayer de faire un double")
                jail_chooseDouble(player)
        else:
            input(""+player.getUserName()+"Vous n'avez pas assez d'argent pour sortir en payant 50€, vous pouvez tenter de sortir en faisant un double") 
            jail_chooseDouble(player)
    else :
        print("Vous avez passé 3 tours en prison, vous sortez de prison")
        player.setInPrison(False)
        player.setPrisonTurn(None)
        actualizePosition(player)
        
##        


def nbOfStations(owner):
    
    """
    How many stations does a player have ? 
    """
    
    goods = owner.getGoods()
    nb = 0
    n=len(goods)
    for i in range(n):
        if (goods[i].getType() == "station"):
            nb = nb +1
    return nb
    
    
    
def getRentStreet(player):

    """
    The rent is different if their is homes in it or if the owner has all streets of the same color
    
    """

    pos = player.getPosition()
    numberOfHomes = board.getBox(pos).getHome()
    if (numberOfHomes !=0):
        rent = board.getBox(pos).getRent()[numberOfHomes]
        return rent
    else :
        rent = board.getBox(pos).getRent()[0]            #recup value of rent withour houses to check if owner has 
        streetColor = board.getBox(pos).getColor()       # all properties with the same color 
        owner = board.getBox(pos).getOwner()
        hasAllColors = playerHasAllColorStreets(owner, pos)
        if (hasAllColors == True):
            rent = rent*2
            return rent
        else :
            return rent
            



def getRentStation(player):
    
    """
    What is the rent to pay for the player on the station (position of station is player.position)
    """
    
    pos = player.getPosition()
    case = board.getBox(pos)
    owner = case.getOwner()
    nbStations = nbOfStations(owner)
    rent = 50*nbStations
    return rent 
    
                
                
        
def onAStreet(player):
    
    """
    The player is on a street, there is different cases 
    
    case 1 : the street has no owner yet and the player has enough money to buy it, he has to choose if yes or
    not he wants it
    
    case 2 : the street has no owner yet but the player does not have enough money to buy it
    
    case 3 : the street belongs to the player, he can either do nothing or buy homes if possible 
    
    case 4 : the street belongs to someone, we use 'getRentStreet' to know what is the rent to pay
    
    """
    
    pos = player.getPosition()
    case=board.getBox(pos)
    price = case.getPrice()[0]
    if (case.owner == None  and player.money>=price):
        choice = input("Cette propriété est libre, son prix est de "+str(price)+" euros. Voulez-vous l'acheter ? (Il vous reste "+str(player.money)+ " euros)")
        if (choice.lower() == "oui".lower()):
            player.buyAStreet(case)
            input("Vous venez d'acheter la propriété "+ str(case.name) +". Il vous reste "+str(player.getMoney())+ " euros.")
            putHomes(player)    #after buying a land, putHomes verifies that the owner has all properties and if
                                #yes can offer to construct houses 
        else : 
            input("Vous avez décidé de ne pas acheter, vous avez toujours "+str(player.money)+" euros.")
    else : 
        if (case.getOwner() == None and player.getMoney()<price):
            input("Cette propriété est libre, malheureusement vous n'avez pas assez d'argent pour l'acheter. Il vous reste "+ str(player.money) +" euros et le prix est de "+str(price) + " euros.")
        else :      #the street belongs to someone
            ownerName = case.getOwner().getUserName()
            if (case.getOwner() == player):
                input("Cette propriété vous appartient")
                putHomes(player)
            else:
                rent = getRentStreet(player)
                print("Cette propriété appartient à "+ownerName+", vous lui devez "+str(rent)+" euros.")
                player.LooseMoney(rent)
                print("Il vous reste "+str(player.money)+" euros.")
                case.owner.EarnMoney(rent)
                input(""+ownerName+" gagne "+str(rent)+" euros, il lui reste "+str(case.owner.money)+" euros.")
                    
                
def onAStation(player):
    
    """
    The player is on a station, like for a street, there is different cases
    
    case 1 : no owner and enough money to buy
    case 2 : no owner but no money to buy it
    case 3 : owner = player --> nothing to do
    case 4 : owner = other player, rent with 'getRentStation'
    """
    
    
    pos = player.getPosition()
    case=board.getBox(pos)
    price = case.getPrice()
    if (case.getOwner() == None):
        if (player.getMoney() >= price):
            choice = input("Cette gare est libre, son prix est de "+str(price)+" euros. Voulez-vous l'acheter ? (Il vous reste "+str(player.money)+ " euros)")
            if (choice.lower() == "oui".lower()):
                player.buyAStation(case)
                input("Vous venez d'acheter la propriété "+ str(case.name) +". Il vous reste "+str(player.money)+ "€.")
            else : 
                input("Vous avez décidé de ne pas acheter, vous avez toujours "+str(player.money)+" euros.")
        else :
            input("Cette propriété est libre, malheureusement vous n'avez pas assez d'argent pour l'acheter. Il vous reste "+ str(player.money) +" euros et le prix est de "+str(price) + " euros.")
    else:
        owner = case.getOwner()
        if (owner == player):
            input("Cette gare vous appartient")
        else : 
            rent = getRentStation(player)
            print("Cette propriété appartient à "+owner.getUserName()+", vous lui devez "+str(rent)+" euros.")
            player.LooseMoney(rent)
            print("Il vous reste "+str(player.getMoney())+" euros.")
            owner.EarnMoney(rent)
            input(""+owner.getUserName()+" gagne "+str(rent)+" euros, il lui reste "+str(owner.getMoney())+" euros.")
            
            

      
            
    
    
def turn(order):
    
    """
    Simulates one turn : 
    1-actualize position of the player
    2- different actions if on street station or jail
    3- if the player has not mony anymore --> he looses 
    """
    
    
    numberOfPlayers = len(order)
    for i in range(numberOfPlayers):
        player = order[i]
        actualizePosition(player)
        pos = player.getPosition()
        playerStreetPosition = board.getBox(pos).getBoxName()
        input("Tu es sur la case : " + playerStreetPosition)
        case=board.getBox(pos)
        if (case.getType() == "street"):
            onAStreet(player)
        else:
            if (case.getType() == "station"):
                onAStation(player)
            else:
                if (case.getType() == "to-jail"):
                    goToJail(player)
                else:   
                    input("ce n'est pas une rue, pour l'instant vous ne pouvez pas l'acheter.") 
        loosers = []
        if (player.getMoney() <0):
            input(""+ player.getUserName()+ ", tu as perdu! Tu n'as plus d'argent.")
            loosers.append(player)
    if (len(loosers)>0):
        for looser in loosers : 
            order.remove(looser)
    return order
    
    
    


if __name__ == "__main__":
    board = initGame()
    main()
    
        
    

































