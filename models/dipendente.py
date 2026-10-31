from models.utente import Utente

class Dipendente(Utente):
    def __init__(self, id_utente: int, id_dipendente: int, nome: str, cognome: str,
                 email: str, password: str, numero_telefono: str):
        super().__init__(id_utente, nome, cognome, email, password, numero_telefono)
        self._id_dipendente = id_dipendente

    @property
    def id_dipendente(self) -> int:
        return self._id_dipendente

    @id_dipendente.setter
    def id_dipendente(self, valore: int):
        self._id_dipendente = valore

    def get_ruolo(self) -> str:
        return "Dipendente"