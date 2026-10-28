# API H: cryptografie en geheimen in code

Compacte regels van `dicht-api`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/api-code.md` (regelnummer in `regel-index.tsv`).

### API-61 Maak onraadbare waarden met een CSPRNG en minimaal 128 bits
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Genereer tokens, sleutels, resetcodes en eenmalige links met `crypto.randomBytes(32)` (Node) of `random_bytes(32)` (PHP); gebruik nooit `Math.random`, `mt_rand`, `rand`, `uniqid`, een tijdstempel of een oplopend id.
- Bewijs: `grep -rnE "Math\.random|mt_rand|\brand\(|uniqid\(" src` is leeg in code die tokens, namen van privébestanden of codes maakt. Een UUID v4 mag als id, niet als geheim.
- Norm: ASVS 5.0.0 V11.5.1 (L2).

### API-62 → AUTH-57
Samengevoegd: "Vergelijk geheimen in constante tijd" is gedekt door AUTH-57. Gebruik die regel.

### API-63 Kies bewust tussen hashen en versleutelen
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Hash wat je alleen hoeft te herkennen (API-sleutels, tokens: SHA-256 van een waarde met hoge entropie; wachtwoorden: zie AUTH), versleutel wat je terug moet kunnen lezen met geauthenticeerde versleuteling (AES-256-GCM of libsodium secretbox) met per bericht een nieuwe nonce, en gebruik MD5 en SHA-1 nergens voor beveiliging.
- Bewijs: `grep -rnE "createCipher\(|aes-...-(ecb|cbc)|md5|sha1" src` wordt per treffer beoordeeld. De kolom voor API-sleutels bevat een hash; alleen de eerste tekens staan leesbaar voor herkenning. Test: twee keer dezelfde tekst versleutelen geeft verschillende uitvoer.
- Norm: ASVS 5.0.0 V11.3.1 (L1), V11.3.2 (L1), V11.3.3 (L2), V11.3.4 (L3), V11.4.1 (L1).

### API-64 Schrijf geen eigen cryptografie
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor elke cryptografische bewerking `node:crypto`, WebCrypto, libsodium of de ingebouwde PHP-functies (`sodium_*`, `password_hash`, `hash_hmac`), en zet algoritme en sleutelversie bij de opgeslagen waarde zodat wisselen later mogelijk is.
- Bewijs: Review: elke plek waar een handtekening of sleutel wordt gemaakt gebruikt HMAC of een bibliotheekfunctie. Opgeslagen versleutelde waarden hebben een voorvoegsel met versie.
- Norm: ASVS 5.0.0 V11.2.1 (L2), V11.2.2 (L2).

### API-65 Houd geheimen uit code en build en valideer ze bij de start
kritiek · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Lees geheimen alleen uit de omgeving of een secrets-bestand buiten de repository, valideer bij het opstarten met een schema dat ze er zijn en de juiste vorm hebben, en laat het proces niet starten als er een ontbreekt; geef geen standaardwaarde aan een geheim. Zet een geheim ook nooit in een omgevingsvariabele die de bouwstap in de browsercode schrijft (`VITE_*`, `NEXT_PUBLIC_*` en dergelijke): die waarde staat daarna voor iedere bezoeker leesbaar in de bundel (aanscherping 28-10-2026, niet tegengelezen).
- Bewijs: `grep -rnE "process\.env\.[A-Z_]+ *(\|\||\?\?) *['\"]" src` toont geen geheimen. Een secret-scan (gitleaks) is groen; zie GIT en de skill `secrets-management`. Test: starten zonder een verplicht geheim eindigt met exitcode 1. Heeft het project een gebouwde voorkant (aanscherping 28-10-2026, niet tegengelezen): na de build is `gitleaks dir <buildmap>` (bijvoorbeeld `dist/`, `.next/static/` of de map met gebouwde JS en CSS van een thema) groen, en `grep -rnsE '(VITE|NEXT_PUBLIC|NUXT_PUBLIC|REACT_APP|EXPO_PUBLIC|PUBLIC)_[A-Z0-9_]*(KEY|SECRET|TOKEN|PASS)' <elke bronmap van de voorkant: src, app, pages, components> .env*` eindigt met exitcode 1 (niets gevonden), of toont alleen sleutels die de aanbieder zelf als publiek bedoelt (bijvoorbeeld een publishable key) met die reden erbij; exitcode 2 (map of bestand bestaat niet) telt als `niet gemeten`. Afgevinkt met de uitvoer van beide.
- Norm: ASVS 5.0.0 V13.3.1 (L2), V13.2.3 (L2).
- Zie ook: INFRA-72, GIT-32, GIT-95, DB-62, AI-28, WP-33, INFRA-76, WP-71, DB-61, AI-60, ARCH-49

### API-66 Log geen geheimen en geen persoonsgegevens
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel log-redactie in voor `authorization`, `cookie`, handtekening-headers, wachtwoorden, tokens en betaalgegevens, log geen volledige request-body's, en schrijf logs als gestructureerde JSON zodat invoer geen logregels kan vervalsen.
- Bewijs: De logger-configuratie bevat `redact`. Test: een verzoek met een herkenbare nepwaarde in `Authorization` en in een wachtwoordveld; daarna `grep` op die waarde in de logs is leeg. Zie ARCH voor logretentie en PRIV voor persoonsgegevens.
- Norm: ASVS 5.0.0 V16.2.5 (L2), V16.4.1 (L2), V14.2.4 (L2).
- Zie ook: ARCH-62, DB-88, INFRA-88, AUTH-14, AI-67, AI-52, GIT-39
