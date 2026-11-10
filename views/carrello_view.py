from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox
)
from PyQt6.QtCore import Qt


class CarrelloView(QWidget):
    def __init__(self, gestore_utenti, gestore_ordini, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.gestore_ordini = gestore_ordini
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

        if not hasattr(utente, 'prodotti_carrello'):
            utente.prodotti_carrello = []

        carrello = utente.prodotti_carrello
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
                prodotto = getattr(item, 'prodotto', None)
                if not prodotto:
                    continue

                nome = getattr(prodotto, 'nome', 'Prodotto')
                prezzo = getattr(prodotto, 'prezzo', 0.0)
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
        if utente and hasattr(utente, 'prodotti_carrello') and 0 <= index < len(utente.prodotti_carrello):
            utente.prodotti_carrello.pop(index)
            self.salva_dati_utente()
            self.aggiorna_dati()

    def svuota_carrello(self):
        utente = getattr(self.gestore_utenti, 'utente_corrente', None)
        if not utente or not getattr(utente, 'prodotti_carrello', []):
            return

        reply = QMessageBox.question(self, "Conferma", "Sei sicuro di voler svuotare il carrello?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            utente.prodotti_carrello.clear()
            self.salva_dati_utente()
            self.aggiorna_dati()

    def procedi_acquisto(self):
        utente = getattr(self.gestore_utenti, 'utente_corrente', None)
        if not utente or not getattr(utente, 'prodotti_carrello', []):
            return

        metodi_salvati = getattr(utente, 'metodi_pagamento', getattr(utente, '_metodi_pagamento', []))

        if not metodi_salvati:
            QMessageBox.warning(
                self,
                "Metodo di Pagamento Mancante",
                "Impossibile procedere.\nNon hai registrato alcun metodo di pagamento.\nVai nell'area Profilo per aggiungerne uno."
            )
            return

        reply = QMessageBox.question(self, "Conferma Acquisto",
                                     f"Vuoi confermare l'ordine per un {self.lbl_totale.text()}?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            metodo_scelto = metodi_salvati[0]

            self.gestore_ordini.richiestaOrdine(utente, utente.prodotti_carrello, metodo_scelto)

            self.salva_dati_utente()

            QMessageBox.information(self, "Acquisto Completato", "Ordine completato con successo e mail inviata!")
            self.torna_indietro()

        except ValueError as e:
            QMessageBox.warning(self, "Errore durante l'acquisto", str(e))

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