
import sys
import traceback

# Aggiungi questa funzione per catturare i crash silenziosi di PyQt6
def cattura_errori(tipo_eccezione, valore_eccezione, traceback_eccezione):
    print("\n" + "!"*50)
    print("ERRORE FATALE TROVATO:")
    traceback.print_exception(tipo_eccezione, valore_eccezione, traceback_eccezione)
    print("!"*50 + "\n")
    sys.exit(1)

sys.excepthook = cattura_errori
from PyQt6.QtWidgets import QApplication
from controllers.gestore_utenti import GestoreUtenti
from controllers.gestore_mail import GestoreMail
from controllers.gestore_prodotti import GestoreProdotti
from controllers.gestore_ordini import GestoreOrdini
from controllers.gestore_piste import GestorePiste
from views.main_window import MainWindow

def main() -> int:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet("""
            QWidget {
                background-color: white;
                color: black;
                font-family: Arial, sans-serif;
            }
        """)
    gestore_mail = GestoreMail()
    gestore_utenti = GestoreUtenti(gestore_mail)
    gestore_prodotti = GestoreProdotti()
    gestore_ordini = GestoreOrdini(gestore_mail, gestore_prodotti)
    gestore_piste = GestorePiste()
    window = MainWindow(gestore_utenti, gestore_ordini, gestore_prodotti, gestore_piste)
    window.show()
    return app.exec()

if __name__ == "__main__":
    raise SystemExit(main())