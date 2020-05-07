import main

main.main()
board = main.board
from src.classes import User, Street, Box, Station, INITIAL_MONEY

#python input_test.py < input_answers.txt 

def test_isInJail():
    chloe=User("Chloe")                    #0_Money_chooseToTestDouble, double fail, stay in prison, one turn more
    lucien=User("Lucien")                  #1_Money_chooseToTestDouble, double fail, stay in prison, one turn more
    gildas = User("Gildas")                #2_Money_chooseToTestDouble, double fail, stay in prison, one turn more
    camille = User("Camille")              #3_Already 3 turns in prison, should get out  
    milou = User("Milou")                  #0_Money, choose to pay at first turn, gets out
    delcourt = User("Delcourt")            #1_Money, choose to pay at second turn, gets out
    mayeul = User("Mayeul")                #2_Money, choose to pay at third turn, gets out 
    samy = User("Samy")                    #0_No Money, double fail, one turn more in prison
    ines = User("Ines")                    #1_No Money, double fail, one turn more in prison 
    milene = User("Milene")                #2_No Money, double fail, one turn more in prison 
    yushan = User("yushan")                #0_Money_chooseToTestDouble, double suceeds, gets out
    grottier = User("Grottier")            #1_Money_chooseToTestDouble, double suceeds, gets out
    coco = User("Corentin")                #2_Money_chooseToTestDouble, double suceeds, gets out
    valentin = User("Valentin")            #0_NoMoney, double suceeds, gets out
    bielecki = User("Bielecki")            #1_NoMoney, double suceeds, gets out
    dalasse = User("Dalasse")              #2_NoMoney, double suceeds, gets out
    agathe = User("Agathe")                #3_NoMoney, gets out
    main.goToJail(chloe) # enter
    main.goToJail(lucien) # enter
    main.goToJail(gildas) # enter
    main.goToJail(camille) # enter
    main.goToJail(milou) #enter
    main.goToJail(delcourt) #enter
    main.goToJail(mayeul) #enter
    main.goToJail(samy) #enter
    main.goToJail(ines) #enter
    main.goToJail(milene) #enter
    main.goToJail(yushan) #enter
    main.goToJail(grottier) #enter
    main.goToJail(coco) #enter
    main.goToJail(valentin) #enter
    main.goToJail(bielecki) #enter
    main.goToJail(dalasse) #enter
    main.goToJail(agathe)  #enter
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
    main.isInJailAux(chloe, [6,4])    #2 + enter
    main.isInJailAux(lucien, [6,4])   #2 + enter
    main.isInJailAux(gildas, [6,4])   #2 + enter
    main.isInJailAux(camille, [6,4])  #enter + enter
    main.isInJailAux(milou, [6,4])    #1 + enter + enter
    main.isInJailAux(delcourt, [6,4]) #1 + enter + enter
    main.isInJailAux(mayeul, [6,4])   #1 + enter + enter
    main.isInJailAux(samy, [6,4])     #enter + enter
    main.isInJailAux(ines, [6,4])     #enter + enter
    main.isInJailAux(milene, [6,4])   #enter + enter
    main.isInJailAux(yushan, [4,4])   #2 + enter
    main.isInJailAux(grottier, [3,3]) #2 + enter
    main.isInJailAux(coco, [2,2])     #2 + enter
    main.isInJailAux(valentin, [1,1]) #enter + enter
    main.isInJailAux(bielecki, [6,6]) #enter + enter
    main.isInJailAux(dalasse, [5,5])  #enter + enter
    main.isInJailAux(agathe, [5,2])   #enter + enter
    
    if (chloe.getInPrison() == True and chloe.getPrisonTurn() == 1 and chloe.getMoney() == INITIAL_MONEY and lucien.getInPrison() == True and lucien.getPrisonTurn() == 2 and lucien.getMoney() == INITIAL_MONEY and gildas.getInPrison() == True and gildas.getPrisonTurn() == 3 and gildas.getMoney() == INITIAL_MONEY and camille.getInPrison() == False and camille.getPrisonTurn() == None and camille.getMoney() == INITIAL_MONEY and milou.getInPrison() == False and milou.getPrisonTurn() == None and milou.getMoney() == INITIAL_MONEY - 50 and delcourt.getInPrison() == False and delcourt.getPrisonTurn() == None and delcourt.getMoney() == INITIAL_MONEY -50 and mayeul.getInPrison() == False and mayeul.getPrisonTurn() == None and mayeul.getMoney() == INITIAL_MONEY -50 and samy.getInPrison() == True and samy.getPrisonTurn() == 1 and samy.getMoney() == 20 and ines.getInPrison() == True and ines.getPrisonTurn() == 2 and ines.getMoney() == 20 and milene.getInPrison() == True and milene.getPrisonTurn() == 3 and milene.getMoney() == 20 and yushan.getInPrison() == False and yushan.getPrisonTurn() == None and yushan.getMoney() == INITIAL_MONEY and yushan.getPosition() == 18 and grottier.getInPrison() == False and grottier.getPrisonTurn() == None and grottier.getMoney() == INITIAL_MONEY and grottier.getPosition() == 16 and coco.getInPrison() == False and coco.getPrisonTurn() == None and coco.getMoney() == INITIAL_MONEY and coco.getPosition() == 14 and valentin.getInPrison() == False and valentin.getPrisonTurn() == None and valentin.getMoney() == 20 and valentin.getPosition() == 12 and bielecki.getInPrison() == False and bielecki.getPrisonTurn() == None and bielecki.getMoney() == 20 and bielecki.getPosition() == 22 and dalasse.getInPrison() == False and dalasse.getPrisonTurn() == None and dalasse.getMoney() == 20 and dalasse.getPosition() == 20 and agathe.getInPrison() == False and agathe.getPrisonTurn() == None and agathe.getMoney() == 20 and agathe.getPosition() > 10) :
        print("\n",True)
    else : 
        raise Exception('Test test_isInJail failed.')
        
        
        

def test_putHomes():
    chloe = User("Chloe")
    lucien = User("Lucien")
    gildas = User("Gildas")
    camille = User("Camille")
    lucien.buyAStreet(board.getBox(6))
    chloe.buyAStreet(board.getBox(1))
    chloe.buyAStreet(board.getBox(3))
    gildas.buyAStreet(board.getBox(11))
    gildas.buyAStreet(board.getBox(13))
    gildas.buyAStreet(board.getBox(14))
    camille.buyAStreet(board.getBox(16))
    camille.buyAStreet(board.getBox(18))
    camille.buyAStreet(board.getBox(19))
    lucien.setPosition(6)
    chloe.setPosition(1)
    gildas.setPosition(11)
    camille.setPosition(16)
    main.putHomes(chloe)
    main.putHomes(lucien)
    main.putHomes(gildas)
    main.putHomes(camille)
    if (chloe.getMoney() == INITIAL_MONEY - 120 - 5*50 and board.getBox(1).getHome() == 5 and board.getBox(6).getHome() == 0 and lucien.getMoney() == INITIAL_MONEY - 100 and gildas.getMoney() == INITIAL_MONEY - 100 - 140-140-160 and board.getBox(11).getHome() == 1 and board.getBox(13).getHome() == 0 and camille.getMoney() == INITIAL_MONEY -180-180-200 and board.getBox(16).getHome() == 0):
        print("\n",True)
    else :
        raise Exception('Test test_putHomes failed.')
    

def test_jail_chooseDouble():
    chloe = User("chloe")
    lucien = User("lucien")
    main.goToJail(chloe)   #enter
    main.goToJail(lucien)  #enter
    main.jail_chooseDouble(chloe, [2,2])    #enter
    main.jail_chooseDouble(lucien, [2,1])   #enter
    if (chloe.getInPrison() == False and chloe.getPrisonTurn() == None and chloe.getPosition() == 14 and lucien.getPosition() == 10 and lucien.getInPrison() == True and lucien.getPrisonTurn() == 1):
        print("\n",True)
    else :
        raise Exception('Test test_jail_chooseDouble failed.')
        
        

def test_actualizePositionAux(): 
    chloe = User("Chloe", 12)
    lucien = User("Lucien", 39)
    gildas=User("Gildas", 31)
    main.actualizePositionAux(chloe, [2, 1])
    main.actualizePositionAux(lucien, [6, 1])
    main.actualizePositionAux(gildas, [4, 5])
    if (chloe.getPosition() == 15 and lucien.getPosition() == 6 and gildas.getPosition() == 0):
        print("\n",True)
    else :
        raise Exception('Test test_actualizePosition failed.')
        
        
        

def test_jail_chooseToPay():
    chloe = User("Chloe")
    main.goToJail(chloe)
    main.jail_chooseToPay(chloe)
    if (chloe.getPosition() > 10 and chloe.getMoney() == INITIAL_MONEY - 50 and chloe.getInPrison() == False and chloe.getPrisonTurn() == None):
        print("\n",True) 
    else : 
        raise Exception('Test test_jail_chooseToPay failed.')



def test_onAStreetOrStation():
    #cas 1 : terrain dispo et assez d'argent OUI
    #cas 2 : gare diso et assez d'argent   OUI
    #cas 3 : terrain dispo et assez d'argent en ayant les autres terrains de la meme couleur OUI terrain OUI maison
    #cas 4 : terrain dispo mais pas assez d'argent 
    #cas 5 : terrain dispo assez d'argent NON
    #cas 6 : gare dispo assez d'argent NON 
    #cas 7 : sa propriete, pas les autres donc pas de maisons
    #cas 8 : sa propriete, avec les autres donc maisons OUI
    #cas 9: propriete de qqn d'autre --> payer la rent (verif owner gagne argent et player perd)
    chloe=User("Chloe") 
    lucien=User("Lucien") 
    gildas = User("Gildas")  
    camille = User("Camille")    
    milou = User("Milou")   
    delcourt = User("Delcourt")    
    mayeul = User("Mayeul")      
    samy = User("Samy")          
    ines = User("Ines")            
    milene = User("Milene")
    chloe.setPosition(1)
    main.onAStreetOrStation(chloe)    # oui + enter
    gildas.setPosition(5)
    main.onAStreetOrStation(gildas)   # oui + enter
    lucien.setPosition(39)
    lucien.buyAStreet(board.getBox(37))
    main.onAStreetOrStation(lucien)   # oui + enter + oui + 4 + enter
    camille.setPosition(6)
    camille.LooseMoney(INITIAL_MONEY-10)
    main.onAStreetOrStation(camille)  #enter
    milou.setPosition(8)
    main.onAStreetOrStation(milou)    #non + enter
    delcourt.setPosition(15)
    main.onAStreetOrStation(delcourt) #non + enter
    mayeul.setPosition(16)
    mayeul.buyAStreet(board.getBox(16))
    main.onAStreetOrStation(mayeul)   #enter
    samy.setPosition(21)
    samy.buyAStreet(board.getBox(21))
    samy.buyAStreet(board.getBox(23))
    samy.buyAStreet(board.getBox(24))
    main.onAStreetOrStation(samy)     #enter + oui + 2 + enter
    milene.buyAStreet(board.getBox(26))
    ines.setPosition(26)
    main.onAStreetOrStation(ines)     #enter
    if (chloe.getGoods()[0] == board.getBox(1) and chloe.getMoney() == INITIAL_MONEY - 60 and board.getBox(1).getOwner() == chloe and gildas.getGoods()[0] == board.getBox(5) and gildas.getMoney() == INITIAL_MONEY - 200 and board.getBox(5).getOwner() == gildas and lucien.getGoods()[0] == board.getBox(37) and lucien.getGoods()[1]== board.getBox(39) and board.getBox(39).getOwner() == lucien and lucien.getMoney() == INITIAL_MONEY - 750 -4*200 and board.getBox(39).getHome() == 4 and camille.getGoods() == [] and camille.getMoney() == 10 and board.getBox(6).getOwner() == None and milou.getGoods() == [] and milou.getMoney() == INITIAL_MONEY and board.getBox(8).getOwner() == None and delcourt.getGoods() == [] and delcourt.getMoney() == INITIAL_MONEY and board.getBox(15).getOwner() == None and mayeul.getGoods()[0] == board.getBox(16) and board.getBox(16).getOwner() == mayeul and board.getBox(21).getHome() == 2 and samy.getMoney() == INITIAL_MONEY - 220-220-240-2*150 and board.getBox(21).getOwner() == samy and board.getBox(26).getOwner() == milene and ines.getMoney() == INITIAL_MONEY - 22 and milene.getMoney() == INITIAL_MONEY + 22 -260):
        print("\n",True)
    else : 
        raise Exception('Test test_onAStreetOrAStation failed.')
        

test_onAStreetOrStation()














