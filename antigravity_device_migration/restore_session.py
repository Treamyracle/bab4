#!/usr/bin/env python3
"""
Skrip Otomatis Pemulihan Sesi Antigravity pada Perangkat Baru
=============================================================================
Skrip ini akan secara otomatis mendeteksi direktori instalasi Antigravity
pada sistem operasi Anda (Windows, macOS, atau Linux) dan memulihkan:
1. File database riwayat percakapan (.db) ke ~/.gemini/antigravity/conversations/
2. Direktori artefak, memori pemikiran, dan skrip ke ~/.gemini/antigravity/brain/
3. Entri ringkasan obrolan ke ~/.gemini/antigravity/conversation_summaries.db
   sehingga obrolan langsung tampil di sidebar UI Antigravity dan terikat
   sebagai proyek pada folder repositori saat ini.

Cara Pakai di Perangkat Baru:
  python antigravity_device_migration/restore_session.py
=============================================================================
"""

import base64
import json
import os
import sqlite3
import sys
import zipfile
from pathlib import Path

CONVERSATION_ID = "81089962-53ae-4754-ac53-0a755e441870"
MIGRATION_DIR = Path(__file__).parent.resolve()


def get_antigravity_dir() -> Path:
    """Mendeteksi direktori ~/.gemini/antigravity secara lintas platform."""
    home = Path.home()
    return home / ".gemini" / "antigravity"


def restore_summary_db(target_root: Path):
    """Menyinkronkan metadata sesi ke conversation_summaries.db."""
    meta_path = MIGRATION_DIR / "session_metadata.json"
    if not meta_path.exists():
        return

    try:
        with open(meta_path, "r", encoding="utf-8") as f:
            meta = json.load(f)

        db_path = target_root / "conversation_summaries.db"
        conn = sqlite3.connect(db_path, timeout=5.0)
        cur = conn.cursor()

        # Buat tabel jika belum ada (instalasi Antigravity baru)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS conversation_summaries (
                conversation_id text PRIMARY KEY,
                title text NOT NULL DEFAULT '',
                preview text NOT NULL DEFAULT '',
                step_count integer NOT NULL DEFAULT 0,
                last_modified_time datetime NOT NULL,
                workspace_uris text NOT NULL,
                status text NOT NULL DEFAULT '',
                source text NOT NULL DEFAULT '',
                project_id text NOT NULL DEFAULT '',
                agent_name text NOT NULL DEFAULT '',
                parent_conversation_id text NOT NULL DEFAULT '',
                nesting_depth integer NOT NULL DEFAULT 0,
                battle_id text NOT NULL DEFAULT '',
                winning_conversation_id text NOT NULL DEFAULT '',
                not_fully_idle numeric NOT NULL DEFAULT false,
                killed numeric NOT NULL DEFAULT false,
                last_user_input_time datetime NOT NULL,
                last_user_input_step_index integer NOT NULL DEFAULT -1,
                app_data_dir text NOT NULL DEFAULT '',
                raw_summary blob,
                group_id text NOT NULL DEFAULT ''
            )
        """)

        raw_summary_bytes = None
        if "raw_summary_b64" in meta and meta["raw_summary_b64"]:
            raw_summary_bytes = base64.b64decode(meta["raw_summary_b64"])

        # Deteksi URI folder lokal saat ini
        repo_dir = MIGRATION_DIR.parent.resolve()
        drive = repo_dir.drive.lower().replace(":", "%3A")
        posix_tail = repo_dir.as_posix().split(":", 1)[-1]
        detected_uri = f"file:///{drive}{posix_tail}"

        try:
            uris = json.loads(meta.get("workspace_uris", "[]"))
        except Exception:
            uris = []

        if detected_uri not in uris:
            uris.insert(0, detected_uri)

        uris_json = json.dumps(uris)

        cur.execute("""
            INSERT OR REPLACE INTO conversation_summaries (
                conversation_id, title, preview, step_count, last_modified_time,
                workspace_uris, status, source, project_id, agent_name,
                parent_conversation_id, nesting_depth, battle_id, winning_conversation_id,
                not_fully_idle, killed, last_user_input_time, last_user_input_step_index,
                app_data_dir, raw_summary, group_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            meta.get("conversation_id", CONVERSATION_ID),
            meta.get("title", "IndoBERT NER Thesis Progress Review"),
            meta.get("preview", "IndoBERT NER Thesis Progress Review"),
            meta.get("step_count", 2350),
            meta.get("last_modified_time", "2026-10-23 09:55:00.0000000+00:00"),
            uris_json,
            meta.get("status", "CASCADE_RUN_STATUS_RUNNING"),
            meta.get("source", ""),
            meta.get("project_id", "2801f6c9-4682-49fb-bb4c-e779b2924f24"),
            meta.get("agent_name", ""),
            meta.get("parent_conversation_id", ""),
            meta.get("nesting_depth", 0),
            meta.get("battle_id", ""),
            meta.get("winning_conversation_id", ""),
            meta.get("not_fully_idle", 1),
            meta.get("killed", 0),
            meta.get("last_user_input_time", "2026-10-23 09:55:00.0000000+00:00"),
            meta.get("last_user_input_step_index", 2345),
            meta.get("app_data_dir", "antigravity"),
            raw_summary_bytes,
            meta.get("group_id", "")
        ))

        conn.commit()
        conn.close()
        print(f"   -> Sesi berhasil ditautkan ke project folder: {repo_dir}")
        print("   -> Metadata sesi berhasil didaftarkan ke conversation_summaries.db!")
    except Exception as e:
        print(f"   -> [Peringatan] Gagal memperbarui conversation_summaries.db: {e}")


def main():
    print("=" * 70)
    print("🔄 ANTIGRAVITY SESSION RESTORE TOOL")
    print(f"   Target Sesi ID: {CONVERSATION_ID}")
    print("=" * 70)

    target_root = get_antigravity_dir()
    print(f"\n[1/5] Lokasi Antigravity terdeteksi: {target_root}")

    conv_dir = target_root / "conversations"
    brain_dir = target_root / "brain"

    conv_dir.mkdir(parents=True, exist_ok=True)
    brain_dir.mkdir(parents=True, exist_ok=True)
    print("[2/5] Direktori conversations/ dan brain/ siap.")

    # 1. Pulihkan Database Chat
    db_zip = MIGRATION_DIR / f"conversation_db_{CONVERSATION_ID}.zip"
    if not db_zip.exists():
        print(f"❌ Error: Arsip {db_zip.name} tidak ditemukan di {MIGRATION_DIR}!")
        sys.exit(1)

    print(f"[3/5] Mengekstrak database obrolan ({db_zip.name})...")
    with zipfile.ZipFile(db_zip, "r") as zf:
        zf.extractall(conv_dir)
    extracted_db = conv_dir / f"{CONVERSATION_ID}.db"
    print(f"   -> Berhasil dipulihkan ke: {extracted_db} ({extracted_db.stat().st_size:,} bytes)")

    # 2. Pulihkan Brain / Artefak
    brain_zip = MIGRATION_DIR / f"brain_{CONVERSATION_ID}.zip"
    if not brain_zip.exists():
        print(f"❌ Error: Arsip {brain_zip.name} tidak ditemukan di {MIGRATION_DIR}!")
        sys.exit(1)

    print(f"[4/5] Mengekstrak artefak & riwayat pemikiran ({brain_zip.name})...")
    with zipfile.ZipFile(brain_zip, "r") as zf:
        zf.extractall(brain_dir)
    extracted_brain = brain_dir / CONVERSATION_ID
    print(f"   -> Berhasil dipulihkan ke: {extracted_brain}")

    # 3. Pulihkan Metadata ke conversation_summaries.db
    print("[5/5] Mendaftarkan sesi ke indeks Antigravity...")
    restore_summary_db(target_root)

    print("\n" + "=" * 70)
    print("✅ PEMULIHAN SESI BERHASIL 100%!")
    print("=" * 70)
    print("Langkah selanjutnya:")
    print("1. Buka kembali aplikasi Antigravity di perangkat Anda.")
    print(f"2. Buka folder repositori skripsi ({MIGRATION_DIR.parent}) di Antigravity.")
    print("3. Percakapan ini ('IndoBERT NER Thesis Progress Review') akan langsung")
    print("   muncul di sidebar kiri dan siap Anda lanjutkan!")
    print("=" * 70)


if __name__ == "__main__":
    main()
