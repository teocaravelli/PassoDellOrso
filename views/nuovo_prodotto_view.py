from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFrame, QMessageBox,
                             QComboBox, QDoubleSpinBox, QSpinBox, QCheckBox,
                             QFormLayout, QStackedWidget, QDateEdit, QDateTimeEdit)
from PyQt6.QtCore import Qt, QDate, QDateTime

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

        self.lbl_titolo = QLabel("AGGIUNGI NUOVO PRODOTTO")
        self.lbl_titolo.setObjectName("TitoloAzzurro")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.box_layout.addWidget(self.lbl_titolo)
        self.box_layout.addSpacing(10)

        # -- CAMPI COMUNI (Visibili per tutti) --
        self.form_layout = QFormLayout()
        self.form_layout.setSpacing(15)

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems(["Attrezzatura", "Skipass", "Lezione", "Assicurazione"])
        self.combo_tipo.setStyleSheet("background-color: white; padding: 5px; border: 1px solid #1a365d;")
        self.form_layout.addRow("Tipologia:", self.combo_tipo)

        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Es. Sci Nordica, Skipass Giornaliero...")
        self.form_layout.addRow("Nome Prodotto:", self.input_nome)

        self.input_prezzo = QDoubleSpinBox()
        self.input_prezzo.setMaximum(10000.0)
        self.input_prezzo.setDecimals(2)
        self.input_prezzo.setSuffix(" €")
        self.form_layout.addRow("Prezzo:", self.input_prezzo)

        self.input_quantita = QSpinBox()
        self.input_quantita.setMaximum(9999)
        self.input_quantita.setValue(1)
        self.form_layout.addRow("Quantità Iniziale:", self.input_quantita)

        self.check_disponibile = QCheckBox("Imposta subito come disponibile")
        self.check_disponibile.setChecked(True)
        self.form_layout.addRow("", self.check_disponibile)

        self.box_layout.addLayout(self.form_layout)

        # -- CAMPI SPECIFICI DINAMICI (QStackedWidget) --
        self.stacked_specifiche = QStackedWidget()
        self.box_layout.addWidget(self.stacked_specifiche)

        # Pagina 0: Attrezzatura
        self.page_attr = QWidget()
        lay_attr = QFormLayout(self.page_attr)
        self.combo_attr_tipo = QComboBox()
        self.combo_attr_tipo.addItems([e.name for e in TipologiaAttrezzatura])
        self.combo_attr_livello = QComboBox()
        self.combo_attr_livello.addItems([e.name for e in Livello])
        self.input_attr_brand = QLineEdit("Generico")
        self.input_attr_taglia = QLineEdit("Unica")
        lay_attr.addRow("Tipo Attrezzo:", self.combo_attr_tipo)
        lay_attr.addRow("Livello:", self.combo_attr_livello)
        lay_attr.addRow("Brand:", self.input_attr_brand)
        lay_attr.addRow("Taglia:", self.input_attr_taglia)
        self.stacked_specifiche.addWidget(self.page_attr)

        # Pagina 1: Skipass
        self.page_skipass = QWidget()
        lay_ski = QFormLayout(self.page_skipass)
        self.combo_ski_formula = QComboBox()
        self.combo_ski_formula.addItems([e.name for e in FormulaTemporale])
        self.date_ski_inizio = QDateEdit(calendarPopup=True)
        self.date_ski_inizio.setDate(QDate.currentDate())
        self.date_ski_fine = QDateEdit(calendarPopup=True)
        self.date_ski_fine.setDate(QDate.currentDate().addDays(1))
        lay_ski.addRow("Formula Temporale:", self.combo_ski_formula)
        lay_ski.addRow("Data Inizio Val.:", self.date_ski_inizio)
        lay_ski.addRow("Data Fine Val.:", self.date_ski_fine)
        self.stacked_specifiche.addWidget(self.page_skipass)

        # Pagina 2: Lezione
        self.page_lez = QWidget()
        lay_lez = QFormLayout(self.page_lez)
        self.combo_lez_livello = QComboBox()
        self.combo_lez_livello.addItems([e.name for e in Livello])
        self.date_lez_ora = QDateTimeEdit(calendarPopup=True)
        self.date_lez_ora.setDateTime(QDateTime.currentDateTime())
        lay_lez.addRow("Livello Lezione:", self.combo_lez_livello)
        lay_lez.addRow("Data e Ora:", self.date_lez_ora)
        self.stacked_specifiche.addWidget(self.page_lez)

        # Pagina 3: Assicurazione
        self.page_assicur = QWidget()
        lay_ass = QFormLayout(self.page_assicur)
        self.date_ass_inizio = QDateEdit(calendarPopup=True)
        self.date_ass_inizio.setDate(QDate.currentDate())
        self.date_ass_fine = QDateEdit(calendarPopup=True)
        self.date_ass_fine.setDate(QDate.currentDate().addDays(1))
        lay_ass.addRow("Data Inizio Copertura:", self.date_ass_inizio)
        lay_ass.addRow("Data Fine Copertura:", self.date_ass_fine)
        self.stacked_specifiche.addWidget(self.page_assicur)

        self.box_layout.addSpacing(10)

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
                background-color: white; min-width: 420px; max-width: 480px;
            }
            #TitoloAzzurro {
                background-color: #add8e6; color: #1a365d; font-weight: bold;
                font-size: 16px; padding: 10px; border-radius: 5px;
            }
            QLineEdit, QDoubleSpinBox, QSpinBox, QComboBox, QDateEdit, QDateTimeEdit {
                background-color: #add8e6; border: 2px solid #1a365d;
                padding: 6px; border-radius: 3px; color: #333; font-size: 13px;
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
        # Cambio pagina dinamico in base alla selezione della combobox
        self.combo_tipo.currentIndexChanged.connect(self.cambia_campi_specifici)

    def cambia_campi_specifici(self, index):
        """Cambia i form mostrati in base alla tipologia di prodotto scelta."""
        self.stacked_specifiche.setCurrentIndex(index)

        # Le categorie Skipass e Assicurazione tipicamente non hanno "scorte" fisiche da scalare
        if self.combo_tipo.currentText() in ["Skipass", "Assicurazione"]:
            self.input_quantita.setEnabled(False)
            self.input_quantita.setValue(999)  # Illimitati
        else:
            self.input_quantita.setEnabled(True)
            self.input_quantita.setValue(1)

    def esegui_creazione(self):
        tipo = self.combo_tipo.currentText()
        nome = self.input_nome.text().strip()

        if not nome:
            QMessageBox.warning(self, "Attenzione", "Il nome del prodotto è obbligatorio.")
            return

        # 1. Raccogliamo i campi base in un dizionario
        dati_prodotto = {
            "nome": nome,
            "prezzo": self.input_prezzo.value(),
            "quantita": self.input_quantita.value(),
            "is_disponibile": self.check_disponibile.isChecked()
        }

        # 2. Aggiungiamo i campi specifici a seconda della tendina selezionata
        if tipo == "Attrezzatura":
            dati_prodotto["brand"] = self.input_attr_brand.text().strip()
            dati_prodotto["taglia"] = self.input_attr_taglia.text().strip()
            dati_prodotto["livello"] = Livello[self.combo_attr_livello.currentText()]
            dati_prodotto["tipologia"] = TipologiaAttrezzatura[self.combo_attr_tipo.currentText()]

        elif tipo == "Skipass":
            dati_prodotto["formula_temporale"] = FormulaTemporale[self.combo_ski_formula.currentText()]
            dati_prodotto["data_inizio"] = self.date_ski_inizio.date().toPyDate()
            dati_prodotto["data_fine"] = self.date_ski_fine.date().toPyDate()

        elif tipo == "Lezione":
            dati_prodotto["data"] = self.date_lez_ora.dateTime().toPyDateTime()
            dati_prodotto["livello"] = Livello[self.combo_lez_livello.currentText()]

        elif tipo == "Assicurazione":
            dati_prodotto["data_inizio"] = self.date_ass_inizio.date().toPyDate()
            dati_prodotto["data_fine"] = self.date_ass_fine.date().toPyDate()

        # 3. Deleghiamo la creazione reale al Controller
        try:
            self.gestore_prodotti.crea_e_salva_prodotto(tipo, dati_prodotto)

            QMessageBox.information(self, "Successo", f"{tipo} '{nome}' aggiunto al catalogo!")
            self.torna_all_inventario()

        except Exception as e:
            QMessageBox.critical(self, "Errore Creazione", f"Impossibile creare il prodotto:\n{str(e)}")

    def pulisci_campi(self):
        self.input_nome.clear()
        self.input_prezzo.setValue(0.0)
        self.input_quantita.setValue(1)
        self.check_disponibile.setChecked(True)
        self.combo_tipo.setCurrentIndex(0)
        self.input_attr_brand.setText("Generico")
        self.input_attr_taglia.setText("Unica")

    def torna_all_inventario(self):
        self.pulisci_campi()
        if self.main_window:
            self.main_window.mostra_gestione_inventario()