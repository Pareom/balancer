from porteFeuille import PorteFeuille
from random import *
from copy import deepcopy

#qty = {"aZeR":{"BTC":1, "BNB":9}}
class FausseAPI:
    def __init__(self, qty, verbose=False):
        self.qty=qty
        self.step={}
        self.values={}
        self.marketHistory = {}
        for key in qty:
            self.values[key]={"BTC":2, "BNB":200}
            self.step[key] = 0
        self.verbose = verbose

    def getQuantity(self, crypto, apiKey):
        return self.qty[apiKey][crypto["monnaie"]]

    def getValue(self, crypto, apiKey):
        print(self.values)
        return self.values[apiKey][crypto["monnaie"]]

    def send(self, _from, _to, value, apiKey):
        if self.verbose:
            print("{0} a envoyé {1}$ à {2}".format(_from, value, _to))
        self.qty[apiKey][_from]= self.qty[apiKey][_from] - value/self.values[apiKey][_from]
        self.qty[apiKey][_to]= self.qty[apiKey][_to] + value/self.values[apiKey][_to]
        if self.verbose:
            for key in self.qty[apiKey]:
                print("{0}: {1}$".format(key, self.qty[apiKey][key]*self.values[apiKey]))

    def changeValuesRandom(self, ecart=100, med=10):
        for key in self.values:
            chng = (randint(-ecart,ecart)+med)/1000
            tendance=""
            if chng>=0:
                tendance="gagné"
            else:
                tendance="perdu"
            for monnaie in self.values[key]:
                self.values[key][monnaie] += chng * self.values[key][monnaie]
                if self.verbose:
                    print("Le {0} a {1} {2}%! Maintenant il vaut {3}$!".format(key, tendance, chng*100, self.values[key][monnaie]))

    def setMarketHistory(self, start = 1535202562, stop = 1598360962):
        self.marketHistory = []
        while start<stop:
            self.marketHistory.append((deepcopy(start), deepcopy(self.values)))
            self.changeValuesRandom()
            if self.verbose:
                print(self.values)

            start += 604800 #Une semaine
        if self.verbose:
            print(self.marketHistory)
        for key in self.values:
            self.step_(key)
    def step_(self, apiKey):
        if self.step[apiKey]>=len(self.marketHistory):
            return -1
        date, self.values[apiKey] = self.marketHistory[self.step[apiKey]]
        if self.verbose:
            print(self.values[apiKey])
        self.step[apiKey]+=1
        return date
