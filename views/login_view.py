import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from controllers.gestore_utenti import GestoreUtenti
from models.cliente import Cliente
from models.dipendente import Dipendente

class LoginView(QWidget):
    def __init__(self, gestore_utenti, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        # Riferimento alla finestra principale (QStackedWidget) per poter cambiare pagina
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label = QLabel()
        self.logo_label.setText("PASSO DELL'ORSO\nSKI RESORT")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #1a365d;")
        self.main_layout.addWidget(self.logo_label)
        self.main_layout.addSpacing(20)

        self.login_box = QFrame()
        self.login_box.setObjectName("LoginBox")
        self.box_layout = QVBoxLayout(self.login_box)
        self.box_layout.setContentsMargins(30, 20, 30, 20)
        self.box_layout.setSpacing(15)

        self.lbl_titolo = QLabel("Login")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setStyleSheet("font-size: 18px; color: #666;")
        self.box_layout.addWidget(self.lbl_titolo)

        linea1 = QFrame()
        linea1.setFrameShape(QFrame.Shape.HLine)
        linea1.setStyleSheet("color: #1a365d;")
        self.box_layout.addWidget(linea1)

        self.lbl_email = QLabel("Email:")
        self.lbl_email.setStyleSheet("color: #666;")
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("email_esempio@mail.com")
        self.box_layout.addWidget(self.lbl_email)
        self.box_layout.addWidget(self.input_email)

        self.lbl_password = QLabel("Password:")
        self.lbl_password.setStyleSheet("color: #666;")
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("********")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)  # Nasconde i caratteri
        self.box_layout.addWidget(self.lbl_password)
        self.box_layout.addWidget(self.input_password)

        self.btn_accedi = QPushButton("Accedi")
        self.btn_accedi.setCursor(Qt.CursorShape.PointingHandCursor)
        self.box_layout.addWidget(self.btn_accedi, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_recupero = QPushButton("Password dimenticata?")
        self.btn_recupero.setObjectName("LinkButton")
        self.btn_recupero.setCursor(Qt.CursorShape.PointingHandCursor)
        self.box_layout.addWidget(self.btn_recupero, alignment=Qt.AlignmentFlag.AlignCenter)

        linea2 = QFrame()
        linea2.setFrameShape(QFrame.Shape.HLine)
        linea2.setStyleSheet("color: #1a365d;")
        self.box_layout.addWidget(linea2)

        self.lbl_nuovo = QLabel("Sei un nuovo utente?")
        self.lbl_nuovo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_nuovo.setStyleSheet("color: #666;")
        self.box_layout.addWidget(self.lbl_nuovo)

        self.btn_registrati = QPushButton("Registrati")
        self.btn_registrati.setCursor(Qt.CursorShape.PointingHandCursor)
        self.box_layout.addWidget(self.btn_registrati, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.login_box, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(self.main_layout)

    def applica_stili(self):
        self.setStyleSheet("""
                    QWidget {
                        background-color: white;
                        color: black;
                        font-family: Arial, sans-serif;
                    }

                    /* Stile del contenitore centrale */
                    #LoginBox {
                        border: 2px solid #1a365d;
                        border-radius: 5px;
                        background-color: white;
                        min-width: 250px;
                        max-width: 300px;
                    }

                    /* Stile delle caselle di testo (azzurre) */
                    QLineEdit {
                        background-color: #add8e6;
                        border: 2px solid #1a365d;
                        padding: 5px;
                        border-radius: 3px;
                        color: #333;
                    }

                    /* Stile dei bottoni principali */
                    QPushButton {
                        background-color: #1a365d;
                        color: white;
                        font-weight: bold;
                        padding: 8px 20px;
                        border-radius: 5px;
                        min-width: 100px;
                    }
                    QPushButton:hover {
                        background-color: #2a528a;
                    }

                    /* Stile del finto link per la password dimenticata */
                    #LinkButton {
                        background-color: transparent;
                        color: #6a0dad; /* Viola/bluastro come nel mockup */
                        text-decoration: underline;
                        border: none;
                        font-weight: normal;
                        padding: 0px;
                        min-width: 0px;
                    }
                    #LinkButton:hover {
                        color: #8b008b;
                    }
                """)

    def connetti_segnali(self):
        self.btn_accedi.clicked.connect(self.esegui_login)
        self.btn_registrati.clicked.connect(self.vai_a_registrazione)
        self.btn_recupero.clicked.connect(self.recupera_password)

    def esegui_login(self):
        email = self.input_email.text().strip()
        password = self.input_password.text().strip()

        if not email or not password:
            QMessageBox.warning(self, "Attenzione", "Inserisci sia email che password.")
            return
        utente_loggato = self.gestore_utenti.richiestaAccesso(email, password)

        if utente_loggato:
            if isinstance(utente_loggato, Dipendente):
                self.main_window.mostra_area_dipendente()
            else:
                self.main_window.mostra_dashboard_cliente()
        else:
            QMessageBox.critical(self, "Errore", "Credenziali errate.")
            self.input_password.clear()

    def vai_a_registrazione(self):
        if self.main_window:
            self.main_window.mostra_registrazione()

    def recupera_password(self):
        QMessageBox.information(self, "Recupero", "Qui apriremo il popup per il recupero password.")