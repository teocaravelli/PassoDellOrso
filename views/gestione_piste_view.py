from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QComboBox, QMessageBox)
from PyQt6.QtCore import Qt

from models.enums import StatoApertura


class GestionePisteView(QWidget):
    def __init__(self, gestore_piste, main_window=None):
        super().__init__()
        self.gestore_piste = gestore_piste
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # -- INTESTAZIONE --
        self.header_layout = QHBoxLayout()
        self.lbl_titolo = QLabel("GESTIONE STATO PISTE")
        self.lbl_titolo.setObjectName("TitoloAzzurro")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_layout.addWidget(self.lbl_titolo)
        self.main_layout.addLayout(self.header_layout)

        # -- TABELLA PISTE --
        self.tabella_piste = QTableWidget()
        self.tabella_piste.setColumnCount(4)
        self.tabella_piste.setHorizontalHeaderLabels(["ID", "Nome Pista", "Difficoltà", "Modifica Stato"])

        header = self.tabella_piste.horizontalHeader()
        # Le prime 3 colonne si adattano al contenuto, l'ultima prende tutto lo spazio rimanente
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)

        self.tabella_piste.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabella_piste.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabella_piste.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.main_layout.addWidget(self.tabella_piste)

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
            QPushButton:hover { background-color: #2a528a; }
            #BtnIndietro { background-color: #666; }
            #BtnIndietro:hover { background-color: #888; }

            .AggiornaBtn {
                background-color: #add8e6;
                color: #1a365d;
                border: 1px solid #1a365d;
                font-weight: bold;
                padding: 4px 10px;
                border-radius: 3px;
            }
            .AggiornaBtn:hover { background-color: #87ceeb; }

            QComboBox {
                border: 1px solid #1a365d;
                border-radius: 3px;
                padding: 2px 5px;
                background-color: white;
                color: #333;
            }
        """)

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_alla_dashboard)

    # ==========================================
    # LOGICA DI POPOLAMENTO
    # ==========================================

    def aggiorna_vista(self):
        self.tabella_piste.setRowCount(0)
        piste = self.gestore_piste.visualizzaPiste()

        self.tabella_piste.setRowCount(len(piste))
        self.tabella_piste.setAlternatingRowColors(True)

        for riga, pista in enumerate(piste):
            # 0. ID
            id_item = QTableWidgetItem(f"#{pista.id_pista}")
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella_piste.setItem(riga, 0, id_item)

            # 1. Nome Pista
            nome_item = QTableWidgetItem(pista.nome)
            nome_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella_piste.setItem(riga, 1, nome_item)

            # 2. Difficoltà
            diff_item = QTableWidgetItem(pista.difficolta.name.replace("_", " "))
            diff_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella_piste.setItem(riga, 2, diff_item)

            # 3. Widget Azione (Combobox + Bottone)
            pannello_azione = QWidget()
            layout_azione = QHBoxLayout(pannello_azione)
            layout_azione.setContentsMargins(5, 2, 5, 2)

            combo_stato = QComboBox()
            # Popoliamo la tendina con tutti i valori dell'enum
            for stato in StatoApertura:
                combo_stato.addItem(stato.name.replace("_", " "), stato)

            # Impostiamo il valore visibile attuale uguale a quello del model
            combo_stato.setCurrentText(pista.stato_apertura.name.replace("_", " "))

            btn_aggiorna = QPushButton("Salva")
            btn_aggiorna.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_aggiorna.setProperty("class", "AggiornaBtn")

            # Lambda trick per passare ID pista e il riferimento alla Combobox
            btn_aggiorna.clicked.connect(
                lambda checked, p_id=pista.id_pista, cb=combo_stato: self.salva_nuovo_stato(p_id, cb)
            )

            layout_azione.addWidget(combo_stato)
            layout_azione.addWidget(btn_aggiorna)

            self.tabella_piste.setCellWidget(riga, 3, pannello_azione)

    # ==========================================
    # AZIONI
    # ==========================================

    def salva_nuovo_stato(self, id_pista, combo_box):
        """Metodo per salvare il nuovo stato richiamando il GestorePiste."""
        # Estraiamo l'oggetto Enum salvato come "userData" dentro la combobox
        nuovo_stato_enum = combo_box.currentData()

        esito = self.gestore_piste.modificaStatoPista(id_pista, nuovo_stato_enum)

        if esito:
            QMessageBox.information(self, "Successo", "Stato della pista aggiornato correttamente!")
            self.aggiorna_vista()  # Ricarica per visualizzare le modifiche a schermo
        else:
            QMessageBox.critical(self, "Errore", "Impossibile aggiornare lo stato della pista.")

    def torna_alla_dashboard(self):
        if self.main_window:
            self.main_window.mostra_area_dipendente()