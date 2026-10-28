# daemon.json: begrensde containerlogs

Dekt: INFRA-33

`daemon.json` is letterlijk het voorbeeld uit INFRA-33 (JSON kent geen commentaar, daarom staat de uitleg hier).

- Plek: `/etc/docker/daemon.json`. Staat er al een bestand, voeg dan alleen de twee sleutels toe.
- Aanpassen: `max-size` en `max-file` zijn de voorbeeldwaarden uit de regel; leg de gekozen bewaartermijn vast in het logoverzicht (INFRA-88).
- De instelling geldt alleen voor nieuwe containers: maak bestaande containers daarna opnieuw aan (INFRA-33). Het herstarten van de Docker-daemon raakt alle containers en is een bewuste ingreep, niet iets wat een sessie zelf doet.
- Controleren: `docker info --format '{{.LoggingDriver}}'` toont `local`; `docker inspect <container> --format '{{.HostConfig.LogConfig}}'` toont de driver en de grenzen.
- Niet gevalideerd op de server met Docker (geen docker-opdrachten gedraaid); het bestand laadt als JSON.
