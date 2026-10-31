from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QPushButton, QFrame)
from PyQt6.QtCore import Qt


class ProfiloView(QWidget):
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
        self.main_layout.setSpacing(25)

        # Titolo
        self.lbl_titolo = QLabel("IL MIO PROFILO")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setObjectName("Titolo")
        self.main_layout.addWidget(self.lbl_titolo)

        # Riquadro contenente i dati e i pagamenti
        self.info_box = QFrame()
        self.info_box.setObjectName("InfoBox")
        # Impostiamo la dimensione minima direttamente sul widget anziché via CSS
        self.info_box.setMinimumWidth(650)
        self.info_box.setMinimumHeight(250)

        # Layout orizzontale
        self.info_layout = QHBoxLayout(self.info_box)
        self.info_layout.setSpacing(40)
        self.info_layout.setContentsMargins(40, 30, 40, 30)

        # --- LATO SINISTRO (Info Utente) ---
        self.layout_sinistra = QVBoxLayout()

        self.lbl_titolo_info = QLabel("I TUOI DATI")
        self.lbl_titolo_info.setObjectName("Sottotitolo")
        self.layout_sinistra.addWidget(self.lbl_titolo_info)
        self.layout_sinistra.addSpacing(10)

        self.lbl_nome = QLabel("Nome: ")
        self.lbl_cognome = QLabel("Cognome: ")
        self.lbl_email = QLabel("Email: ")
        self.lbl_telefono = QLabel("Telefono: ")

        for lbl in [self.lbl_nome, self.lbl_cognome, self.lbl_email, self.lbl_telefono]:
            lbl.setStyleSheet("font-size: 16px; color: #333; background-color: transparent;")
            self.layout_sinistra.addWidget(lbl)
            self.layout_sinistra.addSpacing(5)

        # Spinge tutto verso l'alto senza schiacciare le label
        self.layout_sinistra.addStretch()

        # --- LATO DESTRO (Metodi di Pagamento) ---
        self.layout_destra = QVBoxLayout()

        self.lbl_titolo_pagamenti = QLabel("METODI DI PAGAMENTO")
        self.lbl_titolo_pagamenti.setObjectName("Sottotitolo")
        self.layout_destra.addWidget(self.lbl_titolo_pagamenti)
        self.layout_destra.addSpacing(10)

        self.layout_lista_pagamenti = QVBoxLayout()
        self.layout_lista_pagamenti.setSpacing(8)
        self.layout_destra.addLayout(self.layout_lista_pagamenti)

        # Spinge tutto verso l'alto
        self.layout_destra.addStretch()

        # Aggiungiamo le due colonne senza forzare lo stretch
        self.info_layout.addLayout(self.layout_sinistra)
        self.info_layout.addLayout(self.layout_destra)

        self.main_layout.addWidget(self.info_box, alignment=Qt.AlignmentFlag.AlignCenter)

        # --- PULSANTI DI NAVIGAZIONE ---
        self.btn_ordini = QPushButton("I miei ordini")
        self.btn_modifica_credenziali = QPushButton("Modifica credenziali")
        self.btn_aggiungi_pagamento = QPushButton("Aggiungi metodo di pagamento")
        self.btn_indietro = QPushButton("Torna alla Dashboard")

        for btn in [self.btn_ordini, self.btn_modifica_credenziali, self.btn_aggiungi_pagamento, self.btn_indietro]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedSize(250, 45)
            self.main_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

    def applica_stili(self):
        self.setStyleSheet("""
            ProfiloView {
                background-color: white;
                font-family: Arial, sans-serif;
            }
            QLabel {
                background-color: transparent;
            }
            #Titolo {
                font-size: 26px;
                font-weight: bold;
                color: #1a365d;
            }
            #Sottotitolo {
                font-size: 16px;
                font-weight: bold;
                color: #1a365d;
            }
            #InfoBox {
                border: 2px solid #1a365d;
                border-radius: 12px;
                background-color: #f8f9fa;
            }
            QPushButton {
                background-color: #132a4a;
                color: white;
                font-weight: bold;
                font-size: 15px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2a528a;
            }
        """)

    def connetti_segnali(self):
        self.btn_ordini.clicked.connect(self.vai_a_ordini)
        self.btn_modifica_credenziali.clicked.connect(self.vai_a_modifica)
        self.btn_aggiungi_pagamento.clicked.connect(self.vai_a_aggiungi_pagamento)
        self.btn_indietro.clicked.connect(self.torna_indietro)

    def aggiorna_dati(self):
        utente = None
        if self.gestore_utenti and hasattr(self.gestore_utenti, 'utente_corrente'):
            utente = self.gestore_utenti.utente_corrente

        if utente:
            nome = str(getattr(utente, 'nome', getattr(utente, '_nome', ''))).strip().title()
            cognome = str(getattr(utente, 'cognome', getattr(utente, '_cognome', ''))).strip().title()
            email = getattr(utente, 'email', getattr(utente, '_email', ''))
            telefono = getattr(utente, 'telefono', getattr(utente, '_telefono', 'Non inserito'))

            self.lbl_nome.setText(f"<b>Nome:</b> {nome}")
            self.lbl_cognome.setText(f"<b>Cognome:</b> {cognome}")
            self.lbl_email.setText(f"<b>Email:</b> {email}")
            self.lbl_telefono.setText(f"<b>Telefono:</b> {telefono}")

            while self.layout_lista_pagamenti.count():
                child = self.layout_lista_pagamenti.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            metodi = getattr(utente, 'metodi_pagamento', getattr(utente, '_metodi_pagamento', []))

            if not metodi:
                lbl_vuoto = QLabel("Nessun metodo registrato.")
                lbl_vuoto.setStyleSheet("font-style: italic; color: #666; font-size: 15px;")
                self.layout_lista_pagamenti.addWidget(lbl_vuoto)
            else:
                for metodo in metodi:
                    if isinstance(metodo, str):
                        nome_metodo = metodo
                    else:
                        nome_metodo = getattr(metodo, 'nome', getattr(metodo, '_nome', None))
                        if not nome_metodo:
                            nome_metodo = metodo.__class__.__name__ if hasattr(metodo, '__class__') else str(metodo)

                    lbl_metodo = QLabel(f"• {nome_metodo}")
                    lbl_metodo.setStyleSheet("font-size: 15px; color: #333;")
                    self.layout_lista_pagamenti.addWidget(lbl_metodo)

    def vai_a_ordini(self):
        if self.main_window and hasattr(self.main_window, 'mostra_miei_ordini'):
            self.main_window.mostra_miei_ordini()

    def vai_a_modifica(self):
        if self.main_window and hasattr(self.main_window, 'mostra_modifica_credenziali'):
            self.main_window.mostra_modifica_credenziali()

    def vai_a_aggiungi_pagamento(self):
        if self.main_window and hasattr(self.main_window, 'mostra_aggiungi_pagamento'):
            self.main_window.mostra_aggiungi_pagamento()
        else:
            print("WIP: Metodo mostra_aggiungi_pagamento non ancora gestito dalla MainWindow")

    def torna_indietro(self):
        if self.main_window and hasattr(self.main_window, 'mostra_dashboard_cliente'):
            self.main_window.mostra_dashboard_cliente()