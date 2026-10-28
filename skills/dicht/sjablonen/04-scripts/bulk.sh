#!/usr/bin/env bash
# Sjabloon: Bash-skelet voor een script dat in bulk wijzigt, verwijdert of verstuurt.
#   Proefstand als standaard, exacte id's, een grens, een dagplafond, een noodstop, en per item eerst de
#   poging vastleggen en dan pas het effect.
# Dekt: ARCH-28, SCR-45, SCR-46, SCR-47, SCR-01, SCR-04, SCR-06, SCR-08, SCR-16, SCR-18, SCR-38 (per stap),
#       AI-26 (plafond, noodstop, automatische pauze), PRIV-51 (idem), BIZ-23 (telt in een bestand, niet in de database)
# Dekt gedeeltelijk:
#   - BIZ-23 vraagt het plafond per tenant en in totaal, geteld in de database. Dit skelet telt in een
#     logboekbestand op een host, voor een enkele lijn. Voor een stroom met geld of meerdere tenants: tel in de
#     database (BIZ-21, BIZ-23) en gebruik dit bestand alleen als vorm.
#   - AI-26 en PRIV-51 vragen ook een vaste tekst of vaste vangrails en een vastgelegd besluit met begin- en
#     einddatum; dat zit niet in een skelet.
#   - ARCH-28 raadt aan eerst te markeren als verwijderd in plaats van te wissen; dat bepaalt verwerk().
# Aanpassen: NAAM, de functie verwerk() en de controle op het type id. De getallen hebben geen standaardwaarde:
#   PLAFOND_PER_DAG en STAP_TIMEOUT moet je zelf zetten, --verwacht geef je per run op.
# Gebruik:
#   PLAFOND_PER_DAG=<n> STAP_TIMEOUT=<duur> bulk.sh --ids <bestand> --verwacht <n>              toont wat er zou gebeuren
#   PLAFOND_PER_DAG=<n> STAP_TIMEOUT=<duur> bulk.sh --ids <bestand> --verwacht <n> --uitvoeren  doet het echt
#   De uitvoer van de proefrun staat in het logboek voor de echte run (ARCH-28, bewijs).
# Noodstop: het bestand $STAAT/schakelaar bevat precies "aan". Elke andere inhoud, een leeg of onleesbaar
#   bestand stopt de lijn (faal gesloten). Uitzetten: echo uit > $STAAT/schakelaar. Werkt zonder deploy.
# Automatische pauze: een item dat op "bezig" of "onzeker" is blijven staan blokkeert elke volgende run tot
#   een mens het logboek heeft beoordeeld en de regel heeft afgesloten (SCR-45).
# Controleren (SCR-46, drie tests): (1) schakelaar uit tijdens een run: het volgende item wordt niet verwerkt;
#   (2) schakelaar of logboek onleesbaar: er gebeurt niets; (3) mislukte pogingen vullen het plafond.
#   En (SCR-47): een leeg bestand met id's of een ander aantal dan --verwacht stopt met een fout.
#   bash -n bulk.sh; shellcheck --severity=warning bulk.sh (SCR-23).
set -euo pipefail
shopt -s inherit_errexit
umask 077
export PATH=/usr/local/bin:/usr/bin:/bin
trap 'echo "fout op regel $LINENO: $BASH_COMMAND" >&2' ERR

NAAM=voorbeeld-lijn
STAAT="${XDG_STATE_HOME:-$HOME/.local/state}/$NAAM"
SCHAKELAAR="$STAAT/schakelaar"
LOGBOEK="$STAAT/logboek.tsv"            # kolommen: datum (Europe/Amsterdam), tijd (UTC), id, staat
PLAFOND_PER_DAG="${PLAFOND_PER_DAG:?zet PLAFOND_PER_DAG (geen standaardwaarde)}"
STAP_TIMEOUT="${STAP_TIMEOUT:?zet STAP_TIMEOUT, bijvoorbeeld de duur van een stap ruim genomen}"

# De ene actie per item. Vervang de inhoud. De aanroep krijgt een harde time-out (SCR-38).
# Zet -- voor het id (SCR-08). Het id is hierboven al op type gecontroleerd.
verwerk() {
  local id="$1"
  timeout -k 30 "$STAP_TIMEOUT" /bin/false -- "$id"   # vervang /bin/false door de echte opdracht
}

# --- argumenten -----------------------------------------------------------------------------------------
IDS_BESTAND="" VERWACHT="" UITVOEREN=0
while [ "$#" -gt 0 ]; do
  case "$1" in
    --ids)       IDS_BESTAND="${2:?--ids vraagt een bestand}"; shift 2 ;;
    --verwacht)  VERWACHT="${2:?--verwacht vraagt een aantal}"; shift 2 ;;
    --uitvoeren) UITVOEREN=1; shift ;;
    *) echo "gebruik: bulk.sh --ids <bestand> --verwacht <n> [--uitvoeren]" >&2; exit 2 ;;
  esac
done
[ -n "$IDS_BESTAND" ] && [[ "$VERWACHT" =~ ^[0-9]+$ ]] && [[ "$PLAFOND_PER_DAG" =~ ^[0-9]+$ ]] \
  || { echo "gebruik: bulk.sh --ids <bestand> --verwacht <n> [--uitvoeren]" >&2; exit 2; }

install -d -m 700 -- "$STAAT"
exec 9>"$STAAT/bulk.lock"
flock -n -E 75 9 || { rc=$?; [ "$rc" -eq 75 ] && { echo "draait al, overgeslagen"; exit 0; }; exit "$rc"; }

# --- selectie: exacte id's van een soort, geteld en vergeleken (ARCH-28, SCR-47) ------------------------
mapfile -t ids < "$IDS_BESTAND"
[ "${#ids[@]}" -gt 0 ] || { echo "fout: geen id's in $IDS_BESTAND; een lege selectie betekent nooit alles" >&2; exit 1; }
[ "${#ids[@]}" -eq "$VERWACHT" ] || { echo "fout: ${#ids[@]} items, verwacht $VERWACHT" >&2; exit 1; }
for id in "${ids[@]}"; do
  [[ "$id" =~ ^[0-9]+$ ]] || { echo "fout: ongeldig id: '$id'" >&2; exit 1; }
done

# --- hulpfuncties: elke leesfout is een harde stop (SCR-46) ---------------------------------------------
schakelaar_aan() {
  local stand
  stand=$(cat -- "$SCHAKELAAR") || return 1
  [ "$stand" = "aan" ]
}
pogingen_vandaag() {
  [ -e "$LOGBOEK" ] || { echo 0; return 0; }
  awk -F'\t' -v d="$(TZ=Europe/Amsterdam date +%F)" '$1 == d && $4 == "bezig" { n++ } END { print n + 0 }' "$LOGBOEK"
}
open_items() {   # id's waarvan de laatste staat "bezig" of "onzeker" is
  [ -e "$LOGBOEK" ] || return 0
  awk -F'\t' '{ laatste[$3] = $4 } END { for (i in laatste) if (laatste[i] == "bezig" || laatste[i] == "onzeker") print i }' "$LOGBOEK"
}
noteer() {       # noteer <id> <staat>
  printf '%s\t%s\t%s\t%s\n' "$(TZ=Europe/Amsterdam date +%F)" "$(date -u +%FT%TZ)" "$1" "$2" >> "$LOGBOEK"
}

# --- automatische pauze (SCR-45) ------------------------------------------------------------------------
open=""
open=$(open_items)
if [ -n "$open" ]; then
  echo "fout: lijn gepauzeerd, onbeoordeelde items (bezig of onzeker): $(echo "$open" | tr '\n' ' ')" >&2
  exit 1
fi

# --- de lus: schakelaar en plafond vlak voor elke afzonderlijke actie (SCR-46) --------------------------
gedaan=0
for id in "${ids[@]}"; do
  schakelaar_aan || { echo "gestopt: noodstop staat niet op 'aan' of is niet leesbaar" >&2; exit 1; }
  n=""
  n=$(pogingen_vandaag)
  [ "$n" -lt "$PLAFOND_PER_DAG" ] || { echo "gestopt: dagplafond $PLAFOND_PER_DAG bereikt ($n pogingen)" >&2; exit 1; }

  if [ "$UITVOEREN" -ne 1 ]; then
    echo "proef: zou verwerken: $id"
    continue
  fi

  noteer "$id" bezig                      # de poging ligt vast voor het effect (SCR-45)
  rc=0
  verwerk "$id" || rc=$?
  case "$rc" in
    0)   noteer "$id" klaar; gedaan=$((gedaan + 1)) ;;
    124|137) noteer "$id" onzeker         # time-out: onbekend is "gebeurd", niet opnieuw proberen (SCR-45)
         echo "gestopt: uitkomst van $id onbekend (time-out); lijn gepauzeerd tot beoordeling" >&2; exit 1 ;;
    *)   noteer "$id" mislukt
         echo "gestopt: $id mislukt met exitcode $rc; lijn stopt bij de eerste fout" >&2; exit 1 ;;
  esac
done

if [ "$UITVOEREN" -eq 1 ]; then echo "klaar: $gedaan van ${#ids[@]} verwerkt"
else echo "proef klaar: ${#ids[@]} items, niets gewijzigd; start opnieuw met --uitvoeren"; fi
