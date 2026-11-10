import unittest
import os
from controllers.gestore_prodotti import GestoreProdotti
from models.prodotto_carrello import ProdottoCarrello

class Attrezzatura:
    def __init__(self, id_prodotto, prezzo=100.0, quantita=10):
        self.id = id_prodotto
        self.prezzo = prezzo
        self.quantita = quantita
        self.is_disponibile = True

class SkiPass:
    def __init__(self, id_prodotto, prezzo=50.0):
        self.id = id_prodotto
        self.prezzo = prezzo
        self.is_disponibile = True

class MockCliente:
    def __init__(self):
        self.prodotti_carrello = []

class UnitTestProdotti(unittest.TestCase):

    def setUp(self):
        self.gestore = GestoreProdotti()
        self.gestore._file_path = "data/test_prodotti.pickle"
        self.gestore._prodotti = []

    def tearDown(self):
        if os.path.exists(self.gestore._file_path):
            os.remove(self.gestore._file_path)

    def test_inserisci_e_ricerca_prodotto(self):
        prodotto = SkiPass(id_prodotto=1)
        self.gestore.inserisciNuovoProdotto(prodotto)
        trovato = self.gestore.getProdottoById(1)
        self.assertIsNotNone(trovato)
        self.assertEqual(trovato.id, 1)

    def test_elimina_prodotto(self):
        self.gestore.inserisciNuovoProdotto(SkiPass(id_prodotto=1))
        esito = self.gestore.eliminaProdotto(1)
        self.assertTrue(esito)
        self.assertEqual(len(self.gestore._prodotti), 0)

    def test_modifica_prodotto(self):
        self.gestore.inserisciNuovoProdotto(SkiPass(id_prodotto=1, prezzo=50.0))
        esito = self.gestore.modificaProdotto(id_prodotto=1, nuovo_prezzo=75.0, is_disponibile=False)
        self.assertTrue(esito)
        prodotto_modificato = self.gestore.getProdottoById(1)
        self.assertEqual(prodotto_modificato.prezzo, 75.0)
        self.assertFalse(prodotto_modificato.is_disponibile)

    def test_filtra_prodotti_per_tipo(self):
        self.gestore.inserisciNuovoProdotto(Attrezzatura(id_prodotto=1))
        self.gestore.inserisciNuovoProdotto(Attrezzatura(id_prodotto=2))
        self.gestore.inserisciNuovoProdotto(SkiPass(id_prodotto=3))
        risultato = self.gestore.filtraProdottiPerTipo("Attrezzatura")
        self.assertEqual(len(risultato), 2)
        risultato_skipass = self.gestore.filtraProdottiPerTipo("SkiPass")
        self.assertEqual(len(risultato_skipass), 1)

    def test_aggiungi_prodotto_carrello_successo(self):
        cliente = MockCliente()
        sci = Attrezzatura(id_prodotto=1, quantita=5)
        self.gestore.aggiungiProdotto(cliente, sci, quantita_richiesta=2)
        self.assertEqual(len(cliente.prodotti_carrello), 1)
        self.assertEqual(cliente.prodotti_carrello[0].quantita, 2)
        self.assertIsInstance(cliente.prodotti_carrello[0], ProdottoCarrello)

    def test_aggiungi_prodotto_carrello_incremento_esistente(self):
        cliente = MockCliente()
        sci = Attrezzatura(id_prodotto=1, quantita=10)
        self.gestore.aggiungiProdotto(cliente, sci, quantita_richiesta=3)
        self.gestore.aggiungiProdotto(cliente, sci, quantita_richiesta=4)
        self.assertEqual(len(cliente.prodotti_carrello), 1)
        self.assertEqual(cliente.prodotti_carrello[0].quantita, 7)

    def test_aggiungi_prodotto_carrello_scorte_insufficienti(self):
        cliente = MockCliente()
        sci = Attrezzatura(id_prodotto=1, quantita=2)  # Solo 2 disponibili
        with self.assertRaises(ValueError):
            self.gestore.aggiungiProdotto(cliente, sci, quantita_richiesta=5)

    def test_modifica_quantita_carrello_azzeramento(self):
        cliente = MockCliente()
        sci = Attrezzatura(id_prodotto=1)
        item_carrello = ProdottoCarrello(sci, 2)
        cliente.prodotti_carrello.append(item_carrello)
        esito = self.gestore.modificaQuantitaCarrello(cliente, item_carrello, nuova_quantita=0)
        self.assertTrue(esito)
        self.assertEqual(len(cliente.prodotti_carrello), 0)

if __name__ == '__main__':
    unittest.main()
