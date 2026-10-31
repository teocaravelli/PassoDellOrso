from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt


class RegistrazioneView(QWidget):
    def __init__(self, gestore_utenti, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_label = QLabel("PASSO DELL'ORSO\nSKI RESORT")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #1a365d;")
        self.main_layout.addWidget(self.logo_label)
        self.main_layout.addSpacing(10)

        self.reg_box = QFrame()
        self.reg_box.setObjectName("RegBox")
        self.box_layout = QVBoxLayout(self.reg_box)
        self.box_layout.setContentsMargins(30, 20, 30, 20)
        self.box_layout.setSpacing(10)

        self.lbl_titolo = QLabel("Registrazione Nuovo Cliente")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setStyleSheet("font-size: 18px; color: #666; margin-bottom: 10px;")
        self.box_layout.addWidget(self.lbl_titolo)

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
        self.input_email.setPlaceholderText("Email")
        self.box_layout.addWidget(self.input_email)

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Password (min. 8 caratteri)")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.box_layout.addWidget(self.input_password)

        self.input_conferma_password = QLineEdit()
        self.input_conferma_password.setPlaceholderText("Conferma Password")
        self.input_conferma_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.box_layout.addWidget(self.input_conferma_password)

        self.box_layout.addSpacing(10)

        self.btn_layout = QHBoxLayout()

        self.btn_indietro = QPushButton("Annulla")
        self.btn_indietro.setObjectName("BtnSecondario")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_registrati = QPushButton("Registrati")
        self.btn_registrati.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_layout.addWidget(self.btn_indietro)
        self.btn_layout.addWidget(self.btn_registrati)

        self.box_layout.addLayout(self.btn_layout)

        self.main_layout.addWidget(self.reg_box, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

    def applica_stili(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
                font-family: Arial, sans-serif;
            }
            #RegBox {
                border: 2px solid #1a365d;
                border-radius: 5px;
                background-color: white;
                min-width: 300px;
                max-width: 350px;
            }
            QLineEdit {
                background-color: #add8e6;
                border: 2px solid #1a365d;
                padding: 6px;
                border-radius: 3px;
                color: #333;
            }
            QPushButton {
                background-color: #1a365d;
                color: white;
                font-weight: bold;
                padding: 8px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2a528a;
            }
            #BtnSecondario {
                background-color: #666;
                border: 2px solid #666;
            }
            #BtnSecondario:hover {
                background-color: #888;
            }
        """)

    def connetti_segnali(self):
        self.btn_registrati.clicked.connect(self.esegui_registrazione)
        self.btn_indietro.clicked.connect(self.torna_al_login)

    def esegui_registrazione(self):
        nome = self.input_nome.text().strip()
        cognome = self.input_cognome.text().strip()
        telefono = self.input_telefono.text().strip()
        email = self.input_email.text().strip()
        password = self.input_password.text().strip()
        conferma = self.input_conferma_password.text().strip()

        if not all([nome, cognome, telefono, email, password, conferma]):
            QMessageBox.warning(self, "Campi Incompleti", "Per favore, compila tutti i campi.")
            return

        if password != conferma:
            QMessageBox.warning(self, "Errore Password", "Le password non coincidono.")
            return

        try:
            nuovo_cliente = self.gestore_utenti.registraCliente(nome, cognome, email, password, telefono)
            QMessageBox.information(
                self,
                "Successo",
                "Registrazione completata con successo!\nÈ stata inviata una mail di benvenuto.\nOra puoi effettuare il login."
            )
            self.torna_al_login()

        except ValueError as e:
            QMessageBox.critical(self, "Errore di Registrazione", str(e))

    def torna_al_login(self):
        self.input_nome.clear()
        self.input_cognome.clear()
        self.input_telefono.clear()
        self.input_email.clear()
        self.input_password.clear()
        self.input_conferma_password.clear()

        if self.main_window:
            self.main_window.mostra_login()