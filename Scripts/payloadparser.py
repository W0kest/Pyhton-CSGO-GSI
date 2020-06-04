import information

class PayloadParser:
    def parse_payload(self, payload, gamestate):

        for item in payload:
            # print(payload)
            if item == 'allplayers':
                for counter, value in enumerate (payload[item]):
                    for i in payload[item][value]:
                        setattr(getattr(gamestate,"allplayers")[counter], i , payload[item][value][i])
                    setattr(getattr(gamestate,"allplayers")[counter],'playerid',value)
            elif item == 'grenades':
                if payload[item] != {}:
                    grenades = gamestate.grenades
                    number_grenades = len(grenades)
                    for grenade_id in payload[item]:
                        #for each grenade, exist in .Grenade list? Yes: edit it. No: append the list with new grenade.
                        found = False
                        for counter in range(number_grenades):
                            if grenade_id == getattr(grenades[counter], 'id'):
                                for i in payload[item][grenade_id]:
                                    setattr(grenades[counter], i, payload[item][grenade_id][i])
                                setattr(grenades[counter], 'id', grenade_id)
                                found = True
                                break

                        if found is False:
                            grenades.append(information.Grenades())
                            for i in payload[item][grenade_id]:
                                setattr(grenades[-1], i, payload[item][grenade_id][i])
                            setattr(grenades[-1], 'id', grenade_id)

            if item == 'round':
                if i == 'phase':
                    if (payload['round']['phase'] == 'freezetime' and 
                    gamestate.round.phase != payload['round']['phase']):
                        gamestate.grenades = []
            else:
                for i in payload[item]:
                    
                    try:
                        setattr(getattr(gamestate, item), i, payload[item][i])
                    except:
                        pass