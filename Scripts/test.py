import server
import amcp
import time
import json

#Starts the server
server = server.GSIServer(("127.0.0.1", 3000), "S8RL9Z6Y22TYQK45JB4V8PHRJJMD9DS9")
server.start_server()

server.get_info("map", "name")
print(server.get_info("map", "name"))
server.get_info("player", "state", "flashed")

roundStatus = server.get_info("phase_countdowns", "phase")
prevRoundStatus = roundStatus

ctWins = server.get_info("map", "team_ct", "score")
prevCT = ctWins
tWins = server.get_info("map", "team_t", "score")
prevT = tWins

bombState = server.get_info("bomb", "state")
prevBombState = bombState

i = 0

while i != 1:

    #print(server.get_info("phase_countdowns", "phase"))
    gameTime = (int(float(server.get_info("phase_countdowns", "phase_ends_in"))))
    print(gameTime)

    roundStatus = server.get_info("phase_countdowns", "phase")

    bombState = server.get_info("bomb", "state")
    #print(server.get_info("bomb", "state"))

    if roundStatus == "over" and prevRoundStatus != roundStatus:
        ctWins = server.get_info("map", "team_ct", "score")
        tWins = server.get_info("map", "team_t", "score")
        prevRoundStatus = roundStatus

        if prevCT != ctWins:
            print(tWins, "T-Side")
            print(ctWins, "CT-Side won")
            prevCT = ctWins
            #amcp.connect.transact('clear 1')
            #amcp.connect.transact('PLAY 1 "IMAGES/CSGO GUI BLANK" CUT 1 Linear RIGHT LOOP')

        elif prevT != tWins:
            print(tWins, "T-Side won")
            print(ctWins, "CT-Side")
            prevT = tWins
            #amcp.connect.transact('clear 1')
            #amcp.connect.transact('PLAY 1 "QUICK DEAG MONTAGE" CUT 1 Linear RIGHT LOOP')
        time.sleep(1)

    #For bomb?
    elif prevRoundStatus != roundStatus and roundStatus == "bomb":
        prevRoundState = roundStatus
        time.sleep(1)

    elif prevBombState != bombState:
        if bombState == "dropped":
            print("The bomb has been dropped")
            prevBombState = bombState
        elif bombState == "carried":
            print("The bomb is getting carried")
            prevBombState = bombState
        elif bombState == "planted":
            print("Tick tick")
            prevBombState = bombState
        #elif bombState == "planting":
        #    print("Saleelul sawarim")
        #    prevBombState = bombState
        elif bombState == "exploded":
            print("Kaboom")
            prevBombState = bombState
        #elif bombState == "defusing":
        #    print("Defusing smile")
        #    prevBombState = bombState
        elif bombState == "defused":
            print("Bomb has been defused")
            prevBombState = bombState
        #elif bombState == "none":
        #    print("No info")
        #    prevBombState = bombState

        time.sleep(1)
    else:
        p = {"BombStatus": prevBombState, "ctWins": prevCT, "tWins": prevT, "roundStatus": prevRoundStatus, "roundTime": gameTime}
        with open("GameInfo.json", "w", encoding="utf-8") as f:
            json.dump(p, f, ensure_ascii=False, indent=4)
            q = json.dumps(p)
            print(q)
            f.seek(0)
        print("Nothing new to report")
        time.sleep(1)