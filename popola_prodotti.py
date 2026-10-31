import os
import pickle
from datetime import date
from models.skipass import SkiPass
from models.attrezzatura import Attrezzatura
from models.lezione import Lezione
from models.assicurazione import Assicurazione
from models.enums import FormulaTemporale, TipologiaAttrezzatura, Livello

def popola():
    os.makedirs("data", exist_ok=True)
    percorso = "data/prodotti.pickle"

    oggi = date.today()

    prodotti = []

    # 1. SkiPass Giornaliero
    p1 = SkiPass(
        id_prodotto=1,
        nome="Skipass Giornaliero",
        descrizione="Accesso completo a tutti gli impianti per l'intera giornata.",
        prezzo=45.0,
        immagine="skipass.png",
        is_disponibile=True,
        formula_temporale=FormulaTemporale.GIORNALIERO,
        data_inizio=oggi,
        data_fine=oggi
    )
    prodotti.append(p1)

    # 2. SkiPass Settimanale
    p2 = SkiPass(
        id_prodotto=2,
        nome="Skipass Settimanale",
        descrizione="Abbonamento valido 7 giorni consecutivi.",
        prezzo=250.0,
        immagine="skipass.png",
        is_disponibile=True,
        formula_temporale=FormulaTemporale.SETTIMANALE,
        data_inizio=oggi,
        data_fine=oggi
    )
    prodotti.append(p2)

    # 3. Attrezzatura (Noleggio Sci)
    p3 = Attrezzatura(
        id_prodotto=3,
        nome="Noleggio Sci Completo",
        descrizione="Set completo di sci, attacchi e scarponi.",
        prezzo=35.0,
        immagine="sci.png",
        is_disponibile=True,
        brand="Salomon",
        taglia="L (175cm)",
        livello=Livello.INTERMEDIO,
        tipologia=TipologiaAttrezzatura.SCI,
        quantita=8,
        data=oggi
    )
    prodotti.append(p3)

    # 4. Attrezzatura (Noleggio Snowboard)
    p4 = Attrezzatura(
        id_prodotto=4,
        nome="Noleggio Snowboard",
        descrizione="Tavola da snowboard flessibile con scarponi.",
        prezzo=35.0,
        immagine="snowboard.png",
        is_disponibile=True,
        brand="Burton",
        taglia="M (160cm)",
        livello=Livello.PRINCIPIANTE,
        tipologia=TipologiaAttrezzatura.SNOWBOARD,
        quantita=5,
        data=oggi
    )
    prodotti.append(p4)

    # 5. Lezione
    p5 = Lezione(
        id_prodotto=5,
        nome="Lezione Privata 1h",
        descrizione="Lezione individuale con maestro federale FISI.",
        prezzo=50.0,
        immagine="lezione.png",
        is_disponibile=True,
        data=oggi,
        livello=Livello.INTERMEDIO,
        quantita=4
    )
    prodotti.append(p5)

    # 6. Assicurazione
    p6 = Assicurazione(
        id_prodotto=6,
        nome="Assicurazione Infortuni",
        descrizione="Copertura assicurativa giornaliera per piste.",
        prezzo=5.0,
        immagine="assicurazione.png",
        is_disponibile=True,
        data_inizio=oggi,
        data_fine=oggi
    )
    prodotti.append(p6)

    with open(percorso, "wb") as f:
        pickle.dump(prodotti, f)

    print(f"✅ Database prodotti rigenerato con successo! Creati {len(prodotti)} prodotti.")

if __name__ == "__main__":
    popola()