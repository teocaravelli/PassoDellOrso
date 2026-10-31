from PyQt6.QtWidgets import QMainWindow, QStackedWidget

from views.catalogo_view import CatalogoView
from views.dashboard_cliente_view import DashboardClienteView
from views.login_view import LoginView
from views.profilo_view import ProfiloView
from views.registrazione_view import RegistrazioneView
from views.dipendente_dashboard_view import DipendenteDashboardView
from views.ordini_dipendente_view import OrdiniDipendenteView
from views.gestione_piste_view import GestionePisteView
from views.inserimento_dipendente_view import InserimentoDipendenteView
from views.gestione_inventario_view import GestioneInventarioView
from views.nuovo_prodotto_view import NuovoProdottoView

class MainWindow(QMainWindow):
    def __init__(self, gestore_utenti, gestore_ordini, gestore_prodotti, gestore_piste):
        super().__init__()

        # Salviamo i controller per poterli passare alle future schermate
        self.gestore_utenti = gestore_utenti
        self.gestore_ordini = gestore_ordini
        self.gestore_prodotti = gestore_prodotti
        self.gestore_piste = gestore_piste

        # Configurazione base della finestra
        self.setWindowTitle("Passo dell'Orso - Ski Resort")
        self.setMinimumSize(900, 600)

        # Inizializziamo il contenitore a strati
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.inizializza_viste()

    def inizializza_viste(self):
        """Istanzia tutte le schermate e le aggiunge allo stack."""
        # Creiamo le view passando il controller necessario e 'self' come main_window
        self.login_view = LoginView(self.gestore_utenti, main_window=self)
        self.registrazione_view = RegistrazioneView(self.gestore_utenti, main_window=self)
        self.dipendente_dashboard_view = DipendenteDashboardView(self.gestore_utenti, self.gestore_ordini, self.gestore_piste, main_window=self)
        self.ordini_dipendente_view = OrdiniDipendenteView(self.gestore_ordini, self.gestore_utenti, main_window=self)
        self.gestione_piste_view = GestionePisteView(self.gestore_piste, main_window=self)
        self.inserimento_dipendente_view = InserimentoDipendenteView(self.gestore_utenti, main_window=self)
        self.dashboard_cliente_view = DashboardClienteView(self.gestore_utenti, self.gestore_piste, main_window=self)
        self.catalogo_view = CatalogoView(self.gestore_prodotti, main_window=self)
        self.profilo_view = ProfiloView(self.gestore_utenti, main_window=self)
        self.gestione_inventario_view = GestioneInventarioView(self.gestore_prodotti, main_window=self)
        self.nuovo_prodotto_view = NuovoProdottoView(self.gestore_prodotti, main_window=self)

        # Aggiungiamo le view al QStackedWidget
        self.stacked_widget.addWidget(self.login_view)  # Indice 0
        self.stacked_widget.addWidget(self.registrazione_view)  # Indice 1
        self.stacked_widget.addWidget(self.dipendente_dashboard_view)
        self.stacked_widget.addWidget(self.ordini_dipendente_view)
        self.stacked_widget.addWidget(self.gestione_piste_view)
        self.stacked_widget.addWidget(self.inserimento_dipendente_view)
        self.stacked_widget.addWidget(self.dashboard_cliente_view)
        self.stacked_widget.addWidget(self.catalogo_view)
        self.stacked_widget.addWidget(self.profilo_view)
        self.stacked_widget.addWidget(self.gestione_inventario_view)
        self.stacked_widget.addWidget(self.nuovo_prodotto_view)

        # Impostiamo la schermata iniziale da mostrare all'avvio
        self.mostra_login()

    def mostra_login(self):
        self.stacked_widget.setCurrentWidget(self.login_view)

    def mostra_registrazione(self):
        self.stacked_widget.setCurrentWidget(self.registrazione_view)

    def mostra_area_dipendente(self):
        self.dipendente_dashboard_view.aggiorna_vista()
        self.stacked_widget.setCurrentWidget(self.dipendente_dashboard_view)

    def mostra_gestione_ordini(self):
        self.ordini_dipendente_view.aggiorna_vista()
        self.stacked_widget.setCurrentWidget(self.ordini_dipendente_view)

    def mostra_area_gestione_piste(self):
        self.gestione_piste_view.aggiorna_vista()
        self.stacked_widget.setCurrentWidget(self.gestione_piste_view)

    def mostra_inserimento_dipendente(self):
        self.stacked_widget.setCurrentWidget(self.inserimento_dipendente_view)

    def mostra_dashboard_cliente(self):
        self.dashboard_cliente_view.aggiorna_dati()
        self.stacked_widget.setCurrentWidget(self.dashboard_cliente_view)

    def mostra_profilo(self):
        self.profilo_view.aggiorna_dati()
        self.stacked_widget.setCurrentWidget(self.profilo_view)

    def mostra_prodotti(self):
        self.catalogo_view.aggiorna_dati()
        self.stacked_widget.setCurrentWidget(self.catalogo_view)

    def mostra_gestione_inventario(self):
        self.gestione_inventario_view.aggiorna_vista()
        self.stacked_widget.setCurrentWidget(self.gestione_inventario_view)

    def mostra_aggiungi_prodotto(self):
        self.stacked_widget.setCurrentWidget(self.nuovo_prodotto_view)


