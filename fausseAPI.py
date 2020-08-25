from porteFeuille import PorteFeuille
from random import *
class FausseAPI:
    def __init__(self, qty = {"aZeR":{"BTC":1, "BNB":9}}):
        self.qty=qty
        self.values={"BTC":2, "BNB":200}

    def getQuantity(self, crypto, apiKey):
        return self.qty[apiKey][crypto["monnaie"]]

    def getValue(self, crypto):
        return self.values[crypto["monnaie"]]

    def send(self, _from, _to, value, apiKey):
        print("{0} a envoyé {1}$ à {2}".format(_from, value, _to))
        self.qty[apiKey][_from]= self.qty[apiKey][_from] - value/self.values[_from]
        self.qty[apiKey][_to]= self.qty[apiKey][_to] + value/self.values[_to]
        for key in self.qty[apiKey]:
            print("{0}: {1}$".format(key, self.qty[apiKey][key]*self.values[key]))

    def changeValuesRandom(self):
        for key in self.values:
            chng = (randint(-100,100)+10)/1000
            tendance=""
            if chng>=0:
                tendance="gagné"
            else:
                tendance="perdu"
            self.values[key] += chng * self.values[key]
            print("Le {0} a {1} {2}%! Maintenant il vaut {3}$!".format(key, tendance, chng*100, self.values[key]))

api = FausseAPI()
pf = PorteFeuille(api, "aZeR")
pf.balance()
api.changeValuesRandom()
pf.balance()
api.changeValuesRandom()
pf.balance()
api.changeValuesRandom()
pf.balance()
api.changeValuesRandom()
pf.balance()
print(pf.getHistory())
