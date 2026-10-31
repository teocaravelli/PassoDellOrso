from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QMessageBox
)


class RecuperoPasswordView(QWidget):
    def __init__(self, gestore_utenti, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.main_window = main_window

        # Stato per seguire il diagramma di sequenza
        self.fase_inserimento_password = False
        self.email_corrente = ""

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.logo_label = QLabel("PASSO DELL'ORSO\nSKI RESORT")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setObjectName("LogoLabel")
        self.main_layout.addWidget(self.logo_label)
        self.main_layout.addSpacing(20)

        self.box_main = QFrame()
        self.box_main.setObjectName("BoxRecupero")
        self.box_layout = QVBoxLayout(self.box_main)
        self.box_layout.setContentsMargins(30, 25, 30, 25)
        self.box_layout.setSpacing(15)

        self.lbl_titolo = QLabel("Recupero Credenziali")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setObjectName("LblTitoloBox")
        self.box_layout.addWidget(self.lbl_titolo)

        linea1 = QFrame()
        linea1.setFrameShape(QFrame.Shape.HLine)
        linea1.setObjectName("Linea")
        self.box_layout.addWidget(linea1)

        self.lbl_istruzioni = QLabel("Inserisci la tua email registrata (richiediMail):")
        self.lbl_istruzioni.setWordWrap(True)
        self.lbl_istruzioni.setObjectName("LblIstruzioni")
        self.box_layout.addWidget(self.lbl_istruzioni)

        self.lbl_input = QLabel("Email:")
        self.lbl_input.setObjectName("LblLabel")

        self.input_campo = QLineEdit()
        self.input_campo.setObjectName("InputCampo")
        self.input_campo.setPlaceholderText("email_esempio@mail.com")

        self.box_layout.addWidget(self.lbl_input)
        self.box_layout.addWidget(self.input_campo)

        self.box_layout.addSpacing(10)

        self.btn_azione = QPushButton("Invia Richiesta")
        self.btn_azione.setObjectName("BtnPrincipale")
        self.btn_azione.setCursor(Qt.CursorShape.PointingHandCursor)
        self.box_layout.addWidget(self.btn_azione, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_indietro = QPushButton("Torna al Login")
        self.btn_indietro.setObjectName("BtnLink")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.box_layout.addWidget(self.btn_indietro, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.box_main, alignment=Qt.AlignmentFlag.AlignCenter)

    def applica_stili(self):
        self.setStyleSheet("""
            RecuperoPasswordView {
                background-color: white;
                font-family: Arial, sans-serif;
            }
            #LogoLabel {
                font-size: 24px;
                font-weight: bold;
                color: #1a365d;
            }
            #BoxRecupero {
                border: 2px solid #1a365d;
                border-radius: 8px;
                background-color: white;
                min-width: 320px;
                max-width: 380px;
            }
            #LblTitoloBox {
                font-size: 18px;
                font-weight: bold;
                color: #1a365d;
            }
            #LblIstruzioni {
                font-size: 13px;
                color: #555;
            }
            #LblLabel {
                font-size: 13px;
                color: #333;
                font-weight: bold;
            }
            #Linea {
                color: #1a365d;
                background-color: #1a365d;
                max-height: 2px;
            }
            QLineEdit#InputCampo {
                background-color: #add8e6;
                border: 2px solid #1a365d;
                padding: 6px;
                border-radius: 4px;
                color: #333;
                font-size: 14px;
            }
            QPushButton#BtnPrincipale {
                background-color: #1a365d;
                color: white;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 5px;
                min-width: 140px;
            }
            QPushButton#BtnPrincipale:hover {
                background-color: #2a528a;
            }
            QPushButton#BtnLink {
                background-color: transparent;
                color: #6a0dad;
                text-decoration: underline;
                border: none;
                font-size: 13px;
                margin-top: 5px;
            }
            QPushButton#BtnLink:hover {
                color: #8b008b;
            }
        """)

    def connetti_segnali(self):
        self.btn_azione.clicked.connect(self.gestisci_clic)
        self.btn_indietro.clicked.connect(self.torna_al_login)

    def gestisci_clic(self):
        if not self.fase_inserimento_password:
            # --- FASE 1: InserisciMail(email) ---
            email = self.input_campo.text().strip()
            if not email:
                QMessageBox.warning(self, "Attenzione", "Inserisci un indirizzo email.")
                return

            try:
                # Sfruttiamo il metodo ufficiale del tuo GestoreUtenti
                self.gestore_utenti.inserisciMail(email)
                self.gestore_utenti.recuperoCredenziali(email)
            except ValueError as e:
                # mailNonValida() -> Loop riproposto
                QMessageBox.critical(self, "Errore", f"mailNonValida(): {str(e)}")
                self.input_campo.clear()
                return

            self.email_corrente = email
            QMessageBox.information(
                self,
                "Email Inviata",
                "confermaEmailRecupero(): Email di recupero inviata con successo tramite GestoreMail."
            )

            # Passa alla fase 2: ImpostaNuovaPassword
            self.fase_inserimento_password = True
            self.lbl_istruzioni.setText("Inserisci la nuova password (minimo 8 caratteri):")
            self.lbl_input.setText("Nuova Password:")
            self.input_campo.clear()
            self.input_campo.setEchoMode(QLineEdit.EchoMode.Password)
            self.input_campo.setPlaceholderText("********")
            self.btn_azione.setText("Aggiorna Password")

        else:
            # --- FASE 2: ImpostaNuovaPassword(nuovaPassword) ---
            nuova_password = self.input_campo.text().strip()

            try:
                # Sfruttiamo il metodo nativo che valida la password, aggiorna l'utente, salva su pickle e invia la mail
                self.gestore_utenti.inserisciNuovaPassword(self.email_corrente, nuova_password)
            except ValueError as e:
                # passwordNonValida() -> Loop riproposto
                QMessageBox.critical(self, "Errore", f"passwordNonValida(): {str(e)}")
                return
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Errore durante l'aggiornamento: {str(e)}")
                return

            # confermaModifica() / mostraConfermaModifica()
            QMessageBox.information(
                self,
                "Successo",
                "confermaModifica(): Password aggiornata con successo! Ora puoi effettuare il login con la nuova password."
            )
            self.torna_al_login()

    def torna_al_login(self):
        self.fase_inserimento_password = False
        self.email_corrente = ""
        self.input_campo.clear()
        self.input_campo.setEchoMode(QLineEdit.EchoMode.Normal)
        self.input_campo.setPlaceholderText("email_esempio@mail.com")
        self.lbl_istruzioni.setText("Inserisci la tua email registrata (richiediMail):")
        self.lbl_input.setText("Email:")
        self.btn_azione.setText("Invia Richiesta")

        if self.main_window and hasattr(self.main_window, 'mostra_login'):
            self.main_window.mostra_login()