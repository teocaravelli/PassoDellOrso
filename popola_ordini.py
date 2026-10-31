import os
import pickle
import datetime
from argparse import Namespace


def popola_database_ordini():
    percorso_utenti = "data/utenti.pickle"
    percorso_ordini = "data/ordini.pickle"

    # 1. Carica gli utenti esistenti dal database
    if not os.path.exists(percorso_utenti):
        print("❌ Errore: File utenti.pickle non trovato.")
        print("Avvia l'app e registra almeno un utente prima di lanciare questo script!")
        return

    with open(percorso_utenti, "rb") as f:
        utenti = pickle.load(f)

    if not utenti:
        print("❌ Errore: Il database utenti è vuoto.")
        return

    # Prendiamo il primo utente registrato (modifica l'indice se vuoi un utente specifico)
    utente_test = utenti[0]
    email_utente = getattr(utente_test, 'email', 'Sconosciuta')

    if not hasattr(utente_test, 'storico_ordini'):
        utente_test.storico_ordini = []

    print(f"👤 Utente selezionato per i test: {getattr(utente_test, 'nome', '')} ({email_utente})")

    # 2. Creiamo dei finti prodotti (simulando quelli del carrello)
    p1 = Namespace(nome="Skipass Giornaliero Adulti", prezzo=45.0, quantita=2)
    p2 = Namespace(nome="Noleggio Sci Salomon (Avanzato)", prezzo=35.5, quantita=1)
    p3 = Namespace(nome="Lezione Privata 1h (Maestro Marco)", prezzo=40.0, quantita=1)

    # 3. Creiamo 3 ordini con date e stati differenti
    ora_attuale = datetime.datetime.now()

    ordine_1 = Namespace(
        id_ordine=int((ora_attuale - datetime.timedelta(days=10)).timestamp()),
        data=(ora_attuale - datetime.timedelta(days=10)).strftime("%d/%m/%Y %H:%M"),
        totale=90.0,
        stato="COMPLETATO",
        prodotti=[p1]
    )

    ordine_2 = Namespace(
        id_ordine=int((ora_attuale - datetime.timedelta(days=2)).timestamp()),
        data=(ora_attuale - datetime.timedelta(days=2)).strftime("%d/%m/%Y %H:%M"),
        totale=35.5,
        stato="RESTITUITO",
        prodotti=[p2]
    )

    ordine_3 = Namespace(
        id_ordine=int(ora_attuale.timestamp()),
        data=ora_attuale.strftime("%d/%m/%Y %H:%M"),
        totale=40.0,
        stato="IN ELABORAZIONE",  # Utile per testare la pagina di "Modifica Ordine"
        prodotti=[p3]
    )

    nuovi_ordini = [ordine_1, ordine_2, ordine_3]

    # Aggiungiamo all'utente
    utente_test.storico_ordini.extend(nuovi_ordini)

    # Salviamo il database utenti aggiornato
    with open(percorso_utenti, "wb") as f:
        pickle.dump(utenti, f)

    # (Opzionale) Se usi un file ordini.pickle globale per il GestoreOrdini, salviamoli anche lì
    tutti_gli_ordini = []
    if os.path.exists(percorso_ordini):
        with open(percorso_ordini, "rb") as f:
            try:
                tutti_gli_ordini = pickle.load(f)
            except EOFError:
                pass

    tutti_gli_ordini.extend(nuovi_ordini)

    with open(percorso_ordini, "wb") as f:
        pickle.dump(tutti_gli_ordini, f)

    print(f"✅ Popolamento completato! Aggiunti {len(nuovi_ordini)} ordini all'utente {email_utente}.")
    print("Ora puoi avviare l'app e testare la pagina 'I Miei Ordini' e il pulsante 'Modifica'!")


if __name__ == "__main__":
    popola_database_ordini()