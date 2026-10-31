from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFrame, QMessageBox,
                             QComboBox, QDoubleSpinBox, QSpinBox, QCheckBox, QFormLayout)
from PyQt6.QtCore import Qt

from datetime import date, datetime


from models.assicurazione import Assicurazione
from models.attrezzatura import Attrezzatura
from models.lezione import Lezione
from models.skipass import SkiPass
from models.enums import Livello, TipologiaAttrezzatura, FormulaTemporale

class NuovoProdottoView(QWidget):
    def __init__(self, gestore_prodotti, main_window=None):
        super().__init__()
        self.gestore_prodotti = gestore_prodotti
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # -- CONTENITORE PRINCIPALE --
        self.form_box = QFrame()
        self.form_box.setObjectName("FormBox")
        self.box_layout = QVBoxLayout(self.form_box)
        self.box_layout.setContentsMargins(40, 30, 40, 30)
        self.box_layout.setSpacing(15)

        # Titolo
        self.lbl_titolo = QLabel("AGGIUNGI NUOVO PRODOTTO")
        self.lbl_titolo.setObjectName("TitoloAzzurro")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.box_layout.addWidget(self.lbl_titolo)
        self.box_layout.addSpacing(10)

        # -- FORM LAYOUT PER GLI INPUT --
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        # 1. Tipologia Prodotto
        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Attrezzatura", "Skipass", "Assicurazione", "Lezione"])
        self.combo_tipo.setStyleSheet("background-color: white; padding: 5px; border: 1px solid #1a365d;")
        self.form_layout.addRow("Tipologia:", self.combo_tipo)

        # 2. Nome
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Es. Sci Nordica, Skipass Giornaliero...")
        self.form_layout.addRow("Nome Prodotto:", self.input_nome)

        # 3. Prezzo (Usiamo QDoubleSpinBox per evitare che l'utente inserisca lettere)
        self.input_prezzo = QDoubleSpinBox()
        self.input_prezzo.setMaximum(10000.0)
        self.input_prezzo.setDecimals(2)
        self.input_prezzo.setSuffix(" €")
        self.form_layout.addRow("Prezzo:", self.input_prezzo)

        # 4. Quantità (Usiamo QSpinBox per i numeri interi)
        self.input_quantita = QSpinBox()
        self.input_quantita.setMaximum(9999)
        self.input_quantita.setValue(1)
        self.form_layout.addRow("Quantità Iniziale:", self.input_quantita)

        # 5. Disponibilità
        self.check_disponibile = QCheckBox("Imposta subito come disponibile")
        self.check_disponibile.setChecked(True)
        self.form_layout.addRow("", self.check_disponibile)

        self.box_layout.addLayout(self.form_layout)
        self.box_layout.addSpacing(20)

        # -- BOTTONI --
        self.btn_layout = QHBoxLayout()

        self.btn_indietro = QPushButton("Annulla")
        self.btn_indietro.setObjectName("BtnSecondario")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_salva = QPushButton("Salva Prodotto")
        self.btn_salva.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_layout.addWidget(self.btn_indietro)
        self.btn_layout.addWidget(self.btn_salva)

        self.box_layout.addLayout(self.btn_layout)
        self.main_layout.addWidget(self.form_box, alignment=Qt.AlignmentFlag.AlignCenter)

    def applica_stili(self):
        self.setStyleSheet("""
            QWidget { background-color: white; font-family: Arial, sans-serif; }
            #FormBox {
                border: 2px solid #1a365d; border-radius: 5px;
                background-color: white; min-width: 400px; max-width: 450px;
            }
            #TitoloAzzurro {
                background-color: #add8e6; color: #1a365d; font-weight: bold;
                font-size: 16px; padding: 10px; border-radius: 5px;
            }
            QLineEdit, QDoubleSpinBox, QSpinBox {
                background-color: #add8e6; border: 2px solid #1a365d;
                padding: 8px; border-radius: 3px; color: #333; font-size: 14px;
            }
            QPushButton {
                background-color: #1a365d; color: white; font-weight: bold;
                padding: 10px 15px; border-radius: 5px; font-size: 14px;
            }
            QPushButton:hover { background-color: #2a528a; }
            #BtnSecondario { background-color: #666; }
            #BtnSecondario:hover { background-color: #888; }
        """)

    def connetti_segnali(self):
        self.btn_salva.clicked.connect(self.esegui_creazione)
        self.btn_indietro.clicked.connect(self.torna_all_inventario)

    def esegui_creazione(self):
        tipo = self.combo_tipo.currentText()
        nome = self.input_nome.text().strip()
        prezzo = self.input_prezzo.value()
        quantita = self.input_quantita.value()
        is_disponibile = self.check_disponibile.isChecked()

        if not nome:
            QMessageBox.warning(self, "Attenzione", "Il nome del prodotto è obbligatorio.")
            return

        try:
            tutti_prodotti = self.gestore_prodotti.get_tutti_prodotti()
            nuovo_id = 1 if not tutti_prodotti else max(p.id for p in tutti_prodotti) + 1

            nuovo_prodotto = None

            if tipo == "Attrezzatura":
                nuovo_prodotto = Attrezzatura(
                    id_prodotto=nuovo_id,
                    nome=nome,
                    descrizione="",
                    prezzo=prezzo,
                    immagine="",
                    is_disponibile=is_disponibile,
                    brand="Generico",
                    data=date.today(),
                    livello=Livello.PRINCIPIANTE,  # <-- Enum Ufficiale
                    quantita=quantita,
                    taglia="Unica",
                    tipologia=TipologiaAttrezzatura.SCI  # <-- Enum Ufficiale
                )
            elif tipo == "Skipass":
                nuovo_prodotto = SkiPass(
                    id_prodotto=nuovo_id,
                    nome=nome,
                    descrizione="",
                    prezzo=prezzo,
                    immagine="",
                    is_disponibile=is_disponibile,
                    formula_temporale=FormulaTemporale.GIORNALIERO,  # <-- Enum Ufficiale
                    data_inizio=None,
                    data_fine=None
                )
            elif tipo == "Lezione":
                nuovo_prodotto = Lezione(
                    id_prodotto=nuovo_id,
                    nome=nome,
                    descrizione="",
                    prezzo=prezzo,
                    immagine="",
                    is_disponibile=is_disponibile,
                    data=datetime.now(),
                    livello=Livello.PRINCIPIANTE,  # <-- Enum Ufficiale
                    quantita=quantita
                )
            else:
                nuovo_prodotto = Assicurazione(
                    id_prodotto=nuovo_id,
                    nome=nome,
                    descrizione="",
                    prezzo=prezzo,
                    immagine="",
                    is_disponibile=is_disponibile,
                    data_inizio=None,
                    data_fine=None
                )

            self.gestore_prodotti.inserisciNuovoProdotto(nuovo_prodotto)

            QMessageBox.information(self, "Successo", f"{tipo} '{nome}' (ID: #{nuovo_id}) aggiunto al catalogo!")
            self.torna_all_inventario()

        except Exception as e:
            QMessageBox.critical(self, "Errore Creazione", f"Impossibile creare il prodotto:\n{str(e)}")

    def pulisci_campi(self):
        """Svuota il form per il prossimo inserimento."""
        self.input_nome.clear()
        self.input_prezzo.setValue(0.0)
        self.input_quantita.setValue(1)
        self.check_disponibile.setChecked(True)
        self.combo_tipo.setCurrentIndex(0)

    def torna_all_inventario(self):
        self.pulisci_campi()
        if self.main_window:
            self.main_window.mostra_gestione_inventario()