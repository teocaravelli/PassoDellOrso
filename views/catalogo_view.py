from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                             QLabel, QPushButton, QFrame, QMessageBox, QScrollArea)
from PyQt6.QtCore import Qt


class CatalogoView(QWidget):
    def __init__(self, gestore_prodotti, main_window=None):
        super().__init__()
        self.gestore_prodotti = gestore_prodotti
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(20)

        # ==========================================
        # HEADER: Indietro | Titolo | Carrello
        # ==========================================
        self.header_layout = QHBoxLayout()

        # Bottone Indietro (Sinistra)
        self.btn_indietro = QPushButton("◄ Torna alla Dashboard")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_indietro.setFixedSize(180, 40)
        self.btn_indietro.setObjectName("BtnAzione")
        self.header_layout.addWidget(self.btn_indietro)

        self.header_layout.addStretch()

        # Titolo (Centro)
        self.lbl_titolo = QLabel("CATALOGO PRODOTTI")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setStyleSheet("font-size: 24px; font-weight: bold; color: #1a365d; background-color: white;")
        self.header_layout.addWidget(self.lbl_titolo)

        self.header_layout.addStretch()

        # Bottone Carrello (Destra)
        self.btn_carrello = QPushButton("Carrello (0)")
        self.btn_carrello.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_carrello.setFixedSize(180, 40)
        self.btn_carrello.setObjectName("BtnAzione")
        self.header_layout.addWidget(self.btn_carrello)

        self.main_layout.addLayout(self.header_layout)

        # ==========================================
        # AREA PRODOTTI (GRIGLIA)
        # ==========================================
        # Aggiungiamo un'area di scorrimento nel caso i prodotti siano tanti
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("border: none; background-color: white;")

        self.container_griglia = QWidget()
        self.grid_layout = QGridLayout(self.container_griglia)
        self.grid_layout.setSpacing(20)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)

        self.scroll_area.setWidget(self.container_griglia)
        self.main_layout.addWidget(self.scroll_area)

    def applica_stili(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
            }
            QScrollArea QWidget {
                background-color: white;
            }
            #BtnAzione {
                background-color: #132a4a;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 8px;
            }
            #BtnAzione:hover {
                background-color: #2a528a;
            }
        """)

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_indietro)
        self.btn_carrello.clicked.connect(self.vai_a_carrello)

    def aggiorna_dati(self):
        # 1. Aggiorna il contatore del carrello in alto a destra
        if self.main_window and hasattr(self.main_window, 'gestore_utenti'):
            gestore_utenti = self.main_window.gestore_utenti
            utente = getattr(gestore_utenti, 'utente_loggato', None)
            if not utente and hasattr(gestore_utenti, 'get_utente_loggato'):
                utente = gestore_utenti.get_utente_loggato()

            if utente:
                carrello = getattr(utente, 'prodotti_carrello', getattr(utente, '_prodotti_carrello', []))
                tot_prodotti = sum(item.quantita for item in carrello) if carrello else 0
                self.btn_carrello.setText(f"Carrello ({tot_prodotti})")

        try:
            # 2. Pulisci la griglia precedente
            while self.grid_layout.count():
                child = self.grid_layout.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # 3. Inizializza e recupera i prodotti
            prodotti = []
            if self.gestore_prodotti:
                if hasattr(self.gestore_prodotti, 'get_tutti_prodotti'):
                    prodotti = self.gestore_prodotti.get_tutti_prodotti()
                elif hasattr(self.gestore_prodotti, 'visualizzaProdotti'):
                    prodotti = self.gestore_prodotti.visualizzaProdotti()
                elif hasattr(self.gestore_prodotti, '_prodotti'):
                    prodotti = self.gestore_prodotti._prodotti

            # 4. Fallback se il database è vuoto
            if not prodotti:
                prodotti = [{"nome": "Errore - DB Vuoto", "prezzo": "0.00", "desc": "Nessun prodotto nel sistema."}]

            # 5. Genera le schede prodotto a schermo
            riga = 0
            colonna = 0
            max_colonne = 3  # 3 prodotti per riga

            for p in prodotti:
                nome = p.get('nome') if isinstance(p, dict) else getattr(p, 'nome', getattr(p, '_nome', 'Prodotto'))
                prezzo = p.get('prezzo') if isinstance(p, dict) else getattr(p, 'prezzo', getattr(p, '_prezzo', '0.00'))

                card = self.crea_card_prodotto(nome, prezzo, p)
                self.grid_layout.addWidget(card, riga, colonna)

                colonna += 1
                if colonna >= max_colonne:
                    colonna = 0
                    riga += 1

        except Exception as e:
            import traceback
            print("\n" + "=" * 50)
            print("❌ ERRORE TROVATO IN CATALOGO_VIEW:")
            traceback.print_exc()
            print("=" * 50 + "\n")

    def crea_card_prodotto(self, nome, prezzo, prodotto_ref):
        """Crea il widget visuale per un singolo prodotto con stili forzati."""
        card = QFrame()
        card.setFixedSize(220, 250)
        card.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 2px solid #add8e6;
                border-radius: 10px;
            }
        """)
        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Immagine segnaposto
        lbl_img = QLabel("🏂")
        lbl_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_img.setStyleSheet(
            "font-size: 50px; background-color: #add8e6; border-radius: 10px; padding: 20px; border: none;")
        layout.addWidget(lbl_img)

        # Nome
        lbl_nome = QLabel(str(nome))
        lbl_nome.setWordWrap(True)
        lbl_nome.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_nome.setStyleSheet("font-size: 16px; font-weight: bold; color: #1a365d; border: none;")
        layout.addWidget(lbl_nome)

        # Prezzo
        lbl_prezzo = QLabel(f"{prezzo} €")
        lbl_prezzo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_prezzo.setStyleSheet("font-size: 16px; color: #d9534f; font-weight: bold; border: none;")
        layout.addWidget(lbl_prezzo)

        layout.addSpacing(10)

        # Bottone dettagli
        btn_dettagli = QPushButton("Vedi Dettagli")
        btn_dettagli.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_dettagli.setStyleSheet("""
            QPushButton {
                background-color: #1a365d;
                color: white;
                font-weight: bold;
                font-size: 14px;
                border-radius: 5px;
                padding: 8px;
                border: none;
            }
            QPushButton:hover {
                background-color: #2a528a;
            }
        """)

        # Gestione sicura del click se prodotto_ref è un dizionario (fallback) o un oggetto vero
        if not isinstance(prodotto_ref, dict):
            btn_dettagli.clicked.connect(lambda checked, p=prodotto_ref: self.apri_dettaglio(p))
        else:
            btn_dettagli.setEnabled(False)
            btn_dettagli.setText("Non disponibile")

        layout.addWidget(btn_dettagli)

        return card

    def apri_dettaglio(self, prodotto):
        if self.main_window and hasattr(self.main_window, 'mostra_dettaglio_prodotto'):
            self.main_window.mostra_dettaglio_prodotto(prodotto)
        else:
            QMessageBox.information(self, "Dettaglio", f"Apertura dettaglio per: {getattr(prodotto, 'nome', '')}")

    def torna_indietro(self):
        if self.main_window:
            # Tenta le varie combinazioni di nome che potresti aver usato nel tuo main_window
            if hasattr(self.main_window, 'mostra_dashboard_cliente'):
                self.main_window.mostra_dashboard_cliente()
            elif hasattr(self.main_window, 'mostra_dashboard'):
                self.main_window.mostra_dashboard()
            elif hasattr(self.main_window, 'mostra_home'):
                self.main_window.mostra_home()
            else:
                QMessageBox.warning(self, "Errore", "Metodo per tornare alla dashboard non trovato nel main.py")

    def vai_a_carrello(self):
        if self.main_window and hasattr(self.main_window, 'mostra_carrello'):
            self.main_window.mostra_carrello()