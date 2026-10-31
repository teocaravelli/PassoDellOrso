from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt


class InserimentoDipendenteView(QWidget):
    def __init__(self, gestore_utenti, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # -- CONTENITORE PRINCIPALE (Form) --
        self.form_box = QFrame()
        self.form_box.setObjectName("FormBox")
        self.box_layout = QVBoxLayout(self.form_box)
        self.box_layout.setContentsMargins(40, 30, 40, 30)
        self.box_layout.setSpacing(15)

        # Titolo
        self.lbl_titolo = QLabel("CREAZIONE NUOVO DIPENDENTE")
        self.lbl_titolo.setObjectName("TitoloAzzurro")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.box_layout.addWidget(self.lbl_titolo)

        self.box_layout.addSpacing(10)

        # -- Campi di Input --
        self.input_nome = QLineEdit()
        self.input_nome.setPlaceholderText("Nome")
        self.box_layout.addWidget(self.input_nome)

        self.input_cognome = QLineEdit()
        self.input_cognome.setPlaceholderText("Cognome")
        self.box_layout.addWidget(self.input_cognome)

        self.input_telefono = QLineEdit()
        self.input_telefono.setPlaceholderText("Numero di Telefono")
        self.box_layout.addWidget(self.input_telefono)

        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email Aziendale")
        self.box_layout.addWidget(self.input_email)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Password temporanea (min. 8 caratteri)")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.box_layout.addWidget(self.input_password)

        self.input_conferma = QLineEdit()
        self.input_conferma.setPlaceholderText("Conferma Password")
        self.input_conferma.setEchoMode(QLineEdit.EchoMode.Password)
        self.box_layout.addWidget(self.input_conferma)

        self.box_layout.addSpacing(20)

        # -- Bottoni --
        self.btn_layout = QHBoxLayout()

        self.btn_indietro = QPushButton("Annulla")
        self.btn_indietro.setObjectName("BtnSecondario")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_salva = QPushButton("Crea Profilo")
        self.btn_salva.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_layout.addWidget(self.btn_indietro)
        self.btn_layout.addWidget(self.btn_salva)

        self.box_layout.addLayout(self.btn_layout)

        self.main_layout.addWidget(self.form_box, alignment=Qt.AlignmentFlag.AlignCenter)

    def applica_stili(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Arial, sans-serif;
            }
            #FormBox {
                border: 2px solid #1a365d;
                border-radius: 5px;
                background-color: white;
                min-width: 350px;
                max-width: 400px;
            }
            #TitoloAzzurro {
                background-color: #add8e6;
                color: #1a365d;
                font-weight: bold;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QLineEdit {
                background-color: #add8e6;
                border: 2px solid #1a365d;
                padding: 8px;
                border-radius: 3px;
                color: #333;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1a365d;
                color: white;
                font-weight: bold;
                padding: 10px 15px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2a528a;
            }
            #BtnSecondario {
                background-color: #666;
            }
            #BtnSecondario:hover {
                background-color: #888;
            }
        """)

    def connetti_segnali(self):
        self.btn_salva.clicked.connect(self.esegui_creazione)
        self.btn_indietro.clicked.connect(self.torna_alla_dashboard)

    def esegui_creazione(self):
        nome = self.input_nome.text().strip()
        cognome = self.input_cognome.text().strip()
        telefono = self.input_telefono.text().strip()
        email = self.input_email.text().strip()
        password = self.input_password.text().strip()
        conferma = self.input_conferma.text().strip()

        if not all([nome, cognome, telefono, email, password, conferma]):
            QMessageBox.warning(self, "Campi Incompleti", "Per favore, compila tutti i campi.")
            return

        if password != conferma:
            QMessageBox.warning(self, "Errore Password", "Le password non coincidono.")
            return

        try:
            nuovo_dipendente = self.gestore_utenti.registraDipendente(
                nome, cognome, email, password, telefono
            )

            QMessageBox.information(
                self,
                "Successo",
                f"Profilo dipendente creato con successo!\nID Assegnato: #{nuovo_dipendente.id_dipendente}"
            )
            self.torna_alla_dashboard()

        except ValueError as e:
            QMessageBox.critical(self, "Errore Creazione", str(e))

    def pulisci_campi(self):
        """Svuota il form per il prossimo utilizzo."""
        self.input_nome.clear()
        self.input_cognome.clear()
        self.input_telefono.clear()
        self.input_email.clear()
        self.input_password.clear()
        self.input_conferma.clear()

    def torna_alla_dashboard(self):
        self.pulisci_campi()
        if self.main_window:
            self.main_window.mostra_area_dipendente()