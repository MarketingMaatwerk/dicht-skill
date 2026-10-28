# GIT B: GitHub-account en toegang

Compacte regels van `dicht-git`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/git-supplychain.md` (regelnummer in `regel-index.tsv`).

### GIT-14 Beveilig het GitHub-account met TOTP plus een passkey, zonder sms
kritiek · hard · alles · tegenlezer: scherpen (04-10-2026)
- Regel: Zet tweestapsverificatie aan met een TOTP-app als eerste methode, voeg een passkey of beveiligingssleutel toe, verwijder sms als methode, en bewaar de herstelcodes buiten de wachtwoordmanager waarin het wachtwoord staat.
- Bewijs: In Settings, Password and authentication staan TOTP en minstens één passkey of sleutel, en geen sms; de herstelcodes liggen op een tweede plek (noteer waar, niet de codes). Afgevinkt met een notitie met datum. Let op: GitHub staat een passkey of sleutel niet toe als eerste 2FA-methode; er moet eerst 2FA via een TOTP-app (of sms, wat deze regel afraadt) zijn ingesteld.
- Norm: NIST SSDF PO.5.1 (voorbeeld 1: multifactor voor elke omgeving); OWASP CI/CD CICD-SEC-2 Inadequate Identity and Access Management; zie AUTH-16 en AUTH-18.
- Zie ook: AUTH-16, AUTH-82, WP-58, INFRA-98, PRIV-53, INFRA-11

### GIT-15 Gebruik tokens met een einddatum en de kleinste reikwijdte
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik voor elke toepassing een eigen fine-grained token dat alleen de benodigde repo's en rechten heeft en binnen 90 dagen verloopt, en vervang elk klassiek token met de scope `repo` of `workflow`.
- Bewijs: De lijst onder Settings, Developer settings toont geen klassiek token met `repo` of `workflow`; elk fine-grained token heeft een einddatum en een beschreven doel. Op de server: `gh api -i user | grep -i x-oauth-scopes`. Afgevinkt met de lijst.
- Norm: ASVS 5.0.0 V13.3.2 (L2, minimale rechten voor geheimen), V13.3.4 (L3, verloop en rotatie); OWASP CI/CD CICD-SEC-6; zie AUTH-54.

### GIT-16 Geef een server alleen een deploy key met leesrecht op één repo
hoog · hard · klantproject | api | app | website · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat een server of bouwmachine code ophalen met een deploy key zonder schrijfrecht voor precies die repo, en zet nooit een persoonlijk token of de eigen SSH-sleutel op een machine die code van anderen draait.
- Bewijs: `gh api repos/<eigenaar>/<repo>/keys --jq '.[]|{title,read_only}'` toont `read_only: true`; op de server staat geen `~/.config/gh/hosts.yml` en geen sleutel die ook op het account is geregistreerd. Afgevinkt met de uitvoer. Voor de eigen VPS, waar ook ontwikkeld wordt, geldt GIT-15 en GIT-11.
- Norm: ASVS 5.0.0 V13.3.2 (L2); OWASP CI/CD CICD-SEC-2 en CICD-SEC-6; zie AUTH-56.

### GIT-17 SSH-sleutels: ed25519, met wachtwoordzin, één per machine
middel · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Maak per machine een eigen sleutel met `ssh-keygen -t ed25519`, zet er een wachtwoordzin op waar een mens hem gebruikt, en verwijder sleutels van machines die je niet meer gebruikt.
- Bewijs: `gh api user/keys --jq '.[]|{title,created_at}'` (of de pagina SSH and GPG keys) toont per sleutel een herkenbare machine en geen sleutel ouder dan de machine; `ssh-keygen -y -P "" -f ~/.ssh/id_ed25519 >/dev/null` faalt op een sleutel met wachtwoordzin. Afgevinkt met beide.
- Norm: NIST SSDF PO.5.2; OWASP CI/CD CICD-SEC-6.

### GIT-18 Onderteken commits en tags
middel · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Onderteken in elke repo die op GitHub staat alle commits en tags met een SSH-sleutel (`gpg.format ssh`, `user.signingkey`, `commit.gpgsign true`, `tag.gpgsign true`), registreer de sleutel op GitHub als signing key, en houd lokaal een `allowed_signers`-bestand bij.
- Bewijs: `git log -1 --format='%G? %GS'` geeft `G` met de naam uit `allowed_signers`; op GitHub staat "Verified" bij de commit. Afgevinkt met de uitvoer. SSH-ondertekening vraagt git 2.34 of hoger; de server zit precies op die grens. Zonder `allowedSignersFile` faalt `git verify-commit` lokaal.
- Norm: NIST SSDF PS.1.1 (voorbeeld 3: "Use commit signing for code repositories"); besluit 15.

### GIT-19 Zet vigilant mode pas aan als alles ondertekend is
laag · richtlijn · alles · tegenlezer: gecorrigeerd (04-10-2026)
- Regel: Zet in het account "Flag unsigned commits as unverified" aan zodra GIT-18 op elke machine werkt.
- Bewijs: Een testcommit zonder handtekening toont op GitHub "Unverified". Afgevinkt met een schermafbeelding of de API-uitvoer `gh api repos/<o>/<r>/commits/<sha> --jq .commit.verification`.
- Norm: NIST SSDF PS.1.1.

### GIT-20 Geef anderen toegang via een organisatie of een deploy key, niet als collaborator
middel · richtlijn · klantproject | alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef een klant, freelancer of student die alleen moet lezen geen collaborator-rol op een privé-repo van het persoonlijke account, maar een export, een deploy key of een plek in een organisatie met een leesrol.
- Bewijs: `gh api repos/<o>/<r>/collaborators --jq '.[].login'` toont alleen wie moet kunnen schrijven; elke naam heeft een reden en een einddatum in de notitie. Afgevinkt met de lijst. Zie AUTH-85 voor het intrekken bij vertrek.
- Norm: OWASP CI/CD CICD-SEC-2; NIST SSDF PS.1.1.

### GIT-21 Loop per kwartaal sessies, sleutels, tokens en apps na
middel · richtlijn · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Controleer elk kwartaal in het account de actieve sessies, SSH-sleutels, tokens, geautoriseerde OAuth- en GitHub-apps en het security log, en trek in wat je niet herkent of niet meer gebruikt.
- Bewijs: Een notitie met datum en per onderdeel het aantal en wat is ingetrokken. Afgevinkt met de notitie. GitHub verwijdert tokens die een jaar niet zijn gebruikt zelf; dat is geen vervanging van deze controle.
- Norm: OWASP CI/CD CICD-SEC-2 en CICD-SEC-10 Insufficient Logging and Visibility.

### GIT-22 Maak een repo alleen publiek na een scan van de hele geschiedenis
hoog · hard · alles · tegenlezer: bevestigd (04-10-2026)
- Regel: Houd elke repo privé tenzij publiek een besluit is, en scan vóór het publiek maken de volledige geschiedenis op geheimen en klantgegevens; begin bij twijfel een nieuwe repo zonder geschiedenis.
- Bewijs: `gitleaks git --redact .` en `trufflehog git file://. --results=verified,unknown --fail` zijn schoon op de volledige geschiedenis (GIT-34), en het besluit staat genoteerd. Afgevinkt met beide uitvoeren.
- Norm: ASVS 5.0.0 V13.3.1 (L2); OWASP Top 10 2025 A02 Security Misconfiguration.
