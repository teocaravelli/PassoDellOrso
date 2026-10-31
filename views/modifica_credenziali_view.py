from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QMessageBox,
    QFormLayout
)
from PyQt6.QtCore import Qt


class ModificaCredenzialiView(QWidget):
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

        # Titolo
        self.lbl_titolo = QLabel("MODIFICA CREDENZIALI")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setObjectName("Titolo")
        self.main_layout.addWidget(self.lbl_titolo)

        self.main_layout.addSpacing(20)

        # Riquadro del Form
        self.form_frame = QFrame()
        self.form_frame.setObjectName("FormFrame")
        self.form_layout = QFormLayout(self.form_frame)
        self.form_layout.setSpacing(15)
        self.form_layout.setContentsMargins(30, 30, 30, 30)

        # Campi di input
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Nuova Email (lascia vuoto per non modificare)")

        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("Nuova Password")
        self.input_password.setEchoMode(QLineEdit.EchoMode.Password)

        self.input_conferma_password = QLineEdit()
        self.input_conferma_password.setPlaceholderText("Conferma Nuova Password")
        self.input_conferma_password.setEchoMode(QLineEdit.EchoMode.Password)

        # Aggiunta dei campi al FormLayout
        self.form_layout.addRow(QLabel("Nuova Email:"), self.input_email)
        self.form_layout.addRow(QLabel("Nuova Password:"), self.input_password)
        self.form_layout.addRow(QLabel("Conferma Password:"), self.input_conferma_password)

        self.main_layout.addWidget(self.form_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addSpacing(20)

        # Pulsanti
        self.layout_pulsanti = QHBoxLayout()
        self.layout_pulsanti.setSpacing(20)

        self.btn_salva = QPushButton("Salva Modifiche")
        self.btn_salva.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_annulla = QPushButton("Annulla / Indietro")
        self.btn_annulla.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_annulla.setObjectName("BtnAnnulla")

        self.layout_pulsanti.addWidget(self.btn_salva)
        self.layout_pulsanti.addWidget(self.btn_annulla)

        self.main_layout.addLayout(self.layout_pulsanti)

    def applica_stili(self):
        self.setStyleSheet("""
            ModificaCredenzialiView { background-color: white; font-family: Arial, sans-serif; }
            #Titolo { font-size: 26px; font-weight: bold; color: #1a365d; }
            #FormFrame { border: 2px solid #1a365d; border-radius: 12px; background-color: #f8f9fa; min-width: 450px; }
            QLabel { font-size: 15px; font-weight: bold; color: #333; }
            QLineEdit { padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px; background-color: white; }
            QLineEdit:focus { border: 1px solid #1a365d; }
            QPushButton { background-color: #132a4a; color: white; font-weight: bold; font-size: 15px; border-radius: 8px; padding: 12px; min-width: 200px; }
            QPushButton:hover { background-color: #2a528a; }
            #BtnAnnulla { background-color: #6c757d; }
            #BtnAnnulla:hover { background-color: #5a6268; }
        """)

    def connetti_segnali(self):
        self.btn_salva.clicked.connect(self.salva_modifiche)
        self.btn_annulla.clicked.connect(self.torna_indietro)

    def aggiorna_dati(self):
        """Pulisce i campi ogni volta che si entra nella pagina."""
        self.input_email.clear()
        self.input_password.clear()
        self.input_conferma_password.clear()

        # Precompila l'email attuale per comodità se l'utente è loggato
        utente = getattr(self.gestore_utenti, 'utente_corrente', None)
        if utente:
            email_attuale = getattr(utente, 'email', getattr(utente, '_email', ''))
            self.input_email.setText(email_attuale)

    def salva_modifiche(self):
        utente = getattr(self.gestore_utenti, 'utente_corrente', None)

        if not utente:
            QMessageBox.warning(self, "Errore", "Devi effettuare l'accesso per modificare le credenziali.")
            return

        nuova_email = self.input_email.text().strip()
        nuova_password = self.input_password.text().strip()
        conferma_password = self.input_conferma_password.text().strip()

        modifiche_effettuate = False

        # 1. Controllo ed aggiornamento Email
        if nuova_email:
            email_attuale = getattr(utente, 'email', getattr(utente, '_email', ''))
            if nuova_email != email_attuale:
                try:
                    utente.email = nuova_email
                except AttributeError:
                    utente._email = nuova_email
                modifiche_effettuate = True

        # 2. Controllo ed aggiornamento Password
        if nuova_password or conferma_password:
            if nuova_password != conferma_password:
                QMessageBox.warning(self, "Errore", "Le due password non corrispondono. Riprova.")
                return
            if len(nuova_password) < 4:
                QMessageBox.warning(self, "Errore", "La password deve contenere almeno 4 caratteri.")
                return

            try:
                utente.password = nuova_password
            except AttributeError:
                utente._password = nuova_password
            modifiche_effettuate = True

        # 3. Salvataggio
        if modifiche_effettuate:
            try:
                if hasattr(self.gestore_utenti, '_salva_dati'):
                    self.gestore_utenti._salva_dati()
                elif hasattr(self.gestore_utenti, 'salva_dati'):
                    self.gestore_utenti.salva_dati()

                QMessageBox.information(self, "Successo", "Le tue credenziali sono state aggiornate correttamente!")
                self.torna_indietro()
            except Exception as e:
                QMessageBox.critical(self, "Errore", f"Si è verificato un errore durante il salvataggio: {e}")
        else:
            QMessageBox.information(self, "Nessuna Modifica", "Non hai inserito nuovi dati da salvare.")
            self.torna_indietro()

    def torna_indietro(self):
        if self.main_window and hasattr(self.main_window, 'mostra_profilo'):
            self.main_window.mostra_profilo()