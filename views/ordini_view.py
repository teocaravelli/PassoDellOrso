from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QScrollArea,
    QMessageBox
)
from PyQt6.QtCore import Qt


class OrdiniView(QWidget):
    def __init__(self, gestore_utenti, gestore_ordini, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.gestore_ordini = gestore_ordini
        self.main_window = main_window

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(40, 40, 40, 40)

        # Titolo
        self.lbl_titolo = QLabel("I MIEI ORDINI")
        self.lbl_titolo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_titolo.setObjectName("Titolo")
        self.main_layout.addWidget(self.lbl_titolo)

        # Area di scorrimento per gli ordini
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("ScrollArea")

        self.scroll_content = QWidget()
        self.layout_ordini = QVBoxLayout(self.scroll_content)
        self.layout_ordini.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_ordini.setSpacing(15)

        self.scroll_area.setWidget(self.scroll_content)
        self.main_layout.addWidget(self.scroll_area)

        # Pulsante Indietro
        self.btn_indietro = QPushButton("Torna al Profilo")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_indietro.setFixedSize(250, 45)
        self.btn_indietro.setObjectName("BtnIndietro")
        self.main_layout.addWidget(self.btn_indietro, alignment=Qt.AlignmentFlag.AlignCenter)

    def applica_stili(self):
        self.setStyleSheet("""
            OrdiniView { background-color: white; font-family: Arial, sans-serif; }
            #Titolo { font-size: 26px; font-weight: bold; color: #1a365d; }
            #ScrollArea { border: 1px solid #ccc; border-radius: 8px; background-color: #f8f9fa; }
            .OrdineFrame { background-color: white; border: 2px solid #e0e0e0; border-radius: 8px; padding: 15px; }
            .TitoloOrdine { font-size: 16px; font-weight: bold; color: #1a365d; }
            .InfoOrdine { font-size: 14px; color: #333; }
            .StatoOrdine { font-size: 14px; font-weight: bold; color: #d9534f; }
            .TotaleOrdine { font-size: 16px; font-weight: bold; color: #5cb85c; }
            .ProdottiLista { font-size: 13px; color: #555; }
            QPushButton#BtnModifica { 
                background-color: #d9534f; 
                color: white; 
                font-weight: bold; 
                font-size: 14px; 
                border-radius: 6px; 
                padding: 10px;
            }
            QPushButton#BtnModifica:hover { background-color: #c9302c; }
            QPushButton#BtnIndietro { 
                background-color: #1a365d; 
                color: white; 
                font-weight: bold; 
                font-size: 15px; 
                border-radius: 8px; 
            }
            QPushButton#BtnIndietro:hover { background-color: #2a528a; }
        """)

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_indietro)

    def aggiorna_dati(self):
        # Svuotiamo il layout per ricaricare gli ordini freschi
        while self.layout_ordini.count():
            child = self.layout_ordini.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        utente = getattr(self.gestore_utenti, 'utente_corrente', None)
        if not utente:
            return

        storico = getattr(utente, 'storico_ordini', getattr(utente, '_storico_ordini', []))

        if not storico:
            lbl_vuoto = QLabel("Non hai ancora effettuato nessun ordine.")
            lbl_vuoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_vuoto.setStyleSheet("font-size: 16px; color: #666; margin-top: 20px;")
            self.layout_ordini.addWidget(lbl_vuoto)
            return

        # Cicliamo gli ordini invertendoli (per mostrare prima i più recenti)
        for ordine in reversed(storico):
            id_ordine = getattr(ordine, 'id_ordine', 'Sconosciuto')
            data_ordine = getattr(ordine, 'data', 'Data Sconosciuta')
            stato = getattr(ordine, 'stato', 'IN ELABORAZIONE')
            totale = getattr(ordine, 'totale', 0.0)
            lista_prodotti = getattr(ordine, 'prodotti', [])

            # Creazione della Card dell'ordine
            frame = QFrame()
            frame.setProperty("class", "OrdineFrame")
            lay_card = QHBoxLayout(frame)

            # --- PARTE SINISTRA: Informazioni e Prodotti ---
            lay_info = QVBoxLayout()
            lay_info.setSpacing(5)

            lbl_titolo_ordine = QLabel(f"Ordine #{id_ordine}")
            lbl_titolo_ordine.setProperty("class", "TitoloOrdine")

            lbl_data = QLabel(f"Data: {data_ordine}")
            lbl_data.setProperty("class", "InfoOrdine")

            lbl_stato = QLabel(f"Stato: {stato}")
            lbl_stato.setProperty("class", "StatoOrdine")
            # Cambia colore in base allo stato
            if stato.upper() == "COMPLETATO":
                lbl_stato.setStyleSheet("color: #5cb85c; font-weight: bold;")
            elif stato.upper() == "RESTITUITO" or stato.upper() == "ANNULLATO":
                lbl_stato.setStyleSheet("color: #6c757d; font-weight: bold;")

            lbl_totale = QLabel(f"Totale: € {totale:.2f}")
            lbl_totale.setProperty("class", "TotaleOrdine")

            # Creiamo l'elenco puntato dei prodotti
            testo_prodotti = "Prodotti acquistati:\n"
            for item in lista_prodotti:
                nome = getattr(item, 'nome', getattr(item, '_nome', 'Prodotto'))
                prezzo = getattr(item, 'prezzo', getattr(item, '_prezzo', 0.0))
                qta = getattr(item, 'quantita', getattr(item, '_quantita', 1))
                testo_prodotti += f"  • {qta}x {nome} (€ {prezzo:.2f} cad.)\n"

            lbl_prodotti = QLabel(testo_prodotti.strip())
            lbl_prodotti.setProperty("class", "ProdottiLista")

            # Aggiunta al layout sinistro
            lay_info.addWidget(lbl_titolo_ordine)
            lay_info.addWidget(lbl_data)
            lay_info.addWidget(lbl_stato)
            lay_info.addWidget(lbl_totale)
            lay_info.addWidget(lbl_prodotti)

            # --- PARTE DESTRA: Pulsante Modifica ---
            lay_azione = QVBoxLayout()
            lay_azione.setAlignment(Qt.AlignmentFlag.AlignCenter)

            btn_modifica = QPushButton("Modifica")
            btn_modifica.setObjectName("BtnModifica")
            btn_modifica.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_modifica.setFixedSize(120, 40)

            # Usiamo lambda per passare l'oggetto ordine specifico alla funzione
            btn_modifica.clicked.connect(lambda checked, o=ordine: self.vai_a_modifica_ordine(o))

            # Disabilitiamo il tasto modifica se l'ordine è già stato restituito o annullato (opzionale)
            if stato.upper() in ["RESTITUITO", "ANNULLATO"]:
                btn_modifica.setEnabled(False)
                btn_modifica.setStyleSheet("background-color: #cccccc; color: #666666; border-radius: 6px;")

            lay_azione.addWidget(btn_modifica)

            # Aggiungiamo le due parti alla card
            lay_card.addLayout(lay_info, stretch=3)
            lay_card.addLayout(lay_azione, stretch=1)

            self.layout_ordini.addWidget(frame)

    def vai_a_modifica_ordine(self, ordine):
        """Metodo per navigare alla pagina di modifica dell'ordine selezionato."""
        if self.main_window and hasattr(self.main_window, 'mostra_modifica_ordine'):
            self.main_window.mostra_modifica_ordine(ordine)
        else:
            QMessageBox.warning(self, "In Sviluppo",
                                "La pagina di modifica ordine non è ancora stata creata in MainWindow.")

    def torna_indietro(self):
        if self.main_window and hasattr(self.main_window, 'mostra_profilo'):
            self.main_window.mostra_profilo()