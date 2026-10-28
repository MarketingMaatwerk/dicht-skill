# DB G: data-integriteit en transacties

Compacte regels van `dicht-database`. Waarom, aanvalsvoorbeeld, fout en goed, bron en de toelichting van de tegenlezer staan per ID in `research/database.md` (regelnummer in `regel-index.tsv`).

### DB-66 → API-32
Samengevoegd: "Eén bedrijfshandeling is één transactie" is gedekt door API-32. Gebruik die regel.

### DB-67 → API-30
Samengevoegd: "Controleren en handelen gebeurt atomair" is gedekt door API-30. Gebruik die regel.

### DB-68 Verwerk webhooks en opdrachten idempotent met een unieke sleutel
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Sla de externe gebeurtenis-id (Mollie-betaling, webhook-id, idempotency-key) op in een kolom met een unieke constraint en schrijf met `INSERT ... ON CONFLICT DO NOTHING`; voer het gevolg alleen uit als de insert een rij opleverde, in dezelfde transactie.
- Bewijs: Test die dezelfde webhook twee keer parallel aanbiedt en één gevolg telt; `\d verwerkte_events` toont de unieke index. Afgevinkt als beide kloppen.
- Norm: ASVS 5.0.0 2.3.4 (L2), 15.4.2 (L3).
- Zie ook: API-30, API-31, API-33, API-38, ARCH-18, AUTH-59, BIZ-30, BIZ-34, BIZ-35, BIZ-39, BIZ-41, BIZ-43, BIZ-46

### DB-69 Wie een strenger isolatieniveau kiest, bouwt de herhaling erbij
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Gebruik `REPEATABLE READ` of `SERIALIZABLE` alleen met een lus die de hele transactie opnieuw uitvoert bij SQLSTATE `40001` (en `40P01` bij een deadlock), met een maximum aantal pogingen.
- Bewijs: `grep -rn "serializable\|repeatable read" src/` en bij elke treffer een herhaallus met test. Afgevinkt als elke treffer een lus heeft, of er geen treffers zijn.
- Norm: ASVS 5.0.0 16.5.3 (L2).

### DB-70 Leg regels vast in de database: NOT NULL, CHECK, UNIQUE en foreign keys
hoog · hard · api | app | mcp | klantproject · tegenlezer: bevestigd (04-10-2026)
- Regel: Geef elke kolom die niet leeg mag zijn `NOT NULL`, elke relatie een foreign key met een bewuste `ON DELETE`, elke uniciteitsregel een unieke constraint en elke waardegrens een `CHECK`; vertrouw niet alleen op validatie in de applicatie.
- Bewijs: Review van het schema per tabel; test die ongeldige waarden rechtstreeks met SQL probeert in te voegen en een fout verwacht. Afgevinkt als de test voor de kerntabellen bestaat.
- Norm: ASVS 5.0.0 2.3.2 (L2).

### DB-71 Wachtrijtabellen lezen met FOR UPDATE SKIP LOCKED
middel · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat workers taken uit een tabel claimen met `SELECT ... FOR UPDATE SKIP LOCKED` in een korte transactie, en gebruik dat nergens anders.
- Bewijs: Test met twee parallelle workers en N taken: elke taak precies één keer verwerkt. Afgevinkt als die test bestaat voor elke tabel die als wachtrij dient.
- Norm: ASVS 5.0.0 15.4.2 (L3).
- Zie ook: ARCH-19, API-23, ARCH-18, ARCH-20, BIZ-42

### DB-72 Neem locks in een vaste volgorde
laag · richtlijn · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Laat transacties die meerdere rijen of tabellen wijzigen dat altijd in dezelfde volgorde doen (bijvoorbeeld oplopend op id).
- Bewijs: Codereview bij transacties met meer dan één `UPDATE`; `log_lock_waits` (DB-90) toont geen terugkerende deadlocks. Afgevinkt als het serverlog over 30 dagen geen "deadlock detected" bevat of elke melding is verklaard.
- Norm: ASVS 5.0.0 15.4.3 (L3).

### DB-73 Houd transacties kort: geen netwerkaanroepen binnen een transactie
middel · hard · api | app | mcp · tegenlezer: bevestigd (04-10-2026)
- Regel: Doe binnen een open transactie geen HTTP-aanroepen, geen AI-aanroepen, geen mailverzending en geen wachten op gebruikersinvoer; haal gegevens op, sluit de transactie, doe de aanroep, en open een nieuwe transactie voor het resultaat.
- Bewijs: Codereview op `db.transaction(` en `sql.begin(` met een zoekopdracht naar `fetch(`, `axios`, mail- en modelclients binnen de callback; `SELECT count(*) FROM pg_stat_activity WHERE state = 'idle in transaction' AND now() - state_change > interval '10 seconds';` is nul onder normale belasting. Afgevinkt als beide kloppen en DB-65 als vangnet is ingesteld.
- Norm: ASVS 5.0.0 15.2.2 (L2).
