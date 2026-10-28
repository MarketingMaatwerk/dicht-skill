#!/usr/bin/env python3
"""Sjabloon: controleert de vorm van een bewijsbestand en van het uitzonderingenregister.

Dekt: ARCH-53 (de vorm), ARCH-30 (verloopdatum), GIT-65 (hooguit 90 dagen voor een scannerbevinding), ARCH-85
Dekt gedeeltelijk: dit controleert de vorm, niet of het bewijs waar is, en niet of elk punt van de checklist
  erin staat (dat doet het auditscript van ARCH-84, dat nog gebouwd wordt).
Gebruik: python3 controleer-bewijs.py bewijs/<bestand>.md [docs/uitzonderingen.md]
Alleen lezen (ARCH-85). Exitcode 0: de vorm klopt en niets staat open; 1: er is iets gevonden.
Wat het controleert:
  - de kop heeft alle vaste velden en geen ingevulde plek tussen < en >
  - elke rij heeft een bekende status; "nvt" en "voldaan" hebben een bewijs of reden
  - "niet gemeten" telt als open
  - "uitzondering" verwijst naar een ID dat in het register staat en niet verlopen is
  - elke rij in het register heeft een regel, datum, reden, verloopdatum en vervangende maatregel
"""
import datetime
import pathlib
import re
import sys

VELDEN = ["project", "type", "commit", "datum", "door", "akkoord", "runtime", "hulpmiddelen", "gate", "uitzonderingen"]
STATUSSEN = {"voldaan", "nvt", "uitzondering", "niet gemeten"}
REGEL_ID = re.compile(r"^[A-Z]+-\d+$")
DATUM = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def rijen(tekst):
    """Geeft de cellen van elke tabelrij, zonder kop- en scheidingsrijen."""
    for regel in tekst.splitlines():
        if regel.startswith("|") and not set(regel) <= set("|- "):
            yield [cel.strip() for cel in regel.strip().strip("|").split("|")]


def lees_register(pad, vandaag):
    fouten, geldig = [], {}
    for cellen in rijen(pad.read_text()):
        if len(cellen) != 7 or cellen[0] == "ID":
            continue
        uid, regel, datum, door, reden, verloopt, maatregel = cellen
        if not all([regel, door, reden, maatregel]) or "<" in "".join(cellen):
            fouten.append(f"register {uid}: onvolledig of nog niet ingevuld")
            continue
        if not DATUM.match(datum) or not DATUM.match(verloopt):
            fouten.append(f"register {uid}: datum of verloopdatum ontbreekt of heeft een andere vorm dan jjjj-mm-dd")
            continue
        einde = datetime.date.fromisoformat(verloopt)
        if einde < vandaag and "afgesloten" not in reden:
            fouten.append(f"register {uid}: verlopen op {verloopt}; telt als niet afgevinkt (ARCH-30)")
        geldig[uid] = einde
    return fouten, geldig


def main():
    if len(sys.argv) not in (2, 3):
        print(__doc__.splitlines()[0], "\ngebruik: controleer-bewijs.py <bewijsbestand> [register]", file=sys.stderr)
        return 2
    vandaag = datetime.datetime.now(datetime.timezone.utc).date()
    tekst = pathlib.Path(sys.argv[1]).read_text()
    tekst = re.sub(r"<!--.*?-->", "", tekst, flags=re.S)
    fouten, register = [], {}
    if len(sys.argv) == 3:
        fouten, register = lees_register(pathlib.Path(sys.argv[2]), vandaag)

    kop = re.search(r"^---\n(.*?)\n---$", tekst, flags=re.S | re.M)
    if not kop:
        fouten.append("kop ontbreekt")
    else:
        gevonden = dict(r.split(":", 1) for r in kop.group(1).splitlines() if ":" in r)
        for veld in VELDEN:
            waarde = gevonden.get(veld, "").strip()
            if not waarde or "<" in waarde:
                fouten.append(f"kop: {veld} is leeg of nog niet ingevuld")

    aantal = 0
    for cellen in rijen(tekst):
        if len(cellen) != 3 or cellen[0] == "Regel":
            continue
        regel, status, bewijs = cellen
        aantal += 1
        if not REGEL_ID.match(regel):
            fouten.append(f"{regel}: geen regel-ID")
        if status not in STATUSSEN:
            fouten.append(f"{regel}: onbekende status '{status}'")
        elif status == "niet gemeten":
            fouten.append(f"{regel}: niet gemeten ({bewijs or 'geen toelichting'})")
        elif not bewijs:
            fouten.append(f"{regel}: {status} zonder bewijs of reden telt als niet afgevinkt")
        elif status == "uitzondering":
            uid = re.search(r"U-\d+", bewijs)
            if not uid:
                fouten.append(f"{regel}: uitzondering zonder ID uit het register")
            elif len(sys.argv) == 3 and uid.group() not in register:
                fouten.append(f"{regel}: {uid.group()} staat niet (geldig) in het register")
            elif len(sys.argv) == 3 and register[uid.group()] < vandaag:
                fouten.append(f"{regel}: {uid.group()} is verlopen")
    if aantal == 0:
        fouten.append("geen enkele regel in het bewijsbestand")

    for fout in fouten:
        print(fout)
    print(f"{aantal} regels, {len(fouten)} open punten")
    return 1 if fouten else 0


if __name__ == "__main__":
    sys.exit(main())
