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
        self.btn_indietro = QPushButton("Torna alla Dashboard")
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

        # 1. CORREZIONE: Usiamo l'attributo reale del tuo Cliente
        storico = getattr(utente, 'ordini', getattr(utente, '_ordini', []))

        if not storico:
            lbl_vuoto = QLabel("Non hai ancora effettuato nessun ordine.")
            lbl_vuoto.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_vuoto.setStyleSheet("font-size: 16px; color: #666; margin-top: 20px;")
            self.layout_ordini.addWidget(lbl_vuoto)
            return

        # Cicliamo gli ordini invertendoli (per mostrare prima i più recenti)
        for ordine in reversed(storico):
            # 2. CORREZIONE: Utilizziamo le property e gli attributi esatti del tuo Ordine
            id_ordine = ordine.id_ordine

            # Estraiamo la data formattata
            data_obj = getattr(ordine, '_data', None)
            data_ordine = data_obj.strftime('%d/%m/%Y %H:%M') if data_obj else "Data Sconosciuta"

            # Gestione sicura dell'Enum StatoOrdine
            stato_enum = ordine.stato
            stato = stato_enum.name.replace("_", " ") if hasattr(stato_enum, 'name') else str(stato_enum)

            totale = ordine.prezzo_totale
            lista_prodotti = ordine.prodotti

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

            # Colori dinamici in base allo stato
            if "COMPLETATO" in stato.upper():
                lbl_stato.setStyleSheet("color: #5cb85c; font-weight: bold;")
            elif "RIMBORSO" in stato.upper() or "ANNULLATO" in stato.upper():
                lbl_stato.setStyleSheet("color: #6c757d; font-weight: bold;")

            lbl_totale = QLabel(f"Totale: € {totale:.2f}")
            lbl_totale.setProperty("class", "TotaleOrdine")

            # Creiamo l'elenco puntato dei prodotti
            testo_prodotti = "Prodotti acquistati:\n"
            for item in lista_prodotti:
                # 3. CORREZIONE: Navighiamo dentro ProdottoOrdine per estrarre Prodotto
                prodotto_reale = item.prodotto
                nome = prodotto_reale.nome
                prezzo = prodotto_reale.prezzo
                qta = item.quantita
                testo_prodotti += f"  • {qta}x {nome} (€ {prezzo:.2f} cad.)\n"

            lbl_prodotti = QLabel(testo_prodotti.strip())
            lbl_prodotti.setProperty("class", "ProdottiLista")

            lay_info.addWidget(lbl_titolo_ordine)
            lay_info.addWidget(lbl_data)
            lay_info.addWidget(lbl_stato)
            lay_info.addWidget(lbl_totale)
            lay_info.addWidget(lbl_prodotti)

            # --- PARTE DESTRA: Pulsante Modifica ---
            lay_azione = QVBoxLayout()
            lay_azione.setAlignment(Qt.AlignmentFlag.AlignCenter)

            btn_modifica = QPushButton("Opzioni Ordine")
            btn_modifica.setObjectName("BtnModifica")
            btn_modifica.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_modifica.setFixedSize(130, 40)

            btn_modifica.clicked.connect(lambda checked, o=ordine: self.vai_a_modifica_ordine(o))

            # Se è già in fase di rimborso, disabilitiamo l'interazione
            if "RIMBORSO" in stato.upper() or "ANNULLATO" in stato.upper():
                btn_modifica.setEnabled(False)
                btn_modifica.setStyleSheet("background-color: #cccccc; color: #666666; border-radius: 6px;")

            lay_azione.addWidget(btn_modifica)

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
        if self.main_window and hasattr(self.main_window, 'mostra_dashboard_cliente'):
            self.main_window.mostra_dashboard_cliente()