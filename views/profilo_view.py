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
        self.main_layout.setSpacing(20)

        self.lbl_titolo = QLabel("IL MIO PROFILO")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setObjectName("Titolo")
        self.main_layout.addWidget(self.lbl_titolo)

        self.frame_info = QFrame()
        self.frame_info.setObjectName("FrameInfo")

        self.layout_info = QHBoxLayout(self.frame_info)
        self.layout_info.setContentsMargins(40, 40, 40, 40)
        self.layout_info.setSpacing(50)

        self.layout_dati = QVBoxLayout()
        self.layout_dati.setSpacing(15)

        self.lbl_titolo_dati = QLabel("DATI ANAGRAFICI")
        self.lbl_titolo_dati.setObjectName("TitoloSezione")
        self.layout_dati.addWidget(self.lbl_titolo_dati)

        self.lbl_nome = QLabel("<b>Nome:</b> -")
        self.lbl_nome.setWordWrap(True)
        self.lbl_cognome = QLabel("<b>Cognome:</b> -")
        self.lbl_cognome.setWordWrap(True)
        self.lbl_email = QLabel("<b>Email:</b> -")
        self.lbl_email.setWordWrap(True)
        self.lbl_telefono = QLabel("<b>Telefono:</b> -")
        self.lbl_telefono.setWordWrap(True)

        self.layout_dati.addWidget(self.lbl_nome)
        self.layout_dati.addWidget(self.lbl_cognome)
        self.layout_dati.addWidget(self.lbl_email)
        self.layout_dati.addWidget(self.lbl_telefono)

        self.layout_dati.addStretch()

        self.layout_info.addLayout(self.layout_dati, stretch=1)

        self.layout_pagamenti = QVBoxLayout()
        self.layout_pagamenti.setSpacing(15)

        self.lbl_titolo_pagamenti = QLabel("METODI DI PAGAMENTO")
        self.lbl_titolo_pagamenti.setObjectName("TitoloSezione")
        self.layout_pagamenti.addWidget(self.lbl_titolo_pagamenti)

        self.layout_lista_pagamenti = QVBoxLayout()
        self.layout_lista_pagamenti.setSpacing(10)
        self.layout_pagamenti.addLayout(self.layout_lista_pagamenti)

        self.layout_pagamenti.addStretch()

        self.layout_info.addLayout(self.layout_pagamenti, stretch=1)

        self.main_layout.addWidget(self.frame_info)

        self.layout_pulsanti = QVBoxLayout()
        self.layout_pulsanti.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_pulsanti.setSpacing(15)

        self.btn_ordini = QPushButton("I miei ordini")
        self.btn_ordini.setFixedSize(300, 45)

        self.btn_modifica_credenziali = QPushButton("Modifica credenziali")
        self.btn_modifica_credenziali.setFixedSize(300, 45)

        self.btn_aggiungi_pagamento = QPushButton("Aggiungi metodo di pagamento")
        self.btn_aggiungi_pagamento.setFixedSize(300, 45)

        self.btn_indietro = QPushButton("Torna alla Dashboard")
        self.btn_indietro.setFixedSize(300, 45)

        for btn in [self.btn_ordini, self.btn_modifica_credenziali, self.btn_aggiungi_pagamento, self.btn_indietro]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            self.layout_pulsanti.addWidget(btn)

        self.main_layout.addLayout(self.layout_pulsanti)

    def applica_stili(self):
        self.setStyleSheet("""
            ProfiloView { background-color: white; font-family: Arial, sans-serif; }
            #Titolo { font-size: 28px; font-weight: bold; color: #1a365d; margin-bottom: 10px; }
            #FrameInfo { 
                border: 2px solid #1a365d; 
                border-radius: 12px; 
                background-color: #ffffff; 
                min-width: 800px;
                min-height: 250px;
            }
            #TitoloSezione { font-size: 16px; font-weight: bold; color: #1a365d; }
            QLabel { font-size: 15px; color: #333; }
            QPushButton { 
                background-color: #1a365d; 
                color: white; 
                font-weight: bold; 
                font-size: 14px; 
                border-radius: 8px; 
            }
            QPushButton:hover { background-color: #2a528a; }
        """)

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_indietro)
        self.btn_modifica_credenziali.clicked.connect(self.vai_a_modifica_credenziali)
        self.btn_aggiungi_pagamento.clicked.connect(self.vai_a_aggiungi_pagamento)
        self.btn_ordini.clicked.connect(self.vai_a_ordini)

    def aggiorna_dati(self):
        utente = getattr(self.gestore_utenti, 'utente_corrente', None)

        if not utente:
            return

        self.lbl_nome.setText(f"<b>Nome:</b> {getattr(utente, 'nome', '-')}")
        self.lbl_cognome.setText(f"<b>Cognome:</b> {getattr(utente, 'cognome', '-')}")
        self.lbl_email.setText(f"<b>Email:</b> {getattr(utente, 'email', '-')}")

        telefono = getattr(utente, 'telefono', getattr(utente, 'numero_telefono', getattr(utente, '_telefono', '-')))
        self.lbl_telefono.setText(f"<b>Telefono:</b> {telefono}")

        while self.layout_lista_pagamenti.count():
            child = self.layout_lista_pagamenti.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        metodi = getattr(utente, 'metodi_pagamento', getattr(utente, '_metodi_pagamento', []))

        if metodi:
            for metodo in metodi:
                testo_metodo = metodo if isinstance(metodo, str) else getattr(metodo, 'nome', str(metodo))
                lbl_metodo = QLabel(f"• {testo_metodo}")
                lbl_metodo.setWordWrap(True)
                self.layout_lista_pagamenti.addWidget(lbl_metodo)
        else:
            lbl_vuoto = QLabel("Nessun metodo registrato.")
            lbl_vuoto.setStyleSheet("color: #777; font-style: italic;")
            self.layout_lista_pagamenti.addWidget(lbl_vuoto)

    def torna_indietro(self):
        if self.main_window and hasattr(self.main_window, 'mostra_dashboard_cliente'):
            self.main_window.mostra_dashboard_cliente()

    def vai_a_modifica_credenziali(self):
        if self.main_window and hasattr(self.main_window, 'mostra_modifica_credenziali'):
            self.main_window.mostra_modifica_credenziali()

    def vai_a_aggiungi_pagamento(self):
        if self.main_window and hasattr(self.main_window, 'mostra_aggiungi_pagamento'):
            self.main_window.mostra_aggiungi_pagamento()

    def vai_a_ordini(self):
        if self.main_window and hasattr(self.main_window, 'mostra_miei_ordini'):
            self.main_window.mostra_miei_ordini()