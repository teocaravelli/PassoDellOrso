from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt


class CatalogoView(QWidget):
    def __init__(self, gestore_utenti, gestore_prodotti, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.gestore_prodotti = gestore_prodotti
        self.main_window = main_window
        self.prodotti = []

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # HEADER
        self.layout_header = QHBoxLayout()

        self.btn_indietro = QPushButton("◀ Torna alla Dashboard")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_indietro.setFixedSize(200, 40)
        self.btn_indietro.setStyleSheet("""
            QPushButton { background-color: #1a365d; color: white; font-weight: bold; font-size: 14px; border: none; border-radius: 6px; }
            QPushButton:hover { background-color: #2a528a; }
        """)

        self.lbl_titolo = QLabel("CATALOGO PRODOTTI")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1a365d; border: none;")

        self.btn_carrello = QPushButton("Carrello")
        self.btn_carrello.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_carrello.setFixedSize(140, 40)
        self.btn_carrello.setStyleSheet("""
            QPushButton { background-color: #1a365d; color: white; font-weight: bold; font-size: 14px; border: none; border-radius: 6px; }
            QPushButton:hover { background-color: #2a528a; }
        """)

        self.layout_header.addWidget(self.btn_indietro)
        self.layout_header.addWidget(self.lbl_titolo, stretch=1)
        self.layout_header.addWidget(self.btn_carrello)

        self.main_layout.addLayout(self.layout_header)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("QScrollArea { border: none; background-color: white; }")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background-color: white;")
        self.grid_layout = QGridLayout(self.scroll_content)
        self.grid_layout.setSpacing(25)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

    def applica_stili(self):
        self.setStyleSheet("CatalogoView { background-color: white; font-family: Arial, sans-serif; }")

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.vai_a_dashboard)
        self.btn_carrello.clicked.connect(self.vai_al_carrello)

    def aggiorna_dati(self):
        self.prodotti = self.gestore_prodotti.get_tutti_prodotti()

        utente = getattr(self.gestore_utenti, 'utente_corrente', None)
        num_carrello = 0

        if utente and hasattr(utente, 'prodotti_carrello'):
            num_carrello = sum(item.quantita for item in utente.prodotti_carrello)

        self.btn_carrello.setText(f"Carrello ({num_carrello})")

        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        riga = 0
        colonna = 0
        max_colonne = 3

        for prodotto in self.prodotti:
            nome = prodotto.nome
            prezzo = prodotto.prezzo
            is_disp = prodotto.is_disponibile
            qta = getattr(prodotto, 'quantita', None)

            card = QFrame()
            card.setObjectName("CardSingola")
            card.setFixedSize(260, 340)
            card.setStyleSheet("""
                QFrame#CardSingola { border: 2px solid #b3d4e6; border-radius: 12px; background-color: white; }
            """)

            lay_card = QVBoxLayout(card)
            lay_card.setContentsMargins(15, 15, 15, 15)
            lay_card.setSpacing(8)

            lbl_img = QLabel("🏂")
            lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_img.setFixedHeight(110)
            lbl_img.setStyleSheet("background-color: #add8e6; border: none; border-radius: 8px; font-size: 45px;")

            if is_disp and (qta is None or qta > 0):
                testo_disp = f"Disponibile ({qta})" if qta is not None else "Disponibile"
                colore_badge = "#5cb85c"
            else:
                testo_disp = "Esaurito (0)" if qta == 0 else "Non Disponibile"
                colore_badge = "#d9534f"

            lbl_disp = QLabel(testo_disp)
            lbl_disp.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_disp.setFixedHeight(24)
            lbl_disp.setStyleSheet(f"""
                color: white; background-color: {colore_badge}; font-weight: bold; 
                border: none; border-radius: 4px; padding: 2px 8px; font-size: 11px;
            """)

            lbl_nome = QLabel(nome)
            lbl_nome.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_nome.setWordWrap(True)
            lbl_nome.setStyleSheet(
                "background: transparent; border: none; font-size: 15px; font-weight: bold; color: #1a365d;")

            lbl_prezzo = QLabel(f"€ {prezzo:.2f}")
            lbl_prezzo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_prezzo.setStyleSheet(
                "background: transparent; border: none; font-size: 16px; font-weight: bold; color: #d9534f;")

            btn_dettagli = QPushButton("Vedi Dettagli")
            btn_dettagli.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_dettagli.setFixedHeight(36)
            btn_dettagli.setStyleSheet("""
                QPushButton { background-color: #1a365d; color: white; font-weight: bold; font-size: 13px; border: none; border-radius: 6px; }
                QPushButton:hover { background-color: #2a528a; }
            """)
            btn_dettagli.clicked.connect(lambda checked, p=prodotto: self.apri_prodotto(p))

            lay_card.addWidget(lbl_img)
            lay_card.addWidget(lbl_disp, alignment=Qt.AlignmentFlag.AlignCenter)
            lay_card.addWidget(lbl_nome, stretch=1)
            lay_card.addWidget(lbl_prezzo)
            lay_card.addWidget(btn_dettagli)

            self.grid_layout.addWidget(card, riga, colonna)

            colonna += 1
            if colonna >= max_colonne:
                colonna = 0
                riga += 1

    def apri_prodotto(self, prodotto):
        if self.main_window and hasattr(self.main_window, 'mostra_singolo_prodotto'):
            self.main_window.mostra_singolo_prodotto(prodotto)

    def vai_a_dashboard(self):
        if self.main_window:
            if hasattr(self.main_window, 'mostra_dashboard_cliente'):
                self.main_window.mostra_dashboard_cliente()
            elif hasattr(self.main_window, 'mostra_dashboard'):
                self.main_window.mostra_dashboard()

    def vai_al_carrello(self):
        if self.main_window and hasattr(self.main_window, 'mostra_carrello'):
            self.main_window.mostra_carrello()