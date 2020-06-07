import server
import amcp
import time
import keyboard

#Starts the server
server = server.GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
server.start_server()

uiSide = "Left"
visible = False

roundStatus = server.get_info("phase_countdowns", "phase")
prevRoundStatus = roundStatus

roundsPlayed = server.get_info("map", "round")

ctWins = server.get_info("map", "team_ct", "score")
prevCT = ctWins
tWins = server.get_info("map", "team_t", "score")
prevT = tWins

bombState = server.get_info("bomb", "state")
prevBombState = bombState

gameTime = 10

planted = False

team1 = "DYNASTY"
team2 = "MCON ESPORTS"

i = 0

# amcp.connect.transact("clear 1")
amcp.connect.transact('PLAY 1-15 "CASPARJS2/01_INTERVIEW" CUT 1 Linear RIGHT')
#amcp.connect.transact('PLAY 1-14 "GUI-ELEMENTS/CSGO-GUI-ROUND-GRAPHS/T_CLEAN_UP_AFTER_PLANTED"')
#amcp.connect.transact('PLAY 1-14 "GUI-ELEMENTS/CSGO-GUI-ROUND-GRAPHS/T_BOMB_PLANT_TO_EXPLODE"')
#amcp.connect.transact('PLAY 1-14 "GUI-ELEMENTS/CSGO-GUI-ROUND-GRAPHS/T_WIN_CLEAN"')
#amcp.connect.transact('PLAY 1-14 "GUI-ELEMENTS/CSGO-GUI-ROUND-GRAPHS/CT_WIN_DEFUSE"')
#amcp.connect.transact('PLAY 1-14 "GUI-ELEMENTS/CSGO-GUI-ROUND-GRAPHS/CT_WIN_CLEAN"')


while i != 1:

    roundsPlayed = server.get_info("map", "round") + 1

    print(server.get_info("phase_countdowns", "phase"))
    roundStatus = server.get_info("phase_countdowns", "phase")

    if roundStatus == "live" or roundStatus == "freezetime":
        gameTime = (int(round(float(server.get_info("phase_countdowns", "phase_ends_in")))))
        print(gameTime)
    else:
        gameTime = ""

    # Tside is on the left upon boot up. Hold for half to a full second to let it switch sides.
    if keyboard.is_pressed('x') and uiSide == "Left":
        uiSide = "Right"
    elif keyboard.is_pressed('x') and uiSide == "Right":
        uiSide = "Left"

    if keyboard.is_pressed('v') and visible == False:
        visible = True
        amcp.connect.transact('PLAY 1-15 "CASPARJS2/01_INTERVIEW" CUT 1 Linear RIGHT')
    elif keyboard.is_pressed('v') and visible == True:
        visible = False

    if keyboard.is_pressed('1'):
        team1 = "DYNASTY"
    elif keyboard.is_pressed('2'):
        team1 = "MCON ESPORTS"
    elif keyboard.is_pressed('3'):
        team1 = "4ELEMENTS"
    elif keyboard.is_pressed('4'):
        team1 = "ECV ESPORTS"

    if keyboard.is_pressed('6'):
        team2 = "DYNASTY"
    elif keyboard.is_pressed('7'):
        team2 = "MCON ESPORTS"
    elif keyboard.is_pressed('8'):
        team2 = "4ELEMENTS"
    elif keyboard.is_pressed('9'):
        team2 = "ECV ESPORTS"

    bombState = server.get_info("bomb", "state")
    #print(server.get_info("bomb", "state"))vvvvvv

    if visible == False:
        amcp.connect.transact('clear 1-14')
        amcp.connect.transact('clear 1-15')
    elif uiSide == "Left":
        amcp.connect.transact(
            r'CG 1-15 UPDATE 1 "<templateData><componentData id=\"f0\"><data id=\"text\" value=\"' + str(gameTime) + r'\"/></componentData><componentData id=\"f1\"><data id=\"text\" value=\"' + team1 + r'\"/></componentData><componentData id=\"f2\"><data id=\"text\" value=\"' + team2 + r'\"/></componentData><componentData id=\"f4\"><data id=\"text\" value=\"' + str(roundsPlayed) + r'/30\"/></componentData><componentData id=\"f5\"><data id=\"text\" value=\"' + str(
                tWins) + r'\"/></componentData><componentData id=\"f6\"><data id=\"text\" value=\"' + str(
                ctWins) + r'\"/></componentData></templateData>"')
    elif uiSide == "Right":
        amcp.connect.transact(
            r'CG 1-15 UPDATE 1 "<templateData><componentData id=\"f0\"><data id=\"text\" value=\"' + str(gameTime) + r'\"/></componentData><componentData id=\"f1\"><data id=\"text\" value=\"' + team2 + r'\"/></componentData><componentData id=\"f2\"><data id=\"text\" value=\"' + team1 + r'\"/></componentData><componentData id=\"f4\"><data id=\"text\" value=\"' + str(roundsPlayed) + r'/30\"/></componentData><componentData id=\"f5\"><data id=\"text\" value=\"' + str(
                ctWins) + r'\"/></componentData><componentData id=\"f6\"><data id=\"text\" value=\"' + str(
                tWins) + r'\"/></componentData></templateData>"')

    if roundStatus == "over" and prevRoundStatus != roundStatus:
        ctWins = server.get_info("map", "team_ct", "score")
        tWins = server.get_info("map", "team_t", "score")

    #For bomb graphic
    #elif prevRoundStatus != roundStatus and roundStatus == "bomb":
    #    prevRoundState = roundStatus
    #    if(bombState == "defused" and prevBombState != bombState):
    #        time.sleep(1)

    elif prevBombState != bombState:
        if bombState == "dropped":
            print("The bomb has been dropped")
            prevBombState = bombState
        elif bombState == "carried":
            print("The bomb is getting carried")
            RoundEnd = False
            prevBombState = bombState
        elif bombState == "planted":
            print("Tick tick")
            prevBombState = bombState
        elif bombState == "planting":
            print("Saleelul sawarim")
            prevBombState = bombState
        elif bombState == "exploded":
            print("Kaboom")
            prevBombState = bombState
        elif bombState == "defusing":
            print("Defusing smile")
            prevBombState = bombState
        elif bombState == "defused":
            print("Bomb has been defused")
            prevBombState = bombState
        elif bombState == "none":
            print("No info")
            prevBombState = bombState

    else:
        print("Nothing new to report")

    # Bomb naar clean up T werkt nu, defuse works, Clean round wins work, just not bomb to Clean up Bomb naar clean up ook?

    #If the bomb explodes, some states go weird?
    if roundStatus == "bomb" and planted == False and visible == True:
        planted = True
        amcp.connect.transact('PLAY 1-14 "GUI-ELEMENTS/CSGO-BOMB-GRAPHS/T_BOMB_KABOOM"')
    elif roundStatus == "over" and prevT != tWins and prevBombState == "exploded" and planted == True and visible == True:
        planted = False
        prevT = tWins
    #Dit werkt
    elif roundStatus == "over" and prevT != tWins and prevBombState == "planted" and planted == True and visible == True:
        planted = False
        prevT = tWins
        amcp.connect.transact('PLAY 1-14 "GUI-ELEMENTS/CSGO-BOMB-GRAPHS/T_CLEAN_UP"')
    elif roundStatus == "over" and prevT != tWins and prevBombState == "planted" and planted == False and visible == True:
        prevT = tWins
        amcp.connect.transact('PLAY 1-14 "GUI-ELEMENTS/CSGO-BOMB-GRAPHS/T_CLEAN"')
    #Dit werkt
    elif roundStatus == "over" and bombState == "defused" and planted == True and visible == True:
        planted = False
        prevCT = ctWins
        amcp.connect.transact('PLAY 1-14 "GUI-ELEMENTS/CSGO-BOMB-GRAPHS/CT_DEFUSE"')
    elif roundStatus == "over" and prevCT != ctWins and planted == False and visible == True:
        prevCT = ctWins
        amcp.connect.transact('PLAY 1-14 "GUI-ELEMENTS/CSGO-BOMB-GRAPHS/CT_CLEAN"')


    #amcp.connect.transact(r'CG 1-15 UPDATE 1 "<templateData><componentData id=\"f0\"><data id=\"text\" value=\"' + str(gameTime) + r'\"/></componentData><componentData id=\"f1\"><data id=\"text\" value=\"ecv\"/></componentData><componentData id=\"f2\"><data id=\"text\" value=\"mco\"/></componentData></templateData>"')
    time.sleep(0.5)
