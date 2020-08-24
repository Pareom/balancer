from porteFeuille import PorteFeuille

class FausseAPI:
    def __init__(self):
        self.qty={"BTC":0.03, "BNB":300}
        self.values={"BTC":9500, "BNB":21}

    def getQuantity(self, crypto):
        print("Quantité de {0}: {1}".format(crypto["monnaie"], self.qty[crypto["monnaie"]]))
        return self.qty[crypto["monnaie"]]

    def getValue(self, crypto):
        return self.values[crypto["monnaie"]]

    def send(self, _from, _to, value):
        self.qty[_from]-=value
        usdVal = value*self.values[_from]
        self.qty[_to]+= usdVal/self.values[_to]
        return usdVal

api = FausseAPI()
pf = PorteFeuille(api)
pf.balance()
pf.balance()
pf.balance()
pf.balance()
pf.balance()
pf.balance()
