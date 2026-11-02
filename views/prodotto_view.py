from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QMessageBox, QSpinBox
)
from PyQt6.QtCore import Qt


class ProdottoView(QWidget):
    # 1. MODIFICA: Aggiunto gestore_prodotti al costruttore
    def __init__(self, gestore_utenti, gestore_prodotti, main_window=None):
        super().__init__()
        self.gestore_utenti = gestore_utenti
        self.gestore_prodotti = gestore_prodotti
        self.main_window = main_window
        self.prodotto_corrente = None

        self.setup_ui()
        self.connetti_segnali()
        self.applica_stili()

    def setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.main_layout.setSpacing(15)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.frame_main = QFrame()
        self.frame_main.setObjectName("FrameMain")
        self.frame_main.setFixedSize(760, 440)

        self.layout_frame = QHBoxLayout(self.frame_main)
        self.layout_frame.setContentsMargins(30, 30, 30, 30)
        self.layout_frame.setSpacing(30)

        self.lbl_immagine = QLabel("🏂")
        self.lbl_immagine.setObjectName("ImgBox")
        self.lbl_immagine.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_immagine.setFixedSize(200, 200)
        self.layout_frame.addWidget(self.lbl_immagine, alignment=Qt.AlignmentFlag.AlignTop)

        self.layout_dettagli = QVBoxLayout()
        self.layout_dettagli.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.layout_dettagli.setSpacing(6)

        self.lbl_nome = QLabel("Nome Prodotto")
        self.lbl_nome.setObjectName("LblNome")
        self.lbl_nome.setWordWrap(True)

        self.lbl_prezzo = QLabel("€ 0.00")
        self.lbl_prezzo.setObjectName("LblPrezzo")

        self.lbl_disponibilita = QLabel("")
        self.lbl_disponibilita.setObjectName("LblDisp")

        self.lbl_descrizione = QLabel("Descrizione...")
        self.lbl_descrizione.setObjectName("LblDesc")
        self.lbl_descrizione.setWordWrap(True)

        self.lbl_info_extra = QLabel("")
        self.lbl_info_extra.setObjectName("LblExtra")
        self.lbl_info_extra.setWordWrap(True)

        self.layout_dettagli.addWidget(self.lbl_nome)
        self.layout_dettagli.addWidget(self.lbl_prezzo)
        self.layout_dettagli.addWidget(self.lbl_disponibilita)
        self.layout_dettagli.addWidget(self.lbl_descrizione)
        self.layout_dettagli.addWidget(self.lbl_info_extra)

        self.layout_dettagli.addSpacing(10)

        self.layout_azioni = QHBoxLayout()
        self.layout_azioni.setSpacing(10)

        self.lbl_qta = QLabel("Quantità:")
        self.lbl_qta.setObjectName("LblQta")

        self.spin_qta = QSpinBox()
        self.spin_qta.setObjectName("SpinQta")
        self.spin_qta.setMinimum(1)
        self.spin_qta.setFixedSize(70, 36)

        self.btn_aggiungi = QPushButton("Aggiungi al Carrello")
        self.btn_aggiungi.setObjectName("BtnAggiungi")
        self.btn_aggiungi.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_aggiungi.setFixedSize(180, 38)

        self.layout_azioni.addWidget(self.lbl_qta)
        self.layout_azioni.addWidget(self.spin_qta)
        self.layout_azioni.addWidget(self.btn_aggiungi)
        self.layout_azioni.addStretch()

        self.layout_dettagli.addLayout(self.layout_azioni)
        self.layout_frame.addLayout(self.layout_dettagli, stretch=1)

        self.main_layout.addWidget(self.frame_main, alignment=Qt.AlignmentFlag.AlignCenter)

        self.btn_indietro = QPushButton("Torna al Catalogo")
        self.btn_indietro.setObjectName("BtnIndietro")
        self.btn_indietro.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_indietro.setFixedSize(220, 42)
        self.main_layout.addWidget(self.btn_indietro, alignment=Qt.AlignmentFlag.AlignCenter)

    def applica_stili(self):
        self.setStyleSheet("""
            ProdottoView { background-color: white; font-family: Arial, sans-serif; }
            QFrame#FrameMain { border: 2px solid #1a365d; border-radius: 12px; background-color: #f8fcfd; }
            QLabel { background-color: transparent; border: none; color: #333; }
            QLabel#ImgBox { background-color: #add8e6; border-radius: 10px; font-size: 70px; }
            QLabel#LblNome { font-size: 22px; font-weight: bold; color: #1a365d; }
            QLabel#LblPrezzo { font-size: 18px; font-weight: bold; color: #d9534f; }
            QLabel#LblDesc { font-size: 13px; color: #555; }
            QLabel#LblExtra { font-size: 12px; color: #222; line-height: 130%; }
            QLabel#LblQta { font-size: 13px; font-weight: bold; color: #1a365d; }
            QSpinBox#SpinQta { 
                font-size: 14px; font-weight: bold; padding: 2px; 
                border: 1px solid #1a365d; border-radius: 5px; 
                background-color: white; color: #1a365d;
            }
            QPushButton#BtnAggiungi { background-color: #5cb85c; color: white; font-weight: bold; font-size: 13px; border: none; border-radius: 6px; }
            QPushButton#BtnAggiungi:hover { background-color: #4cae4c; }
            QPushButton#BtnAggiungi:disabled { background-color: #cccccc; color: #666666; }
            QPushButton#BtnIndietro { background-color: #1a365d; color: white; font-weight: bold; font-size: 14px; border: none; border-radius: 6px; }
            QPushButton#BtnIndietro:hover { background-color: #2a528a; }
        """)

    def connetti_segnali(self):
        self.btn_indietro.clicked.connect(self.torna_al_catalogo)
        self.btn_aggiungi.clicked.connect(self.aggiungi_al_carrello)

    def _leggi_valore(self, obj, metodo_uml, possibili_attributi, default=None):
        if hasattr(obj, metodo_uml) and callable(getattr(obj, metodo_uml)):
            return getattr(obj, metodo_uml)()
        for attr in possibili_attributi:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                return val() if callable(val) else val
        if hasattr(obj, '__dict__'):
            for k, v in obj.__dict__.items():
                for attr in possibili_attributi:
                    if k.lower().endswith(attr.lower()):
                        return v
        return default

    def imposta_prodotto(self, prodotto):
        self.prodotto_corrente = prodotto

        id_p = getattr(prodotto, 'id', getattr(prodotto, '_id', 'N/D'))
        nome = getattr(prodotto, 'nome', getattr(prodotto, '_nome', 'Prodotto'))
        prezzo = getattr(prodotto, 'prezzo', getattr(prodotto, '_prezzo', 0.0))
        desc = getattr(prodotto, 'descrizione', getattr(prodotto, '_descrizione', 'Nessuna descrizione.'))
        is_disp = getattr(prodotto, 'is_disponibile', getattr(prodotto, '_is_disponibile', True))

        self.lbl_nome.setText(str(nome))
        self.lbl_prezzo.setText(f"€ {float(prezzo):.2f}")
        self.lbl_descrizione.setText(str(desc))

        ha_quantita = hasattr(prodotto, 'quantita')
        qta_inventario = getattr(prodotto, 'quantita', 0) if ha_quantita else None
        categoria = type(prodotto).__name__

        info_html = f"<b>Info:</b> ID: {id_p} | Categoria: {categoria}"
        if ha_quantita:
            info_html += f" | Magazzino: {qta_inventario}"
        info_html += "<br>"

        brand = self._leggi_valore(prodotto, 'getBrand', ['brand', '_brand'], None)
        if brand: info_html += f"• <b>Brand:</b> {brand} "

        taglia = self._leggi_valore(prodotto, 'getTaglia', ['taglia', '_taglia'], None)
        if taglia: info_html += f"• <b>Taglia:</b> {taglia} "

        tipologia = self._leggi_valore(prodotto, 'getTipologia', ['tipologia', '_tipologia'], None)
        if tipologia:
            val_t = tipologia.name if hasattr(tipologia, 'name') else tipologia
            info_html += f"• <b>Tipologia:</b> {val_t} "

        livello = self._leggi_valore(prodotto, 'getLivello', ['livello', '_livello'], None)
        if livello:
            val_l = livello.name if hasattr(livello, 'name') else livello
            info_html += f"• <b>Livello:</b> {val_l} "

        formula = self._leggi_valore(prodotto, 'getFormulaTemporale', ['formula_temporale', '_formula_temporale'], None)
        if formula:
            val_f = formula.name if hasattr(formula, 'name') else formula
            info_html += f"• <b>Formula:</b> {val_f} "

        d_inizio = self._leggi_valore(prodotto, 'getDataInizio', ['data_inizio', '_data_inizio'], None)
        d_fine = self._leggi_valore(prodotto, 'getDataFine', ['data_fine', '_data_fine'], None)
        if d_inizio and d_fine:
            # 2. MODIFICA: Corretto l'errore di formattazione stringa che mandava in crash la View
            info_html += f"• <b>Validità:</b> {d_inizio} - {d_fine}"

        self.lbl_info_extra.setText(info_html)

        if ha_quantita:
            if is_disp and qta_inventario > 0:
                self.lbl_disponibilita.setText(f"✔ Disponibile (Max acquistabile: {qta_inventario})")
                self.lbl_disponibilita.setStyleSheet("color: #5cb85c; font-weight: bold; font-size: 12px;")
                self.spin_qta.setEnabled(True)
                self.spin_qta.setMinimum(1)
                self.spin_qta.setMaximum(qta_inventario)
                self.spin_qta.setValue(1)
                self.btn_aggiungi.setEnabled(True)
                self.btn_aggiungi.setText("Aggiungi al Carrello")
            else:
                self.lbl_disponibilita.setText("✖ Esaurito")
                self.lbl_disponibilita.setStyleSheet("color: #d9534f; font-weight: bold; font-size: 12px;")
                self.spin_qta.setEnabled(False)
                self.spin_qta.setValue(0)
                self.btn_aggiungi.setEnabled(False)
                self.btn_aggiungi.setText("Esaurito")
        else:
            if is_disp:
                self.lbl_disponibilita.setText("✔ Disponibile")
                self.lbl_disponibilita.setStyleSheet("color: #5cb85c; font-weight: bold; font-size: 12px;")
                self.spin_qta.setEnabled(True)
                self.spin_qta.setMinimum(1)
                self.spin_qta.setMaximum(99)
                self.spin_qta.setValue(1)
                self.btn_aggiungi.setEnabled(True)
                self.btn_aggiungi.setText("Aggiungi al Carrello")
            else:
                self.lbl_disponibilita.setText("✖ Non Disponibile")
                self.lbl_disponibilita.setStyleSheet("color: #d9534f; font-weight: bold; font-size: 12px;")
                self.spin_qta.setEnabled(False)
                self.btn_aggiungi.setEnabled(False)
                self.btn_aggiungi.setText("Non Disponibile")

    # 3. MODIFICA: Logica MVC perfetta. Delega tutto al controller e salva su disco!
    def aggiungi_al_carrello(self):
        utente = getattr(self.gestore_utenti, 'utente_corrente', None)
        if not utente:
            QMessageBox.warning(self, "Errore", "Devi effettuare l'accesso per aggiungere prodotti al carrello.")
            return

        qta_selezionata = self.spin_qta.value()

        try:
            # Chiama il GestoreProdotti che fa tutti i controlli (limiti, scorte, ecc.) e aggiunge l'item
            self.gestore_prodotti.aggiungiProdotto(utente, self.prodotto_corrente, qta_selezionata)

            # Salva l'utente per mantenere il carrello in memoria
            self.gestore_utenti._salva_dati()

            QMessageBox.information(self, "Aggiunto",
                                    f"{qta_selezionata}x '{self.prodotto_corrente.nome}' aggiunto al carrello!")
            self.torna_al_catalogo()

        except ValueError as e:
            # Cattura in automatico eventuali avvisi del controller (es. quantità massima superata)
            QMessageBox.warning(self, "Attenzione", str(e))

    def torna_al_catalogo(self):
        if self.main_window and hasattr(self.main_window, 'mostra_catalogo'):
            self.main_window.mostra_catalogo()