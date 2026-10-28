<!--
Sjabloon: SECURITY.md in de root van de repository.
Dekt: PRIV-72, GIT-30, INFRA-65 (samen met security.txt)
Aanpassen: alles tussen < en >.
Reactietermijnen (besluit van Marketing Maatwerk, 05-10-2026): ontvangstbevestiging binnen 1 werkdag, eerste beoordeling binnen
  5 werkdagen. Het onderzoek eist dat er een termijn staat (PRIV-72), niet welke: de 5 werkdagen zijn een eigen
  voorstel zonder bron, de 1 werkdag is een keuze van Marketing Maatwerk. Het is een belofte aan buitenstaanders: pas de
  getallen alleen aan met een besluit van Marketing Maatwerk. De wettelijke meldtermijn van 24 uur bij een actief uitgebuite kwetsbaarheid in een
  product (PRIV-71) is jouw plicht, geen belofte aan de melder.
Controleren (PRIV-72): SECURITY.md bestaat, /.well-known/security.txt bestaat op de productsite, het adres staat
  in de readme van het pakket, en een testbericht naar het adres komt aan.
-->

# Beveiligingsbeleid

## Een kwetsbaarheid melden

Meld een kwetsbaarheid per e-mail aan <security@voorbeeld.nl>. Meld hem niet via een publiek issue.

Zet in je melding:

- welk product en welke versie het betreft;
- wat je hebt gevonden en hoe het te reproduceren is;
- wat een aanvaller ermee zou kunnen.

## Wat je van mij mag verwachten

- Een ontvangstbevestiging binnen 1 werkdag.
- Een eerste beoordeling binnen 5 werkdagen, met een inschatting van de ernst en een verwachte hersteldatum.
- Bericht zodra het herstel beschikbaar is.
- Geen juridische stappen als je je aan de afspraken hieronder houdt.

## Wat ik van jou verwacht

- Geef mij de tijd om het te herstellen voordat je erover publiceert; we spreken samen een datum af.
- Gebruik de kwetsbaarheid niet verder dan nodig is om hem aan te tonen.
- Bekijk, wijzig of verwijder geen gegevens van anderen.
- Geen aanvallen op de beschikbaarheid, geen social engineering en geen spam.

## Ondersteunde versies

| Versie | Beveiligingsupdates tot |
|---|---|
| <versie> | <datum> |

Beveiligingsupdates zijn kosteloos en komen los van nieuwe functies (PRIV-74).
