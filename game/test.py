from game import main

main.main()
board = main.initGame()

##Test Class User

from game.src import User, Street, Box, Station, INITIAL_MONEY

chloe = User("Chloé")
chloe.position = 5
gildas = User("Gildas")
gildas.position = 39
lucien = User("Lucien")


def test_getUserName():
    chloe = User("Chloé")
    gildas = User("Gildas")
    lucien = User("Lucien")
    test1 = chloe.getUserName()
    test2 = gildas.getUserName()
    test3 = lucien.getUserName()
    if (test1 == "Chloé" and test2 == "Gildas" and test3 == "Lucien"):
        return True
    else : 
        return False
        
def test_getMoney():
    chloe = User("Chloé")
    chloe.money = 0
    gildas = User("Gildas")
    gildas.money = 10000
    lucien = User("Lucien")
    test1 = chloe.getMoney()
    test2 = gildas.getMoney()
    test3 = lucien.getMoney()
    if (test1 == 0 and test2 == 10000 and test3 == INITIAL_MONEY):
        return True
    else : 
        return False
        
        
def test_getPosition():
    chloe = User("Chloé")
    chloe.position = 5
    gildas = User("Gildas")
    gildas.position = 39
    lucien = User("Lucien")
    test1 = chloe.getPosition()
    test2 = gildas.getPosition()
    test3 = lucien.getPosition()
    if (test1 == 5 and test2 == 39 and test3 == 0):
        return True
    else : 
        return False
        
        
def test_getGoods():
    chloe = User("Chloé")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.goods.append(board.boxes[3])
    chloe.goods.append(board.boxes[5])
    chloe.goods.append(board.boxes[11])
    gildas.goods.append(board.boxes[3])
    if (lucien.getGoods() == []):
        if (len(gildas.getGoods())==1 and gildas.getGoods()[0].name == "Rue Lecourbe"):
            if (len(chloe.getGoods())==3 and chloe.getGoods()[0].name == "Rue Lecourbe" and chloe.getGoods()[1].name == "Gare Montparnasse" and chloe.getGoods()[2].name == "Boulevard de la Vilette"):
                return True
            else:
                return False
        else :
            return False
    else:
        return False
        
        
        
def test_getInPrison():
    chloe = User("Chloé")
    gildas = User("Gildas")
    chloe.inPrison = True
    if (chloe.getInPrison() == True and gildas.getInPrison() == False):
        return True
    else:
        return False
    
    
        
def test_getPrisonTurn():
    chloe = User("Chloé")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.prisonTurn = 3
    gildas.prisonTurn = 0
    if (chloe.getPrisonTurn() == 3 and gildas.getPrisonTurn() == 0 and lucien.getPrisonTurn() == None):
        return True
    else:
        return False
        
        
def test_setPrisonTurn():        #depends on getPrisonTurn
    chloe = User("Chloé")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.setPrisonTurn(2)
    gildas.setPrisonTurn(0)
    lucien.setPrisonTurn(None)
    if (chloe.getPrisonTurn() == 2 and gildas.getPrisonTurn() == 0 and lucien.getPrisonTurn() == None):
        return True
    else : 
        return False
        
        
def test_setInPrison():
    chloe = User("Chloé")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.setInPrison(True)
    gildas.setInPrison(False)
    if (chloe.getInPrison() == True and gildas.getInPrison() == False and lucien.getInPrison() == False):
        return True
    else:
        return False 
        
        

def test_setPosition():
    chloe = User("Chloé")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.setPosition(24)
    gildas.setPosition(0)
    if (chloe.getPosition() == 24 and gildas.getPosition() == 0 and lucien.getPosition()==0):
        return True
    else:
        return False
    
def test_EarnMoney():
    chloe = User("Chloé")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.EarnMoney(50)
    gildas.EarnMoney(0)
    if (chloe.getMoney() == INITIAL_MONEY + 50 and gildas.getMoney() == INITIAL_MONEY and lucien.getMoney()==INITIAL_MONEY):
        return True
    else:
        return False
        
        
def test_LooseMoney():
    chloe = User("Chloé")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.LooseMoney(50)
    gildas.LooseMoney(0)
    if (chloe.getMoney() == INITIAL_MONEY - 50 and gildas.getMoney() == INITIAL_MONEY and lucien.getMoney()==INITIAL_MONEY):
        return True
    else:
        return False
        
        
def test_buyAStreet():
    chloe = User("Chloé")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.buyAStreet(board.boxes[39])
    chloe.buyAStreet(board.boxes[1])
    gildas.buyAStreet(board.boxes[3])
    if (lucien.getGoods() == [] and lucien.getMoney() == INITIAL_MONEY):
        if len(gildas.getGoods()) == 1 and gildas.getGoods()[0].name == "Rue Lecourbe" and board.boxes[3].owner ==gildas and gildas.getMoney() == INITIAL_MONEY - 60:
            if len(chloe.getGoods()) == 2 and chloe.getGoods()[0].name == "Rue de la Paix" and chloe.getGoods()[1].name == "Boulevard de Belleville" and chloe.getMoney() == INITIAL_MONEY - 400 - 60 :
                return True
            else:
                return False
        else:
            return False
    else:
        return False
        
        
        
def test_buyAStation():
    chloe = User("Chloé")
    gildas = User("Gildas")
    lucien = User("Lucien")
    chloe.buyAStation(board.boxes[5])
    chloe.buyAStation(board.boxes[15])
    gildas.buyAStation(board.boxes[25])
    if (lucien.getGoods() == [] and lucien.getMoney() == INITIAL_MONEY):
        if len(gildas.getGoods()) == 1 and gildas.getGoods()[0].name == "Gare du Nord" and board.boxes[25].owner ==gildas and gildas.getMoney() == INITIAL_MONEY - 200:
            if len(chloe.getGoods()) == 2 and chloe.getGoods()[0].name == "Gare Montparnasse" and chloe.getGoods()[1].name == "Gare de Lyon" and chloe.getMoney() == INITIAL_MONEY - 200 - 200 :
                return True
            else:
                return False
        else:
            return False
    else:
        return False

        
    
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
        return False
        
        
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
        return False
        
        
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
    chloe = User("Chloé")
    gildas = User("Gildas")
    street1 = Street(12, "street", "test", 25, 22, "yellow")
    street2 = Street(15, "street", "gravelines", 250,85, "red")
    street3 = Street(17, "street", "dunkerque", 52, 74, "blue", chloe , gildas)
    street2.owner = chloe
    test1 = street1.getOwner()
    test2 = street2.getOwner()
    test3 = street3.getOwner()
    if (test1 == None and test2 == chloe and test3 == gildas):
        return True
    else:
        return False
        
        
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
        return False
        
        
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
        return False
        
        
def test_getRent():
    street1 = Street(12, "street", "test", 25, 22, "yellow")
    street2 = Street(15, "street", "gravelines", 250,None, "red")
    test1 = street1.getRent()
    test2 = street2.getRent()
    if (test1 == 22 and test2 == None):
        return True
    else : 
        return False
        

def test_getHome():
    chloe = User("Chloé")
    street1 = Street(12, "street", "test", 25, 22, "yellow")
    street2 = Street(15, "street", "gravelines", 250,None, "red", chloe, chloe, 3)
    test1 = street1.getHome()
    test2 = street2.getHome()
    if (test1 == 0 and test2 == 3):
        return True
    else: 
        return False
        
        
def test_addHomes():
    chloe = User("Chloé")
    street1 = Street(12, "street", "test", 25, 22, "yellow")
    street2 = Street(15, "street", "gravelines", 250,None, "red", chloe, chloe, 3)
    street3 = Street(17, "street", "dunkerque", 326,58, "red", chloe, chloe, 8)
    test1 = street1.addHomes(5)
    test2 = street2.addHomes(4)
    test3 = street3.addHomes(0)
    if (street1.getHome() == 5 and street2.getHome()==7 and street3.getHome()==8):
        return True 
    else : 
        return False
        
        
        
def test_classStreet():
    print(str(test_getOwner())+", test getOwner")
    print(str(test_getPrice())+", test getPrice")
    print(str(test_getColor()) + ", test getColor")
    print(str(test_getRent())+", test getRent")
    print(str(test_getHome()) + ", test getHome")
    print(str(test_addHomes())+", test addHomes")
    L=[test_getOwner(), test_getPrice(), test_getColor(), test_getRent(), test_getHome(), test_addHomes()]
    n=len(L)
    count = 0
    for i in range(n):
        if L[i] == True:
            count = count + 1
    return "La class Street passe les tests a "+ str(count)+"/"+str(n)+""
    
    
## Class Station


def test_getOwnerStation():
    chloe = User("Chloé")
    gildas = User("Gildas")
    station1 = Station(15, "station", "montparnasse", 200) 
    station2 = Station(25, "station", "gravelines", 250, chloe, gildas)
    test1 = station1.getOwner()
    test2 = station2.getOwner()
    if (test1 == None and test2 == gildas):
        return True 
    else:
        return False
        
def test_getPriceStation():
    station1 = Station(15, "station", "montparnasse", 200) 
    station2 = Station(25, "station", "gravelines", None, chloe, gildas)
    test1 = station1.getPrice()
    test2 = station2.getPrice()
    if (test1 == 200 and test2 == None):
        return True
    else:
        return False

        
        
def test_classStation():
    print(str(test_getOwnerStation())+", test getOwner")
    print(str(test_getPriceStation())+", test getPrice")
    L=[test_getOwnerStation(), test_getPriceStation()]
    n=len(L)
    count = 0
    for i in range(n):
        if L[i] == True:
            count = count + 1
    return "La class Street passe les tests a "+ str(count)+"/"+str(n)+""
    
    
## Class Board

def test_getBox():
    position = 39
    if (board.boxes[position] == board.getBox(position)):
        return True
    else :
        return False
        
        
def test_classBoard():
    print(str(test_getBox())+", test getBox")
    L=[test_getBox()]
    n=len(L)
    count = 0
    for i in range(n):
        if L[i] == True:
            count = count + 1
    return "La class Street passe les tests a "+ str(count)+"/"+str(n)+""
        
        
## Main Functions


def test_actualizePositionAux():
    chloe = User("Chloé", 12)
    lucien = User("Lucien", 39)
    gildas=User("Gildas", 31)
    main.actualizePositionAux(chloe, [2, 1])
    main.actualizePositionAux(lucien, [6, 1])
    main.actualizePositionAux(gildas, [4, 5])
    if (chloe.getPosition() == 15 and lucien.getPosition() == 6 and gildas.getPosition() == 0):
        return True 
    else :
        return False
    
    


##Bilan

print(test_classUser())
print(test_classStreet())
print(test_classStation())
print(test_classBox())
print(test_classBoard())      
        
        
        
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
