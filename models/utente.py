from abc import ABC, abstractmethod
from datetime import datetime

class Utente(ABC):
    def __init__(self, id_utente: int, nome: str, cognome: str, email: str,
                 password: str, numero_telefono: str):
        self._id_utente = id_utente
        self._nome = nome
        self._cognome = cognome
        self._email = email
        self._password = password
        self._numero_telefono = numero_telefono
        self._data_creazione = datetime.now()  # Data di creazione del profilo
        self._ultimo_accesso = datetime.now()

    @property
    def id_utente(self) -> int:
        return self._id_utente

    @property
    def nome(self) -> str:
        return self._nome

    @nome.setter
    def nome(self, valore: str):
        self._nome = valore

    @property
    def cognome(self) -> str:
        return self._cognome

    @cognome.setter
    def cognome(self, valore: str):
        self._cognome = valore

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, valore: str):
        self._email = valore

    @property
    def password(self) -> str:
        return self._password

    @password.setter
    def password(self, valore: str):
        self._password = valore

    @property
    def numero_telefono(self) -> str:
        return self._numero_telefono

    @numero_telefono.setter
    def numero_telefono(self, valore: str):
        self._numero_telefono = valore

    @property
    def data_creazione(self) -> datetime:
        return self._data_creazione

    @property
    def ultimo_accesso(self) -> datetime:
        return self._ultimo_accesso

    @ultimo_accesso.setter
    def ultimo_accesso(self, data: datetime):
        self._ultimo_accesso = data

    def aggiorna_ultimo_accesso(self):
        self._ultimo_accesso = datetime.now()

    def verifica_credenziali(self, email: str, password: str) -> bool:
        return self._email == email and self._password == password

    @abstractmethod
    def get_ruolo(self) -> str:
        pass