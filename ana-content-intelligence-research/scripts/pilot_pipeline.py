#!/usr/bin/env python3
"""
ANA Pilot Pipeline — kleinste funktionierende Kombination (Architektur A/B).
Schritte: URLs aus urls.txt -> yt-dlp (echte Mediendatei + info.json) ->
SHA256-Dedup in SQLite -> optional faster-whisper Transkript (SRT/JSON mit Zeitmarken).
Keine Logins, keine Cookies, keine Umgehung. Fehler werden pro URL protokolliert, Lauf setzt fort.
Nutzung:
  python pilot_pipeline.py --urls urls.txt --out ../data --dry-run
  python pilot_pipeline.py --urls urls.txt --out ../data --transcribe --model small
Voraussetzungen: pip install yt-dlp faster-whisper ; ffmpeg im PATH (nur fuer --transcribe/Keyframes)
"""
import argparse, hashlib, json, sqlite3, subprocess, sys
from pathlib import Path

SCHEMA = """
CREATE TABLE IF NOT EXISTS posts(platform TEXT, post_id TEXT, url TEXT, caption TEXT,
 published_at TEXT, format TEXT, language TEXT, PRIMARY KEY(platform, post_id));
CREATE TABLE IF NOT EXISTS assets(asset_id TEXT PRIMARY KEY, path TEXT, sha256 TEXT UNIQUE, rights TEXT);
CREATE TABLE IF NOT EXISTS transcript_segments(post_id TEXT, start REAL, end REAL, text TEXT, kind TEXT DEFAULT 'observed_transcript');
"""

def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''): h.update(chunk)
    return h.hexdigest()

def main():
    a = argparse.ArgumentParser()
    a.add_argument('--urls', required=True); a.add_argument('--out', default='../data')
    a.add_argument('--transcribe', action='store_true'); a.add_argument('--model', default='small')
    a.add_argument('--dry-run', action='store_true')
    args = a.parse_args()
    out = Path(args.out); (out / 'media').mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(out / 'ana.db'); db.executescript(SCHEMA)
    urls = [u.strip() for u in Path(args.urls).read_text().splitlines() if u.strip() and not u.startswith('#')]
    log = []
    for url in urls:
        if args.dry_run:
            log.append({'url': url, 'status': 'DRY_RUN'}); continue
        r = subprocess.run(['yt-dlp', '--no-overwrites', '--write-info-json', '-o',
                            str(out / 'media' / '%(platform)s_%(id)s.%(ext)s'), url],
                           capture_output=True, text=True)
        if r.returncode != 0:
            log.append({'url': url, 'status': 'FAIL', 'error': r.stderr[-500:]}); continue
        for info in (out / 'media').glob('*_*.info.json'):
            d = json.loads(info.read_text())
            media = [p for p in (out / 'media').glob(f"{d.get('platform','')}_{d['id']}.*")
                     if p.suffix not in ('.json',)]
            if not media: continue
            digest = sha256(media[0])
            db.execute('INSERT OR IGNORE INTO posts VALUES (?,?,?,?,?,?,?)',
                       (d.get('platform') or d.get('extractor'), d['id'], url,
                        d.get('description') or d.get('title'), str(d.get('upload_date')), d.get('ext'), d.get('language')))
            db.execute('INSERT OR IGNORE INTO assets VALUES (?,?,?,?)',
                       (digest[:16], str(media[0]), digest, 'own_or_public_download_review_needed'))
            if args.transcribe:
                from faster_whisper import WhisperModel
                model = WhisperModel(args.model)
                segs, infofw = model.transcribe(str(media[0]), vad_filter=True)
                db.executemany('INSERT INTO transcript_segments VALUES (?,?,?,?)',
                               [(d['id'], s.start, s.end, s.text) for s in segs])
            log.append({'url': url, 'status': 'OK', 'post_id': d['id']})
        db.commit()
    (out / 'run_log.json').write_text(json.dumps(log, indent=2, ensure_ascii=False))
    print(json.dumps(log, indent=2, ensure_ascii=False))

if __name__ == '__main__':
    main()
