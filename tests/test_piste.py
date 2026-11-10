import unittest
import os

from controllers.gestore_piste import GestorePiste

class MockPista:
    def __init__(self, id_pista, nome, difficolta, stato_apertura="APERTA"):
        self.id_pista = id_pista
        self.nome = nome
        self.difficolta = difficolta
        self.stato_apertura = stato_apertura

class UnitTestPiste(unittest.TestCase):

    def setUp(self):
        self.gestore = GestorePiste()
        self.gestore._file_path = "data/test_piste.pickle"
        self.gestore._piste = []

    def tearDown(self):
        if os.path.exists(self.gestore._file_path):
            os.remove(self.gestore._file_path)

    def test_inserisci_e_ricerca_pista(self):
        pista_nuova = MockPista(id_pista=0, nome="Rossa 1", difficolta="ROSSA")
        self.gestore.inserisciNuovaPista(pista_nuova)
        self.assertEqual(pista_nuova.id_pista, 1)
        self.assertEqual(len(self.gestore._piste), 1)
        trovata = self.gestore.getPistaById(1)
        self.assertIsNotNone(trovata)
        self.assertEqual(trovata.nome, "Rossa 1")

    def test_modifica_stato_pista_successo(self):
        pista = MockPista(1, "Azzurra", "AZZURRA", stato_apertura="APERTA")
        self.gestore.inserisciNuovaPista(pista)
        esito = self.gestore.modificaStatoPista(id_pista=1, nuovo_stato="MANUTENZIONE")
        self.assertTrue(esito)
        pista_modificata = self.gestore.getPistaById(1)
        self.assertEqual(pista_modificata.stato_apertura, "MANUTENZIONE")

    def test_modifica_stato_pista_inesistente(self):
        esito = self.gestore.modificaStatoPista(id_pista=999, nuovo_stato="CHIUSA")
        self.assertFalse(esito)

if __name__ == '__main__':
    unittest.main()
