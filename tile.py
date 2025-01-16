import math

class tile :
    is_mine = False
    is_flagged = False
    mine_value = 1
    location = []
    surrounding_mine = 0
    
    def __init__(self,location, is_mine = False, mine_value = 1,):
        self.is_mine = is_mine
        self.location = location
        self.mine_value = 1
    
    def surronding_mines(self, list, away=1):
        '''checks the surronding tile and count the mine to update the surounding mine value'''
        for i in range(0, 1+away**2):
            for f in range(0, 1+away**2):
                try :
                    if list[math.floor(self.location[0]-away/2+f)][math.floor(self.location[0]-away/2+i)].is_mine():
                        self.surronding_mines += 1
                except:
                    pass
    

    def discover():
        pass