#!/usr/bin/env bash
# Sjabloon: stuurt een korte foutmelding naar het alarmkanaal (een webhook).
# Dekt: INFRA-69, SCR-01, SCR-06, SCR-19, SCR-21, MSG-41, ARCH-62
# Aanpassen: de vorm van de body als het kanaal iets anders dan {"content": "..."} verwacht.
# Het webhookadres komt uit $CREDENTIALS_DIRECTORY/webhook_url (LoadCredential in meld-fout@.service) of, uit
#   cron, uit het bestand in ALARM_WEBHOOK_BESTAND, en wordt via een configuratiebestand op standaardinvoer aan curl gegeven, nooit als argument (SCR-19).
# De melding bevat alleen de naam van de unit en de host: geen logregels, geen geheimen, geen persoonsgegevens
#   (ARCH-62, MSG-48).
# Controleren: bash -n meld-fout.sh; shellcheck --severity=warning meld-fout.sh (SCR-23).
set -euo pipefail

UNIT="${1:?gebruik: meld-fout.sh <unit>}"
[[ "$UNIT" =~ ^[A-Za-z0-9@_.:-]+$ ]] || { echo "fout: ongeldige unitnaam" >&2; exit 2; }

# Onder systemd: het credential van de unit. Uit cron: het pad in ALARM_WEBHOOK_BESTAND (modus 600).
if [ -n "${CREDENTIALS_DIRECTORY:-}" ]; then
  BRON="$CREDENTIALS_DIRECTORY/webhook_url"
else
  BRON="${ALARM_WEBHOOK_BESTAND:?zet ALARM_WEBHOOK_BESTAND of start via de unit}"
fi
[ -r "$BRON" ] || { echo "fout: webhookadres niet leesbaar" >&2; exit 1; }

HOST=$(hostname)
BODY=$(printf '{"content":"Unit %s op %s is mislukt. Zie het journal."}' "$UNIT" "$HOST")

# url en body gaan via standaardinvoer naar curl; in ps staat alleen "curl -K -".
{
  printf 'url = "%s"\n' "$(tr -d '\r\n' < "$BRON")"
  printf 'header = "Content-Type: application/json"\n'
  printf 'data = "%s"\n' "${BODY//\"/\\\"}"
} | curl --silent --show-error --fail --proto '=https' --connect-timeout 10 --max-time 30 -K - >/dev/null
