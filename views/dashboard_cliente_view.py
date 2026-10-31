from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from models.enums import StatoApertura, Difficolta


class DashboardClienteView(QWidget):
    def __init__(self, gestore_utenti, gestore_piste, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.gestore_piste = gestore_piste
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        # Layout principale
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(40, 30, 40, 30)
        self.main_layout.setSpacing(30)

        # ==========================================
        # COLONNA SINISTRA: LOGO E MENÙ
        # ==========================================
        self.left_layout = QVBoxLayout()
        self.left_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        self.left_layout.setSpacing(15)

        self.logo_label = QLabel("⛰️ PASSO DELL'ORSO\nSKI RESORT")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setObjectName("LogoLabel")
        self.left_layout.addWidget(self.logo_label)

        self.left_layout.addSpacing(10)

        self.lbl_menu = QLabel("MENÙ")
        self.lbl_menu.setObjectName("HeaderAzzurro")
        self.lbl_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_menu.setFixedSize(220, 55)
        self.left_layout.addWidget(self.lbl_menu)

        self.left_layout.addSpacing(10)

        self.btn_prodotti = QPushButton("Prodotti")
        self.btn_ordini = QPushButton("I miei ordini")
        self.btn_profilo = QPushButton("Profilo")
        self.btn_logout = QPushButton("Logout")

        for btn in [self.btn_prodotti, self.btn_ordini, self.btn_profilo, self.btn_logout]:
            btn.setObjectName("MenuButton")
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedSize(160, 42)
            self.left_layout.addWidget(btn)

        # ==========================================
        # LINEA SEPARATRICE VERTICALE
        # ==========================================
        self.linea_verticale = QFrame()
        self.linea_verticale.setFrameShape(QFrame.Shape.VLine)
        self.linea_verticale.setObjectName("LineaSeparazione")

        # ==========================================
        # COLONNA DESTRA: BENVENUTO, CARRELLO E PISTE
        # ==========================================
        self.right_layout = QVBoxLayout()
        self.right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.right_layout.setSpacing(20)

        self.top_right_layout = QHBoxLayout()

        self.lbl_benvenuto = QLabel("Ciao Utente")
        self.lbl_benvenuto.setStyleSheet("font-size: 18px; font-weight: bold; color: #1a365d;")
        self.top_right_layout.addWidget(self.lbl_benvenuto)

        self.top_right_layout.addStretch()

        self.btn_carrello = QPushButton("Carrello (0)")
        self.btn_carrello.setObjectName("CarrelloButton")
        self.btn_carrello.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_carrello.setFixedSize(180, 42)
        self.top_right_layout.addWidget(self.btn_carrello)

        self.right_layout.addLayout(self.top_right_layout)
        self.right_layout.addSpacing(5)

        self.lbl_stato_piste = QLabel("STATO PISTE")
        self.lbl_stato_piste.setObjectName("HeaderAzzurro")
        self.lbl_stato_piste.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_stato_piste.setFixedHeight(55)
        self.right_layout.addWidget(self.lbl_stato_piste)

        self.piste_container = QWidget()
        self.piste_layout = QVBoxLayout(self.piste_container)
        self.piste_layout.setContentsMargins(10, 10, 10, 10)
        self.piste_layout.setSpacing(15)
        self.piste_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.right_layout.addWidget(self.piste_container)

        self.main_layout.addLayout(self.left_layout, 1)
        self.main_layout.addWidget(self.linea_verticale)
        self.main_layout.addLayout(self.right_layout, 2)

    def applica_stili(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                font-family: Arial, sans-serif;
            }
            #LogoLabel {
                font-size: 20px;
                font-weight: bold;
                color: #1a365d;
            }
            #HeaderAzzurro {
                background-color: #a3d8f4;
                color: #111111;
                font-size: 18px;
                font-weight: bold;
                border-radius: 12px;
            }
            #MenuButton, #CarrelloButton {
                background-color: #132a4a;
                color: white;
                font-weight: bold;
                font-size: 15px;
                border-radius: 8px;
            }
            #MenuButton:hover, #CarrelloButton:hover {
                background-color: #2a528a;
            }
            #LineaSeparazione {
                border: 1px solid #1a365d;
                background-color: #1a365d;
                max-width: 2px;
            }
        """)

    def connetti_segnali(self):
        self.btn_prodotti.clicked.connect(self.vai_a_prodotti)
        self.btn_ordini.clicked.connect(self.vai_a_ordini)
        self.btn_profilo.clicked.connect(self.vai_a_profilo)
        self.btn_carrello.clicked.connect(self.vai_a_carrello)
        self.btn_logout.clicked.connect(self.esegui_logout)

    def aggiorna_dati(self):
        # Cerchiamo l'utente loggato in modo sicuro
        utente = None
        if self.gestore_utenti:
            if hasattr(self.gestore_utenti, 'utente_corrente'):
                utente = self.gestore_utenti.utente_corrente
            elif hasattr(self.gestore_utenti, 'utente_loggato'):
                utente = self.gestore_utenti.utente_loggato
            elif hasattr(self.gestore_utenti, 'get_utente_loggato'):
                utente = self.gestore_utenti.get_utente_loggato()

        if utente:
            nome_grezzo = getattr(utente, 'nome', getattr(utente, '_nome', ''))
            cognome_grezzo = getattr(utente, 'cognome', getattr(utente, '_cognome', ''))

            nome = str(nome_grezzo).strip().title()
            cognome = str(cognome_grezzo).strip().title()

            if self.main_window:
                self.main_window.setWindowTitle(f"Ciao, {nome} {cognome}!")

            self.lbl_benvenuto.setText(f"Ciao {nome} {cognome}")

            carrello = getattr(utente, 'prodotti_carrello', getattr(utente, '_prodotti_carrello', []))
            tot_prodotti = sum(item.quantita for item in carrello) if carrello else 0
            self.btn_carrello.setText(f"Carrello ({tot_prodotti})")
        else:
            self.lbl_benvenuto.setText("Benvenuto Ospite")

        # Pulizia e ricaricamento delle piste
        while self.piste_layout.count():
            child = self.piste_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        piste = self.gestore_piste.visualizzaPiste()

        if not piste:
            lbl = QLabel("Nessuna pista caricata nel database.")
            self.piste_layout.addWidget(lbl)
            return

        for pista in piste:
            nome_pista = getattr(pista, 'nome', getattr(pista, '_nome', 'Nome Sconosciuto'))
            stato = getattr(pista, 'stato_apertura', getattr(pista, '_stato_apertura', None))
            difficolta = getattr(pista, 'difficolta', getattr(pista, '_difficolta', None))

            if stato == StatoApertura.APERTA:
                icona, testo_stato = "🟢", "APERTA"
            elif stato == StatoApertura.CHIUSA:
                icona, testo_stato = "🔴", "CHIUSA"
            else:
                icona, testo_stato = "🟡", "MANUTENZIONE"

            if difficolta == Difficolta.AZZURRA:
                colore_diff, nome_diff = "#007BFF", "Azzurra"
            elif difficolta == Difficolta.ROSSA:
                colore_diff, nome_diff = "#DC3545", "Rossa"
            elif difficolta == Difficolta.NERA:
                colore_diff, nome_diff = "#000000", "Nera"
            else:
                colore_diff, nome_diff = "#888888", "Sconosciuta"

            testo_html = f"<span style='font-size: 16px; color: #333333;'>- <b>{nome_pista}</b> " \
                         f"(<span style='color: {colore_diff}; font-weight: bold;'>{nome_diff}</span>) " \
                         f": &nbsp;{icona} {testo_stato}</span>"

            lbl = QLabel(testo_html)
            self.piste_layout.addWidget(lbl)

    def vai_a_prodotti(self):
        if self.main_window and hasattr(self.main_window, 'mostra_prodotti'):
            self.main_window.mostra_prodotti()

    def vai_a_ordini(self):
        if self.main_window and hasattr(self.main_window, 'mostra_miei_ordini'):
            self.main_window.mostra_miei_ordini()

    def vai_a_profilo(self):
        if self.main_window and hasattr(self.main_window, 'mostra_profilo'):
            self.main_window.mostra_profilo()

    def vai_a_carrello(self):
        if self.main_window and hasattr(self.main_window, 'mostra_carrello'):
            self.main_window.mostra_carrello()

    def esegui_logout(self):
        if hasattr(self.gestore_utenti, 'logout'):
            self.gestore_utenti.logout()
        if self.main_window:
            self.main_window.setWindowTitle("Passo dell'Orso - Ski Resort")
            self.main_window.mostra_login()