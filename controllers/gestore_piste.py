import os
import pickle


from models.pista import Pista
from models.enums import StatoApertura, Difficolta

class GestorePiste:
    def __init__(self):
        self._piste = []
        self._file_path = "data/piste.pickle"
        self._carica_dati()

    def visualizzaPiste(self) -> list:
        return self._piste

    def getPistaById(self, id_pista: int):
        for pista in self._piste:
            if getattr(pista, 'id_pista', None) == id_pista:
                return pista
        return None

    def filtraPistePerDifficolta(self, difficolta) -> list:
        return [p for p in self._piste if p.difficolta == difficolta]

    def modificaStatoPista(self, id_pista: int, nuovo_stato) -> bool:
        pista = self.getPistaById(id_pista)
        if pista:
            pista.stato_apertura = nuovo_stato
            self._salva_dati()
            return True
        return False

    def inserisciNuovaPista(self, pista) -> None:
        if getattr(pista, 'id', None) is None:
            nuovo_id = 1 if not self._piste else max(p.id_pista for p in self._piste) + 1
            pista.id_pista = nuovo_id
        self._piste.append(pista)
        self._salva_dati()

    def _salva_dati(self):
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, 'wb') as f:
            pickle.dump(self._piste, f)

    def _carica_dati(self):
        if os.path.exists(self._file_path):
            # Se il file esiste, proviamo a leggerlo
            try:
                # Controlliamo anche che non sia un file completamente vuoto
                if os.path.getsize(self._file_path) > 0:
                    with open(self._file_path, 'rb') as f:
                        self._piste = pickle.load(f)
                else:
                    self._piste = []
            except (EOFError, pickle.UnpicklingError):
                # Se il file è un testo non valido (errore \xef) o è rovinato, lo ignoriamo
                print(f"Attenzione: il file {self._file_path} era illeggibile. Inizializzo le piste da zero.")
                self._piste = []