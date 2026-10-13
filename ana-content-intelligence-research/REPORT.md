# ANA Content Acquisition & Intelligence — Deep Research

**Stichtag:** 2026-10-13 · **Evidenzlegende:** `TESTED_OK` · `TESTED_FAIL` · `FACT_VERIFIED` ·
`VENDOR_CLAIM` · `CONDITIONAL` · `UNKNOWN` · `BLOCKED` · `NOT_TESTED_ACCESS_BLOCKED`
**Detailtests:** siehe `TEST_LOG.md` · **Maschinenlesbar:** siehe `results.json` · **Pilot-Code:** `scripts/pilot_pipeline.py`

---

## 1. Executive Decision

**Empfehlung (heute startbar, ohne eigene API-Entwicklung): Architektur A+ — „Originale zuerst, yt-dlp als Fallback, Apify nur für Metadaten/Kommentare".**

1. **Primärquelle sind Anas Originaldateien** (MOV/MP4 aus Handy/Cloud/Schnittprojekt) + **native Exporte** (YouTube Studio, TikTok Studio CSV, Meta Business Suite). Das ist die einzige Quelle mit echten Dateien, voller Historie der eigenen Uploads und Creator-Analytics (Watchtime, Saves, Retention) — ohne Login-Risiko bei Dritten, ohne Scraper-Kosten. `FACT_VERIFIED` (Exportwege existieren, §4.1), konkrete Feldabdeckung in Anas Accounts: `SOURCE_NEEDED` (nur sie kann exportieren).
2. **Lücken füllen mit `yt-dlp`** (kostenlos, aktiv gewartet, `FACT_VERIFIED` GitHub-Push 2026-10-10) für öffentliche YouTube-/TikTok-Einzel-URLs: echte Mediendatei + `info.json`, `--download-archive` = eingebaute Dedup. Instagram per yt-dlp/Instaloader nur `CONDITIONAL` (Login nötig, Kontorisiko — nicht mit Anas Hauptkonto).
3. **Apify nur punktuell** (Instagram Scraper, TikTok Scraper, Comments Scraper) für das, was yt-dlp nicht liefert: Instagram-Metadaten/Kommentare ohne eigenes Login. Kosten im Pilot: < 1 USD Datenvolumen (Rechnung §10). `VENDOR_CLAIM` für Felder/Vollständigkeit — vor Kauf mit 20-Post-Test verifizieren (§11). **Wichtig:** Apify liefert i. d. R. CDN-URLs, die ablaufen (bei Instagram-Media-Downloader dokumentiert ~24 h) — Medien sofort herunterladen und per SHA-256 ablegen, nie nur URLs archivieren.
4. **Verstehen lokal:** `faster-whisper` (Transkript + Zeitmarken, mehrsprachig — Ana publiziert u. a. ein „5 Sprachen"-Video, `FACT_VERIFIED` aus TikTok-Titel) + FFmpeg-Keyframes + PySceneDetect + Tesseract-OCR. Multimodale Cloud (Gemini/Twelve Labs) nur für eine Stichprobe von ~20 Posts, um zu prüfen, ob visuelles Verständnis über das Transkript hinaus Substack-relevante Aussagen liefert — sonst weglassen.
5. **Ablage:** Ordner + SQLite (Schema §7) + ein Google Sheet als Lese-/Freigabeansicht für Ana. Kein Data Warehouse, kein Vektorsystem, kein n8n, bis der Pilot Nutzen belegt.

**Was diese Empfehlung falsifizieren würde:** (a) yt-dlp scheitert auf Anas Rechner an >30 % der 20 Test-URLs, (b) Apify liefert im bezahlten Kleinsttest keine echten Video-Dateien/Kommentare, (c) Ana hat keine Originale mehr und Exporte decken <50 % der Historie ab → dann Architektur B (Apify-first) bzw. C prüfen (§5, §12).

**Variante C (vollautomatisch ohne Login/Schnittstelle) ist nicht seriös verfügbar** — Blocker §3.

---

## 2. Research Coverage

**Verifiziert am 2026-10-13:**

| Quelle | Befund | Status |
|---|---|---|
| YouTube `@anasavu` | Kanal „Ana Savu", Channel-ID `UCjzMuM_SuB5wkwFnN9ycaFg`; Bio: „sharing my travel adventures, daily vlogs and some making money while travelling ideas"; Crosslinks IG/TikTok bestätigt. Sichtbar: Shorts-Serie Camino de Santiago (u. a. `xfJScnaS-v4`, 261 Views; `Jwvh0YLIAJo`, 905 Views), Longform (Packing-Camino 8:00, `CUrmDg2seNA`; Siargao-Serie bis 10K Views/21:21), Sponsored Shorts (#NomadEsimPartner, #FiverrPartner), Collaborations (Pinoy Floyd 41:03, 10K; Calvin Castiel 26:08, 31K) | `TESTED_OK` (öffentliche Seite gelesen) |
| TikTok `@anasavu` | Direkt-Fetch HTTP 403 (Bot-Schutz, keine Umgehung). Über Suchindex verifiziert: Video `7472778649872239894` „Introducing myself in the 5 languages that I speak", 2025-02-18, 1.065 Likes / 57 Kommentare | Profil: `CONDITIONAL`; Einzelvideo-Metadaten: `FACT_VERIFIED` (Suchindex) |
| Instagram `@anasavu` | Kein direkter Lesezugriff in dieser Umgebung möglich; Existenz über YouTube-Bio + Substack-Bio („@anasavu on IG & TT") verifiziert. Inhalte/Follower: `UNKNOWN` | `BLOCKED` (für Detaildaten) |
| Substack **In-Between** | `https://anasavu.substack.com`, Publication-ID `6216941`, gegründet 2025-09-07, `payments_state=enabled`, Hero: „A newsletter for people figuring out how to build a life with more freedom. Travel, career pivots, making money online, content creation, side hustles, and the honest lessons in between." Archiv-API liefert **exakt 3 Newsletter** (limit=50): (1) 2026-10-11 „You Don't Need a Niche to Grow on Social Media in 2026" — **paid-only**, 2.149 Wörter, Tags Personal Branding/Content Creation/Social Media, 2 Reactions, 0 Kommentare; (2) 2026-09-16 „What's in my backpack: slow travel edition" — free, 686 Wörter, Tags Travel/Slow Travel/Solo Travel, 9 Reactions; (3) 2026-09-09 „Why I'm starting my Substack 1 week before I walk 280km to Santiago de Compostela" — free, 871 Wörter, 13 Reactions, 4 Kommentare. Dazu kuratierte Seiten „Start Here", „Travel", „Money & Work" | `TESTED_OK` |

**Tatsächliche Themen (aus verifizierten Titeln/Tags, keine Hochrechnung auf die Gesamthistorie):**
Solo-/Slow-Travel (Siargao, Camino, Porto), Pack-/Gear-Guides, Geld & Arbeit (9-to-5-Ausstieg London, Marketing→Creator, Side Hustles, Geld-online), Creator-Arbeit/Personal Branding (inkl. bezahlter Kooperationen Nomad eSIM, Fiverr, Bagsmart), Mehrsprachigkeit/persönliche Geschichte. **Das ist eine Stichprobe der öffentlich sichtbaren Oberfläche, keine gemessene Taxonomie** — die vollständige Clusterbildung braucht den Korpus aus §11. Followerzahlen, Postingfrequenz, Instagram-Inhalte, Watchtime: `UNKNOWN / SOURCE_NEEDED`.

**Suchansatz:** offizielle Produkt-/Store-Seiten, GitHub-API (Wartung/Archivstatus), Preis-Recherchen mit Datum, eigene Installations-/Lese-Tests (`TEST_LOG.md`). **Lücken:** keine Creator-Analytics (nur Ana), keine Instagram-/TikTok-Vollprofile, keine bezahlten Apify-Tests (keine Autorisierung zur Registrierung/Zahlung), Sandbox-Netz blockiert Plattform-Direktzugriff (T5/T6).

---

## 3. Drei Bedeutungen von „ohne API"

- **Variante A — keine eigene API-Programmierung: REALISTISCH und empfohlen.** GUI/No-Code (Apify Console, MacWhisper, native Exporte) + ein fertiges CLI-Skript (`pilot_pipeline.py`, kein eigener API-Code). Interne API-Nutzung der Tools ist dabei unschädlich.
- **Variante B — keine offizielle Social-API: REALISTISCH.** Originale + Plattform-Exporte + yt-dlp/öffentliche Apify-Akteure. Einschränkung Instagram: ohne eigenes Login liefern Drittanbieter nur öffentliche Daten in von ihnen kontrollierter Vollständigkeit (`CONDITIONAL`).
- **Variante C — vollautomatisch, ohne Login, Schnittstelle oder manuelle Handlung, dauerhaft zuverlässig: NICHT VERFÜGBAR.** Blocker: (1) Instagram verlangt seit 2023 für fast alles ein Login (Session/Cookies = faktisch Login, Kontosperr-Risiko); (2) TikTok/Instagram blockieren unauthentifizierte Automatisierung aktiv (403 im Test T3); (3) Creator-Analytics (Watchtime, Saves, Retention, Demografie) existieren nur hinter autorisiertem Login — kein Dritter kann sie liefern; (4) Plattform-ToS/technische Schutzmaßnahmen verbieten Umgehung. Wer Variante C verspricht, verkauft entweder ein Login-Risiko oder unvollständige Daten.

---

## 4. Tool-Matrix (≥12 Kandidaten)

Kurzform; vollständige Attribute je Tool in `results.json`. Preise: Stand 2026-10-09…13, Quellen dort.

| # | Tool | Plattformen / Zugriff | Echte Mediendatei? | Kommentare | Analytics | Transkript / Vision | Export | Kosten | Wartung | Urteil |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **Native Exporte** (YouTube Studio/Takeout, TikTok Studio CSV ≤60 Tage, Meta Accounts Center/Business Suite) | eigene, autorisiert | Ja (Takeout/Originale) | eigene teils | **Nur hier: Watchtime, Saves, Retention, Demografie** | nein | CSV/JSON/MP4 | kostenlos | Plattform | **Sofort geeignet (Primärquelle)** |
| 2 | **yt-dlp** 2026.08.19 | YT `TESTED_OK`-Design, TT/IG öffentlich, CLI | **Ja** | nur YT (Extractor), IG/TT nein | öffentlich (Views/Likes im info.json) | nein (Untertitel-Download möglich) | MP4 + info.json, `--download-archive` Dedup | kostenlos | Push 2026-10-10, 197K Stars `FACT_VERIFIED` | **Sofort geeignet** (YT/TT), IG `CONDITIONAL` |
| 3 | **Apify Instagram Scraper** (apify/instagram-scraper) | IG, kein Login | Nur CDN-URL (`CONDITIONAL`, Ablauf!) | Ja, als Event-Typ | öffentlich | nein | JSON/CSV/Excel, Scheduler | ab $1,50/1K Results (Business) bis $2,70/1K (Free-Plan) + Plattformplan | Store-Akteur, 388K Nutzer `VENDOR_CLAIM` | **Bedingt geeignet** — erst 20-Post-Test |
| 4 | **Apify Instagram Reel/Media Downloader** | IG, kein Login | **Ja, wenn Storage aktiviert** (sonst ~24-h-URL) | nein | öffentlich | nein | Datei in Key-Value-Store | ab $3,80/1K | `VENDOR_CLAIM` | Bedingt geeignet (Datei-Lieferant zu #3) |
| 5 | **Apify TikTok Scraper** (clockworks) + **TikTok Comments Scraper** | TT, kein Login | Video-URL im Datensatz, Download separat zu prüfen | **Ja** ($0,50/1K) | öffentlich (Plays/Likes/Shares) | nein | JSON/CSV, Scheduler | $1,70/1K Videos; Kommentare $0,50/1K | 275K Nutzer, Rating 4,76 `VENDOR_CLAIM` | **Bedingt geeignet** (bester TT-Metadatenweg ohne Login) |
| 6 | **Instaloader** | IG, **eigenes Login** | Ja | Ja (mit Login) | öffentlich | nein | Dateien + JSON | kostenlos | Push 2026-10-12 `FACT_VERIFIED` | **Ungeeignet mit Anas Hauptkonto** (Sperr-Risiko); nur Wegwerf-Konto + Freigabe |
| 7 | **gallery-dl** | IG/TT/300+ Sites, Browser-Cookies | Ja | nein (Metadaten-Sidecars) | öffentlich | nein | Dateien + JSON | kostenlos | Push 2026-10-09 `FACT_VERIFIED` | Bedingt geeignet (wie #6, Cookie=Login) |
| 8 | **Apify-Konkurrenz: ScrapeCreators / EnsembleData / Bright Data** | IG/TT/YT per API-Key | URL-basiert, Download prüfen | endpointabhängig | öffentlich | TT-Transkripte teils als Endpoint | JSON (Entwickler-API) | ScrapeCreators $47/25K Credits; EnsembleData ~$100/Mon.; Bright Data ab $1,50/1K Records, Mindestvolumina beachten | `VENDOR_CLAIM`, Preise 2026-07/08 geprüft (Drittquellen) | Bedingt geeignet — erst relevant in Architektur C; für den Pilot überdimensioniert |
| 9 | **faster-whisper** (Whisper large-v3/turbo lokal) | lokale Dateien | – | – | – | **Transkript + Zeitmarken, 99 Sprachen, VAD gegen Musik**; keine Vision | SRT/JSON via Skript | kostenlos (eigene Hardware); API-Alternative OpenAI Whisper $0,006/Min | Push 2026-10-13 `FACT_VERIFIED` | **Sofort geeignet** |
| 10 | **MacWhisper** (GUI-Alternative zu #9) | macOS, lokale Dateien + YT-URL | – | – | – | wie #9, GUI, Batch, Diarization (Pro) | TXT/SRT/VTT | Free; Pro $69 einmalig | kommerziell gepflegt `VENDOR_CLAIM`/Preis geprüft 2026-10-08 | **Sofort geeignet**, falls Ana macOS nutzt und kein Terminal will |
| 11 | **FFmpeg + PySceneDetect + Tesseract OCR** | lokale Dateien | – | – | – | Szenen, Keyframes, On-Screen-Text (OCR); **kein** Handlungverstehen | JPG/TXT/CSV | kostenlos | PySceneDetect Push 2026-10-12 `FACT_VERIFIED` | **Sofort geeignet** als Baustein |
| 12 | **Twelve Labs (Marengo/Pegasus)** oder **Gemini Video (API)** | Cloud-Upload/API | – | – | – | **Echte multimodale Analyse** (Bild+Ton+Zeit), nicht nur Transkript | JSON/Text | Twelve Labs: $0,042/Min Index + $0,0292/Min Analyse, 600 Min Free-Tier; Gemini: tokenbasiert, Preis `VENDOR_CLAIM` streut stark | aktiv | Bedingt geeignet — nur Stichprobe, API-Arbeit nötig (widerspricht „wenig Eigenentwicklung", daher nicht Pilot-Kern) |
| 13 | **Metricool** (Analytics-Layer) | IG/TT/YT per autorisierter Verbindung | nein | nein | **Cross-Channel Creator-Analytics**, Reports | nein | CSV/Reports | Free (1 Brand, 30 Tage); Starter ~$18–20/Mon. | aktiv, Preis geprüft 2026-10-05 | Bedingt geeignet — ersetzt keine Exporte, aber erspart monatliches CSV-Zusammenführen, sobald Architektur C läuft |
| 14 | **n8n / Make** | Orchestrierung | – | – | – | – | – | n8n self-hosted kostenlos | aktiv | **Zurückstellen** — Automatisierung ohne belegten Nutzen verstößt gegen das Ziel „kleinste Kombination" |
| 15 | **InstagramOSINT (sc1341)** — Negativbeispiel | IG | nein | nein | nein | nein | – | – | **`archived=true`, letzter Push 2024-06-08** `FACT_VERIFIED` | **Ungeeignet/blockiert** — Name/Stars (1.682) sind kein Funktionsnachweis; nicht installieren |

**Harte Ausschlüsse (§10 des Auftrags) angewendet:** #15 (Wartung tot), Instaloader/gallery-dl mit Hauptkonto (Kontorisiko), alle Tools, die für Videoanalyse nur Thumbnails liefern würden (in der Shortlist keine), Variante-C-Versprechen (kein glaubwürdiger Zugriff).

---

## 5. Top-5-Shortlist

1. **Native Exporte + Originaldateien** — einzige Quelle für echte Dateien in Historie + Creator-Analytics. Aufwand: einmalig durch Ana, ~1–2 h.
2. **yt-dlp** — kostenloser Datei-/Metadaten-Fallback für YT/TT, Dedup eingebaut.
3. **Apify (IG Scraper + TT Scraper/Comments)** — Metadaten/Kommentare ohne eigenes Login; Dateien sofort lokal sichern.
4. **faster-whisper / MacWhisper** — Transkripte mit Zeitmarken, lokal, keine Minutekosten.
5. **FFmpeg + PySceneDetect + Tesseract** — Szenen/Keyframes/OCR als Referenzierbarkeit (Post-ID + Timecode).

## 6. Drei vollständige Stack-Optionen

| | **A. Sofort (empfohlen)** | **B. Hybrid** | **C. Dauerhaft** |
|---|---|---|---|
| Erfassung | Originale + native Exporte + yt-dlp (URL-Liste) | A + Apify-Scheduler (wöchentlich, nur neue Posts), Medien-Download-Job | B + offizielle APIs, wo zulässig (YouTube Data API: 10.000 Quota/Tag `FACT_VERIFIED`; IG Graph API nur mit App-Review/Business-Setup; TikTok Research API i. d. R. nicht für Creator-Eigenauswertung) + Metricool |
| Verstehen | faster-whisper/MacWhisper + FFmpeg/Szenen/OCR lokal | A + Gemini/Twelve-Labs-Stichprobe pro neuem Post (Budget-Cap) | B + feste Analyse-Pipeline, Modell-Versionierung |
| Ablage | Ordner + SQLite + Google Sheet | B + Baserow (UI) | PostgreSQL/SQLite + Backups + Monitoring |
| Zugänge | nur Anas eigene Logins für Exporte | + Apify-Konto (Zahlung!) | + API-Keys, App-Reviews, Metricool-Verbindung |
| Einrichtung | 0,5–1 Tag | +0,5 Tag | 3–10 Tage + Wartezeiten (Reviews) |
| Laufend | ~30 Min/Monat (neue Exporte ablegen) | ~1 h/Monat (Runs prüfen) | 2–4 h/Monat Wartung |
| Kosten | 0 € (ggf. MacWhisper $69 einmalig) | Apify Starter ~$19–29/Mon. + Daten < $5/Mon. in Anas Größenordnung (Schätzung, §10) | + Metricool ~$18–20/Mon., API-Kosten klein; Hauptposten: Wartungszeit |
| Risiken | manuelle Export-Disziplin; IG-Lücken | Apify-Feldänderungen, CDN-Ablauf, ToS-Grauzone der Anbieter | Review-Ablehnung, API-Brüche, Over-Engineering |
| Wechsel/Export | alles lokale offene Formate | JSON/CSV exportierbar | eigene DB, voll portabel |
| Kleinster End-to-End-Test | §11 Runbook (20 Posts) | 20 Posts über Apify statt yt-dlp, Felder diffen | erst nach belegtem Pilot-Nutzen |

**„Nichts bauen" geprüft:** Nur Substack + native Apps weiter nutzen = 0 €, aber keine durchsuchbare Wissensbasis, keine Crosspost-Erkennung, keine systematische Wiederverwendung. Für das erklärte Ziel (Wissensbasis) unzureichend — als bewusste Entscheidung aber legitim, falls der Pilot keinen Substack-Mehrwert zeigt (§12).

---

## 7. Datenarchitektur (minimaler Datenvertrag)

Ordner: `data/media/<platform>_<post_id>.<ext>` · `data/raw/` (unveränderte Exporte/JSON) · `data/ana.db` (SQLite) · `exports/` (Sheets/Briefs).

Tabellen (Rohdaten ≠ Beobachtung ≠ Interpretation — Pflichtspalte `kind`/`evidence`):
`posts(platform, post_id, url, caption, published_at, format, language)` ·
`creatives(creative_id, fingerprint_sha256, note)` — Crosspost-Zuordnung per Datei-Hash + Dauer/Titel-Abgleich, manuell bestätigt ·
`assets(asset_id, path, sha256 UNIQUE, rights)` ·
`performance_snapshots(post_id, metric, platform_definition, value, captured_at)` — **nie Werte schätzen/übertragen; fehlend = NULL mit Grund** ·
`transcript_segments(post_id, start, end, text, kind='observed_transcript')` ·
`visual_segments(post_id, start, end, on_screen_text, observed_action, kind)` — KI-Deutung separat `kind='interpretation', model, model_version` ·
`audience_signals(signal_id, post_id, signal_class[question|request|objection|praise|other], anonymized_text, captured_at)` — **keine Usernamen speichern** ·
`topic_clusters(cluster_id, label, post_ids[], support_count, counterexamples[], status[hypothesis|supported])` — Cluster ohne Post-IDs ist nicht zulässig ·
`reuse_candidates(candidate_id, post_ids[], reader_problem, new_value, ana_effort_min, missing_facts[], approval[open|approved|rejected])`.

`pilot_pipeline.py` erzeugt `posts/assets/transcript_segments` bereits genau so (Smoketest `TESTED_OK`).

## 8. Content-Knowledge-Modell & Impact-Regeln

- **Trennung:** Beobachtung (Transkript/OCR/Metrik mit Zeitstempel) → Muster (≥3 unabhängige Posts, Plattformen getrennt gezählt) → Interpretation (als solche markiert, mit Gegenbelegen).
- **Impact nur plattformintern vergleichen**, normiert auf Alter (Views/Tag seit Upload) und Format (Short vs. Longform nie mischen). YouTube-View ≠ TikTok-View (Zähl-/Loop-Definitionen verschieden) — kein unbereinigter Cross-Plattform-Rang.
- **Verbotene Schlüsse:** Views≠Kaufinteresse; Likes≠Nachfrage; ein viraler Ausreißer (z. B. Collaboration mit 31K Views auf fremdem Kanal) sagt nichts über Anas eigenen Kanal; Kommentarfragen einzelner Viel-Kommentierer ≠ Zielgruppe. **Fehlende Analytics werden als `UNKNOWN` geführt, niemals aus anderen Kennzahlen „geschätzt" und als Fakt ausgegeben.**
- Nachfrage-Signal-Hierarchie (absteigend belastbar): Substack-Anmeldung/Zahlung nach Post → konkrete „Wie/was kostet/wo"-Fragen mehrerer Personen → Saves/Shares → Kommentarfragen Einzelner → Likes/Views.
- Erste, **stichprobenbasierte** Cluster-Hypothesen (Status `hypothesis`, Quellen §2): Camino/Slow-Travel-Tagebuch; Siargao-Leben & Kosten; 9-to-5→Creator-Übergang & Geld online; Creator-Handwerk/Personal Branding; Pack-/Tool-Guides mit Affiliate-Bezug. **Gegenbeleg/Unsicherheit:** Instagram-Korpus fehlt komplett; Cluster können sich nach Vollerfassung (Runbook Schritt 2) auflösen.

## 9. Substack-Reuse-Modell — drei belegbare Kandidaten

Ausgangslage `TESTED_OK`: In-Between existiert seit 2025-09, erst 3 Newsletter; der jüngste (Niche/Personal Branding) ist **paid-only** — zahlende Leser existieren (`payments_state=enabled`), Höhe `UNKNOWN`. Ton (aus Texten verifiziert): englisch, persönlich, „hihi"-Humor, Erfahrungsbericht statt Lehrbuch — Entwürfe müssen daran gemessen werden, Generik ist ein Ablehnungsgrund.

**Kandidat 1 — „What social media actually pays for: my first year of money online, with numbers" (Serie: Money & Work, monatlich)**
Leserproblem: „Kann man davon leben — was kommt woher?" · Quellen: Substack „Money & Work"-Seite + Niche-Post 2026-10-11 (paid, 2.149 Wörter) als Gerüst; Social-Posts dazu: `SOURCE_NEEDED` (Korpus). Neuer Wert ggü. Reel: vollständige Einnahmequellen/Erfahrungen an einem Ort, aktualisierbar. **Fehlende Belege (harter Blocker für Veröffentlichung): echte Zahlen nur von Ana — nichts erfinden.** Nachfrage-Test: Substack Note mit der einen Frage „Want the full breakdown of what I earned my first year?" + Antwort-/Anmelde-Zählung über 7 Tage. Verwerfen, wenn <10 qualifizierte Reaktionen oder Ana die Zahlen nicht teilen will.

**Kandidat 2 — „Camino Portugués: the honest 14-day diary (Porto → Santiago)" (Serie: Slow Travel Diaries)**
Leserproblem: konkrete Planung + ehrliche Erwartung für die erste lange Wanderung. Quellen `TESTED_OK`: Substack-Startpost 2026-09-09 (871 Wörter) + YT-Shorts-Serie (mind. 5 Camino-Shorts, §2) + Longform „What I'm Packing for the Camino" (8:00, `CUrmDg2seNA`). Neuer Wert: Route, Tagesetappen, Kosten, Fehler — im Reel-Format nicht darstellbar. Fehlend: Etappen-/Kosten-Notizen von Ana (30 Min Interview/Voice Note). Nachfrage-Test: Note „I'm turning my Camino into one full honest guide — what do you want to know?" Fragen zählen/clustern. Verwerfen, wenn keine Planungsfragen kommen (dann nur Tagebuch-Post ohne Serie).

**Kandidat 3 — „Slow-travel packing system" (wiederkehrender Guide, quartalsweise aktualisiert)**
Leserproblem: leicht & lang reisen ohne Fehlkäufe. Quellen `TESTED_OK`: Substack „What's in my backpack" (2026-09-16, free, mit Affiliate-Links) + YT-Packing-Video (überlappt: Crosspost-/Creative-Kandidat, im Pilot per Hash zu prüfen). Neuer Wert: lebende, versionierte Liste statt veraltendem Video; Affiliate-Erlös bereits angelegt. Ana-Aufwand: ~20 Min Update/Quartal. Nachfrage-Test: bestehenden Post mit „reply with your route/climate"-CTA als Note restacken, Antworten zählen. Verwerfen, wenn Klicks auf Links ≈ 0 bei zwei Restacks.

**Format-Regel für alle:** jeder Entwurf entsteht als `reuse_candidates`-Eintrag mit Post-IDs; ohne Quellen-ID kein Entwurf; Veröffentlichung nur nach Anas Freigabe (`approval`).

## 10. Kosten- und Wartungsmodell (Rechenszenarien, keine Ist-Mengen)

Preise verifiziert 2026-10-09…13 (Apify-Store, Dritt-Preisvergleiche mit Datum, Twelve-Labs-Rate-Card 2026-09-11). Formel statt Scheingenauigkeit; Plattform-Grundgebühren separat.

| Posten | Pilot: 30 Posts / 30 Min / 100 Kommentare | Basis: 300 / 300 Min / 1.000 | Archiv: 1.500 / 1.500 Min / 5.000 |
|---|---|---|---|
| Apify Metadaten IG ($1,50–2,70/1K) + TT ($1,70/1K) | ≤ $0,10 | ≤ $0,85 | ≤ $4,20 |
| Apify Kommentare (TT $0,50/1K; IG im IG-Scraper als Results, ~$1,50–2,70/1K) | ≤ $0,30 | ≤ $2,70 | ≤ $13,50 |
| Apify Dateidownload IG ($3,80/1K, nur falls nötig) | $0,11 | $1,14 | $5,70 |
| Apify Plattform | Free ($5 Guthaben/Mon.) reicht für Pilot | Starter ~$19–29/Mon. | Starter/Scale, Preis vor Kauf prüfen |
| Transkription lokal (faster-whisper) | 0 € (Strom/Zeit; ~Echtzeit×0,2–1 je nach Rechner, `CONDITIONAL`) | 0 € | 0 € · Alternative Whisper-API: $0,18 / $1,80 / $9,00 ($0,006/Min) |
| Multimodal-Stichprobe Twelve Labs ($0,0712/Min Index+Analyse) | $2,14 (30 Min) — Free-Tier 600 Min: **$0** | nur Stichprobe empfohlen: $0–21 | nicht flächendeckend empfohlen |
| Speicher (lokal/Drive) | Videos ~30–60 MB/Post (Annahme `UNKNOWN` je Quelle) ⇒ Pilot 1–2 GB, Archiv 45–90 GB: lokal 0 €, Cloud ggf. Tarif von Ana | | |
| Einrichtung (Zeit) | 0,5–1 Tag (A) | +2–4 h | +0,5–1 Tag Backfill-Prüfung |
| Betrieb | ~30 Min/Mon. | ~1 h/Mon. | ~1–2 h/Mon. + Quartals-Export aus TikTok Studio (60-Tage-Fenster!) |

Unbekannt/`UNKNOWN`: Anas tatsächliche Post-/Minutenanzahl, MacWhisper-Notwendigkeit, Gemini-API-Endpreis für diesen Workload, Apify-Feldänderungen nach Stichtag. **Wartungsrisiko:** yt-dlp/Instaloader/gallery-dl = aktiv (Push ≤4 Tage) aber plattformänderungsanfällig (Breaking Changes sind Normalfall, Updates einplanen); Apify = Anbieterabhängigkeit, Export (JSON/CSV) sichert Wechsel; InstagramOSINT = tot (Negativbeispiel).

## 11. Sofortiger Umsetzungsplan — Runbook: 20 echte Posts → 1 prüfbarer Substack-Entwurf

1. **Ana (30 Min, nur sie kann das):** YouTube Studio + TikTok Studio + Meta Business Suite → Analytics-CSVs exportieren; Originale-Ordner (Handy/Cloud) freigeben; Liste ihrer 20 wichtigsten Posts (URLs) **oder** Freigabe: „nimm die letzten 20 über meine Profile". Stopp-Kriterium: keine Freigabe → nur öffentlich Verifiziertes aus §2 nutzen.
2. **URL-Liste** `data/urls.txt` anlegen: je 5× IG-Reel/Post, TikTok, YT-Short, YT-Longform + 1 bekannter Crosspost (z. B. Packing: Substack 2026-09-16 ↔ YT `CUrmDg2seNA`-Umfeld; Hash-Abgleich entscheidet).
3. **Erfassen:** `python scripts/pilot_pipeline.py --urls data/urls.txt --out data` (yt-dlp). Erfolgsquote + Fehler ins `run_log.json` — Ziel ≥17/20 mit echter Datei. Für IG-Fehlschläge: Apify-Kleinsttest (Free-Guthaben $5) mit denselben URLs; Felder/Dateien gegen Erwartungsliste diffen (Caption, Zeit, ID, Dauer, Kommentare, echte Datei statt 24-h-URL). **Kein Instagram-Login, keine Cookies von Ana.**
4. **Verstehen:** `--transcribe --model small` (oder MacWhisper-GUI) + FFmpeg-Keyframes (1 Bild/5 s) für die 5 stärksten Posts; 2 Posts zusätzlich durch multimodale Analyse (Free-Tier) — Mehrwert gegen reines Transkript schriftlich bewerten, sonst streichen.
5. **Befüllen:** Exporte aus Schritt 1 als `performance_snapshots` einlesen (nur echte Werte); Kommentare (falls Apify-Test positiv) anonymisiert als `audience_signals` (Namen weg).
6. **Clustern:** `topic_clusters` nur mit ≥3 Post-IDs je Cluster; Gegenbelege notieren. Sheet-Ansicht für Ana erzeugen.
7. **Ein Entwurf:** Kandidat 2 (Camino, stärkste Quellenlage) als redaktioneller Brief + Entwurf aus `reuse_candidates`, jede Tatsachenbehauptung mit Post-ID/Timecode, Lücken als `[SOURCE_NEEDED: …]` markiert. **Keine Veröffentlichung ohne Anas `approval=approved`.**
8. **Abnahme (Definition of Done des Pilots):** 20 Posts mit Datei+Metadaten+Transkript in SQLite; 1 Entwurf mit durchgehenden Quellen; Zeit-/Kostenprotokoll; Go/No-Go für Architektur B anhand §1-Falsifikatoren.

Zeit bis zum ersten verwertbaren Bestand: **1 Arbeitstag** nach Schritt 1.

## 12. Empfehlung & Gegenbelege — was NICHT gebaut werden sollte

- **Nicht bauen:** eigene Social-API-Integration (Architektur C) vor Pilot-Nutzen; n8n/Make-Automatisierung „auf Vorrat"; Vektor-Datenbank/RAG-Chatbot über Anas Leben (erfindet ohne Quellenbindung Erfahrungen — verboten laut Ziel); vollautomatische Kommentar-Scrapes im Dauerbetrieb; Instaloader/gallery-dl mit Anas Hauptkonto; InstagramOSINT o. ä. Archiv-Repos.
- **Gegenbelege zur eigenen Empfehlung:** Substack hat erst 3 Posts und kleine sichtbare Reaktionen (2–13) — der Engpass ist möglicherweise nicht Content-Nachschub, sondern Distribution; der Pilot muss deshalb Nachfrage **messen** (Schritt 7/Tests in §9), statt Output zu maximieren. Wenn Anas Originale/Exporte lückenhaft sind und Apify im Test nur ablaufende URLs liefert, kippt die Empfehlung auf „manuelle Kuratierung der Top-50-Posts" statt Vollarchiv — das ist dann die ehrlich kleinste Kombination.
- **Recht/Ethik (Hard Gate):** öffentliche Sichtbarkeit ≠ freie Verwendbarkeit; fremde Kommentare nur anonymisiert/minimiert; keine Umgehung von Login/CAPTCHA/Rate-Limits; keine Veröffentlichung ohne Anas Freigabe; Personen-/Kooperationsinhalte (z. B. Collaboration-Partner) nicht ohne Rechteklärung wiederverwenden.

## 13. Maschinenlesbare Ergebnisse

Siehe **`results.json`** (Tools, Features, Evidenzstatus, Quellen, Tests, Kostenszenarien, Stacks, Blocker, nächster Schritt) — valide JSON, generiert zusammen mit diesem Bericht.

