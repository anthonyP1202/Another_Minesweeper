import math
from typing import List

class tile :
    is_mine = False
    is_flagged = False
    mine_value = 1
    location = []
    surrounding_mine = 0
    
    def __init__(self,location, is_mine = False, mine_value = 1,):
        self.is_mine = is_mine
        self.location = location
    
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


import random

long=15
larg=15

def make_table(x,y):
    table=[]
    for _ in range(y):
        bby_tab=[]
        for _ in range (x):
            bby_tab.append(0)
        table.append(bby_tab)
    return table




def random_bomb_location(table:List[List[tile]],numb_bomb):
    trash=[]
    rows = len(table)
    cols = len(table[0]) if rows > 0 else 0
    rand_row=0
    rand_col=0

    for rando in range(numb_bomb):
        rand_row=random.randint(0,rows-1)
        rand_col=random.randint(0,cols-1)
        if [rand_row,rand_col] in trash:
            rando-=1
        else:
            trash.append([rand_row,rand_col])
            table[rand_row][rand_col]=tile(is_mine=True, is_flagged = False, mine_value = 1 ,location = [] ,surrounding_mine = 0)
    
    return table





