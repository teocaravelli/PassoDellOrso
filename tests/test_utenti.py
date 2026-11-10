import unittest
import os
from unittest.mock import MagicMock

from controllers.gestore_utenti import GestoreUtenti
from models.cliente import Cliente
from models.dipendente import Dipendente


class UnitTestUtenti(unittest.TestCase):
    def setUp(self):
        self.mock_mail = MagicMock()
        self.gestore = GestoreUtenti(self.mock_mail)
        self.gestore._file_path = "data/test_utenti.pickle"
        self.gestore._utenti = []
        self.gestore.utente_corrente = None

    def tearDown(self):
        if os.path.exists(self.gestore._file_path):
            os.remove(self.gestore._file_path)

    def test_registra_cliente_successo(self):
        cliente = self.gestore.registraCliente("Mario", "Rossi", "mario@email.com", "password123", "3331234567")
        self.assertEqual(len(self.gestore._utenti), 1)
        self.assertIsInstance(cliente, Cliente)
        self.assertEqual(cliente.email, "mario@email.com")

        self.mock_mail.inviaEmailBenvenuto.assert_called_once_with("mario@email.com", "Mario")

    def test_registra_cliente_email_duplicata(self):
        self.gestore.registraCliente("Mario", "Rossi", "mario@email.com", "password123", "3331234567")
        with self.assertRaises(ValueError):
            self.gestore.registraCliente("Luigi", "Verdi", "mario@email.com", "passsicura89", "3330000000")

    def test_registra_cliente_password_corta(self):
        with self.assertRaises(ValueError):
            self.gestore.registraCliente("Mario", "Rossi", "mario@email.com", "corta", "3331234567")

    def test_richiesta_accesso_e_logout(self):
        self.gestore.registraCliente("Mario", "Rossi", "mario@email.com", "password123", "3331234567")
        utente_loggato = self.gestore.richiestaAccesso("mario@email.com", "password123")
        self.assertIsNotNone(utente_loggato)
        self.assertEqual(self.gestore.utente_corrente, utente_loggato)
        utente_fallito = self.gestore.richiestaAccesso("mario@email.com", "sbagliata")
        self.assertIsNone(utente_fallito)
        self.gestore.effettuaLogout()
        self.assertIsNone(self.gestore.utente_corrente)

    def test_aggiungi_metodo_pagamento_dipendente_rifiutato(self):
        dipendente = self.gestore.registraDipendente("Anna", "Neri", "anna@admin.com", "adminpass1", "3339999999")
        with self.assertRaises(TypeError):
            self.gestore.aggiungiNuovoMetodoPagamento(dipendente, "CartaFinta")


if __name__ == '__main__':
    unittest.main()
