#!/usr/bin/env python3
"""
Skrip untuk Menautkan Sesi Antigravity ke Folder Proyek Baru
=============================================================================
Skrip ini memperbarui metadata Antigravity agar percakapan skripsi ini
langsung muncul dan terikat sebagai proyek di folder:
C:\\Users\\tream\\OneDrive\\Documents\\SKRIPSI\\skripsi
=============================================================================
"""

import json
import sqlite3
import sys
from pathlib import Path

CONVERSATION_ID = "81089962-53ae-4754-ac53-0a755e441870"
DEFAULT_TARGET_FOLDER = r"C:\Users\tream\OneDrive\Documents\SKRIPSI\skripsi"


def path_to_uri(path_str: str) -> str:
    p = Path(path_str).resolve()
    # Format Antigravity: file:///c%3A/Users/...
    drive = p.drive.lower().replace(":", "%3A")
    posix_tail = p.as_posix().split(":", 1)[-1]
    return f"file:///{drive}{posix_tail}"


def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_TARGET_FOLDER
    print("=" * 70)
    print("🔗 ANTIGRAVITY WORKSPACE LINKER")
    print(f"   Target Sesi ID: {CONVERSATION_ID}")
    print(f"   Target Folder : {target_dir}")
    print("=" * 70)

    target_uri = path_to_uri(target_dir)
    print(f"[*] Workspace URI yang dihasilkan: {target_uri}")

    db_path = Path.home() / ".gemini" / "antigravity" / "conversation_summaries.db"
    if not db_path.exists():
        print(f"❌ Error: Database Antigravity tidak ditemukan di {db_path}")
        return

    try:
        conn = sqlite3.connect(db_path, timeout=5.0)
        c = conn.cursor()

        row = c.execute(
            "SELECT workspace_uris, title FROM conversation_summaries WHERE conversation_id = ?",
            (CONVERSATION_ID,),
        ).fetchone()

        if not row:
            print(f"⚠️ Sesi {CONVERSATION_ID} belum ada di conversation_summaries.db.")
            print("   Membuat entri baru untuk sesi ini...")
            c.execute(
                """
                INSERT OR REPLACE INTO conversation_summaries (
                    conversation_id, title, preview, step_count, last_modified_time,
                    workspace_uris, last_user_input_time, last_user_input_step_index
                ) VALUES (
                    ?, ?, ?, ?, datetime('now'),
                    ?, datetime('now'), 0
                )
            """,
                (
                    CONVERSATION_ID,
                    "IndoBERT NER Thesis Progress Review",
                    "IndoBERT NER Thesis Progress Review",
                    2300,
                    json.dumps([target_uri]),
                ),
            )
        else:
            current_uris_str, title = row
            try:
                current_uris = json.loads(current_uris_str)
            except Exception:
                current_uris = []

            if target_uri not in current_uris:
                current_uris.insert(0, target_uri)

            c.execute(
                "UPDATE conversation_summaries SET workspace_uris = ? WHERE conversation_id = ?",
                (json.dumps(current_uris), CONVERSATION_ID),
            )
            print(f"[*] Berhasil memperbarui workspace_uris untuk '{title}'!")

        conn.commit()
        conn.close()
        print("=" * 70)
        print("✅ SUKSES! Sesi percakapan kini telah terhubung ke proyek:")
        print(f"   {target_dir}")
        print("\nSilakan buka / restart Antigravity, lalu pilih:")
        print(f"   Open Folder -> {target_dir}")
        print("Sesi percakapan ini akan langsung aktif di dalam proyek tersebut!")
        print("=" * 70)
    except sqlite3.OperationalError as e:
        print("\n⚠️ Perhatian: Database Antigravity sedang dikunci oleh aplikasi.")
        print("   Silakan TUTUP terlebih dahulu aplikasi Antigravity, lalu jalankan:")
        print("   python antigravity_device_migration/link_to_workspace.py")
        print("=" * 70)


if __name__ == "__main__":
    main()
