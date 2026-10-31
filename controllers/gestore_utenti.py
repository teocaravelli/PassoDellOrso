import os
import pickle
from models.utente import Utente
from models.cliente import Cliente
from models.dipendente import Dipendente
from controllers.gestore_mail import GestoreMail

class GestoreUtenti:
    def __init__(self, gestore_mail: GestoreMail):
        self._utenti = []
        self._gestore_mail = gestore_mail
        self._file_path = "data/utenti.pickle"
        self.utente_corrente = None
        self._carica_dati()

    def getUtenteByMail(self, email:str ):
        for utente in self._utenti:
            if utente.email == email:
                return utente
        return None

    def validaPassword(self, password: str) -> bool:
        return len(password) >= 8

    def validaCredenziali(self, email: str, password: str) -> bool:
        utente = self.getUtenteByMail(email)
        if utente is not None and utente.password == password:
            return True
        return False

    def richiestaAccesso(self, email: str, password: str):
        if self.validaCredenziali(email, password):
            self.utente_corrente = self.getUtenteByMail(email)
            return self.utente_corrente
        return None

    def effettuaLogout(self) -> None:
        if self.utente_corrente is not None:
            self.utente_corrente = None

    def registraCliente(self, nome: str, cognome: str, email: str, password: str, telefono: str):
        if self.getUtenteByMail(email) is not None:
            raise ValueError("Email già in uso nel sistema.")
        if not self.validaPassword(password):
            raise ValueError("La password non rispetta i requisiti di sicurezza.")
        nuovo_id = 1 if not self._utenti else max(u.id_utente for u in self._utenti) + 1
        nuovo_cliente = Cliente(nuovo_id, nome, cognome, email, password, telefono)
        self._utenti.append(nuovo_cliente)
        self._salva_dati()
        self._gestore_mail.inviaEmailBenvenuto(email, nome)
        return nuovo_cliente

    def registraDipendente(self, nome: str, cognome: str, email: str, password: str, telefono: str):
        if self.getUtenteByMail(email) is not None:
            raise ValueError("Email già in uso nel sistema.")
        if not self.validaPassword(password):
            raise ValueError("La password non rispetta i requisiti di sicurezza.")
        nuovo_id_utente = 1 if not self._utenti else max(u.id_utente for u in self._utenti) + 1
        dipendenti = [u for u in self._utenti if isinstance(u, Dipendente)]
        nuovo_id_dipendente = 1 if not dipendenti else max(d.id_dipendente for d in dipendenti) + 1
        nuovo_dipendente = Dipendente(nuovo_id_utente, nuovo_id_dipendente, nome, cognome, email, password, telefono)
        self._utenti.append(nuovo_dipendente)
        self._salva_dati()
        self._gestore_mail.inviaEmailBenvenuto(email, nome)
        return nuovo_dipendente

    def rimuoviUtente(self, id_utente: int) -> bool:
        for utente in self._utenti:
            if utente.id_utente == id_utente:
                self._utenti.remove(utente)
                self._salva_dati()
                return True
        return False

    def aggiungiNuovoMetodoPagamento(self, utente, metodo_pagamento) -> None:
        if hasattr(utente, 'aggiungi_metodo_pagamento'):
            utente.aggiungi_metodo_pagamento(metodo_pagamento)
            self._salva_dati()
        else:
            raise TypeError("Operazione non consentita per questo tipo di utente.")

    def rimuoviMetodoPagamento(self, utente, codice_carta: str) -> bool:
        """Rimuove una carta dal profilo del cliente."""
        if hasattr(utente, 'rimuovi_metodo_pagamento'):
            esito = utente.rimuovi_metodo_pagamento(codice_carta)
            if esito:
                self._salva_dati()
            return esito
        return False

    def inserisciMail(self, email: str) -> None:
        if self.getUtenteByMail(email) is None:
            raise ValueError("Nessun utente trovato con questa email.")

    def recuperoCredenziali(self, email: str) -> None:
        if self.getUtenteByMail(email):
            self._gestore_mail.inviaEmailRecupero(email)

    def inserisciNuovaPassword(self, email: str, nuova_password: str) -> None:
        utente = self.getUtenteByMail(email)
        if utente and self.validaPassword(nuova_password):
            utente.password = nuova_password
            self._salva_dati()
            self._gestore_mail.inviaEmailModificaCredenziali(email)

    def _salva_dati(self):
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, "wb") as f:
            pickle.dump(self._utenti, f)

    def _carica_dati(self):
        if os.path.exists(self._file_path):
            with open(self._file_path, "rb") as f:
                self._utenti = pickle.load(f)
