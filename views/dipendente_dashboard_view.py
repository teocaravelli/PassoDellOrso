from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame, QMessageBox)
from PyQt6.QtCore import Qt


class DipendenteDashboardView(QWidget):
    def __init__(self, gestore_utenti, gestore_ordini, gestore_piste, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.gestore_ordini = gestore_ordini
        self.gestore_piste = gestore_piste
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        # Layout principale
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # 1. TOP BAR (Saluto utente)
        self.top_bar = QFrame()
        self.top_bar.setObjectName("TopBar")
        self.top_layout = QHBoxLayout(self.top_bar)

        self.lbl_saluto = QLabel("Ciao, Utente (Dipendente)")
        self.lbl_saluto.setObjectName("SalutoTesto")
        self.top_layout.addWidget(self.lbl_saluto, alignment=Qt.AlignmentFlag.AlignLeft)

        self.main_layout.addWidget(self.top_bar)

        # 2. CORPO PRINCIPALE (Split in due colonne)
        self.body_layout = QHBoxLayout()
        self.body_layout.setContentsMargins(0, 0, 0, 0)
        self.body_layout.setSpacing(20)

        self.crea_menu_laterale()
        self.crea_area_widget()

        self.body_layout.addWidget(self.sidebar)
        self.body_layout.addWidget(self.content_area, stretch=1)  # stretch=1 fa espandere la parte destra

        self.main_layout.addLayout(self.body_layout)

    def crea_menu_laterale(self):
        """Crea la colonna di sinistra con il menù di navigazione."""
        self.sidebar = QFrame()
        self.sidebar.setObjectName("Sidebar")
        self.sidebar.setFixedWidth(250)

        self.sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.sidebar_layout.setSpacing(15)
        self.sidebar_layout.setContentsMargins(20, 20, 20, 20)

        # Logo / Titolo Sidebar
        self.logo_label = QLabel("PASSO DELL'ORSO\nSKI RESORT")
        self.logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo_label.setObjectName("LogoText")
        self.sidebar_layout.addWidget(self.logo_label)
        self.sidebar_layout.addSpacing(10)

        # Intestazione Menù
        self.lbl_menu = QLabel("MENÙ DIPENDENTE")
        self.lbl_menu.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_menu.setObjectName("HeaderAzzurro")
        self.sidebar_layout.addWidget(self.lbl_menu)
        self.sidebar_layout.addSpacing(10)

        # Bottoni di navigazione (Aggiornati secondo le tue direttive)
        self.btn_ordini = QPushButton("Gestione Ordini")
        self.btn_piste = QPushButton("Gestione Piste")
        self.btn_inventario = QPushButton("Inventario")
        self.btn_nuovo_dip = QPushButton("Nuovo Dipendente")
        self.btn_logout = QPushButton("Logout")

        # Assegnazione classi per il CSS
        bottoni = [self.btn_ordini, self.btn_piste, self.btn_inventario, self.btn_nuovo_dip, self.btn_logout]
        for btn in bottoni:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.sidebar_layout.addWidget(btn)

        self.sidebar_layout.addStretch()  # Spinge il layout verso l'alto

    def crea_area_widget(self):
        """Crea la colonna di destra con i widget riepilogativi della Dashboard."""
        self.content_area = QFrame()
        self.content_layout = QVBoxLayout(self.content_area)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.content_layout.setContentsMargins(20, 20, 40, 20)
        self.content_layout.setSpacing(30)

        # -- WIDGET 1: ULTIMI ORDINI --
        self.widget_ordini = QFrame()
        self.w_ordini_layout = QVBoxLayout(self.widget_ordini)

        lbl_titolo_ordini = QLabel("ULTIMI ORDINI")
        lbl_titolo_ordini.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_titolo_ordini.setObjectName("HeaderAzzurro")

        # Testo segnaposto (nella versione finale lo popolerai tramite self.gestore_ordini)
        testo_ordini = QLabel(
            "- Ordine #999 | Mario Rossi | 320.00 €\n- Ordine #998 | Luigi Neri | [Rimborso Richiesto]")
        testo_ordini.setStyleSheet("font-size: 14px; color: #333;")

        self.btn_vedi_ordini = QPushButton("Vedi tutti")
        self.btn_vedi_ordini.setFixedWidth(150)
        self.btn_vedi_ordini.setCursor(Qt.CursorShape.PointingHandCursor)

        self.w_ordini_layout.addWidget(lbl_titolo_ordini)
        self.w_ordini_layout.addWidget(testo_ordini)
        self.w_ordini_layout.addWidget(self.btn_vedi_ordini, alignment=Qt.AlignmentFlag.AlignCenter)

        # -- WIDGET 2: GESTIONE RAPIDA PISTE --
        self.widget_piste = QFrame()
        self.w_piste_layout = QVBoxLayout(self.widget_piste)

        lbl_titolo_piste = QLabel("GESTIONE RAPIDA PISTE")
        lbl_titolo_piste.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_titolo_piste.setObjectName("HeaderAzzurro")

        testo_piste = QLabel("- Direttissima: [ APERTA ]\n- Raccordo: [ CHIUSA ]")
        testo_piste.setStyleSheet("font-size: 14px; color: #333;")

        self.btn_vedi_piste = QPushButton("Vedi tutte")
        self.btn_vedi_piste.setFixedWidth(150)
        self.btn_vedi_piste.setCursor(Qt.CursorShape.PointingHandCursor)

        self.w_piste_layout.addWidget(lbl_titolo_piste)
        self.w_piste_layout.addWidget(testo_piste)
        self.w_piste_layout.addWidget(self.btn_vedi_piste, alignment=Qt.AlignmentFlag.AlignCenter)

        self.content_layout.addWidget(self.widget_ordini)
        self.content_layout.addWidget(self.widget_piste)
        self.content_layout.addStretch()

    def applica_stili(self):
        self.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
                font-family: Arial, sans-serif;
            }
            #TopBar {
                border-bottom: 2px solid #1a365d;
                background-color: white;
                padding: 10px 20px;
            }
            #SalutoTesto {
                font-size: 16px;
                color: #1a365d;
                font-weight: bold;
            }
            #Sidebar {
                border-right: 2px solid #1a365d;
                background-color: white;
            }
            #LogoText {
                font-size: 20px;
                font-weight: bold;
                color: #1a365d;
            }
            #HeaderAzzurro {
                background-color: #add8e6;
                color: #1a365d;
                font-weight: bold;
                font-size: 16px;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #1a365d;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #2a528a;
            }
        """)

    def connetti_segnali(self):
        self.btn_logout.clicked.connect(self.esegui_logout)

        # Connessioni verso schermate future
        self.btn_nuovo_dip.clicked.connect(self.vai_a_nuovo_dipendente)
        self.btn_ordini.clicked.connect(self.vai_a_ordini)
        self.btn_vedi_ordini.clicked.connect(self.vai_a_ordini)
        self.btn_piste.clicked.connect(self.vai_a_piste)
        self.btn_vedi_piste.clicked.connect(self.vai_a_piste)
        self.btn_inventario.clicked.connect(self.vai_a_inventario)

    def aggiorna_vista(self):
        """Metodo da chiamare quando si accede alla dashboard per aggiornare il nome."""
        utente = self.gestore_utenti.utente_corrente
        if utente:
            self.lbl_saluto.setText(f"Ciao, {utente.nome} (Dipendente #{getattr(utente, 'id_dipendente', 'N/A')})")

    def esegui_logout(self):
        risposta = QMessageBox.question(self, "Logout", "Sei sicuro di voler uscire?",
                                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if risposta == QMessageBox.StandardButton.Yes:
            self.gestore_utenti.effettuaLogout()
            if self.main_window:
                self.main_window.mostra_login()

    def vai_a_nuovo_dipendente(self):
        if self.main_window:
            self.main_window.mostra_inserimento_dipendente()

    def vai_a_ordini(self):
        if self.main_window:
            self.main_window.mostra_gestione_ordini()

    def vai_a_piste(self):
        if self.main_window:
            self.main_window.mostra_area_gestione_piste()

    def vai_a_inventario(self):
        if self.main_window:
            self.main_window.mostra_gestione_inventario()
