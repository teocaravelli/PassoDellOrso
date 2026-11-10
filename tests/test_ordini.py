import unittest
import os
from unittest.mock import MagicMock

from controllers.gestore_ordini import GestoreOrdini
from models.enums import StatoOrdine
from models.ordine import Ordine

class MockProdotto:
    def __init__(self, id_prodotto, nome, prezzo, quantita=10):
        self.id_prodotto = id_prodotto
        self.id = id_prodotto  # <-- RIGA AGGIUNTA PER RISOLVERE L'ERRORE
        self.nome = nome
        self.prezzo = prezzo
        self.quantita = quantita
        self.is_disponibile = True

class MockItemCarrello:
    def __init__(self, prodotto, quantita):
        self.prodotto = prodotto
        self.quantita = quantita

class MockCliente:
    def __init__(self):
        self.email = "cliente@email.com"
        self.ordini = []
        self.carrello_svuotato = False

    def aggiungi_ordine(self, ordine):
        self.ordini.append(ordine)

    def svuota_carrello(self):
        self.carrello_svuotato = True

class UnitTestOrdini(unittest.TestCase):

    def setUp(self):
        self.mock_mail = MagicMock()
        self.mock_prodotti = MagicMock()
        self.gestore = GestoreOrdini(self.mock_mail, self.mock_prodotti)
        self.gestore._file_path = "data/test_ordini.pickle"
        self.gestore._ordini = []

    def tearDown(self):
        if os.path.exists(self.gestore._file_path):
            os.remove(self.gestore._file_path)

    def test_richiesta_ordine_successo(self):
        cliente = MockCliente()
        prodotto_finto = MockProdotto(id_prodotto=1, nome="Snowboard", prezzo=150.0, quantita=5)
        item = MockItemCarrello(prodotto=prodotto_finto, quantita=2)
        self.mock_prodotti.getProdottoById.return_value = prodotto_finto
        self.gestore.richiestaOrdine(cliente=cliente, carrello=[item], metodo_pagamento="CartaFinta")
        self.assertEqual(prodotto_finto.quantita, 3)
        self.mock_prodotti._salva_dati.assert_called_once()
        self.assertEqual(len(self.gestore._ordini), 1)
        ordine_creato = self.gestore._ordini[0]
        self.assertEqual(ordine_creato.prezzo_totale, 300.0)
        self.assertIn(ordine_creato, cliente.ordini)
        self.assertTrue(cliente.carrello_svuotato)
        self.mock_mail.inviaEmailConferma.assert_called_once_with("cliente@email.com", ordine_creato)

    def test_richiesta_ordine_quantita_insufficiente(self):
        cliente = MockCliente()
        prodotto_finto = MockProdotto(id_prodotto=1, nome="Snowboard", prezzo=150.0, quantita=1)
        item = MockItemCarrello(prodotto=prodotto_finto, quantita=3)
        self.mock_prodotti.getProdottoById.return_value = prodotto_finto
        with self.assertRaises(ValueError):
            self.gestore.richiestaOrdine(cliente, [item], "CartaFinta")

    def test_rimborso(self):
        ordine = Ordine(id_ordine=1, metodo_pagamento="Carta", prezzo_totale=100.0, prodotti=[])
        ordine.stato = StatoOrdine.COMPLETATO
        self.gestore._ordini.append(ordine)
        esito_richiesta = self.gestore.richiediRimborso(id_ordine=1, motivazione="Taglia errata")
        self.assertTrue(esito_richiesta)
        self.assertEqual(ordine.stato, StatoOrdine.RIMBORSO_RICHIESTO)
        self.gestore.gestisciRimborso(id_ordine=1, approvato=True)
        self.assertEqual(ordine.stato, StatoOrdine.RIMBORSO_COMPLETATO)

if __name__ == '__main__':
    unittest.main()
