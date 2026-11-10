from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QLineEdit,
    QMessageBox,
    QFormLayout,
    QComboBox
)
from PyQt6.QtCore import Qt


class AggiungiPagamentoView(QWidget):
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

        self.lbl_titolo = QLabel("AGGIUNGI METODO DI PAGAMENTO")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setObjectName("Titolo")
        self.main_layout.addWidget(self.lbl_titolo)

        self.main_layout.addSpacing(20)

        self.form_frame = QFrame()
        self.form_frame.setObjectName("FormFrame")
        self.form_layout = QFormLayout(self.form_frame)
        self.form_layout.setSpacing(15)
        self.form_layout.setContentsMargins(30, 30, 30, 30)

        self.combo_tipo = QComboBox()
        self.combo_tipo.addItems([
            "Carta di Credito (Visa/Mastercard)",
            "Carta di Debito",
            "American Express",
            "PayPal",
            "Satispay",
            "Apple Pay",
            "Google Pay"
        ])

        self.input_dati = QLineEdit()
        self.input_dati.setPlaceholderText("Numero carta o Email")

        self.input_scadenza = QLineEdit()
        self.input_scadenza.setPlaceholderText("MM/AA (Solo per carte)")

        self.input_cvv = QLineEdit()
        self.input_cvv.setPlaceholderText("CVV (Solo per carte)")
        self.input_cvv.setEchoMode(QLineEdit.EchoMode.Password)

        self.form_layout.addRow(QLabel("Tipologia:"), self.combo_tipo)
        self.form_layout.addRow(QLabel("Dati:"), self.input_dati)
        self.form_layout.addRow(QLabel("Scadenza:"), self.input_scadenza)
        self.form_layout.addRow(QLabel("CVV/CVC:"), self.input_cvv)

        self.main_layout.addWidget(self.form_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addSpacing(20)

        self.layout_pulsanti = QHBoxLayout()
        self.layout_pulsanti.setSpacing(20)

        self.btn_salva = QPushButton("Salva Metodo")
        self.btn_salva.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_annulla = QPushButton("Annulla / Indietro")
        self.btn_annulla.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_annulla.setObjectName("BtnAnnulla")

        self.layout_pulsanti.addWidget(self.btn_salva)
        self.layout_pulsanti.addWidget(self.btn_annulla)

        self.main_layout.addLayout(self.layout_pulsanti)

    def applica_stili(self):
        self.setStyleSheet("""
            AggiungiPagamentoView { background-color: white; font-family: Arial, sans-serif; }
            #Titolo { font-size: 26px; font-weight: bold; color: #1a365d; }
            #FormFrame { border: 2px solid #1a365d; border-radius: 12px; background-color: #f8f9fa; min-width: 450px; }
            QLabel { font-size: 15px; font-weight: bold; color: #333; }
            QLineEdit, QComboBox { padding: 8px; font-size: 14px; border: 1px solid #ccc; border-radius: 5px; background-color: white; }
            QLineEdit:focus, QComboBox:focus { border: 1px solid #1a365d; }
            QPushButton { background-color: #132a4a; color: white; font-weight: bold; font-size: 15px; border-radius: 8px; padding: 12px; min-width: 200px; }
            QPushButton:hover { background-color: #2a528a; }
            #BtnAnnulla { background-color: #6c757d; }
            #BtnAnnulla:hover { background-color: #5a6268; }
        """)

    def connetti_segnali(self):
        self.btn_salva.clicked.connect(self.salva_metodo)
        self.btn_annulla.clicked.connect(self.torna_indietro)

    def aggiorna_dati(self):
        """Pulisce i campi ogni volta che si entra nella pagina."""
        self.combo_tipo.setCurrentIndex(0)
        self.input_dati.clear()
        self.input_scadenza.clear()
        self.input_cvv.clear()

    def salva_metodo(self):
        utente = None
        if self.gestore_utenti and hasattr(self.gestore_utenti, 'utente_corrente'):
            utente = self.gestore_utenti.utente_corrente

        if not utente:
            QMessageBox.warning(self, "Errore", "Devi effettuare l'accesso per aggiungere un metodo di pagamento.")
            return

        tipo = self.combo_tipo.currentText()
        dati = self.input_dati.text().strip()

        if not dati:
            QMessageBox.warning(self, "Errore", "Il campo 'Dati' è obbligatorio.")
            return

        metodi_digitali = ["PayPal", "Satispay", "Apple Pay", "Google Pay"]

        if tipo in metodi_digitali:
            nuovo_metodo_str = f"{tipo} - {dati}"
        else:
            ultimi_numeri = dati[-4:] if len(dati) >= 4 else dati
            nuovo_metodo_str = f"{tipo} - **** {ultimi_numeri}"

        if hasattr(utente, 'aggiungi_metodo_pagamento'):
            utente.aggiungi_metodo_pagamento(nuovo_metodo_str)
        else:
            if not hasattr(utente, '_metodi_pagamento'):
                utente._metodi_pagamento = []
            utente._metodi_pagamento.append(nuovo_metodo_str)

        if hasattr(self.gestore_utenti, '_salva_dati'):
            self.gestore_utenti._salva_dati()
        elif hasattr(self.gestore_utenti, 'salva_dati'):
            self.gestore_utenti.salva_dati()

        QMessageBox.information(self, "Successo", "Metodo di pagamento aggiunto con successo!")
        self.torna_indietro()

    def torna_indietro(self):
        if self.main_window and hasattr(self.main_window, 'mostra_profilo'):
            self.main_window.mostra_profilo()