#!/usr/bin/env python3
"""Sjabloon: Python-skelet voor een script dat iets naar buiten doet (versturen, wijzigen, verwijderen).

Dekt: SCR-24, SCR-25, SCR-26, SCR-31, SCR-40, SCR-45, SCR-46, SCR-47, ARCH-28, ARCH-58, ARCH-62, API-66,
      SCR-19, AI-26 (plafond, noodstop, automatische pauze), PRIV-51 (idem), BIZ-23 (telt in een bestand)
Dekt gedeeltelijk:
  - BIZ-23 vraagt het plafond per tenant en in totaal, geteld in de database; dit skelet telt in een eigen
    logboekbestand voor een enkele lijn op een host.
  - ARCH-58 vraagt ook correlatie-id, route, methode en duur; die velden spelen in een script niet en staan
    er niet in. De overige vaste velden wel.
  - SCR-32 (venv met hashes) en SCR-35 (ruff als gate) gelden zodra het script iets buiten de
    standaardbibliotheek gebruikt; dit skelet gebruikt alleen de standaardbibliotheek.
  - SCR-28 (yaml.safe_load) en SCR-30 (SQL met parameters): zie de twee voorbeeldregels onderaan.
Aanpassen: NAAM, verwerk(), geldig_id() en de configuratie. PLAFOND_PER_DAG heeft geen standaardwaarde.
Gebruik:
  PLAFOND_PER_DAG=<n> python3 -I skelet.py --ids <bestand> --verwacht <n>              proefstand (standaard)
  PLAFOND_PER_DAG=<n> python3 -I skelet.py --ids <bestand> --verwacht <n> --uitvoeren  echt
Noodstop: <staat>/schakelaar.json bevat {"actief": true}. Elke andere inhoud of een leesfout stopt de lijn.
Controleren: python3 -m py_compile skelet.py; ruff check --select S,RUF006 skelet.py (SCR-35); de drie tests
  van SCR-46 (schakelaar uit tijdens een run, opslag onleesbaar, mislukte pogingen vullen het plafond).
"""
import argparse
import datetime
import json
import logging
import os
import pathlib
import subprocess
import sys
import tempfile
import urllib.request
import zoneinfo

NAAM = "voorbeeld-lijn"
RELEASE = os.environ.get("RELEASE", "onbekend")
STAAT = pathlib.Path(os.environ.get("XDG_STATE_HOME", pathlib.Path.home() / ".local/state")) / NAAM
SCHAKELAAR = STAAT / "schakelaar.json"
LOGBOEK = STAAT / "logboek.jsonl"
AMSTERDAM = zoneinfo.ZoneInfo("Europe/Amsterdam")  # SCR-40: de tijdzone expliciet
OPEN_STATEN = {"bezig", "onzeker"}


class JsonFormatter(logging.Formatter):
    """Een regel per gebeurtenis, alleen benoemde velden (ARCH-58, ARCH-62)."""

    VELDEN = ("event", "item_id", "uitkomst", "aantal")  # alleen deze extra velden komen in het log

    def format(self, record):
        regel = {
            "time": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="milliseconds"),
            "level": record.levelname.lower(),
            "app": NAAM,
            "release": RELEASE,
            "msg": record.getMessage(),
        }
        for veld in self.VELDEN:
            if hasattr(record, veld):
                regel[veld] = getattr(record, veld)
        return json.dumps(regel, ensure_ascii=False)  # JSON: invoer kan geen logregel vervalsen (API-66)


log = logging.getLogger(NAAM)


def lees_geheim(naam):
    """Een geheim komt uit een bestand met modus 600, nooit uit een argument (SCR-19). Log het nooit."""
    basis = pathlib.Path(os.environ.get("CREDENTIALS_DIRECTORY", pathlib.Path.home() / ".config" / NAAM))
    pad = basis / naam
    if pad.stat().st_mode & 0o077:
        raise PermissionError(f"{pad} is leesbaar voor anderen; verwacht modus 600")
    return pad.read_text().strip()


def schakelaar_aan():
    """Faalt gesloten: een leesfout of een andere waarde dan true is een uitzondering of False (SCR-46)."""
    return json.loads(SCHAKELAAR.read_text())["actief"] is True


def lees_logboek():
    if not LOGBOEK.exists():
        return []
    return [json.loads(regel) for regel in LOGBOEK.read_text().splitlines() if regel]


def pogingen_vandaag():
    """Telt pogingen, niet alleen successen (SCR-46)."""
    vandaag = datetime.datetime.now(AMSTERDAM).date().isoformat()
    return sum(1 for r in lees_logboek() if r["datum"] == vandaag and r["staat"] == "bezig")


def open_items():
    laatste = {}
    for r in lees_logboek():
        laatste[r["id"]] = r["staat"]
    return sorted(i for i, staat in laatste.items() if staat in OPEN_STATEN)


def noteer(item_id, staat):
    regel = {
        "datum": datetime.datetime.now(AMSTERDAM).date().isoformat(),
        "tijd": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "id": item_id,
        "staat": staat,
    }
    with LOGBOEK.open("a") as f:
        f.write(json.dumps(regel) + "\n")
        f.flush()
        os.fsync(f.fileno())


def geldig_id(tekst):
    return tekst.isascii() and tekst.isdigit()


def verwerk(item_id):
    """De ene actie per item. Vervang de inhoud. Twee patronen als voorbeeld."""
    # Proces starten: lijst, geen shell, "--" voor waarden van buiten, time-out en check (SCR-24, SCR-25).
    subprocess.run(["/bin/true", "--", item_id], check=True, timeout=60, capture_output=True, text=True)

    # HTTP: time-out, certificaatcontrole blijft aan, alleen https, status controleren (SCR-26).
    # token = lees_geheim("api_token")
    # verzoek = urllib.request.Request("https://api.example.nl/v1/items/" + item_id,
    #                                  headers={"Authorization": "Bearer " + token}, method="POST")
    # with urllib.request.urlopen(verzoek, timeout=20) as antwoord:   # noqa: S310 (vast https-adres)
    #     if antwoord.status != 200:
    #         raise RuntimeError(f"onverwachte status {antwoord.status}")

    # Tijdelijke bestanden alleen via tempfile (SCR-31):
    # with tempfile.TemporaryDirectory() as werk:
    #     pad = pathlib.Path(werk) / "export.csv"

    # YAML alleen met yaml.safe_load(tekst) (SCR-28).
    # SQL alleen met plaatshouders: cur.execute("UPDATE t SET staat = %s WHERE id = %s", (staat, item_id)) (SCR-30).


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--ids", required=True, type=pathlib.Path, help="bestand met een id per regel")
    parser.add_argument("--verwacht", required=True, type=int, help="het aantal id's dat je verwacht")
    parser.add_argument("--uitvoeren", action="store_true", help="zonder deze vlag: alleen tonen (ARCH-28)")
    args = parser.parse_args()

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    log.addHandler(handler)
    log.setLevel(logging.INFO)

    plafond = int(os.environ["PLAFOND_PER_DAG"])  # geen standaardwaarde: ontbreekt hij, dan stopt het script
    os.umask(0o077)
    STAAT.mkdir(mode=0o700, parents=True, exist_ok=True)

    # Selectie: exacte id's, geteld en vergeleken; leeg betekent nooit alles (SCR-47).
    ids = [r.strip() for r in args.ids.read_text().splitlines() if r.strip()]
    if not ids or len(ids) != args.verwacht:
        log.error("aantal klopt niet", extra={"event": "selectie_fout", "aantal": len(ids)})
        return 1
    if not all(geldig_id(i) for i in ids):
        log.error("ongeldig id in de selectie", extra={"event": "selectie_fout"})
        return 1

    # Automatische pauze: een onbeoordeeld item blokkeert elke volgende run (SCR-45).
    wacht = open_items()
    if wacht:
        log.error("lijn gepauzeerd, onbeoordeelde items", extra={"event": "lijn_gepauzeerd", "aantal": len(wacht)})
        return 1

    gedaan = 0
    for item_id in ids:
        # Schakelaar en plafond vlak voor elke afzonderlijke actie (SCR-46). Een leesfout is een uitzondering
        # en stopt het script.
        if not schakelaar_aan():
            log.warning("noodstop", extra={"event": "noodstop"})
            return 1
        if pogingen_vandaag() >= plafond:
            log.warning("dagplafond bereikt", extra={"event": "plafond", "aantal": plafond})
            return 1
        if not args.uitvoeren:
            log.info("proef: zou verwerken", extra={"event": "proef", "item_id": item_id})
            continue

        noteer(item_id, "bezig")  # de poging ligt vast voor het effect (SCR-45)
        try:
            verwerk(item_id)
        except (subprocess.TimeoutExpired, TimeoutError):
            noteer(item_id, "onzeker")  # onbekend is "gebeurd": niet opnieuw proberen (SCR-45)
            log.error("uitkomst onbekend, lijn gepauzeerd", extra={"event": "onzeker", "item_id": item_id})
            return 1
        except Exception as fout:  # de lijn stopt bij de eerste fout; log alleen het type, niet de inhoud
            noteer(item_id, "mislukt")
            log.error("mislukt", extra={"event": "mislukt", "item_id": item_id, "uitkomst": type(fout).__name__})
            return 1
        noteer(item_id, "klaar")
        gedaan += 1
        log.info("verwerkt", extra={"event": "verwerkt", "item_id": item_id})

    log.info("klaar", extra={"event": "klaar", "aantal": gedaan})
    return 0


if __name__ == "__main__":
    sys.exit(main())
