from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QMessageBox, QComboBox
)
from PyQt6.QtCore import Qt


class ModificaOrdineView(QWidget):
    def __init__(self, gestore_utenti, gestore_ordini, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.gestore_ordini = gestore_ordini
        self.main_window = main_window
        self.ordine_corrente = None

        self.prodotti_modificati = []

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)

        self.lbl_titolo = QLabel("MODIFICA ORDINE")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setObjectName("Titolo")
        self.main_layout.addWidget(self.lbl_titolo)

        self.lbl_stato = QLabel("Stato: -")
        self.lbl_stato.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_stato.setObjectName("Sottotitolo")
        self.main_layout.addWidget(self.lbl_stato)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("ScrollArea")

        self.scroll_content = QWidget()
        self.layout_prodotti = QVBoxLayout(self.scroll_content)
        self.layout_prodotti.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_prodotti.setSpacing(10)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        self.lbl_nuovo_totale = QLabel("Nuovo Totale: € 0.00")
        self.lbl_nuovo_totale.setObjectName("Totale")
        self.lbl_nuovo_totale.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.main_layout.addWidget(self.lbl_nuovo_totale)

        self.frame_rimborso = QFrame()
        self.frame_rimborso.setObjectName("FrameRimborso")
        self.frame_rimborso.setVisible(False)
        self.layout_rimborso = QHBoxLayout(self.frame_rimborso)

        self.layout_rimborso.addWidget(QLabel("<b>Motivazione:</b>"))

        self.combo_motivazioni = QComboBox()
        self.combo_motivazioni.addItems([
            "Seleziona un motivo...",
            "Motivi di salute / Infortunio",
            "Maltempo / Impianti chiusi",
            "Cambio di programma",
            "Errore nell'acquisto",
            "Altro"
        ])
        self.layout_rimborso.addWidget(self.combo_motivazioni, stretch=1)

        self.btn_conferma_rimborso = QPushButton("Conferma Richiesta")
        self.btn_conferma_rimborso.setObjectName("BtnConfermaRimborso")
        self.btn_conferma_rimborso.setCursor(Qt.CursorShape.PointingHandCursor)
        self.layout_rimborso.addWidget(self.btn_conferma_rimborso)

        self.main_layout.addWidget(self.frame_rimborso)

        self.layout_pulsanti = QHBoxLayout()
        self.layout_pulsanti.setSpacing(15)

        self.btn_salva = QPushButton("Salva Modifiche")
        self.btn_salva.setObjectName("BtnSalva")

        self.btn_annulla_ordine = QPushButton("Annulla Intero Ordine")
        self.btn_annulla_ordine.setObjectName("BtnAnnullaOrdine")

        self.btn_richiedi_rimborso = QPushButton("Richiedi Rimborso")
        self.btn_richiedi_rimborso.setObjectName("BtnRimborso")

        self.btn_indietro = QPushButton("Torna Indietro")
        self.btn_indietro.setObjectName("BtnIndietro")

        for btn in [self.btn_salva, self.btn_annulla_ordine, self.btn_richiedi_rimborso, self.btn_indietro]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setMinimumHeight(40)
            self.layout_pulsanti.addWidget(btn)

        self.main_layout.addLayout(self.layout_pulsanti)

    def applica_stili(self):
        self.setStyleSheet("""
            ModificaOrdineView { background-color: white; font-family: Arial, sans-serif; }
            #Titolo { font-size: 26px; font-weight: bold; color: #1a365d; }
            #Sottotitolo { font-size: 16px; font-weight: bold; color: #555; margin-bottom: 10px; }
            #ScrollArea { border: 1px solid #ccc; border-radius: 8px; background-color: #f8f9fa; }
            #Totale { font-size: 20px; font-weight: bold; color: #1a365d; }
            #FrameRimborso { border: 2px dashed #d9534f; border-radius: 8px; background-color: #fdf5f5; padding: 10px; }

            .RigaProdotto { background-color: white; border: 1px solid #e0e0e0; border-radius: 6px; padding: 10px; }
            .NomeProdotto { font-size: 15px; font-weight: bold; color: #333; }

            QComboBox { padding: 5px; font-size: 14px; border: 1px solid #ccc; border-radius: 4px; }

            /* Regola generica base per i pulsanti */
            QPushButton { 
                background-color: #007bff; /* Sfondo default blu per evitare pulsanti bianchi su bianco */
                color: white; 
                font-weight: bold; 
                font-size: 14px; 
                border-radius: 6px; 
                padding: 8px; 
            }

            /* --- FIX PER I POPUP (QMessageBox) --- */
            QMessageBox { 
                background-color: white; 
            }
            QMessageBox QLabel { 
                color: black; 
                font-size: 14px; 
            }
            QMessageBox QPushButton {
                background-color: #e0e0e0;
                color: black;
                min-width: 80px;
                border: 1px solid #ccc;
            }
            QMessageBox QPushButton:hover {
                background-color: #d0d0d0;
            }
            /* ------------------------------------- */

            /* Stile per il pulsantino rimuovi vicino al prodotto */
            QPushButton#BtnRimuoviProdotto { background-color: #d9534f; padding: 5px 15px; font-size: 12px; }
            QPushButton#BtnRimuoviProdotto:hover { background-color: #c9302c; }

            QPushButton#BtnSalva { background-color: #5cb85c; }
            QPushButton#BtnSalva:hover { background-color: #4cae4c; }

            QPushButton#BtnAnnullaOrdine { background-color: #f0ad4e; }
            QPushButton#BtnAnnullaOrdine:hover { background-color: #eea236; }

            QPushButton#BtnRimborso, QPushButton#BtnConfermaRimborso { background-color: #d9534f; }
            QPushButton#BtnRimborso:hover, QPushButton#BtnConfermaRimborso:hover { background-color: #c9302c; }

            QPushButton#BtnIndietro { background-color: #6c757d; }
            QPushButton#BtnIndietro:hover { background-color: #5a6268; }
        """)

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_indietro)
        self.btn_salva.clicked.connect(self.salva_modifiche)
        self.btn_annulla_ordine.clicked.connect(self.annulla_ordine)
        self.btn_richiedi_rimborso.clicked.connect(self.mostra_sezione_rimborso)
        self.btn_conferma_rimborso.clicked.connect(self.invia_richiesta_rimborso)

    def imposta_ordine(self, ordine):
        """Carica l'ordine selezionato nella vista."""
        self.ordine_corrente = ordine
        self.prodotti_modificati.clear()
        self.frame_rimborso.setVisible(False)
        self.combo_motivazioni.setCurrentIndex(0)

        id_ord = getattr(ordine, 'id_ordine', '---')
        stato = getattr(ordine, 'stato', 'SCONOSCIUTO')

        self.lbl_titolo.setText(f"MODIFICA ORDINE #{id_ord}")
        self.lbl_stato.setText(f"Stato attuale: {stato}")

        # Pulisce la lista visiva
        while self.layout_prodotti.count():
            child = self.layout_prodotti.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        prodotti = getattr(ordine, 'prodotti', [])

        for index, item in enumerate(prodotti):
            nome = getattr(item, 'nome', 'Prodotto')
            prezzo = getattr(item, 'prezzo', 0.0)
            qta = getattr(item, 'quantita', 1)

            frame = QFrame()
            frame.setProperty("class", "RigaProdotto")
            lay = QHBoxLayout(frame)

            lbl_info = QLabel(
                f"<span class='NomeProdotto'>{nome}</span><br>Quantità: {qta} | Prezzo unitario: € {prezzo:.2f}")
            lbl_info.setTextFormat(Qt.TextFormat.RichText)

            btn_rimuovi = QPushButton("Rimuovi")
            btn_rimuovi.setObjectName("BtnRimuoviProdotto")
            btn_rimuovi.setCursor(Qt.CursorShape.PointingHandCursor)

            dati_prodotto = {
                'prodotto_obj': item,
                'frame': frame,
                'prezzo': prezzo,
                'quantita': qta,
                'rimosso': False
            }
            self.prodotti_modificati.append(dati_prodotto)

            btn_rimuovi.clicked.connect(lambda checked, pd=dati_prodotto: self.rimuovi_singolo_prodotto(pd))

            lay.addWidget(lbl_info, stretch=1)
            lay.addWidget(btn_rimuovi)

            self.layout_prodotti.addWidget(frame)

        self.ricalcola_totale()

    def rimuovi_singolo_prodotto(self, dati_prodotto):
        dati_prodotto['rimosso'] = True
        dati_prodotto['frame'].setVisible(False)  # Nascondiamo la riga
        self.ricalcola_totale()

    def ricalcola_totale(self):
        nuovo_totale = 0.0
        for p in self.prodotti_modificati:
            if not p['rimosso']:
                nuovo_totale += p['quantita'] * p['prezzo']
        self.lbl_nuovo_totale.setText(f"Nuovo Totale: € {nuovo_totale:.2f}")

    def salva_modifiche(self):
        if not self.ordine_corrente:
            return

        nuova_lista_prodotti = []
        nuovo_totale = 0.0

        for p in self.prodotti_modificati:
            if not p['rimosso']:
                nuova_lista_prodotti.append(p['prodotto_obj'])
                nuovo_totale += p['quantita'] * p['prezzo']

        if not nuova_lista_prodotti:
            return self.annulla_ordine()

        self.ordine_corrente.prodotti = nuova_lista_prodotti
        self.ordine_corrente.totale = nuovo_totale

        self.salva_e_torna("L'ordine è stato aggiornato. I prodotti selezionati sono stati rimossi.")

    def annulla_ordine(self):
        reply = QMessageBox.question(self, "Conferma Annullamento",
                                     "Sei sicuro di voler annullare l'intero ordine?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.ordine_corrente.stato = "ANNULLATO"
            self.salva_e_torna("L'ordine è stato annullato con successo.")

    def mostra_sezione_rimborso(self):
        self.frame_rimborso.setVisible(True)

    def invia_richiesta_rimborso(self):
        if self.combo_motivazioni.currentIndex() == 0:
            QMessageBox.warning(self, "Attenzione", "Seleziona una motivazione valida per il rimborso.")
            return

        motivo = self.combo_motivazioni.currentText()
        self.ordine_corrente.stato = "IN ATTESA DI RIMBORSO"

        if not hasattr(self.ordine_corrente, 'note'):
            self.ordine_corrente.note = ""
        self.ordine_corrente.note += f" [Richiesta rimborso: {motivo}]"

        self.salva_e_torna(f"Richiesta di rimborso inviata correttamente.\nMotivazione: {motivo}")

    def salva_e_torna(self, messaggio):
        if hasattr(self.gestore_utenti, '_salva_dati'):
            self.gestore_utenti._salva_dati()
        elif hasattr(self.gestore_utenti, 'salva_dati'):
            self.gestore_utenti.salva_dati()

        QMessageBox.information(self, "Successo", messaggio)
        self.torna_indietro()

    def torna_indietro(self):
        if self.main_window and hasattr(self.main_window, 'mostra_miei_ordini'):
            self.main_window.mostra_miei_ordini()