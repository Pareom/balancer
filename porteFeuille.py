import time

class PorteFeuille:
    def __init__(self, api, perGoal=[{"monnaie":"BTC","goal":0.8},{"monnaie":"BNB","goal":0.2}], loss_level=3, simulation=True):
        self.api = api
        self.perGoal = perGoal
        self.history = []
        self.perActual = []
        self.total = 0
        self.simulation = simulation
        if loss_level < 1:
            self.loss_level = 1
        if loss_level > 3:
            self.loss_level = 3
        self.loss_level = loss_level
        self.initCrypto()

    def initCrypto(self):
        self.crypto=[]
        for val in self.perGoal:
            self.crypto.append({"monnaie":val["monnaie"],\
                                "qty":0,\
                                "usdVal":0,\
                                "goal":val["goal"],\
                                "actual":0})
        self.update()

    def balance_1(self, senders, receivers):#TODO
        print("op")
    def balance_2(self, senders, receivers):#TODO
        print("moyen")
    def balance_3(self, senders, receivers):
        for sender in senders:
            if sender["monnaie"]!="BNB":#D'abord verifier si toutes les monnaies sont compatibles
                toSend = (sender["actual"]-sender["goal"])*sender["qty"]/sender["actual"]
                toSendUSD = self.api.send(sender["monnaie"], "BNB", toSend)
                print("Envoie de {0} {1} à BNB, cela fait {2}$".format(toSend, sender["monnaie"], toSendUSD))#TODO
        for receiver in receivers:
            if receiver["monnaie"]!="BNB":#D'abord verifier si toutes les monnaies sont compatibles
                toSend = (receiver["goal"]-receiver["actual"])*receiver["qty"]/receiver["actual"]
                toSendUSD = self.api.send("BNB", receiver["monnaie"], toSend)
                print("Envoie de {0} BNB à {1}, cela fait {2}$".format(toSend, receiver["monnaie"], toSendUSD))#TODO


    def balance(self):
        self.update()
        time.sleep(0.200)
        senders = [] #crypto qui sont trop hautes
        receivers = [] #crypto qui sont trop basses
        for crypto in self.crypto:
            if crypto["goal"]-crypto["actual"]>(0.001/100):
                receivers.append(crypto)
            elif crypto["actual"]-crypto["goal"]>(0.001/100):
                senders.append(crypto)
            else:
                print("{0}: G:{1}% Act:{2}% ==> Pas de transfert su cette monnaie".format(crypto["monnaie"],crypto["goal"]*100,crypto["actual"]*100))
        if self.loss_level == 1:
            self.balance_1(senders, receivers)
        if self.loss_level == 2:
            self.balance_2(senders, receivers)
        if self.loss_level == 3:
            self.balance_3(senders, receivers)

        self.history.append(("now",self.total))

    def getHistory(self, start=None, end=None):
        print("getHistory")

    def updateValues(self):
        self.total = 0
        for i in range(len(self.crypto)):
            value = self.api.getValue(self.crypto[i])
            self.crypto[i]["qty"] = self.api.getQuantity(self.crypto[i])
            self.crypto[i]["usdVal"] = self.crypto[i]["qty"] * value
            self.total+= self.crypto[i]["usdVal"]

    def update(self):
        self.updateValues()
        for i in range(len(self.crypto)):
            self.crypto[i]["actual"] = self.crypto[i]["usdVal"]/self.total