from src.porteFeuille import PorteFeuille
from random import *
from copy import deepcopy

#qty = {"aZeR":{"BTC":1, "BNB":9}}
class FausseAPI:
    def __init__(self, qty, values, verbose=False):
        self.qty=qty
        self.step={}
        self.values={}
        self.marketHistory = {}
        for key in qty:
            self.values[key]= values
            self.step[key] = 0
        self.verbose = verbose

    def getQuantity(self, crypto, apiKey):
        return self.qty[apiKey][crypto["monnaie"]]

    def getValue(self, crypto, apiKey):
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
        chng={}
        for key in self.values:
            tendance=""
            for monnaie in self.values[key]:
                if not monnaie in chng.keys():
                    chng[monnaie] = (randint(-ecart,ecart)+med)/1000

                if chng[monnaie]>=0:
                    tendance="gagné"
                else:
                    tendance="perdu"

                self.values[key][monnaie] += chng[monnaie] * self.values[key][monnaie]
                if self.verbose:
                    print("{4}: Le {0} a {1} {2}%! Maintenant il vaut {3}$!".format(monnaie, tendance, chng[monnaie]*100, self.values[key][monnaie], key))

    def setMarketHistory(self, start = 1535202562, stop = 1598360962, ecart=100, med=10):
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
    def printMarketHistory(self):
        for couple in self.marketHistory:
            _, values = couple
            for key in values:
                print("{0}:    {1}".format(key,values[key]))
    def step_(self, apiKey):
        if self.step[apiKey]>=len(self.marketHistory):
            return -1
        date, val = self.marketHistory[self.step[apiKey]]
        self.values[apiKey] = val[apiKey]
        if self.verbose:
            print(self.values[apiKey])
        self.step[apiKey]+=1
        return date
