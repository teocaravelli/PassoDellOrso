from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFrame, QMessageBox)
from PyQt6.QtCore import Qt


class OrdiniDipendenteView(QWidget):
    def __init__(self, gestore_ordini, gestore_utenti, main_window=None):
        super().__init__()
        self.gestore_ordini = gestore_ordini
        self.gestore_utenti = gestore_utenti
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        self.header_layout = QHBoxLayout()
        self.lbl_titolo = QLabel("GESTIONE ORDINI CLIENTI")
        self.lbl_titolo.setObjectName("TitoloAzzurro")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_layout.addWidget(self.lbl_titolo)
        self.main_layout.addLayout(self.header_layout)

        self.tabella_ordini = QTableWidget()
        self.tabella_ordini.setColumnCount(6)
        self.tabella_ordini.setHorizontalHeaderLabels(["ID Ordine", "Cliente", "Data", "Totale", "Stato", "Azioni"])

        header = self.tabella_ordini.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabella_ordini.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabella_ordini.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        self.tabella_ordini.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.main_layout.addWidget(self.tabella_ordini)

        # -- BOTTONI INFERIORI --
        self.footer_layout = QHBoxLayout()
        self.btn_indietro = QPushButton("Torna alla Dashboard")
        self.btn_indietro.setObjectName("BtnIndietro")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_indietro.setFixedWidth(200)
        self.footer_layout.addWidget(self.btn_indietro, alignment=Qt.AlignmentFlag.AlignLeft)

        self.main_layout.addLayout(self.footer_layout)

    def applica_stili(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Arial, sans-serif;
            }
            #TitoloAzzurro {
                background-color: #add8e6;
                color: #1a365d;
                font-weight: bold;
                font-size: 20px;
                padding: 15px;
                border-radius: 5px;
                border: 2px solid #1a365d;
            }
            QTableWidget {
                background-color: white;
                alternate-background-color: #f0f8ff;
                gridline-color: #add8e6;
                border: 2px solid #1a365d;
                border-radius: 5px;
                font-size: 14px;
            }
            QHeaderView::section {
                background-color: #1a365d;
                color: white;
                font-weight: bold;
                padding: 5px;
                border: 1px solid #1a365d;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1a365d;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2a528a;
            }
            #BtnIndietro { background-color: #666; }
            #BtnIndietro:hover { background-color: #888; }

            .GestisciBtn {
                background-color: #add8e6;
                color: #1a365d;
                border: 1px solid #1a365d;
                font-weight: bold;
                padding: 5px;
                border-radius: 3px;
                margin: 2px;
            }
            .GestisciBtn:hover { background-color: #87ceeb; }
        """)

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_alla_dashboard)

    # ==========================================
    # LOGICA DI AGGIORNAMENTO
    # ==========================================

    def aggiorna_vista(self):
        self.tabella_ordini.setRowCount(0)
        ordini = self.gestore_ordini._ordini

        self.tabella_ordini.setRowCount(len(ordini))
        self.tabella_ordini.setAlternatingRowColors(True)

        for riga, ordine in enumerate(ordini):
            # 0. ID
            id_item = QTableWidgetItem(f"#{ordine.id_ordine}")
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella_ordini.setItem(riga, 0, id_item)

            # 1. CLIENTE (Reverse Lookup)
            dati_cliente = "Cliente Sconosciuto"
            for utente in self.gestore_utenti._utenti:
                if hasattr(utente, 'ordini'):  # Controlla se è un Cliente
                    # Verifica se questo specifico ordine è nella sua lista
                    if any(o.id_ordine == ordine.id_ordine for o in utente.ordini):
                        dati_cliente = f"{utente.nome} {utente.cognome}\n({utente.email})"
                        break  # Trovato, usciamo dal ciclo

            cliente_item = QTableWidgetItem(dati_cliente)
            cliente_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella_ordini.setItem(riga, 1, cliente_item)

            # 2. Data
            data_str = "N/A"
            if hasattr(ordine, '_data'):
                data_str = ordine._data.strftime('%d/%m/%Y\n%H:%M')
            data_item = QTableWidgetItem(data_str)
            data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella_ordini.setItem(riga, 2, data_item)

            # 3. Totale
            totale_item = QTableWidgetItem(f"€ {ordine.prezzo_totale:.2f}")
            totale_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella_ordini.setItem(riga, 3, totale_item)

            # 4. Stato
            stato_item = QTableWidgetItem(ordine.stato.name.replace("_", " "))
            stato_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella_ordini.setItem(riga, 4, stato_item)

            # 5. Pulsante Azione
            btn_azione = QPushButton("Dettagli / Gestisci")
            btn_azione.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_azione.setProperty("class", "GestisciBtn")
            btn_azione.clicked.connect(lambda checked, id_o=ordine.id_ordine: self.apri_dettaglio_ordine(id_o))
            self.tabella_ordini.setCellWidget(riga, 5, btn_azione)

    # ==========================================
    # LOGICA DI NAVIGAZIONE E AZIONI
    # ==========================================

    def torna_alla_dashboard(self):
        if self.main_window:
            self.main_window.mostra_area_dipendente()

    def apri_dettaglio_ordine(self, id_ordine):
        QMessageBox.information(self, "Gestione Ordine",
                                f"Apertura dettagli per l'Ordine #{id_ordine}.")