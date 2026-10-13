# Verifizierungsprotokoll — Stichtag 2026-10-13 (UTC)

| # | Test | Input | Ergebnis | Evidenzstatus |
|---|------|-------|----------|---------------|
| T1 | YouTube-Kanal öffentlich lesbar (Web-Fetch) | https://www.youtube.com/@anasavu | Kanal "Ana Savu", Channel-ID UCjzMuM_SuB5wkwFnN9ycaFg (aus /posts-URL), Shorts + Longform + Collaborations sichtbar, View-Zahlen öffentlich sichtbar | TESTED_OK (Lesezugriff über Recherche-Fetch, keine Analytics) |
| T2 | Substack-Archiv-API öffentlich lesbar | https://anasavu.substack.com/api/v1/archive?sort=new&offset=0&limit=50 | Genau 3 Newsletter-Einträge zurückgegeben (Details in REPORT §2/§9). Publication-ID 6216941, Name "In-Between", payments_state=enabled | TESTED_OK |
| T3 | TikTok-Profil direkt fetchen | https://www.tiktok.com/@anasavu | HTTP 403 im Fetch-Tool | TESTED_FAIL (Bot-Schutz; kein Umgehungsversuch) |
| T4 | yt-dlp Installation | pip venv, yt-dlp 2026.08.19 | Installiert und lauffähig (`--version`) | TESTED_OK |
| T5 | yt-dlp Extraktion YouTube/TikTok/Instagram aus Sandbox | Video CUrmDg2seNA, TikTok 7472778649872239894, IG-Profil | TLS-EOF: Sandbox-Egress ist auf github/pypi/npm beschränkt → Plattformen nicht erreichbar. Kein Tool-Fehler nachgewiesen, kein Erfolg behauptet | NOT_TESTED_ACCESS_BLOCKED |
| T6 | faster-whisper Installation | pip venv | Paket installiert; Modell-Download (HuggingFace) aus Sandbox nicht möglich → keine Transkription eines Ana-Videos getestet | NOT_TESTED_ACCESS_BLOCKED |
| T7 | GitHub-Wartungsstatus (api.github.com, 2026-10-13) | yt-dlp, instaloader, gallery-dl, PySceneDetect, faster-whisper, InstagramOSINT | Alle aktiv (pushed ≤4 Tage alt) außer InstagramOSINT: archived=true, letzter Push 2024-06-08 | FACT_VERIFIED |
| T8 | Lokaler Pilot-Skript-Smoketest | scripts/pilot_pipeline.py --help / --dry-run | Läuft, erzeugt SQLite-Schema + Dedup-Logik ohne Netz | TESTED_OK |

Nicht durchgeführt (braucht Anas Autorisierung, wird NICHT ohne Freigabe gemacht):
Apify-Registrierung/Zahlung, Instagram-/TikTok-Login oder Cookies, Creator-Analytics-Exporte,
Kommentar-Scraping an echten Posts, Twelve-Labs-/Gemini-Upload von Ana-Medien.
