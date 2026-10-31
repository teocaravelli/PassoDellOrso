from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QHeaderView, QFrame, QMessageBox, QDialog,
                             QLineEdit, QFormLayout, QSpinBox, QDoubleSpinBox, QCheckBox)
from PyQt6.QtCore import Qt

class ModificaProdottoDialog(QDialog):
    """Un popup che si adatta dinamicamente agli attributi del prodotto."""

    def __init__(self, prodotto, parent=None):
        super().__init__(parent)
        self.prodotto = prodotto
        self.setWindowTitle(f"Modifica: {prodotto.nome}")
        self.setMinimumWidth(300)
        self.setStyleSheet("background-color: white; color: black;")

        layout = QVBoxLayout(self)
        form_layout = QFormLayout()

        # CAMPO NOME
        self.input_nome = QLineEdit(prodotto.nome)
        self.input_nome.setStyleSheet("background-color: #add8e6; border: 1px solid #1a365d; padding: 5px;")
        form_layout.addRow("Nome:", self.input_nome)

        # CAMPO PREZZO
        self.input_prezzo = QDoubleSpinBox()
        self.input_prezzo.setMaximum(10000.0)
        self.input_prezzo.setDecimals(2)
        # Supponiamo che l'attributo sia 'prezzo' (adattalo se si chiama diversamente)
        prezzo_attuale = getattr(prodotto, 'prezzo', 0.0)
        self.input_prezzo.setValue(float(prezzo_attuale))
        self.input_prezzo.setStyleSheet("background-color: #add8e6; border: 1px solid #1a365d; padding: 5px;")
        form_layout.addRow("Prezzo (€):", self.input_prezzo)

        # CAMPO QUANTITÀ (Dinamico: solo se il prodotto ha questo attributo)
        self.input_quantita = None
        if hasattr(prodotto, 'quantita'):
            self.input_quantita = QSpinBox()
            self.input_quantita.setMaximum(9999)
            self.input_quantita.setValue(int(prodotto.quantita))
            self.input_quantita.setStyleSheet("background-color: #add8e6; border: 1px solid #1a365d; padding: 5px;")
            form_layout.addRow("Quantità:", self.input_quantita)

        # CAMPO DISPONIBILITÀ (Es. Checkbox)
        self.check_disponibile = QCheckBox("Prodotto Disponibile")
        # Supponiamo l'attributo si chiami 'disponibile' (booleano)
        disp_attuale = getattr(prodotto, 'disponibile', True)
        self.check_disponibile.setChecked(disp_attuale)
        form_layout.addRow("", self.check_disponibile)

        layout.addLayout(form_layout)

        # BOTTONI SALVA/ANNULLA
        btn_layout = QHBoxLayout()
        btn_salva = QPushButton("Salva Modifiche")
        btn_salva.setStyleSheet("background-color: #1a365d; color: white; padding: 8px; font-weight: bold;")
        btn_salva.clicked.connect(self.accept)  # Chiude il dialog con successo

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setStyleSheet("background-color: #666; color: white; padding: 8px; font-weight: bold;")
        btn_annulla.clicked.connect(self.reject)  # Chiude il dialog annullando

        btn_layout.addWidget(btn_annulla)
        btn_layout.addWidget(btn_salva)
        layout.addLayout(btn_layout)

    def get_dati_aggiornati(self):
        """Restituisce un dizionario con i nuovi dati inseriti."""
        dati = {
            'nome': self.input_nome.text().strip(),
            'prezzo': self.input_prezzo.value(),
            'disponibile': self.check_disponibile.isChecked()
        }
        if self.input_quantita is not None:
            dati['quantita'] = self.input_quantita.value()
        return dati

class GestioneInventarioView(QWidget):
    def __init__(self, gestore_prodotti, main_window=None):
        super().__init__()
        self.gestore_prodotti = gestore_prodotti
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(30, 30, 30, 30)
        self.main_layout.setSpacing(20)

        # -- INTESTAZIONE E TASTO AGGIUNGI --
        self.header_layout = QHBoxLayout()
        self.lbl_titolo = QLabel("INVENTARIO PRODOTTI")
        self.lbl_titolo.setObjectName("TitoloAzzurro")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.btn_aggiungi = QPushButton("+ Nuovo Prodotto")
        self.btn_aggiungi.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_aggiungi.setObjectName("BtnAggiungi")

        self.header_layout.addWidget(self.lbl_titolo, stretch=1)
        self.header_layout.addWidget(self.btn_aggiungi)

        self.main_layout.addLayout(self.header_layout)

        # -- TABELLA --
        self.tabella = QTableWidget()
        self.tabella.setColumnCount(5)
        self.tabella.setHorizontalHeaderLabels(["ID", "Nome e Tipo", "Prezzo", "Dettagli Extra", "Azioni"])

        header = self.tabella.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tabella.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.tabella.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabella.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

        self.main_layout.addWidget(self.tabella)

        # -- BOTTONE INDIETRO --
        self.btn_indietro = QPushButton("Torna alla Dashboard")
        self.btn_indietro.setObjectName("BtnIndietro")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_indietro.setFixedWidth(200)
        self.main_layout.addWidget(self.btn_indietro, alignment=Qt.AlignmentFlag.AlignLeft)

    def applica_stili(self):
        self.setStyleSheet("""
            QWidget { background-color: white; font-family: Arial, sans-serif; }
            #TitoloAzzurro {
                background-color: #add8e6; color: #1a365d; font-weight: bold;
                font-size: 20px; padding: 15px; border-radius: 5px; border: 2px solid #1a365d;
            }
            #BtnAggiungi {
                background-color: #28a745; color: white; font-weight: bold;
                font-size: 16px; padding: 15px 20px; border-radius: 5px;
            }
            #BtnAggiungi:hover { background-color: #218838; }

            QTableWidget {
                alternate-background-color: #f0f8ff; gridline-color: #add8e6;
                border: 2px solid #1a365d; border-radius: 5px; font-size: 14px;
            }
            QHeaderView::section {
                background-color: #1a365d; color: white; font-weight: bold;
                padding: 5px; border: 1px solid #1a365d; font-size: 14px;
            }

            QPushButton { background-color: #1a365d; color: white; font-weight: bold; padding: 10px; border-radius: 5px; }
            QPushButton:hover { background-color: #2a528a; }
            #BtnIndietro { background-color: #666; }
            #BtnIndietro:hover { background-color: #888; }

            /* Bottoni dentro la tabella */
            .BtnTabella { padding: 5px; margin: 2px; font-weight: bold; border-radius: 3px; }
            .BtnModifica { background-color: #ffc107; color: #333; }
            .BtnModifica:hover { background-color: #e0a800; }
            .BtnElimina { background-color: #dc3545; color: white; }
            .BtnElimina:hover { background-color: #c82333; }
        """)

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_alla_dashboard)
        self.btn_aggiungi.clicked.connect(self.vai_a_nuovo_prodotto)

    def aggiorna_vista(self):
        self.tabella.setRowCount(0)

        # Usiamo il metodo corretto del tuo GestoreProdotti
        prodotti = self.gestore_prodotti.get_tutti_prodotti()

        self.tabella.setRowCount(len(prodotti))
        self.tabella.setAlternatingRowColors(True)

        for riga, prodotto in enumerate(prodotti):
            id_item = QTableWidgetItem(f"#{prodotto.id}")
            id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella.setItem(riga, 0, id_item)

            # Estrae dinamicamente "Attrezzatura", "SkiPass", ecc.
            tipo_classe = prodotto.__class__.__name__
            nome_item = QTableWidgetItem(f"{prodotto.nome}\n[{tipo_classe}]")
            nome_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella.setItem(riga, 1, nome_item)

            prezzo_item = QTableWidgetItem(f"€ {prodotto.prezzo:.2f}")
            prezzo_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella.setItem(riga, 2, prezzo_item)

            # Verifica della disponibilità (usando is_disponibile) e quantità
            dettagli_testo = "🟢 Disp." if prodotto.is_disponibile else "🔴 Esaurito"

            if hasattr(prodotto, 'quantita'):
                dettagli_testo += f"\nQuantità: {prodotto.quantita}"
            else:
                dettagli_testo += "\nQtà: N/A"

            dettagli_item = QTableWidgetItem(dettagli_testo)
            dettagli_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tabella.setItem(riga, 3, dettagli_item)

            pannello_azioni = QWidget()
            layout_azioni = QHBoxLayout(pannello_azioni)
            layout_azioni.setContentsMargins(0, 0, 0, 0)

            btn_modifica = QPushButton("Modifica")
            btn_modifica.setProperty("class", "BtnTabella BtnModifica")
            btn_modifica.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_modifica.clicked.connect(lambda checked, p=prodotto: self.apri_modifica_prodotto(p))

            btn_elimina = QPushButton("Elimina")
            btn_elimina.setProperty("class", "BtnTabella BtnElimina")
            btn_elimina.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_elimina.clicked.connect(lambda checked, p_id=prodotto.id: self.elimina_prodotto(p_id))

            layout_azioni.addWidget(btn_modifica)
            layout_azioni.addWidget(btn_elimina)
            self.tabella.setCellWidget(riga, 4, pannello_azioni)

    def apri_modifica_prodotto(self, prodotto):
        dialog = ModificaProdottoDialog(prodotto, self)

        # Adattiamo il dialog al nome corretto dell'attributo
        dialog.check_disponibile.setChecked(prodotto.is_disponibile)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            dati_nuovi = dialog.get_dati_aggiornati()

            prodotto.nome = dati_nuovi['nome']
            prodotto.prezzo = dati_nuovi['prezzo']
            prodotto.is_disponibile = dati_nuovi['disponibile']

            if 'quantita' in dati_nuovi and hasattr(prodotto, 'quantita'):
                prodotto.quantita = dati_nuovi['quantita']

            self.gestore_prodotti._salva_dati()
            QMessageBox.information(self, "Successo", "Prodotto aggiornato correttamente.")
            self.aggiorna_vista()

    def elimina_prodotto(self, id_prodotto):
        risposta = QMessageBox.question(
            self, "Conferma Eliminazione",
            f"Sei sicuro di voler eliminare il prodotto #{id_prodotto}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if risposta == QMessageBox.StandardButton.Yes:
            if self.gestore_prodotti.eliminaProdotto(id_prodotto):
                QMessageBox.information(self, "Eliminato", "Prodotto rimosso dal catalogo.")
                self.aggiorna_vista()
            else:
                QMessageBox.warning(self, "Errore", "Impossibile eliminare il prodotto.")

    def vai_a_nuovo_prodotto(self):
        if self.main_window:
            self.main_window.mostra_aggiungi_prodotto()

    def torna_alla_dashboard(self):
        if self.main_window:
            self.main_window.mostra_area_dipendente()