import os

os.environ["PYTHONPATH"] = "."



from game.board import Board
from game.user import User
from game.boxes import Box, Street, Station
from game.game import Game
from game.globs import INITIAL_MONEY
from game.cards import Card

# Class User

def test_getUserName():
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    test1 = chloe.getUserName()
    test2 = gildas.getUserName()
    test3 = lucien.getUserName()
    if (test1 == "Chloe" and test2 == "Gildas" and test3 == "Lucien"):
        return True
    else:
        raise Exception('Test test_getUserName failed.')
        
def test_getMoney():
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.money = 0
    gildas.money = 10000
    test1 = chloe.getMoney()
    test2 = gildas.getMoney()
    test3 = lucien.getMoney()
    if (test1 == 0 and test2 == 10000 and test3 == INITIAL_MONEY):
        return True
    else : 
        raise Exception('Test test_getMoney failed.')
        
        
def test_getPosition():
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.position = 5
    gildas.position = 39
    test1 = chloe.getPosition()
    test2 = gildas.getPosition()
    test3 = lucien.getPosition()
    if (test1 == 5 and test2 == 39 and test3 == 0):
        return True
    else :
        raise Exception('Test test_getPosition failed.')
        
        
def test_getGoods():
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    board = Board()
    chloe.goods.append(board.boxes[3])
    chloe.goods.append(board.boxes[5])
    chloe.goods.append(board.boxes[11])
    gildas.goods.append(board.boxes[3])
    if lucien.getGoods() == []:
        if len(gildas.getGoods())==1 and gildas.getGoods()[0].name == "Rue Lecourbe":
            if len(chloe.getGoods())==3 and chloe.getGoods()[0].name == "Rue Lecourbe" and chloe.getGoods()[1].name == "Gare Montparnasse" and chloe.getGoods()[2].name == "Boulevard de la Vilette":
                return True
            else:
                raise Exception('Test test_getGoods failed.')
        else:
            raise Exception('Test test_getGoods failed.')
    else:
        raise Exception('Test test_getGoods failed.')

        
def test_getInPrison():
    chloe = User("Chloe")
    gildas = User("Gildas")
    chloe.inPrison = True
    if (chloe.getInPrison() == True and gildas.getInPrison() == False):
        return True
    else:
        raise Exception('Test test_getInPrison failed.')
    

def test_getPrisonTurn():
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.prisonTurn = 3
    gildas.prisonTurn = 0
    if (chloe.getPrisonTurn() == 3 and gildas.getPrisonTurn() == 0 and lucien.getPrisonTurn() == None):
        return True
    else:
        raise Exception('Test test_getPrisonTurn failed.')
        
        
def test_setPrisonTurn():        #depends on getPrisonTurn
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.setPrisonTurn(2)
    gildas.setPrisonTurn(0)
    lucien.setPrisonTurn(None)
    if (chloe.getPrisonTurn() == 2 and gildas.getPrisonTurn() == 0 and lucien.getPrisonTurn() == None):
        return True
    else : 
        raise Exception('Test test_setPrisonTurn failed.')
        
        
def test_setInPrison():
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.setInPrison(True)
    gildas.setInPrison(False)
    if (chloe.getInPrison() == True and gildas.getInPrison() == False and lucien.getInPrison() == False):
        return True
    else:
        raise Exception('Test test_setInPrison failed.') 
        
        

def test_setPosition():
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.setPosition(24)
    gildas.setPosition(0)
    if (chloe.getPosition() == 24 and gildas.getPosition() == 0 and lucien.getPosition()==0):
        return True
    else:
        raise Exception('Test test_setPosition failed.')
    
def test_EarnMoney():
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.EarnMoney(50)
    gildas.EarnMoney(0)
    if (chloe.getMoney() == INITIAL_MONEY + 50 and gildas.getMoney() == INITIAL_MONEY and lucien.getMoney()==INITIAL_MONEY):
        return True
    else:
        raise Exception('Test test_EarnMoney failed.')
        
        
def test_LooseMoney():
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.LooseMoney(50)
    gildas.LooseMoney(0)
    if (chloe.getMoney() == INITIAL_MONEY - 50 and gildas.getMoney() == INITIAL_MONEY and lucien.getMoney()==INITIAL_MONEY):
        return True
    else:
        raise Exception('Test test_LooseMoney failed.')
        
        
def test_buyAStreet():
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    board = Board()
    chloe.buyAStreet(board.boxes[39])
    chloe.buyAStreet(board.boxes[1])
    gildas.buyAStreet(board.boxes[3])
    if (lucien.getGoods() == [] and lucien.getMoney() == INITIAL_MONEY):
        if len(gildas.getGoods()) == 1 and gildas.getGoods()[0].name == "Rue Lecourbe" and board.boxes[3].owner == gildas and gildas.getMoney() == INITIAL_MONEY - 60:
            if len(chloe.getGoods()) == 2 and chloe.getGoods()[0].name == "Rue de la Paix" and chloe.getGoods()[1].name == "Boulevard de Belleville" and chloe.getMoney() == INITIAL_MONEY - 400 - 60:
                return True
            else:
                raise Exception('Test test_buyAStreet failed.')
        else:
            raise Exception('Test test_buyAStreet failed.')
    else:
        raise Exception('Test test_buyAStreet failed.')
        
        
        
def test_buyAStation():
    chloe = User("Chloe")
    gildas = User("Gildas")
    lucien = User("Lucien")
    board = Board()
    chloe.buyAStation(board.boxes[5])
    chloe.buyAStation(board.boxes[15])
    gildas.buyAStation(board.boxes[25])
    if (lucien.getGoods() == [] and lucien.getMoney() == INITIAL_MONEY):
        if len(gildas.getGoods()) == 1 and gildas.getGoods()[0].name == "Gare du Nord" and board.boxes[25].owner ==gildas and gildas.getMoney() == INITIAL_MONEY - 200:
            if len(chloe.getGoods()) == 2 and chloe.getGoods()[0].name == "Gare Montparnasse" and chloe.getGoods()[1].name == "Gare de Lyon" and chloe.getMoney() == INITIAL_MONEY - 200 - 200:
                return True
            else:
                raise Exception('Test test_buyAStation failed.')
        else:
            raise Exception('Test test_buyAStation failed.')
    else:
        raise Exception('Test test_buyAStation failed.')

        
    
def test_classUser():
    print(str(test_getUserName())+ ", test getUserName")
    print(str(test_getPosition())+ ", test getPosition")
    print(str(test_getMoney())+ ", test getMoney")
    print(str(test_getInPrison())+", test getInPrison")
    print(str(test_getGoods())+", test getGoods")
    print(str(test_getPrisonTurn())+ ", test getPrisonTurn")
    print(str(test_setPrisonTurn())+ ", test setPrisonTurn")
    print(str(test_setInPrison())+ ", test setInPrison")
    print(str(test_setPosition())+ ", test setPosition")
    print(str(test_EarnMoney())+ ", test EarnMoney")
    print(str(test_LooseMoney())+ ", test LooseMoney")
    print(str(test_buyAStreet())+ ", test buyAStreet")
    print(str(test_buyAStation())+ ", test buyAStation")
    L=[test_getUserName(), test_getPosition(), test_getMoney(), test_getInPrison(), test_getGoods(), test_getPrisonTurn(), test_setPrisonTurn(), test_setInPrison(), test_setPosition(), test_EarnMoney(), test_LooseMoney(), test_buyAStreet(), test_buyAStation()]
    n=len(L)
    count = 0
    for i in range(n):
        if L[i] == True:
            count = count + 1
    return "La class User passe les tests a "+ str(count)+"/"+str(n)+""
    
    
    
    
## Class Box

def test_getBoxName():
    box1 = Box(25, "street", "box1")
    box2 = Box(86, "station", "box2")
    test1 = box1.getBoxName()
    test2 = box2.getBoxName()
    if (test1 == "box1" and test2=="box2"):
        return True 
    else:
        raise Exception('Test test_getBoxName failed.')
        
        
def test_getType():
    box1 = Box(25, "street", "box1")
    box2 = Box(86, "station", "box2")
    box3 = Box(45, None, "box3")
    test1 = box1.getType()
    test2 = box2.getType()
    test3 = box3.getType()
    if (test1 == "street" and test2=="station" and test3 == None):
        return True 
    else:
        raise Exception('Test test_getType failed.')
        
        
def test_classBox():
    print(str(test_getBoxName())+", test getBoxName")
    print(str(test_getType())+", test getType")
    L = [test_getBoxName(), test_getType()]
    n=len(L)
    count = 0
    for i in range(n):
        if L[i] == True:
            count = count + 1
    return "La class Box passe les tests a "+ str(count)+"/"+str(n)+""
    
    
    
## Class Street 


def test_getOwner():
    chloe = User("Chloe")
    gildas = User("Gildas")
    street1 = Street(12, "street", "test", 25, 22, "yellow")
    street2 = Street(15, "street", "gravelines", 250,85, "red")
    street3 = Street(17, "street", "dunkerque", 52, 74, "blue", chloe, gildas)
    street2.owner = chloe
    test1 = street1.getOwner()
    test2 = street2.getOwner()
    test3 = street3.getOwner()
    if (test1 == None and test2 == chloe and test3 == gildas):
        return True
    else:
        raise Exception('Test getOwner failed.')
        
        
def test_getPrice():
    street1 = Street(12, "street", "test", 25, 22, "yellow")
    street2 = Street(15, "street", "gravelines", None,85, "red")
    street3 = Street(17, "street", "dunkerque", 0, 74, "blue")
    test1 = street1.getPrice()
    test2 = street2.getPrice()
    test3 = street3.getPrice()
    if (test1 == 25 and test2 == None and test3 == 0):
        return True
    else:
        raise Exception('Test test_getPrice failed.')
        
        
def test_getColor():
    street1 = Street(12, "street", "test", 25, 22, "yellow")
    street2 = Street(15, "street", "gravelines", 250,85, "red")
    street3 = Street(17, "street", "dunkerque", 0, 74, None)
    test1 = street1.getColor()
    test2 = street2.getColor()
    test3 = street3.getColor()
    if (test1 == "yellow" and test2 == "red" and test3 == None):
        return True
    else:
        raise Exception('Test test_getColor failed.')
        
        
def test_getRent():
    street1 = Street(12, "street", "test", 25, 22, "yellow")
    street2 = Street(15, "street", "gravelines", 250,None, "red")
    test1 = street1.getRent()
    test2 = street2.getRent()
    if (test1 == 22 and test2 == None):
        return True
    else : 
        raise Exception('Test test_getRent failed.')
        

def test_getHome():
    chloe = User("Chloe")
    street1 = Street(12, "street", "test", 25, 22, "yellow")
    street2 = Street(15, "street", "gravelines", 250, None, "red", chloe, chloe, 3)
    test1 = street1.getHome()
    test2 = street2.getHome()
    if (test1 == 0 and test2 == 3):
        return True
    else: 
        raise Exception('Test test_getHome failed.')
        
        
def test_setHomes():
    chloe = User("Chloe")
    street1 = Street(12, "street", "test", 25, 22, "yellow")
    street2 = Street(15, "street", "gravelines", 250,None, "red", chloe, chloe, 3)
    street3 = Street(17, "street", "dunkerque", 326,58, "red", chloe, chloe, 8)
    street1.setHomes(5)
    street2.setHomes(4)
    street3.setHomes(0)
    if (street1.getHome() == 5 and street2.getHome()==4 and street3.getHome()==0):
        return True 
    else : 
        raise Exception('Test test_setHomes failed.')
        

def test_classStreet():
    print(str(test_getOwner())+", test getOwner")
    print(str(test_getPrice())+", test getPrice")
    print(str(test_getColor()) + ", test getColor")
    print(str(test_getRent())+", test getRent")
    print(str(test_getHome()) + ", test getHome")
    print(str(test_setHomes())+", test setHomes")
    L = [test_getOwner(), test_getPrice(), test_getColor(), test_getRent(), test_getHome(), test_setHomes()]
    n = len(L)
    count = 0
    for i in range(n):
        if L[i] == True:
            count = count + 1
    return "La class Street passe les tests a "+ str(count)+"/"+str(n)+""
    
    
## Class Station


def test_getOwnerStation():
    chloe = User("Chloe")
    gildas = User("Gildas")
    station1 = Station(15, "station", "montparnasse", 200) 
    station2 = Station(25, "station", "gravelines", 250, chloe, gildas)
    test1 = station1.getOwner()
    test2 = station2.getOwner()
    if (test1 == None and test2 == gildas):
        return True 
    else:
        raise Exception('Test test_getOwnerStation failed.')
        
def test_getPriceStation():
    chloe = User("chloe")
    gildas = User("gildas")
    station1 = Station(15, "station", "montparnasse", 200) 
    station2 = Station(25, "station", "gravelines", None, chloe, gildas)
    test1 = station1.getPrice()
    test2 = station2.getPrice()
    if (test1 == 200 and test2 == None):
        return True
    else:
        raise Exception('Test test_getPriceStation failed.')

        
        
def test_classStation():
    print(str(test_getOwnerStation())+", test getOwner")
    print(str(test_getPriceStation())+", test getPrice")
    L = [test_getOwnerStation(), test_getPriceStation()]
    n = len(L)
    count = 0
    for i in range(n):
        if L[i] == True:
            count = count + 1
    return "La class Street passe les tests a "+ str(count)+"/"+str(n)+""
    
    
## Class Board

def test_getBox():
    position = 39
    board = Board()
    if (board.boxes[position] == board.getBox(position)):
        return True
    else :
        raise Exception('Test test_getBox failed.')
        
        
def test_classBoard():
    print(str(test_getBox())+", test getBox")
    L=[test_getBox()]
    n=len(L)
    count = 0
    for i in range(n):
        if L[i] == True:
            count = count + 1
    return "La class Street passe les tests a "+ str(count)+"/"+str(n)+""



        
## GAME Functions


def test_playerHasAllColorsStreets():
    players = {0: "Chloe", 1: "Lucien"}
    game = Game(players)
    chloe = game.players[0]
    lucien = game.players[1]
    chloe.buyAStreet(game.board.getBox(37))
    chloe.buyAStreet(game.board.getBox(39))
    lucien.buyAStreet(game.board.getBox(34))
    lucien.buyAStreet(game.board.getBox(32))
    lucien.buyAStreet(game.board.getBox(31))
    lucien.buyAStreet(game.board.getBox(29))
    test1 = game.playerHasAllColorStreets(chloe, 37)
    test2 = game.playerHasAllColorStreets(chloe, 34)
    test3 = game.playerHasAllColorStreets(lucien, 34)
    test4 = game.playerHasAllColorStreets(lucien, 29)
    if (test1 == True and test2 == False and test3 == True and test4 == False):
        return True
    else :
        raise Exception('Test test_playerHasAllColorsStreet failed.') 
    


def test_goToJail():
    players = {0: "Chloe", 1: "Lucien"}
    game = Game(players)
    chloe = game.players[0]
    chloe.setPosition(25)
    game.goToJail(chloe)
    if (chloe.getPosition() == 10 and chloe.getInPrison() == True and chloe.getPrisonTurn() == 0):
        return True
    else:
        raise Exception('Test test_goToJail failed.')

    
def test_nbOfStations():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas"}
    game = Game(players)
    chloe = game.players[0]
    lucien = game.players[1]
    gildas = game.players[2]
    chloe.buyAStation(game.board.getBox(5))
    chloe.buyAStation(game.board.getBox(15))
    lucien.buyAStation(game.board.getBox(25))
    test1 = game.nbOfStations(chloe)
    test2 = game.nbOfStations(lucien)
    test3 = game.nbOfStations(gildas)
    if (test1 == 2 and test2 == 1 and test3 == 0):
        return True 
    else:
        raise Exception('Test test_nbOfStations failed.')
        
        
def test_getRentStreet():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
    game = Game(players)
    chloe = game.players[0]
    lucien = game.players[1]
    gildas = game.players[2]
    camille = game.players[3]
    gildas.setPosition(1)
    lucien.setPosition(6)
    camille.setPosition(8)
    chloe.buyAStreet(game.board.getBox(1))
    chloe.buyAStreet(game.board.getBox(3))
    chloe.buyAStreet(game.board.getBox(6))
    chloe.buyAStreet(game.board.getBox(8))
    game.board.getBox(6).setHomes(2)
    test1 = game.getRentStreet(gildas)   #loyer double
    test2 = game.getRentStreet(lucien)   #loyer avec 2 maisons
    test3 = game.getRentStreet(camille)  #loyer normal
    if test1 == 4 and test2 == 90 and test3 == 6:
        return True
    else:
        raise Exception('Test test_getRentStreet failed.')
    

def test_getRentStation():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
    game = Game(players)
    chloe = game.players[0]
    lucien = game.players[1]
    gildas = game.players[2]
    camille = game.players[3]
    camille.setPosition(5)
    lucien.setPosition(15)
    chloe.buyAStation(game.board.getBox(5))
    gildas.buyAStation(game.board.getBox(15))
    gildas.buyAStation(game.board.getBox(25))
    gildas.buyAStation(game.board.getBox(35))
    test1 = game.getRentStation(camille)
    test2 = game.getRentStation(lucien)
    if test1 == 50 and test2 == 150:
        return True
    else:
        raise Exception('Test test_getRentStation failed.')
    
    
    
def test_mainFunction():
    print(str(test_playerHasAllColorsStreets()) + ", test playerHasAllColorsStreet")
    print(str(test_goToJail()) + ", test goToJail")
    print(str(test_nbOfStations())+", test nbOfStations")
    print(str(test_getRentStreet()) + ", test getRentStreet")
    print(str(test_getRentStation())+", test getRentStation")
    L=[test_playerHasAllColorsStreets(), test_goToJail(), test_nbOfStations(), test_getRentStreet(), test_getRentStation()]
    n=len(L)
    count = 0
    for i in range(n):
        if L[i] == True:
            count = count + 1
    return "Les fonctions de la classe Game passent les tests a "+ str(count)+"/"+str(n)+""


def test_make_community_funds():
    board = Board()
    test1 = board.community_funds[0].name
    test2 = board.community_funds[0].card_type
    test3 = board.community_funds[0].value
    test4 = len(board.community_funds)
    test5 = board.community_funds[test4-1].value
    if test1 == "Vous heritez 100 euros." and test2 == "earn-money" and test3 == 100 and test4 == 17 and test5==-1 :
        return True
    else:
        raise Exception('Test test_make_community_funds failed.')


def test_community_earn_money():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
    game = Game(players)
    chloe = User(players[0])
    chloe.setPosition(2)
    game.community_earn_money(chloe, 15)
    if chloe.getMoney() == INITIAL_MONEY + 10:
        return True
    else:
        raise Exception('Test test_community_earn_money failed.')

def test_community_loose_money():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
    game = Game(players)
    chloe = User(players[0])
    chloe.setPosition(2)
    game.community_loose_money(chloe, 7)
    if chloe.getMoney() == INITIAL_MONEY - 100:
        return True
    else:
        raise Exception('Test test_community_loose_money failed.')



def test_community_moove_forward():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
    game = Game(players)
    chloe = User(players[0])
    game.community_moove_forward(chloe, 11)
    if chloe.getPosition() == 0 and chloe.getMoney() == INITIAL_MONEY + 200:
        return True
    else:
        raise Exception('Test test_community_moove_forward failed.')


if __name__ == "__main__":
    print(test_classUser())
    print(test_classStreet())
    print(test_classStation())
    print(test_classBox())
    print(test_classBoard())
    print(test_mainFunction())
    print(test_make_community_funds())
    print(test_community_earn_money())
    print(test_community_loose_money())
    print(test_community_moove_forward())
