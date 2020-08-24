import random
import sys
import time
from threading import Thread
from porteFeuille import PorteFeuille

class SimulatorPF(Thread):

    """Thread chargé simplement d'afficher une lettre dans la console."""

    def __init__(self, lettre):
        Thread.__init__(self)
        self.pf = PorteFeuille()
        self.lettre = lettre

    def run(self):
        """Code à exécuter pendant l'exécution du thread."""
        i = 0
        while i < 104:
            self.pf.balance()
            i += 1

threads = []
for i in range(1):
    threads.append(SimulatorPF(str(i)))
print("début")
start = time.time()
for i in threads:
    i.start()
for i in threads:
    i.join()

print("--- %s seconds ---" % (time.time() - start))
