import server
import amcp
import time
import keyboard

### Small disclaimer, the match has to run, in order for this work.

#Starts the server
try:
    print("Initialize FASE 1")
    server = server.GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
    print("Almost there")
    server.start_server()
    print("Server started")
except:
    print("Oepsie")

# All the Caspar paths.
HTMLTemplate = 'PLAY 1-15 "CASPARJS2/01_INTERVIEW" easenone 1 Linear RIGHT'

TBombPlanted = 'PLAY 1-14 "GUI-ELEMENTS/CSGO-BOMB-GRAPHS/T_BOMB_KABOOM"'
TCleanUpAfterPlant = 'PLAY 1-14 "GUI-ELEMENTS/CSGO-BOMB-GRAPHS/T_CLEAN_UP"'
TClean = 'PLAY 1-14 "GUI-ELEMENTS/CSGO-BOMB-GRAPHS/T_CLEAN"'

CTDefuse = 'PLAY 1-14 "GUI-ELEMENTS/CSGO-BOMB-GRAPHS/CT_DEFUSE"'
CTClean = 'PLAY 1-14 "GUI-ELEMENTS/CSGO-BOMB-GRAPHS/CT_CLEAN"'

# For the UI Elements.
uiSide = "Left"
visible = False
planted = False

# The standings in the match.
ctWins = server.get_info("map", "team_ct", "score")
prevCT = ctWins
tWins = server.get_info("map", "team_t", "score")
prevT = tWins

prevBombState = ""

team1 = "BUTTER"
team2 = "MARGARINE"

i = 0

# Keeps looping itself in order to update the overlay.
while i != 1:

    # Visibility toggle upon holding V for 0.5 seconds.
    if keyboard.is_pressed('v') and visible == False:
        amcp.connect.transact(HTMLTemplate)
        visible = True
        time.sleep(0.3)  # Is necessary so that the update doesn't overwrite something that isn't loaded yet.
    elif keyboard.is_pressed('v') and visible == True:
        visible = False

    # Makes the time appear as digital format.
    def convert(seconds):
        seconds = seconds % (24 * 3600)
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        # if minutes == 0:
        #     if seconds < 10:
        #         return "%d" % (seconds)
        #     return "%02d" % (seconds)

        # else:
        return "%2d:%02d" % (minutes, seconds)

    # Gets the round number.
    roundsPlayed = server.get_info("map", "round") + 1

    # Gets the round phase.
    roundStatus = server.get_info("phase_countdowns", "phase")

    # Rounds the phase timer and converts to int.
    if roundStatus == "live" or roundStatus == "freezetime":
        gameTime = (int(round(float(server.get_info("phase_countdowns", "phase_ends_in")))))
        gameTime = convert(gameTime)
        #print(gameTime)
    else:
        gameTime = ""

    # Tside is on the left upon boot up. Hold for half second to let it switch sides.
    if keyboard.is_pressed('x') and uiSide == "Left":
        uiSide = "Right"
    elif keyboard.is_pressed('x') and uiSide == "Right":
        uiSide = "Left"

    # This changes the team names, for now it's till manual instead of automatic.
    if keyboard.is_pressed('1'):
        team1 = "BUTTER"
    elif keyboard.is_pressed('2'):
        team1 = "MCON ESPORTS"
    elif keyboard.is_pressed('3'):
        team1 = "4ELEMENTS"
    elif keyboard.is_pressed('4'):
        team1 = "ECV ESPORTS"

    if keyboard.is_pressed('6'):
        team2 = "MARGARINE"
    elif keyboard.is_pressed('7'):
        team2 = "MCON ESPORTS"
    elif keyboard.is_pressed('8'):
        team2 = "4ELEMENTS"
    elif keyboard.is_pressed('9'):
        team2 = "ECV ESPORTS"

    # Here is where the visibility toggle gets executed.
    if visible == False:
        amcp.connect.transact('clear 1-14')
        amcp.connect.transact('clear 1-15')
    # Updates the graphic with all the information.
    else:
        if uiSide == "Left":
            amcp.connect.transact(
                r'CG 1-15 UPDATE 1 "<templateData><componentData id=\"f0\"><data id=\"text\" value=\"' + str(gameTime) + r'\"/></componentData><componentData id=\"f1\"><data id=\"text\" value=\"' + team1 + r'\"/></componentData><componentData id=\"f2\"><data id=\"text\" value=\"' + team2 + r'\"/></componentData><componentData id=\"f4\"><data id=\"text\" value=\"' + str(roundsPlayed) + r'/30\"/></componentData><componentData id=\"f5\"><data id=\"text\" value=\"' + str(
                    tWins) + r'\"/></componentData><componentData id=\"f6\"><data id=\"text\" value=\"' + str(
                    ctWins) + r'\"/></componentData></templateData>"')
        elif uiSide == "Right":
            amcp.connect.transact(
                r'CG 1-15 UPDATE 1 "<templateData><componentData id=\"f0\"><data id=\"text\" value=\"' + str(gameTime) + r'\"/></componentData><componentData id=\"f1\"><data id=\"text\" value=\"' + team2 + r'\"/></componentData><componentData id=\"f2\"><data id=\"text\" value=\"' + team1 + r'\"/></componentData><componentData id=\"f4\"><data id=\"text\" value=\"' + str(roundsPlayed) + r'/30\"/></componentData><componentData id=\"f5\"><data id=\"text\" value=\"' + str(
                    ctWins) + r'\"/></componentData><componentData id=\"f6\"><data id=\"text\" value=\"' + str(
                    tWins) + r'\"/></componentData></templateData>"')

    # When the round ends, gets the score of both teams to check who won.
    if roundStatus == "over" and prevT != tWins or roundStatus == "over" and prevCT != ctWins:
        ctWins = server.get_info("map", "team_ct", "score")
        tWins = server.get_info("map", "team_t", "score")

    # Gets the bomb state.
    bombState = server.get_info("bomb", "state")

    # Checks for all the different bomb states.
    if prevBombState != bombState:
        if bombState == "dropped":
            print("The bomb has been dropped")
            prevBombState = bombState
        elif bombState == "carried":
            print("The bomb is getting carried")
            RoundEnd = False
            prevBombState = bombState
        elif bombState == "planted":
            print("Planted")
            prevBombState = bombState
        elif bombState == "planting":
            print("Planting")
            prevBombState = bombState
        elif bombState == "exploded":
            print("Kaboom")
            prevBombState = bombState
        elif bombState == "defusing":
            print("Defusing")
            prevBombState = bombState
        elif bombState == "defused":
            print("Bomb has been defused")
            prevBombState = bombState
        elif bombState == "none":
            print("No info")
            prevBombState = bombState

    ### All the win conditions with graphics attached to it

    # Bomb has been planted
    if roundStatus == "bomb" and planted == False and visible == True:
        planted = True
        amcp.connect.transact(TBombPlanted)
    # Win condition when the bomb explodes.
    elif roundStatus == "over" and prevT != tWins and prevBombState == "exploded" and planted == True and visible == True:
        planted = False
        prevT = tWins
    # Clean up after plant T
    elif roundStatus == "over" and prevT != tWins and prevBombState == "planted" and planted == True and visible == True:
        planted = False
        prevT = tWins
        amcp.connect.transact(TCleanUpAfterPlant)
    # Clean T Win
    elif roundStatus == "over" and prevT != tWins and prevBombState == "planted" and planted == False and visible == True:
        prevT = tWins
        amcp.connect.transact(TClean)
    # CT Defused the bomb
    elif roundStatus == "over" and bombState == "defused" and planted == True and visible == True:
        planted = False
        prevCT = ctWins
        amcp.connect.transact(CTDefuse)
    # Clean CT Win
    elif roundStatus == "over" and prevCT != ctWins and planted == False and visible == True:
        prevCT = ctWins
        amcp.connect.transact(CTClean)

    # Sleeps the script so it doesn't keep looping without a break.
    time.sleep(0.5)