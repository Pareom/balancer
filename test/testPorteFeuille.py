import unittest
from src.porteFeuille import PorteFeuille
from src.fausseAPI import FausseAPI



class TestPorteFeuille(unittest.TestCase):
    def test_initialisation(self):
        try:
            pf = PorteFeuille(None, 3)
        except AttributeError as err:
            self.assertEqual(err.args, ("'NoneType' object has no attribute 'getValue'",))

    def test_crypto(self):
        qty={}
        qty["3"] = {"BTC":1, "BNB":1}
        values = {"BTC":2, "BNB":2}
        goal = {"BTC":0.8, "BNB":0.2}
        api = FausseAPI(qty=qty, values=values,verbose=False)
        pf = PorteFeuille(api, "3", perGoal=goal)
        for c in pf.crypto:
            self.assertEqual(c["usdVal"],values[c["monnaie"]]*qty["3"][c["monnaie"]])
            self.assertEqual(c["goal"], goal[c["monnaie"]])
            self.assertEqual(c["actual"], 0.5)

    def test_balance(self):
        qty={}
        qty["3"] = {"BTC":1, "BNB":1}
        values = {"BTC":1, "BNB":3}
        goal = {"BTC":0.5, "BNB":0.5}
        api = FausseAPI(qty=qty, values=values,verbose=False)
        pf = PorteFeuille(api, "3", perGoal=goal)
        self.assertEqual(pf.crypto[0]["actual"], 0.25)
        self.assertEqual(pf.crypto[1]["actual"], 0.75)
        pf.balance(5)
        pf.update()
        for c in pf.crypto:
            self.assertEqual(c["actual"], 0.5)


    def test_total(self):
        qty={}
        values={}
        qty["3"] = {"BTC":1, "BNB":1}
        values = {"BTC":2, "BNB":50}
        api = FausseAPI(qty=qty, values= values,verbose=False)
        pf = PorteFeuille(api, "3")
        self.assertEqual(pf.total, 52)

if __name__ == '__main__':
    unittest.main()
