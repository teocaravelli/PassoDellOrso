import os
import pickle

from models.prodotto import Prodotto
from models.prodotto_carrello import ProdottoCarrello

class GestoreProdotti:
    def __init__(self):
        self._prodotti = []
        self._file_path = "data/prodotti.pickle"
        self._carica_dati()

    def inserisciNuovoProdotto(self, prodotto) -> None:
        self._prodotti.append(prodotto)
        self._salva_dati()

    def getProdottoById(self, id_prodotto: int):
        for prodotto in self._prodotti:
            if prodotto.id == id_prodotto:
                return prodotto
        return None

    def eliminaProdotto(self, id_prodotto: int) -> bool:
        prodotto = self.getProdottoById(id_prodotto)
        if prodotto is not None:
            self._prodotti.remove(prodotto)
            self._salva_dati()
            return True
        return False

    def filtraProdottiPerTipo(self, tipo: str) -> list:
        return  [
            p for p in self._prodotti
            if p.__class__.__name__.lower() == tipo.lower()
        ]

    def modificaProdotto(self, id_prodotto: int, nuovo_prezzo: float, is_disponibile: bool) -> bool:
        prodotto = self.getProdottoById(id_prodotto)
        if prodotto is not None:
            prodotto.prezzo = nuovo_prezzo
            prodotto.is_disponibile = is_disponibile
            self._salva_dati()
            return True
        return False

    def aggiungiProdotto(self, cliente, prodotto, quantita_richiesta: int) -> None:
        if quantita_richiesta <= 0:
            raise ValueError("La quantità deve essere maggiore di zero.")
        if not getattr(prodotto, 'is_disponibile', True):
            raise ValueError("Il prodotto selezionato non è attualmente disponibile.")
        if hasattr(prodotto, 'quantita') and prodotto.quantita < quantita_richiesta:
            raise ValueError(f"Quantità richiesta non disponibile. Scorta attuale: {prodotto.quantita}")
        for item in cliente.prodotti_carrello:
            if item.prodotto.id == prodotto.id:
                nuova_quantita = item.quantita + quantita_richiesta
                if hasattr(prodotto, 'quantita') and prodotto.quantita < nuova_quantita:
                    raise ValueError("Quantità totale nel carrello superiore alla disponibilità.")
                item.quantita = nuova_quantita
                return
        nuovo_item = ProdottoCarrello(prodotto = prodotto, quantita = quantita_richiesta)
        cliente.prodotti_carrello.append(nuovo_item)

    def visualizzaCarrello(self, cliente) -> list:
        return cliente.prodotti_carrello

    def rimuoviProdottoDalCarrello(self, cliente, prodotto_carrello) -> None:
        if prodotto_carrello in cliente.prodotti_carrello:
            cliente.prodotti_carrello.remove(prodotto_carrello)

    def modificaQuantitaCarrello(self, cliente, prodotto_carrello, nuova_quantita: int) -> bool:
        if prodotto_carrello not in cliente.prodotti_carrello:
            return False
        if nuova_quantita <= 0:
            self.rimuoviProdottoDalCarrello(cliente, prodotto_carrello)
            return True
        prodotto_catalogo = prodotto_carrello.prodotto
        if hasattr(prodotto_catalogo, 'quantita') and prodotto_catalogo.quantita < nuova_quantita:
            return False
        prodotto_carrello.quantita = nuova_quantita
        return True

    def _salva_dati(self):
        os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
        with open(self._file_path, "wb") as f:
            pickle.dump(self._prodotti, f)

    def _carica_dati(self):
        if os.path.exists(self._file_path):
            try:
                # Controlla che il file non sia completamente vuoto
                if os.path.getsize(self._file_path) > 0:
                    with open(self._file_path, 'rb') as f:
                        self._prodotti = pickle.load(f)
                else:
                    self._prodotti = []
            except (EOFError, pickle.UnpicklingError):
                # Se il file è un testo non valido (\xef) o è rovinato, lo ignora
                print(f"Attenzione: il file {self._file_path} era illeggibile. Inizializzo i prodotti da zero.")
                self._prodotti = []

    def get_tutti_prodotti(self) -> list:
        """Restituisce la lista di tutti i prodotti a catalogo."""
        return self._prodotti