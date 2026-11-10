import os
import pickle
import random
from datetime import datetime, date, timedelta

from models.enums import Difficolta, StatoApertura, FormulaTemporale, Livello, StatoOrdine, TipologiaAttrezzatura

# ==============================================================================
# IMPORT DELLE TUE VERE CLASSI
# ==============================================================================
from models.pista import Pista
from models.cliente import Cliente
from models.dipendente import Dipendente
from models.ordine import Ordine
from models.prodotto_ordine import ProdottoOrdine
from models.metodo_pagamento import MetodoPagamento

from models.assicurazione import Assicurazione
from models.attrezzatura import Attrezzatura
from models.skipass import SkiPass
from models.lezione import Lezione

# ==============================================================================
# NOMI DEI FILE E CARTELLA
# ==============================================================================
CARTELLA = "data"
os.makedirs(CARTELLA, exist_ok=True)

FILE_UTENTI = os.path.join(CARTELLA, "utenti.pickle")
FILE_ORDINI = os.path.join(CARTELLA, "ordini.pickle")
FILE_PISTE = os.path.join(CARTELLA, "piste.pickle")
FILE_PRODOTTI = os.path.join(CARTELLA, "prodotti.pickle")


def distruggi_vecchi_file():
    print("🧨 Distruzione vecchi database in corso...")
    for file in [FILE_UTENTI, FILE_ORDINI, FILE_PISTE, FILE_PRODOTTI]:
        if os.path.exists(file):
            os.remove(file)
            print(f"  [-] File {file} eliminato.")
        else:
            print(f"  [ ] File {file} non trovato (già pulito).")


def genera_piste():
    print("🏔️ Generazione di 15 piste...")
    nomi_piste = [
        ("Lupo Bianco", Difficolta.ROSSA), ("Aquila Nera", Difficolta.NERA),
        ("Orsetto", Difficolta.AZZURRA), ("Direttissima", Difficolta.NERA),
        ("Panoramica", Difficolta.ROSSA), ("Scoiattolo", Difficolta.AZZURRA),
        ("Marmotta", Difficolta.AZZURRA), ("Ghiacciaio", Difficolta.ROSSA),
        ("Muro del Pianto", Difficolta.NERA), ("Baita", Difficolta.ROSSA),
        ("Baby", Difficolta.AZZURRA), ("Slalom", Difficolta.ROSSA),
        ("Olimpica", Difficolta.NERA), ("Raccordo", Difficolta.AZZURRA),
        ("Boschetto", Difficolta.ROSSA)
    ]
    piste = []
    for i, (nome, diff) in enumerate(nomi_piste):
        p = Pista(id_pista=i + 1, nome=nome, difficolta=diff)
        piste.append(p)
    return piste


def genera_utenti():
    print("👥 Generazione utenti (3 Dipendenti, 5 Clienti)...")
    utenti = []

    for i in range(1, 4):
        u = Dipendente(
            id_utente=i,
            id_dipendente=i + 100,
            nome=f"Dipendente{i}",
            cognome="Staff",
            email=f"dipendente{i}@passodellorso.it",
            password="password123",
            numero_telefono="3331234567"
        )
        utenti.append(u)

    nomi_clienti = [("Mario", "Rossi"), ("Giulia", "Bianchi"), ("Luca", "Verdi"),
                    ("Anna", "Neri"), ("Marco", "Gialli")]

    clienti = []
    for i, (nome, cogn) in enumerate(nomi_clienti):
        c = Cliente(
            id_utente=i + 10,
            nome=nome,
            cognome=cogn,
            email=f"{nome.lower()}@email.com",
            password="password123",
            numero_telefono="3339876543"
        )
        clienti.append(c)
        utenti.append(c)

    return utenti, clienti


def genera_prodotti():
    print("🎫 Generazione Prodotti (SkiPass, Attrezzatura, Assicurazioni e Lezioni)...")
    prodotti = []
    id_counter = 1

    data_inizio_stagione = date(2026, 12, 1)
    data_fine_stagione = date(2027, 4, 30)

    # ==========================================
    # 1. SKIPASS E ASSICURAZIONI STAGIONALI
    # ==========================================
    prodotti.append(SkiPass(
        id_prodotto=id_counter, nome="Skipass STAGIONALE 26/27", descrizione="Accesso illimitato stagione",
        prezzo=650.00, immagine="default.png", is_disponibile=True,
        formula_temporale=FormulaTemporale.STAGIONALE, data_inizio=data_inizio_stagione, data_fine=data_fine_stagione
    ))
    id_counter += 1

    prodotti.append(Assicurazione(
        id_prodotto=id_counter, nome="Assicurazione Infortuni STAGIONALE", descrizione="Copertura completa",
        prezzo=100.00, immagine="default.png", is_disponibile=True,
        data_inizio=data_inizio_stagione, data_fine=data_fine_stagione
    ))
    id_counter += 1

    # ==========================================
    # 2. SKIPASS E ASSICURAZIONI MENSILI
    # ==========================================
    data_fine_mese = date(2026, 12, 31)

    prodotti.append(SkiPass(
        id_prodotto=id_counter, nome="Skipass MENSILE - Dicembre", descrizione="Valido tutto dicembre",
        prezzo=250.00, immagine="default.png", is_disponibile=True,
        formula_temporale=FormulaTemporale.MENSILE, data_inizio=data_inizio_stagione, data_fine=data_fine_mese
    ))
    id_counter += 1

    prodotti.append(Assicurazione(
        id_prodotto=id_counter, nome="Assicurazione MENSILE - Dicembre", descrizione="Copertura mese",
        prezzo=40.00, immagine="default.png", is_disponibile=True,
        data_inizio=data_inizio_stagione, data_fine=data_fine_mese
    ))
    id_counter += 1

    # ==========================================
    # 3. SKIPASS E ASSICURAZIONI SETTIMANALI
    # ==========================================
    data_fine_settimana = data_inizio_stagione + timedelta(days=6)
    date_str = f"Dal {data_inizio_stagione.strftime('%d/%m/%y')} al {data_fine_settimana.strftime('%d/%m/%y')}"

    prodotti.append(SkiPass(
        id_prodotto=id_counter, nome=f"Skipass SETTIMANALE - {date_str}", descrizione="7 giorni consecutivi",
        prezzo=180.00, immagine="default.png", is_disponibile=True,
        formula_temporale=FormulaTemporale.SETTIMANALE, data_inizio=data_inizio_stagione, data_fine=data_fine_settimana
    ))
    id_counter += 1

    prodotti.append(Assicurazione(
        id_prodotto=id_counter, nome=f"Assicurazione SETTIMANALE - {date_str}", descrizione="Copertura 7 giorni",
        prezzo=25.00, immagine="default.png", is_disponibile=True,
        data_inizio=data_inizio_stagione, data_fine=data_fine_settimana
    ))
    id_counter += 1

    # ==========================================
    # 4. CICLO DI 31 GIORNI (Giornalieri, Lezioni e Attrezzatura specifica per data)
    # ==========================================
    for giorno in range(31):
        data_corrente = data_inizio_stagione + timedelta(days=giorno)
        data_str = data_corrente.strftime('%d/%m/%Y')

        dt_lezione_gruppo = datetime(data_corrente.year, data_corrente.month, data_corrente.day, 10, 0)
        dt_lezione_privata = datetime(data_corrente.year, data_corrente.month, data_corrente.day, 14, 0)

        # Skipass e Assicurazione
        prodotti.append(SkiPass(
            id_prodotto=id_counter, nome=f"Skipass GIORNALIERO - {data_str}", descrizione="Accesso 1 giorno",
            prezzo=45.00, immagine="default.png", is_disponibile=True,
            formula_temporale=FormulaTemporale.GIORNALIERO, data_inizio=data_corrente, data_fine=data_corrente
        ))
        id_counter += 1

        prodotti.append(Assicurazione(
            id_prodotto=id_counter, nome=f"Assicurazione GIORNALIERA - {data_str}", descrizione="Copertura base",
            prezzo=5.00, immagine="default.png", is_disponibile=True,
            data_inizio=data_corrente, data_fine=data_corrente
        ))
        id_counter += 1

        # Lezioni
        livello_scelto = random.choice([Livello.PRINCIPIANTE, Livello.INTERMEDIO, Livello.AVANZATO])

        prodotti.append(Lezione(
            id_prodotto=id_counter,
            nome=f"Lezione Sci GRUPPO - {livello_scelto.value.capitalize()} | {data_str} (10:00)",
            descrizione="LEZIONE DI GRUPPO 2 ORE", prezzo=35.00, immagine="default.png", is_disponibile=True,
            data=dt_lezione_gruppo, livello=livello_scelto, quantita=10
        ))
        id_counter += 1

        prodotti.append(Lezione(
            id_prodotto=id_counter,
            nome=f"Lezione Sci PRIVATA - {livello_scelto.value.capitalize()} | {data_str} (14:00)",
            descrizione="LEZIONE PRIVATA 1 ORA", prezzo=60.00, immagine="default.png", is_disponibile=True,
            data=dt_lezione_privata, livello=livello_scelto, quantita=1
        ))
        id_counter += 1

        # Attrezzatura (Tutte le combinazioni per questo giorno specifico)
        for tipologia in TipologiaAttrezzatura:
            for livello in Livello:
                prezzo_base = 25.0
                if tipologia in (TipologiaAttrezzatura.SCI, TipologiaAttrezzatura.SNOWBOARD):
                    prezzo_base = 35.0
                elif tipologia == TipologiaAttrezzatura.CASCO:
                    prezzo_base = 10.0
                elif tipologia == TipologiaAttrezzatura.SCARPONI:
                    prezzo_base = 15.0

                nome_attr = f"Noleggio {tipologia.value.capitalize()} - {livello.value.capitalize()} | {data_str}"

                prodotti.append(Attrezzatura(
                    id_prodotto=id_counter,
                    nome=nome_attr,
                    descrizione=f"{tipologia.value.capitalize()} | Livello: {livello.value.capitalize()}",
                    prezzo=prezzo_base,
                    immagine="default.png",
                    is_disponibile=True,
                    brand="Passo dell'Orso Gear",
                    data=data_corrente,  # DATA SPECIFICA DEL GIORNO!
                    livello=livello,
                    quantita=30,
                    taglia="Universale",
                    tipologia=tipologia
                ))
                id_counter += 1

    return prodotti


def genera_ordini(clienti, prodotti):
    print("🛒 Generazione Ordini misti...")
    ordini_globali = []
    id_ordine = 1000

    stati_possibili = [StatoOrdine.COMPLETATO, StatoOrdine.RIMBORSO_RICHIESTO, StatoOrdine.IN_CORSO]

    for cliente in clienti:
        num_ordini = random.randint(2, 3)
        for _ in range(num_ordini):
            prodotti_scelti = random.sample(prodotti, random.randint(1, 4))

            items_ordine = []
            prezzo_totale = 0.0

            for prod in prodotti_scelti:
                qta = random.randint(1, 4) if isinstance(prod, (SkiPass, Assicurazione)) else 1
                items_ordine.append(ProdottoOrdine(prodotto=prod, quantita=qta))
                prezzo_totale += prod.prezzo * qta

            try:
                metodo = MetodoPagamento("Carta di Credito")
            except TypeError:
                try:
                    metodo = MetodoPagamento()
                except TypeError:
                    metodo = None

            nuovo_ordine = Ordine(
                id_ordine=id_ordine,
                metodo_pagamento=metodo,
                prezzo_totale=prezzo_totale,
                prodotti=items_ordine
            )

            data_ordine = datetime.now() - timedelta(days=random.randint(1, 30))
            nuovo_ordine._data = data_ordine
            nuovo_ordine.stato = random.choice(stati_possibili)

            ordini_globali.append(nuovo_ordine)
            cliente.aggiungi_ordine(nuovo_ordine)

            id_ordine += 1

    return ordini_globali


def salva_su_pickle(dati, nome_file):
    with open(nome_file, 'wb') as f:
        pickle.dump(dati, f)
    print(f"  [+] Salvato con successo: {nome_file}")


# ==============================================================================
# ESECUZIONE PRINCIPALE
# ==============================================================================
if __name__ == "__main__":
    print("=== INIZIO RESET E POPOLAMENTO DATABASE ===")

    distruggi_vecchi_file()

    print("\n--- INIZIO GENERAZIONE DATI ---")
    piste = genera_piste()
    utenti, clienti_solo = genera_utenti()
    prodotti = genera_prodotti()
    ordini = genera_ordini(clienti_solo, prodotti)

    print("\n--- SALVATAGGIO NEI FILE .PICKLE ---")
    salva_su_pickle(utenti, FILE_UTENTI)
    salva_su_pickle(piste, FILE_PISTE)
    salva_su_pickle(prodotti, FILE_PRODOTTI)
    salva_su_pickle(ordini, FILE_ORDINI)

    print("\n✅ TUTTO FATTO! Database rigenerato con successo. Ora puoi avviare main.py")