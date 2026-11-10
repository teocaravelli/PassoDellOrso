from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem,
    QHeaderView, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt

from models.enums import StatoOrdine


class DettaglioOrdineDipendenteView(QWidget):
    def __init__(self, gestore_ordini, gestore_utenti, main_window=None):
        super().__init__()
        self.gestore_ordini = gestore_ordini
        self.gestore_utenti = gestore_utenti
        self.main_window = main_window
        self.ordine_corrente = None

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # -- INTESTAZIONE --
        self.header_layout = QHBoxLayout()
        self.lbl_titolo = QLabel("DETTAGLIO ORDINE")
        self.lbl_titolo.setObjectName("TitoloAzzurro")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_layout.addWidget(self.lbl_titolo)
        self.main_layout.addLayout(self.header_layout)

        # -- PANNELLO INFORMAZIONI GENERALI --
        self.info_frame = QFrame()
        self.info_frame.setObjectName("InfoFrame")
        self.info_layout = QVBoxLayout(self.info_frame)
        self.info_layout.setSpacing(10)

        self.lbl_cliente = QLabel("Cliente: ")
        self.lbl_data = QLabel("Data: ")
        self.lbl_stato = QLabel("Stato: ")
        self.lbl_totale = QLabel("Totale: ")

        for lbl in [self.lbl_cliente, self.lbl_data, self.lbl_stato, self.lbl_totale]:
            lbl.setStyleSheet("font-size: 15px; color: #333;")
            self.info_layout.addWidget(lbl)

        self.main_layout.addWidget(self.info_frame)

        # -- TABELLA PRODOTTI --
        self.lbl_prodotti = QLabel("Prodotti Acquistati:")
        self.lbl_prodotti.setStyleSheet("font-weight: bold; font-size: 16px; color: #1a365d;")
        self.main_layout.addWidget(self.lbl_prodotti)

        self.tabella_prodotti = QTableWidget()
        self.tabella_prodotti.setColumnCount(4)
        self.tabella_prodotti.setHorizontalHeaderLabels(["Prodotto", "Quantità", "Prezzo Cad.", "Subtotale"])

        header = self.tabella_prodotti.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)

        self.tabella_prodotti.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabella_prodotti.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.main_layout.addWidget(self.tabella_prodotti)

        # -- PANNELLO AZIONI RIMBORSO (Nascosto di default) --
        self.pannello_rimborso = QFrame()
        self.pannello_rimborso.setObjectName("PannelloRimborso")
        self.layout_rimborso = QHBoxLayout(self.pannello_rimborso)

        self.lbl_avviso_rimborso = QLabel("Il cliente ha richiesto un rimborso per questo ordine.")
        self.lbl_avviso_rimborso.setStyleSheet("font-weight: bold; color: #856404; font-size: 14px;")

        self.btn_rifiuta = QPushButton("Rifiuta Rimborso")
        self.btn_rifiuta.setObjectName("BtnRifiuta")
        self.btn_rifiuta.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_approva = QPushButton("Approva Rimborso")
        self.btn_approva.setObjectName("BtnApprova")
        self.btn_approva.setCursor(Qt.CursorShape.PointingHandCursor)

        self.layout_rimborso.addWidget(self.lbl_avviso_rimborso, stretch=1)
        self.layout_rimborso.addWidget(self.btn_rifiuta)
        self.layout_rimborso.addWidget(self.btn_approva)

        self.main_layout.addWidget(self.pannello_rimborso)
        self.pannello_rimborso.hide()  # Lo mostriamo solo se serve

        # -- BOTTONIERA AZIONI INFERIORE --
        self.bottom_layout = QHBoxLayout()

        self.btn_indietro = QPushButton("Torna alla Lista Ordini")
        self.btn_indietro.setObjectName("BtnIndietro")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_indietro.setFixedWidth(250)

        self.btn_completa = QPushButton("Completa Ordine")
        self.btn_completa.setObjectName("BtnCompleta")
        self.btn_completa.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_completa.setFixedWidth(250)

        self.bottom_layout.addWidget(self.btn_indietro, alignment=Qt.AlignmentFlag.AlignLeft)
        self.bottom_layout.addStretch()  # Spinge il pulsante "Completa Ordine" a destra
        self.bottom_layout.addWidget(self.btn_completa, alignment=Qt.AlignmentFlag.AlignRight)

        self.main_layout.addLayout(self.bottom_layout)
        self.btn_completa.hide()  # Lo mostriamo in base allo stato

    def applica_stili(self):
        self.setStyleSheet("""
            QWidget { background-color: white; font-family: Arial, sans-serif; }
            #TitoloAzzurro {
                background-color: #add8e6; color: #1a365d; font-weight: bold;
                font-size: 20px; padding: 15px; border-radius: 5px; border: 2px solid #1a365d;
            }
            #InfoFrame {
                border: 2px solid #e0e0e0; border-radius: 8px; background-color: #f9f9f9; padding: 10px;
            }
            #PannelloRimborso {
                background-color: #fff3cd; border: 2px solid #ffeeba; border-radius: 8px; padding: 5px;
            }
            QTableWidget {
                alternate-background-color: #f0f8ff; gridline-color: #add8e6;
                border: 2px solid #1a365d; border-radius: 5px; font-size: 14px;
            }
            QHeaderView::section {
                background-color: #1a365d; color: white; font-weight: bold;
                padding: 5px; border: 1px solid #1a365d;
            }
            QPushButton {
                background-color: #1a365d; color: white; font-weight: bold; padding: 10px; border-radius: 5px;
            }
            QPushButton:hover { background-color: #2a528a; }
            #BtnIndietro { background-color: #666; }
            #BtnIndietro:hover { background-color: #888; }
            #BtnApprova, #BtnCompleta { background-color: #28a745; }
            #BtnApprova:hover, #BtnCompleta:hover { background-color: #218838; }
            #BtnRifiuta { background-color: #dc3545; }
            #BtnRifiuta:hover { background-color: #c82333; }
        """)

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_indietro)
        self.btn_approva.clicked.connect(self.accetta_rimborso)
        self.btn_rifiuta.clicked.connect(self.rifiuta_rimborso)
        self.btn_completa.clicked.connect(self.completa_ordine)

    def imposta_ordine(self, ordine):
        self.ordine_corrente = ordine

        # 1. Intestazione e Dati Generali
        self.lbl_titolo.setText(f"DETTAGLIO ORDINE #{ordine.id_ordine}")

        data_str = getattr(ordine, '_data', None)
        if data_str:
            data_str = data_str.strftime('%d/%m/%Y %H:%M')
        self.lbl_data.setText(f"<b>Data:</b> {data_str}")

        self.lbl_totale.setText(f"<b>Totale Pagato:</b> € {ordine.prezzo_totale:.2f}")

        # Ricerca del cliente proprietario dell'ordine
        nome_cliente = "Cliente Sconosciuto"
        utenti = getattr(self.gestore_utenti, '_utenti', getattr(self.gestore_utenti, 'utenti', []))
        for u in utenti:
            ordini_cliente = getattr(u, 'ordini', getattr(u, '_ordini', []))
            if any(o.id_ordine == ordine.id_ordine for o in ordini_cliente):
                nome_cliente = f"{u.nome} {u.cognome} ({u.email})"
                break
        self.lbl_cliente.setText(f"<b>Cliente:</b> {nome_cliente}")

        # Gestione Stato e Colori
        stato_enum = ordine.stato
        stato_str = stato_enum.name.replace("_", " ") if hasattr(stato_enum, 'name') else str(stato_enum)

        colore_stato = "#333"
        if "COMPLETATO" in stato_str:
            colore_stato = "#5cb85c"
        elif "RICHIESTO" in stato_str:
            colore_stato = "#d9534f"

        self.lbl_stato.setText(f"<b>Stato Attuale:</b> <span style='color: {colore_stato};'>{stato_str}</span>")

        # 2. Popolamento Tabella Prodotti
        prodotti = ordine.prodotti
        self.tabella_prodotti.setRowCount(len(prodotti))
        self.tabella_prodotti.setAlternatingRowColors(True)

        for riga, item in enumerate(prodotti):
            prodotto = item.prodotto

            nome_item = QTableWidgetItem(prodotto.nome)
            self.tabella_prodotti.setItem(riga, 0, nome_item)

            qta_item = QTableWidgetItem(str(item.quantita))
            qta_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella_prodotti.setItem(riga, 1, qta_item)

            prezzo_item = QTableWidgetItem(f"€ {prodotto.prezzo:.2f}")
            prezzo_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella_prodotti.setItem(riga, 2, prezzo_item)

            subtotale = prodotto.prezzo * item.quantita
            sub_item = QTableWidgetItem(f"€ {subtotale:.2f}")
            sub_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella_prodotti.setItem(riga, 3, sub_item)

        # 3. Logica visualizzazione azioni rimborso
        stato_check = stato_str.upper()
        if "RICHIESTO" in stato_check or "ATTESA" in stato_check:
            self.pannello_rimborso.show()
        else:
            self.pannello_rimborso.hide()

        # 4. Logica visualizzazione bottone Completa Ordine
        # Lo mostriamo se l'ordine non è ancora completato, non è annullato e non è in fase di rimborso
        if "COMPLETATO" not in stato_check and "RIMBORSO" not in stato_check and "ANNULLATO" not in stato_check:
            self.btn_completa.show()
        else:
            self.btn_completa.hide()

    def completa_ordine(self):
        risposta = QMessageBox.question(
            self, "Completa Ordine",
            f"Sei sicuro di voler completare l'ordine #{self.ordine_corrente.id_ordine}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if risposta == QMessageBox.StandardButton.Yes:

            # 1. Aggiorna lo stato nel gestore ordini e salva
            self.ordine_corrente.stato = StatoOrdine.COMPLETATO
            if hasattr(self.gestore_ordini, 'salva_dati'):
                self.gestore_ordini.salva_dati()
            elif hasattr(self.gestore_ordini, '_salva_dati'):
                self.gestore_ordini._salva_dati()

            # 2. Sincronizza lo stato dell'ordine anche per il cliente e salva gli utenti
            utenti = getattr(self.gestore_utenti, '_utenti', getattr(self.gestore_utenti, 'utenti', []))
            for u in utenti:
                ordini_cliente = getattr(u, 'ordini', getattr(u, '_ordini', []))
                for o in ordini_cliente:
                    if o.id_ordine == self.ordine_corrente.id_ordine:
                        o.stato = StatoOrdine.COMPLETATO
                        if hasattr(self.gestore_utenti, 'salva_dati'):
                            self.gestore_utenti.salva_dati()
                        elif hasattr(self.gestore_utenti, '_salva_dati'):
                            self.gestore_utenti._salva_dati()
                        break

            QMessageBox.information(self, "Successo", "Ordine completato con successo!")
            # Ricarica l'interfaccia per mostrare il nuovo stato e nascondere il pulsante
            self.imposta_ordine(self.ordine_corrente)

    def accetta_rimborso(self):
        risposta = QMessageBox.question(
            self, "Conferma Rimborso",
            f"Sei sicuro di voler APPROVARE il rimborso per l'ordine #{self.ordine_corrente.id_ordine}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if risposta == QMessageBox.StandardButton.Yes:
            self.gestore_ordini.gestisciRimborso(self.ordine_corrente.id_ordine, approvato=True)

            # Sincronizzazione cliente
            utenti = getattr(self.gestore_utenti, '_utenti', getattr(self.gestore_utenti, 'utenti', []))
            for u in utenti:
                ordini_cliente = getattr(u, 'ordini', getattr(u, '_ordini', []))
                for o in ordini_cliente:
                    if o.id_ordine == self.ordine_corrente.id_ordine:
                        o.stato = StatoOrdine.RIMBORSO_COMPLETATO
                        if hasattr(self.gestore_utenti, 'salva_dati'):
                            self.gestore_utenti.salva_dati()
                        elif hasattr(self.gestore_utenti, '_salva_dati'):
                            self.gestore_utenti._salva_dati()

            QMessageBox.information(self, "Successo", "Rimborso approvato e scorte ripristinate.")
            self.imposta_ordine(self.ordine_corrente)

    def rifiuta_rimborso(self):
        risposta = QMessageBox.question(
            self, "Rifiuta Rimborso",
            f"Sei sicuro di voler RIFIUTARE il rimborso per l'ordine #{self.ordine_corrente.id_ordine}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if risposta == QMessageBox.StandardButton.Yes:
            self.gestore_ordini.gestisciRimborso(self.ordine_corrente.id_ordine, approvato=False)

            # Sincronizzazione cliente
            utenti = getattr(self.gestore_utenti, '_utenti', getattr(self.gestore_utenti, 'utenti', []))
            for u in utenti:
                ordini_cliente = getattr(u, 'ordini', getattr(u, '_ordini', []))
                for o in ordini_cliente:
                    if o.id_ordine == self.ordine_corrente.id_ordine:
                        o.stato = StatoOrdine.COMPLETATO
                        if hasattr(self.gestore_utenti, 'salva_dati'):
                            self.gestore_utenti.salva_dati()
                        elif hasattr(self.gestore_utenti, '_salva_dati'):
                            self.gestore_utenti._salva_dati()

            QMessageBox.information(self, "Rimborso Rifiutato", "La richiesta di rimborso è stata respinta.")
            self.imposta_ordine(self.ordine_corrente)

    def torna_indietro(self):
        if self.main_window and hasattr(self.main_window, 'mostra_gestione_ordini'):
            self.main_window.mostra_gestione_ordini()