from datetime import date

from controllers.gestore_mail import GestoreMail
from models.enums import Livello, TipologiaAttrezzatura, FormulaTemporale
from models.skipass import SkiPass
from models.attrezzatura import Attrezzatura

# Importa i tuoi controller (assicurati che i percorsi combacino col tuo progetto)
from controllers.gestore_prodotti import GestoreProdotti
from controllers.gestore_utenti import GestoreUtenti


def popola_database():
    gestore_mail = GestoreMail()
    gestore_prodotti = GestoreProdotti()
    gestore_utenti = GestoreUtenti(gestore_mail)

    # ==========================================
    # 1. POPOLAMENTO PRODOTTI
    # ==========================================
    if not gestore_prodotti.get_tutti_prodotti():
        print("Creazione prodotti in corso...")

        p1 = SkiPass(
            id_prodotto=1, nome="Skipass Giornaliero", descrizione="Accesso completo a tutti gli impianti.",
            prezzo=45.0, immagine="", is_disponibile=True,
            formula_temporale=FormulaTemporale.GIORNALIERO
        )

        p2 = Attrezzatura(
            id_prodotto=2, nome="Sci Head V-Shape", descrizione="Sci da discesa pista.",
            prezzo=25.0, immagine="", is_disponibile=True, brand="Head", data=date.today(),
            livello=Livello.INTERMEDIO, quantita=10, taglia="170", tipologia=TipologiaAttrezzatura.SCI
        )

        p3 = Attrezzatura(
            id_prodotto=3, nome="Scarponi Salomon", descrizione="Scarponi calzata comoda.",
            prezzo=15.0, immagine="", is_disponibile=True, brand="Salomon", data=date.today(),
            livello=Livello.PRINCIPIANTE, quantita=25, taglia="42", tipologia=TipologiaAttrezzatura.SCARPONI
        )

        gestore_prodotti.inserisciNuovoProdotto(p1)
        gestore_prodotti.inserisciNuovoProdotto(p2)
        gestore_prodotti.inserisciNuovoProdotto(p3)
        print("✅ 3 Prodotti salvati in prodotti.pickle")
    else:
        print("I prodotti esistono già.")

    # ==========================================
    # 2. POPOLAMENTO UTENTI
    # ==========================================
    # Assumiamo che la lista interna di GestoreUtenti si chiami _utenti o utenti
    lista_utenti = getattr(gestore_utenti, '_utenti', getattr(gestore_utenti, 'utenti', []))

    if not lista_utenti:
        print("Creazione utenti in corso...")
        try:
            # Creazione Admin (necessario per visualizzare la Dashboard Dipendente e gli ordini)
            gestore_utenti.registraDipendente(
                nome="Admin", cognome="Principale", email="admin@passodellorso.it",
                password="admin12345", telefono="3330000000"
            )

            # Creazione Cliente (necessario per testare il carrello e il checkout)
            gestore_utenti.registraCliente(
                nome="Mario", cognome="Rossi", email="cliente@email.com",
                password="password", telefono="3331112222"
            )
            print("✅ 2 Utenti salvati in utenti.pickle")
        except Exception as e:
            print(f"Errore durante la creazione degli utenti: {e}")
    else:
        print("Gli utenti esistono già.")


if __name__ == "__main__":
    popola_database()