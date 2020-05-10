import sys
from game.game import Game
from game.globs import INITIAL_MONEY

#python tests/input_test.py < tests/scenarios/answers_community_or_chance.txt

def test_isInJail():
    players = {
        0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille", 4: "Milou", 5: "Delcourt", 6: "Mayeul",
        7: "Samy", 8: "Ines", 9: "Milene", 10: "Yushan", 11: "Grottier", 12: "Corentin", 13: "Valentin",
        14: "Bielecki", 15: "Dalasse", 16: "Agathe"
    }
    game = Game(players)
    chloe = game.players[0]       # 0_Money_chooseToTestDouble, double fail, stay in prison, one turn more
    lucien = game.players[1]      # 1_Money_chooseToTestDouble, double fail, stay in prison, one turn more
    gildas = game.players[2]      # 2_Money_chooseToTestDouble, double fail, stay in prison, one turn more
    camille = game.players[3]     # 3_Already 3 turns in prison, should get out
    milou = game.players[4]       # 0_Money, choose to pay at first turn, gets out
    delcourt = game.players[5]    # 1_Money, choose to pay at second turn, gets out
    mayeul = game.players[6]      # 2_Money, choose to pay at third turn, gets out
    samy = game.players[7]        # 0_No Money, double fail, one turn more in prison
    ines = game.players[8]        # 1_No Money, double fail, one turn more in prison
    milene = game.players[9]      # 2_No Money, double fail, one turn more in prison
    yushan = game.players[10]     # 0_Money_chooseToTestDouble, double succeeds, gets out
    grottier = game.players[11]   # 1_Money_chooseToTestDouble, double succeeds, gets out
    coco = game.players[12]       # 2_Money_chooseToTestDouble, double succeeds, gets out
    valentin = game.players[13]   # 0_NoMoney, double succeeds, gets out
    bielecki = game.players[14]   # 1_NoMoney, double succeeds, gets out
    dalasse = game.players[15]    # 2_NoMoney, double succeeds, gets out
    agathe = game.players[16]     # 3_NoMoney, gets out
    game.goToJail(chloe) # enter
    game.goToJail(lucien) # enter
    game.goToJail(gildas) # enter
    game.goToJail(camille) # enter
    game.goToJail(milou) #enter
    game.goToJail(delcourt) #enter
    game.goToJail(mayeul) #enter
    game.goToJail(samy) #enter
    game.goToJail(ines) #enter
    game.goToJail(milene) #enter
    game.goToJail(yushan) #enter
    game.goToJail(grottier) #enter
    game.goToJail(coco) #enter
    game.goToJail(valentin) #enter
    game.goToJail(bielecki) #enter
    game.goToJail(dalasse) #enter
    game.goToJail(agathe)  #enter
    lucien.setPrisonTurn(1)
    gildas.setPrisonTurn(2)
    camille.setPrisonTurn(3)
    delcourt.setPrisonTurn(1)
    mayeul.setPrisonTurn(2)
    ines.setPrisonTurn(1)
    milene.setPrisonTurn(2)
    grottier.setPrisonTurn(1)
    coco.setPrisonTurn(2)
    bielecki.setPrisonTurn(1)
    dalasse.setPrisonTurn(2)
    agathe.setPrisonTurn(3)
    samy.money = 20
    ines.money = 20
    milene.money = 20
    valentin.money = 20
    bielecki.money = 20
    dalasse.money = 20
    agathe.money = 20
    game.isInJailAux(chloe, [6,4])    #2 + enter
    game.isInJailAux(lucien, [6,4])   #2 + enter
    game.isInJailAux(gildas, [6,4])   #2 + enter
    game.isInJailAux(camille, [6,4])  #enter + enter
    game.isInJailAux(milou, [6,4])    #1 + enter + enter
    game.isInJailAux(delcourt, [6,4]) #1 + enter + enter
    game.isInJailAux(mayeul, [6,4])   #1 + enter + enter
    game.isInJailAux(samy, [6,4])     #enter + enter
    game.isInJailAux(ines, [6,4])     #enter + enter
    game.isInJailAux(milene, [6,4])   #enter + enter
    game.isInJailAux(yushan, [4,4])   #2 + enter
    game.isInJailAux(grottier, [3,3]) #2 + enter
    game.isInJailAux(coco, [2,2])     #2 + enter
    game.isInJailAux(valentin, [1,1]) #enter + enter
    game.isInJailAux(bielecki, [6,6]) #enter + enter
    game.isInJailAux(dalasse, [5,5])  #enter + enter
    game.isInJailAux(agathe, [5,2])   #enter + enter
    
    if (chloe.getInPrison() == True and chloe.getPrisonTurn() == 1 and chloe.getMoney() == INITIAL_MONEY and lucien.getInPrison() == True and lucien.getPrisonTurn() == 2 and lucien.getMoney() == INITIAL_MONEY and gildas.getInPrison() == True and gildas.getPrisonTurn() == 3 and gildas.getMoney() == INITIAL_MONEY and camille.getInPrison() == False and camille.getPrisonTurn() == None and camille.getMoney() == INITIAL_MONEY and milou.getInPrison() == False and milou.getPrisonTurn() == None and milou.getMoney() == INITIAL_MONEY - 50 and delcourt.getInPrison() == False and delcourt.getPrisonTurn() == None and delcourt.getMoney() == INITIAL_MONEY -50 and mayeul.getInPrison() == False and mayeul.getPrisonTurn() == None and mayeul.getMoney() == INITIAL_MONEY -50 and samy.getInPrison() == True and samy.getPrisonTurn() == 1 and samy.getMoney() == 20 and ines.getInPrison() == True and ines.getPrisonTurn() == 2 and ines.getMoney() == 20 and milene.getInPrison() == True and milene.getPrisonTurn() == 3 and milene.getMoney() == 20 and yushan.getInPrison() == False and yushan.getPrisonTurn() == None and yushan.getMoney() == INITIAL_MONEY and yushan.getPosition() == 18 and grottier.getInPrison() == False and grottier.getPrisonTurn() == None and grottier.getMoney() == INITIAL_MONEY and grottier.getPosition() == 16 and coco.getInPrison() == False and coco.getPrisonTurn() == None and coco.getMoney() == INITIAL_MONEY and coco.getPosition() == 14 and valentin.getInPrison() == False and valentin.getPrisonTurn() == None and valentin.getMoney() == 20 and valentin.getPosition() == 12 and bielecki.getInPrison() == False and bielecki.getPrisonTurn() == None and bielecki.getMoney() == 20 and bielecki.getPosition() == 22 and dalasse.getInPrison() == False and dalasse.getPrisonTurn() == None and dalasse.getMoney() == 20 and dalasse.getPosition() == 20 and agathe.getInPrison() == False and agathe.getPrisonTurn() == None and agathe.getMoney() == 20 and agathe.getPosition() > 10) :
        print("\n",True)
    else:
        raise Exception('Test test_isInJail failed.')


def test_putHomes():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
    game = Game(players)
    chloe = game.players[0]
    lucien = game.players[1]
    gildas = game.players[2]
    camille = game.players[3]
    lucien.buyAStreet(game.board.getBox(6))
    chloe.buyAStreet(game.board.getBox(1))
    chloe.buyAStreet(game.board.getBox(3))
    gildas.buyAStreet(game.board.getBox(11))
    gildas.buyAStreet(game.board.getBox(13))
    gildas.buyAStreet(game.board.getBox(14))
    camille.buyAStreet(game.board.getBox(16))
    camille.buyAStreet(game.board.getBox(18))
    camille.buyAStreet(game.board.getBox(19))
    lucien.setPosition(6)
    chloe.setPosition(1)
    gildas.setPosition(11)
    camille.setPosition(16)
    game.putHomes(chloe)
    game.putHomes(lucien)
    game.putHomes(gildas)
    game.putHomes(camille)
    if (chloe.getMoney() == INITIAL_MONEY - 120 - 5*50 and game.board.getBox(1).getHome() == 5 and game.board.getBox(6).getHome() == 0 and lucien.getMoney() == INITIAL_MONEY - 100 and gildas.getMoney() == INITIAL_MONEY - 100 - 140-140-160 and game.board.getBox(11).getHome() == 1 and game.board.getBox(13).getHome() == 0 and camille.getMoney() == INITIAL_MONEY -180-180-200 and game.board.getBox(16).getHome() == 0):
        print("\n",True)
    else:
        raise Exception('Test test_putHomes failed.')
    

def test_jail_chooseDouble():
    players = {0: "Chloe", 1: "Lucien"}
    game = Game(players)
    chloe = game.players[0]
    lucien = game.players[1]
    game.goToJail(chloe)   #enter
    game.goToJail(lucien)  #enter
    game.jail_chooseDouble(chloe, [2,2])    #enter
    game.jail_chooseDouble(lucien, [2,1])   #enter
    if (chloe.getInPrison() == False and chloe.getPrisonTurn() == None and chloe.getPosition() == 14 and lucien.getPosition() == 10 and lucien.getInPrison() == True and lucien.getPrisonTurn() == 1):
        print("\n",True)
    else :
        raise Exception('Test test_jail_chooseDouble failed.')
        
        

def test_actualizePositionAux():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas"}
    game = Game(players)
    chloe = game.players[0]
    lucien = game.players[1]
    gildas = game.players[2]
    chloe.setPosition(12)
    lucien.setPosition(39)
    gildas.setPosition(31)
    game.actualizePositionAux(chloe, [2, 1])
    game.actualizePositionAux(lucien, [6, 1])
    game.actualizePositionAux(gildas, [4, 5])
    if chloe.getPosition() == 15 and lucien.getPosition() == 6 and lucien.getMoney() == INITIAL_MONEY +200 and gildas.getPosition() == 0 and gildas.getMoney() == INITIAL_MONEY + 200:
        print("\n",True)
    else:
        raise Exception('Test test_actualizePosition failed.')
        
        
        

def test_jail_chooseToPay():
    players = {0: "Chloe", 1: "Lucien"}
    game = Game(players)
    chloe = game.players[0]
    game.goToJail(chloe)
    game.jail_chooseToPay(chloe)
    if (chloe.getPosition() > 10 and chloe.getMoney() == INITIAL_MONEY - 50 and chloe.getInPrison() == False and chloe.getPrisonTurn() == None):
        print("\n",True) 
    else : 
        raise Exception('Test test_jail_chooseToPay failed.')



def test_onAStreetOrStation():
    # cas 1 : terrain dispo et assez d'argent OUI
    # cas 2 : gare diso et assez d'argent   OUI
    # cas 3 : terrain dispo et assez d'argent en ayant les autres terrains de la meme couleur OUI terrain OUI maison
    # cas 4 : terrain dispo mais pas assez d'argent
    # cas 5 : terrain dispo assez d'argent NON
    # cas 6 : gare dispo assez d'argent NON
    # cas 7 : sa propriete, pas les autres donc pas de maisons
    # cas 8 : sa propriete, avec les autres donc maisons OUI
    # cas 9: propriete de qqn d'autre --> payer la rent (verif owner gagne argent et player perd)
    players = {
        0: "Chloe",
        1: "Lucien",
        2: "Gildas",
        3: "Camille",
        4: "Milou",
        5: "Delcourt",
        6: "Mayeul",
        7: "Samy",
        8: "Ines",
        9: "Milene"
    }
    game = Game(players)
    chloe = game.players[0]
    lucien = game.players[1]
    gildas = game.players[2]
    camille = game.players[3]
    milou = game.players[4]
    delcourt = game.players[5]
    mayeul = game.players[6]
    samy = game.players[7]
    ines = game.players[8]
    milene = game.players[9]
    chloe.setPosition(1)
    game.onAStreetOrStation(chloe)    # oui + enter
    gildas.setPosition(5)
    game.onAStreetOrStation(gildas)   # oui + enter
    lucien.setPosition(39)
    lucien.buyAStreet(game.board.getBox(37))
    game.onAStreetOrStation(lucien)   # oui + enter + oui + 4 + enter
    camille.setPosition(6)
    camille.LooseMoney(INITIAL_MONEY-10)
    game.onAStreetOrStation(camille)  #enter
    milou.setPosition(8)
    game.onAStreetOrStation(milou)    #non + enter
    delcourt.setPosition(15)
    game.onAStreetOrStation(delcourt) #non + enter
    mayeul.setPosition(16)
    mayeul.buyAStreet(game.board.getBox(16))
    game.onAStreetOrStation(mayeul)   #enter
    samy.setPosition(21)
    samy.buyAStreet(game.board.getBox(21))
    samy.buyAStreet(game.board.getBox(23))
    samy.buyAStreet(game.board.getBox(24))
    game.onAStreetOrStation(samy)     #enter + oui + 2 + enter
    milene.buyAStreet(game.board.getBox(26))
    ines.setPosition(26)
    game.onAStreetOrStation(ines)     #enter
    if (chloe.getGoods()[0] == game.board.getBox(1) and chloe.getMoney() == INITIAL_MONEY - 60 and game.board.getBox(1).getOwner() == chloe and gildas.getGoods()[0] == game.board.getBox(5) and gildas.getMoney() == INITIAL_MONEY - 200 and game.board.getBox(5).getOwner() == gildas and lucien.getGoods()[0] == game.board.getBox(37) and lucien.getGoods()[1]== game.board.getBox(39) and game.board.getBox(39).getOwner() == lucien and lucien.getMoney() == INITIAL_MONEY - 750 -4*200 and game.board.getBox(39).getHome() == 4 and camille.getGoods() == [] and camille.getMoney() == 10 and game.board.getBox(6).getOwner() == None and milou.getGoods() == [] and milou.getMoney() == INITIAL_MONEY and game.board.getBox(8).getOwner() == None and delcourt.getGoods() == [] and delcourt.getMoney() == INITIAL_MONEY and game.board.getBox(15).getOwner() == None and mayeul.getGoods()[0] == game.board.getBox(16) and game.board.getBox(16).getOwner() == mayeul and game.board.getBox(21).getHome() == 2 and samy.getMoney() == INITIAL_MONEY - 220-220-240-2*150 and game.board.getBox(21).getOwner() == samy and game.board.getBox(26).getOwner() == milene and ines.getMoney() == INITIAL_MONEY - 22 and milene.getMoney() == INITIAL_MONEY + 22 -260):
        print("\n",True)
    else:
        raise Exception('Test test_onAStreetOrAStation failed.')






def test_card_moove_backwards():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
    game = Game(players)
    chloe = game.players[0]
    chloe.setPosition(2)
    game.card_moove_backwards(chloe, 3)
    if chloe.getPosition() == 1:
        return True
    else:
        raise Exception('Test test_community_moove_backwards failed.')

def test_card_moove_forward():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
    game = Game(players)
    chloe = game.players[0]
    lucien = game.players[1]
    gildas = game.players[2]
    gildas.setPosition(17)
    lucien.setPosition(22)
    game.card_moove_forward(chloe, 11)
    game.card_moove_forward(gildas, 22)
    game.card_moove_forward(lucien, 26)
    if chloe.getPosition() == 0 and chloe.getMoney() == INITIAL_MONEY + 200 and gildas.getMoney() ==INITIAL_MONEY + 200 and gildas.getPosition() == 15 and lucien.getPosition() == 24 and lucien.getMoney() == INITIAL_MONEY :
        return True
    else:
        raise Exception('Test test_card_moove_forward failed.')


def test_card_community_or_chance():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
    game = Game(players)
    chloe = game.players[0]
    lucien = game.players[1]
    game.card_community_or_chance(chloe, 6)
    game.card_community_or_chance(lucien, 6)
    if chloe.getMoney() == INITIAL_MONEY - 10:
        return True
    else:
        raise Exception('Test test_card_community_or_chance failed.')


def test_card_backwards():
    players = {0: "Chloe", 1: "Lucien", 2: "Gildas", 3: "Camille"}
    game = Game(players)
    chloe = game.players[0]
    lucien = game.players[1]
    gildas = game.players[2]
    camille = game.players[3]
    chloe.setPosition(2)
    lucien.setPosition(7)
    gildas.setPosition(33)
    camille.setPosition(36)
    game.card_backwards(chloe, 18)
    game.card_backwards(lucien, 18)
    game.card_backwards(gildas, 18)
    game.card_backwards(camille, 18)
    if chloe.getPosition() == 39 and lucien.getPosition() == 4 and lucien.getMoney() == INITIAL_MONEY - 200 and gildas.getInPrison() == True and gildas.getPosition() == 10 and gildas.getMoney() == INITIAL_MONEY:
        return True
    else:
        raise Exception('Test test_card_backwards failed.')



if __name__ == '__main__':
    if sys.argv[1] == "test_card_moove_forward":
        print(test_card_moove_forward())
    elif sys.argv[1] == "test_card_moove_backwards":
        print(test_card_moove_backwards())
    elif sys.argv[1] == "onAStreetOrStation":
        print(test_onAStreetOrStation())
    elif sys.argv[1] == "test_jail_chooseToPay":
        print(test_jail_chooseToPay())
    elif sys.argv[1] == "test_actualizePositionAux":
        print(test_actualizePositionAux())
    elif sys.argv[1] == "test_jail_chooseDouble":
        print(test_jail_chooseDouble())
    elif sys.argv[1] == "test_putHomes":
        print(test_putHomes())
    elif sys.argv[1] == "test_isInJail":
        print(test_isInJail())
    elif sys.argv[1] == "test_card_community_or_chance":
        print(test_card_community_or_chance())
    elif sys.argv[1] == "test_card_backwards":
        print(test_card_backwards())





