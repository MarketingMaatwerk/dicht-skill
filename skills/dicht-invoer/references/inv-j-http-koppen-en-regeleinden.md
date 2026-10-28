# INV J: HTTP-koppen en regeleinden

Compacte regels van `dicht-invoer`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/invoer-bestandsformaten.md` (regelnummer in `regel-index.tsv`).

### INV-48 Weiger regeleinden en tekens buiten ASCII voordat een waarde in een antwoordkop komt
middel · hard · api | app | mcp | website | klantproject · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Zet een waarde van buiten alleen in een antwoordkop (`Location`, `Content-Disposition`, `Set-Cookie`, een eigen `X-`-kop) nadat CR, LF en NUL zijn geweigerd, en stel `Content-Disposition` samen met een bibliotheek die de bestandsnaam volgens RFC 6266 en RFC 5987 (opgevolgd door RFC 8187) codeert (`content-disposition`).
- Bewijs: Test per route die een waarde van buiten in een kop zet: de waarden `a\r\nSet-Cookie: x=1`, `a%0d%0aX: y` en een naam met `€` en Cyrillische letters geven 400 of een geldig antwoord met een gecodeerde `filename*=UTF-8''...`, nooit 500 en nooit een extra kop (`curl -si`). Afgevinkt met de uitvoer. Zie WEB-47.
- Norm: ASVS 5.0.0 V5.4.2 (L2), V1.2.1 (L1), V4.2.4 (L3).
- Zie ook: WEB-68, INV-56, INV-49, INV-50, MSG-04, MSG-26

### INV-49 Bouw uitgaande aanvragen met URL-objecten en vaste kopwaarden
hoog · hard · api | app | mcp | wp-plugin | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Stel het adres van een uitgaande aanvraag samen met `new URL()` en `URLSearchParams` (of `encodeURIComponent` per padsegment), en zet een waarde van buiten alleen in een kop van die aanvraag na de controle uit INV-48.
- Bewijs: `grep -rnE "fetch\(\s*\`[^\`]*\\$\{" src` toont geen invoer die zonder `encodeURIComponent` in een pad staat; test per uitgaande koppeling met een waarde die `/`, `?`, `#`, `%0d%0a` en `..` bevat: de nepserver ziet precies één aanvraag op het bedoelde pad met de waarde gecodeerd. Afgevinkt met grep en test. Zie API-48 en WEB-40.
- Norm: ASVS 5.0.0 V1.2.2 (L1), V1.3.6 (L2).
- Zie ook: INV-48, WEB-68, INV-56, INV-50, MSG-04, MSG-26

### INV-50 Gebruik in nginx geen $uri in een redirect, een kop of een doorgegeven adres
hoog · hard · website | api | app | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik in `return`, `rewrite`, `add_header`, `proxy_set_header` en `proxy_pass` nooit `$uri` of `$document_uri`, maar `$request_uri` (de aanvraag zoals de client hem stuurde).
- Bewijs: `nginx -T 2>/dev/null | grep -nE "(return|rewrite|add_header|proxy_set_header|proxy_pass)[^;]*\$(uri|document_uri)"` is leeg (Zie INFRA-03: lees de effectieve configuratie); `curl -si "https://<host>/%0d%0aX-Test:%201"` toont geen kop `X-Test`. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V1.2.1 (L1), V4.2.4 (L3).
- Zie ook: INV-48, WEB-68, INV-56, INV-49, MSG-04, MSG-26
