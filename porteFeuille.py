import time

class PorteFeuille:
    def __init__(self, api, apiKey, perGoal=[{"monnaie":"BTC","goal":0.8},{"monnaie":"BNB","goal":0.2}], loss_level=3, simulation=True, verbose=True):
        self.api = api
        self.perGoal = perGoal
        self.history = {}
        self.perActual = []
        self.total = 0
        self.apiKey = apiKey
        self.simulation = simulation
        self.verbose = verbose
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
        if self.verbose:
            print("op")
    def balance_2(self, senders, receivers):#TODO
        if self.verbose:
            print("moyen")
    def balance_3(self, senders, receivers):
        for sender in senders:
            if sender["monnaie"]!="BNB":#D'abord verifier si toutes les monnaies sont compatibles
                toSendUSD = (sender["actual"]-sender["goal"])*sender["usdVal"]/sender["actual"]
                if sender["actual"]-sender["goal"] <0:
                    if self.verbose:
                        print("Erreur sender: {0}%".format(sender["actual"]-sender["goal"]))
                self.api.send(sender["monnaie"], "BNB", toSendUSD, self.apiKey)
        for receiver in receivers:
            if receiver["monnaie"]!="BNB":#D'abord verifier si toutes les monnaies sont compatibles
                toSendUSD = (receiver["goal"]-receiver["actual"])*receiver["usdVal"]/receiver["actual"]
                if receiver["goal"]-receiver["actual"] <0:
                    if self.verbose:
                        print("Erreur receive: {0}%".format(receiver["goal"]-receiver["actual"]))
                self.api.send("BNB", receiver["monnaie"], toSendUSD, self.apiKey)

    def balance(self, _date):
        self.update()
        self.history[_date]= self.total
        time.sleep(0.200)
        senders = [] #crypto qui sont trop hautes
        receivers = [] #crypto qui sont trop basses
        for crypto in self.crypto:
            if crypto["goal"]-crypto["actual"]>(0.001/100):
                receivers.append(crypto)
            elif crypto["actual"]-crypto["goal"]>(0.001/100):
                senders.append(crypto)
            else:
                if self.verbose:
                    print("{0}: G:{1}% Act:{2}% ==> Pas de transfert".format(crypto["monnaie"],crypto["goal"]*100,crypto["actual"]*100))

        if self.loss_level == 1:
            self.balance_1(senders, receivers)
        if self.loss_level == 2:
            self.balance_2(senders, receivers)
        if self.loss_level == 3:
            self.balance_3(senders, receivers)
        if self.verbose:
            print("....................................")
    def getHistory(self, start=None, end=None):
        return self.history
    def getGain(self):
        late = -1
        soon = -1
        for key in self.history:
            if soon==-1 or key<soon:
                soon = key
                soon_v = self.history[key]
            if key>late:
                late = key
                late_v = self.history[key]
        return (late_v/soon_v)
    def updateValues(self):
        self.total = 0
        for i in range(len(self.crypto)):
            value = self.api.getValue(self.crypto[i], self.apiKey)
            self.crypto[i]["qty"] = self.api.getQuantity(self.crypto[i], self.apiKey)
            self.crypto[i]["usdVal"] = self.crypto[i]["qty"] * value
            self.total+= self.crypto[i]["usdVal"]
        if self.verbose:
            print("Total: {0}".format(self.total))
    def update(self):
        self.updateValues()
        for i in range(len(self.crypto)):
            self.crypto[i]["actual"] = self.crypto[i]["usdVal"]/self.total
