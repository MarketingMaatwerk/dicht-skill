# SCR C: Bestanden, tijdelijke bestanden, verwijderen en rechten

Compacte regels van `dicht-scripts`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/scripts-automatisering.md` (regelnummer in `regel-index.tsv`).

### SCR-14 Maak tijdelijke bestanden met mktemp en ruim ze op met een trap
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak elk tijdelijk bestand en elke tijdelijke map met `mktemp` of `mktemp -d`, nooit met een vaste naam in `/tmp`, nooit met `$$` in de naam en nooit met `mktemp -u`; ruim op in een EXIT-trap (SCR-04).
- Bewijs: `/usr/bin/grep -nE '(>|>>|-o|=) *"?/tmp/[A-Za-z0-9._-]+' $(git ls-files '*.sh' '*.py')` en `/usr/bin/grep -nE 'mktemp +-u|\$\$' $(git ls-files '*.sh')` zijn leeg of elke treffer is verklaard; in een unit staat `PrivateTmp=yes` (INFRA-67). Afgevinkt met de uitvoer.
- Norm: ASVS 5.0.0 V15.4.2 (L3, TOCTOU); CWE-377.
- Zie ook: INV-68, INV-69, SCR-31, SCR-04

### SCR-15 Bewaak elk pad dat je recursief verwijdert of overschrijft
kritiek · hard · alles · tegenlezer: scherpen (04-10-2026)
- Regel: Schrijf een recursieve verwijdering alleen als `rm -rf -- "${MAP:?}/vast-deel"` met een absoluut pad, controleer vooraf dat het pad binnen de bedoelde basismap ligt (`case "$(realpath -- "$MAP")" in /srv/app/*) ;; *) exit 1 ;; esac`), en laat `cd` nooit zonder controle voorafgaan aan een verwijdering.
- Bewijs: `shellcheck -i SC2115,SC2164 $(git ls-files '*.sh')` geeft geen meldingen; `/usr/bin/grep -nE 'rm +-[a-z]*r[a-z]* ' $(git ls-files '*.sh')` toont bij elke treffer een absoluut pad met `:?` of een voorafgaande grenscontrole; een test met een lege variabele en met `..` in het argument eindigt met een fout zonder iets te verwijderen. Afgevinkt met de drie uitvoeren. Voor bulkverwijdering in een database of op een site geldt ARCH-28.
- Norm: ASVS 5.0.0 V5.3.2 (L1); past ruim. BRIEF besluit 19 (niets wijzigen zonder akkoord, dus ook niet verwijderen op live).
- Zie ook: API-54, AI-46, WP-25, API-76, WEB-45, WP-29, INV-41, INV-34, ARCH-28, SCR-47, ARCH-51

### SCR-16 Zet umask 077 in elk script dat geheimen, persoonsgegevens of logs schrijft
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Zet `umask 077` bovenaan elk script dat een bestand met een geheim, persoonsgegevens, een export of een log aanmaakt, en gebruik `install -m 600` als je een bestaand bestand op zijn plek zet.
- Bewijs: `/usr/bin/grep -L 'umask 077' $(/usr/bin/grep -lE 'pg_dump|> .*\.(csv|sql|log|json)|\.env' $(git ls-files '*.sh'))` is leeg; `stat -c '%a %n'` op de bestanden die het script schrijft toont 600 (of 640 met een bewuste groep). Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V16.4.2 (L2, "logs are protected from unauthorized access"), V13.3.2 (L2).
- Zie ook: INFRA-76, SCR-19, SCR-20, SCR-05, SCR-13, SCR-50, MSG-41, AI-28

### SCR-17 Schrijf een bestand dat een ander proces leest atomair
middel · richtlijn · website | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Schrijf een bestand dat door een dienst, een webserver of een ander script wordt gelezen eerst naar een tijdelijk bestand in dezelfde map en zet het daarna met `mv` op zijn plek; bouw een map als nieuwe map en wissel met een symbolische koppeling (`ln -sfn` naar een nieuwe naam plus `mv -T`).
- Bewijs: In elk script dat een bestand voor een ander proces schrijft staat het patroon tijdelijk bestand plus `mv` in dezelfde map; een test waarin het genereren met opzet faalt laat het oude bestand ongewijzigd (`sha256sum` voor en na gelijk). Afgevinkt met de testuitvoer.
- Norm: ASVS 5.0.0 V2.3.3 (L2, een bewerking slaagt geheel of wordt teruggedraaid); past ruim.
