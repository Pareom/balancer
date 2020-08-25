import random
import sys
import time
from fausseAPI import FausseAPI
from threading import Thread
from porteFeuille import PorteFeuille

class SimulatorPF(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, verbose, api, apiKey, date):
        Thread.__init__(self)
        self.api = api
        self.date = date
        self.pf = PorteFeuille(self.api, apiKey, verbose=verbose)

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        while self.date!=-1:
            self.pf.balance(self.date)
            self.date = self.api.step_()
        print(self.pf.getGain()*100-100)

threads = []
qty={}
date = 1598360962-5*604800-1
for i in range(10):
    qty[i] = {"BTC":1, "BNB":9}
api = FausseAPI(qty=qty, verbose=False)
api.setMarketHistory(start = date)
for i in range(10):
    threads.append(SimulatorPF(False, api, i, date))
print("début")
start = time.time()
for i in threads:
    i.start()
for i in threads:
    i.join()

print("--- %s seconds ---" % (time.time() - start))
