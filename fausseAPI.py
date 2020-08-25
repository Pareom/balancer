from porteFeuille import PorteFeuille

class FausseAPI:
    def __init__(self):
        self.qty={"aZeR":{"BTC":1, "BNB":98}}
        self.values={"BTC":2, "BNB":1}

    def getQuantity(self, crypto, apiKey):
        return self.qty[apiKey][crypto["monnaie"]]

    def getValue(self, crypto):
        return self.values[crypto["monnaie"]]

    def send(self, _from, _to, value, apiKey):
        print("{0} a envoyé {1}$ à {2}".format(_from, value, _to))
        self.qty[apiKey][_from]-=value/self.values[_from]
        self.qty[apiKey][_to]+= value/self.values[_to]

api = FausseAPI()
pf = PorteFeuille(api, "aZeR")
pf.balance()
pf.balance()
pf.balance()
pf.balance()
pf.balance()
pf.balance()
