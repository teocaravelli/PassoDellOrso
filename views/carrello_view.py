import os
import pickle
import datetime
from argparse import Namespace
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt


class CarrelloView(QWidget):
    def __init__(self, gestore_utenti, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)

        self.lbl_titolo = QLabel("IL TUO CARRELLO")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setStyleSheet("font-size: 26px; font-weight: bold; color: #1a365d; margin-bottom: 10px;")
        self.main_layout.addWidget(self.lbl_titolo)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet(
            "QScrollArea { border: 1px solid #ccc; border-radius: 8px; background-color: #f8f9fa; }")

        self.scroll_content = QWidget()
        self.layout_prodotti = QVBoxLayout(self.scroll_content)
        self.layout_prodotti.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_prodotti.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        self.lbl_totale = QLabel("Totale: € 0.00")
        self.lbl_totale.setStyleSheet("font-size: 22px; font-weight: bold; color: #1a365d;")
        self.lbl_totale.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.lbl_totale)

        self.layout_pulsanti = QHBoxLayout()
        self.layout_pulsanti.setSpacing(15)

        self.btn_acquista = QPushButton("Procedi all'Acquisto")
        self.btn_acquista.setStyleSheet("""
            QPushButton { background-color: #5cb85c; color: white; font-weight: bold; font-size: 15px; border: none; border-radius: 8px; padding: 10px; }
            QPushButton:hover { background-color: #4cae4c; }
            QPushButton:disabled { background-color: #cccccc; color: #666666; }
        """)

        self.btn_svuota = QPushButton("Svuota Carrello")
        self.btn_svuota.setStyleSheet("""
            QPushButton { background-color: #f0ad4e; color: white; font-weight: bold; font-size: 15px; border: none; border-radius: 8px; padding: 10px; }
            QPushButton:hover { background-color: #eea236; }
            QPushButton:disabled { background-color: #cccccc; color: #666666; }
        """)

        self.btn_indietro = QPushButton("Torna alla Dashboard")
        self.btn_indietro.setStyleSheet("""
            QPushButton { background-color: #1a365d; color: white; font-weight: bold; font-size: 15px; border: none; border-radius: 8px; padding: 10px; }
            QPushButton:hover { background-color: #2a528a; }
        """)

        for btn in [self.btn_acquista, self.btn_svuota, self.btn_indietro]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(45)
            self.layout_pulsanti.addWidget(btn)

        self.main_layout.addLayout(self.layout_pulsanti)

    def applica_stili(self):
        self.setStyleSheet("CarrelloView { background-color: white; font-family: Arial, sans-serif; }")

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_indietro)
        self.btn_svuota.clicked.connect(self.svuota_carrello)
        self.btn_acquista.clicked.connect(self.procedi_acquisto)

    def aggiorna_dati(self):
        while self.layout_prodotti.count():
            child = self.layout_prodotti.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        utente = getattr(self.gestore_utenti, 'utente_corrente', None)
        if not utente:
            self.lbl_totale.setText("Totale: € 0.00")
            return

        if not hasattr(utente, 'carrello'):
            utente.carrello = []

        carrello = utente.carrello
        totale = 0.0

        if not carrello:
            lbl_vuoto = QLabel("Il tuo carrello è vuoto.")
            lbl_vuoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_vuoto.setStyleSheet("font-size: 16px; color: #666; margin-top: 20px; border: none;")
            self.layout_prodotti.addWidget(lbl_vuoto)
            self.btn_acquista.setEnabled(False)
            self.btn_svuota.setEnabled(False)
        else:
            self.btn_acquista.setEnabled(True)
            self.btn_svuota.setEnabled(True)

            for index, item in enumerate(carrello):
                nome = getattr(item, 'nome', 'Prodotto')
                prezzo = getattr(item, 'prezzo', 0.0)
                qta = getattr(item, 'quantita', 1)
                subtotale = prezzo * qta
                totale += subtotale

                frame = QFrame()
                frame.setObjectName("RigaCarrello")
                frame.setStyleSheet(
                    "QFrame#RigaCarrello { background-color: white; border: 1px solid #e0e0e0; border-radius: 6px; padding: 10px; }")
                lay = QHBoxLayout(frame)

                lbl_info = QLabel(
                    f"<b style='font-size: 15px; color: #1a365d;'>{nome}</b><br>"
                    f"<span style='color: #555;'>Quantità: <b>{qta}</b> | Prezzo cad: € {prezzo:.2f} | </span>"
                    f"<b style='color: #5cb85c;'>Subtotale: € {subtotale:.2f}</b>"
                )
                lbl_info.setStyleSheet("border: none; background: transparent;")
                lbl_info.setTextFormat(Qt.TextFormat.RichText)

                btn_rimuovi = QPushButton("Rimuovi")
                btn_rimuovi.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_rimuovi.setFixedSize(100, 36)
                btn_rimuovi.setStyleSheet("""
                    QPushButton { background-color: #d9534f; color: white; font-weight: bold; font-size: 13px; border: none; border-radius: 6px; }
                    QPushButton:hover { background-color: #c9302c; }
                """)
                btn_rimuovi.clicked.connect(lambda checked, idx=index: self.rimuovi_singolo_prodotto(idx))

                lay.addWidget(lbl_info, stretch=1)
                lay.addWidget(btn_rimuovi)

                self.layout_prodotti.addWidget(frame)

        self.lbl_totale.setText(f"Totale: € {totale:.2f}")

    def rimuovi_singolo_prodotto(self, index):
        utente = self.gestore_utenti.utente_corrente
        if utente and hasattr(utente, 'carrello') and 0 <= index < len(utente.carrello):
            utente.carrello.pop(index)
            self.salva_dati_utente()
            self.aggiorna_dati()

    def svuota_carrello(self):
        utente = getattr(self.gestore_utenti, 'utente_corrente', None)
        if not utente or not getattr(utente, 'carrello', []):
            return

        reply = QMessageBox.question(self, "Conferma", "Sei sicuro di voler svuotare il carrello?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            utente.carrello.clear()
            self.salva_dati_utente()
            self.aggiorna_dati()

    # --- FUNZIONI DI ACCESSO E MODIFICA DELL'ATTRIBUTO QUANTITÀ ---
    def _leggi_id(self, prod):
        if hasattr(prod, 'getId') and callable(prod.getId):
            return prod.getId()
        if hasattr(prod, '__dict__'):
            for k, v in prod.__dict__.items():
                if k.lower().endswith('id') or k.lower().endswith('id_prodotto'):
                    return v
        return getattr(prod, 'id_prodotto', getattr(prod, 'id', None))

    def _leggi_nome(self, prod):
        if hasattr(prod, 'getNome') and callable(prod.getNome):
            return prod.getNome()
        if hasattr(prod, '__dict__'):
            for k, v in prod.__dict__.items():
                if k.lower().endswith('nome'):
                    return v
        return getattr(prod, 'nome', '')

    def _leggi_quantita(self, prod):
        if hasattr(prod, 'getQuantita') and callable(prod.getQuantita):
            return int(prod.getQuantita())
        for attr in ['quantita', 'quantità', '_quantita', '_quantità']:
            if hasattr(prod, attr):
                val = getattr(prod, attr)
                return int(val() if callable(val) else val)
        if hasattr(prod, '__dict__'):
            for k, v in prod.__dict__.items():
                if 'quantit' in k.lower():
                    return int(v)
        return 5  # Default per oggetti legacy senza attributo

    def _scala_quantita_prodotto(self, prod, qta_da_scalare):
        qta_attuale = self._leggi_quantita(prod)
        nuova_qta = max(0, qta_attuale - int(qta_da_scalare))

        # 1. Prova i metodi UML
        if hasattr(prod, 'decrementaQuantita') and callable(prod.decrementaQuantita):
            try:
                prod.decrementaQuantita(int(qta_da_scalare))
                return
            except Exception:
                pass
        if hasattr(prod, 'setQuantita') and callable(prod.setQuantita):
            try:
                prod.setQuantita(nuova_qta)
                return
            except Exception:
                pass

        # 2. Aggiorna direttamente nel dizionario dell'oggetto (funziona anche con attributi privati __quantita)
        aggiornato = False
        if hasattr(prod, '__dict__'):
            for k in list(prod.__dict__.keys()):
                if 'quantit' in k.lower():
                    prod.__dict__[k] = nuova_qta
                    aggiornato = True

        if not aggiornato:
            prod.quantita = nuova_qta

    def _trova_prodotto_in_inventario(self, inventario, id_cercato, nome_cercato):
        for p in inventario:
            id_p = self._leggi_id(p)
            if id_cercato is not None and id_p is not None and id_p == id_cercato:
                return p
        for p in inventario:
            if str(self._leggi_nome(p)).strip().lower() == str(nome_cercato).strip().lower():
                return p
        return None

    def procedi_acquisto(self):
        utente = getattr(self.gestore_utenti, 'utente_corrente', None)
        if not utente or not getattr(utente, 'carrello', []):
            return

        reply = QMessageBox.question(self, "Conferma Acquisto",
                                     f"Vuoi confermare l'ordine per un {self.lbl_totale.text()}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply != QMessageBox.StandardButton.Yes:
            return

        percorso_prodotti = "data/prodotti.pickle"
        inventario = []
        if os.path.exists(percorso_prodotti):
            with open(percorso_prodotti, "rb") as f:
                inventario = pickle.load(f)

        # Controllo disponibilità scorte prima di procedere
        for item_carrello in utente.carrello:
            ha_qta = getattr(item_carrello, 'ha_quantita_limitata', False)
            if ha_qta:
                id_cercato = getattr(item_carrello, 'id_prodotto', None)
                nome_cercato = getattr(item_carrello, 'nome', '')
                qta_richiesta = int(getattr(item_carrello, 'quantita', 1))

                prod_reale = next((p for p in inventario if
                                   getattr(p, 'id', None) == id_cercato or getattr(p, 'nome', '') == nome_cercato),
                                  None)
                if prod_reale:
                    qta_disp = getattr(prod_reale, 'quantita', 0)
                    if qta_disp < qta_richiesta:
                        QMessageBox.warning(self, "Scorte Insufficienti",
                                            f"Il prodotto '{nome_cercato}' ha esaurito le scorte (disponibili: {qta_disp}).")
                        return

        # Scalatura effettiva delle quantità dall'inventario e salvataggio
        lista_prodotti_ordine = []
        totale_ordine = 0.0

        for item_carrello in utente.carrello:
            ha_qta = getattr(item_carrello, 'ha_quantita_limitata', False)
            id_cercato = getattr(item_carrello, 'id_prodotto', None)
            nome_cercato = getattr(item_carrello, 'nome', 'Prodotto')
            qta_acquistata = int(getattr(item_carrello, 'quantita', 1))
            prezzo_unitario = float(getattr(item_carrello, 'prezzo', 0.0))

            if ha_qta:
                prod_reale = next((p for p in inventario if
                                   getattr(p, 'id', None) == id_cercato or getattr(p, 'nome', '') == nome_cercato),
                                  None)
                if prod_reale:
                    # Scala la quantità usando il metodo o l'attributo diretto
                    if hasattr(prod_reale, 'decrementa_quantita'):
                        prod_reale.decrementa_quantita(qta_acquistata)
                    else:
                        qta_attuale = getattr(prod_reale, 'quantita', 0)
                        prod_reale.quantita = max(0, qta_attuale - qta_acquistata)

            prodotto_ordine = Namespace(
                tipo_oggetto="ProdottoOrdine",
                id_prodotto=id_cercato,
                nome=nome_cercato,
                prezzo=prezzo_unitario,
                quantita=qta_acquistata
            )
            lista_prodotti_ordine.append(prodotto_ordine)
            totale_ordine += (prezzo_unitario * qta_acquistata)

        with open(percorso_prodotti, "wb") as f:
            pickle.dump(inventario, f)

        if self.main_window and hasattr(self.main_window, 'catalogo_view'):
            self.main_window.catalogo_view.prodotti = inventario

        ora_attuale = datetime.datetime.now()
        nuovo_ordine = Namespace(
            id_ordine=int(ora_attuale.timestamp()),
            data=ora_attuale.strftime("%d/%m/%Y %H:%M"),
            totale=totale_ordine,
            stato="COMPLETATO",
            prodotti=lista_prodotti_ordine
        )

        if not hasattr(utente, 'storico_ordini'):
            utente.storico_ordini = []
        utente.storico_ordini.append(nuovo_ordine)

        utente.carrello.clear()
        self.salva_dati_utente()

        QMessageBox.information(self, "Acquisto Completato",
                                "Ordine completato con successo! Le scorte sono state aggiornate.")
        self.torna_indietro()

    def salva_dati_utente(self):
        if hasattr(self.gestore_utenti, '_salva_dati'):
            self.gestore_utenti._salva_dati()
        elif hasattr(self.gestore_utenti, 'salva_dati'):
            self.gestore_utenti.salva_dati()

    def torna_indietro(self):
        if self.main_window:
            if hasattr(self.main_window, 'mostra_dashboard_cliente'):
                self.main_window.mostra_dashboard_cliente()
            elif hasattr(self.main_window, 'mostra_dashboard'):
                self.main_window.mostra_dashboard()