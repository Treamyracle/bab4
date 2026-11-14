# Antigravity Conversation Transfer & Device Migration Guide

This folder contains the complete, portable backup to transfer and continue this exact Antigravity thesis session on another computer or laptop (e.g., while traveling).

- **Conversation ID:** `81089962-53ae-4754-ac53-0a755e441870`
- **Session Title in Antigravity:** `SKRIPSI`
- **Supported OS:** Windows, macOS, and Linux (`~/.gemini/antigravity/`)
- **Supported GitHub Repositories:**
  - Full Thesis Repo (private): `https://github.com/Treamyracle/skripsi.git`
  - Bab 4 & 18-Class Datasets/IAA Repo (public): `https://github.com/Treamyracle/bab4.git`

---

## Quick Transfer Steps (New PC / Laptop)

### 1. Prepare Antigravity on Your Laptop
1. Install Antigravity on your laptop.
2. Open Antigravity **once** so it initializes its local data folder (`~/.gemini/antigravity/`), then **completely close/quit Antigravity** (check the system tray / Task Manager so SQLite database files are not locked).

### 2. Clone the Repository
Clone either repository anywhere on your laptop (you do **not** need to match the old PC's folder path):

```powershell
# Option A: Full thesis repository
git clone https://github.com/Treamyracle/skripsi.git
cd skripsi
```

or

```powershell
# Option B: Bab 4 & 18-class datasets/IAA repository
git clone https://github.com/Treamyracle/bab4.git
cd bab4
```

*(If you already cloned the repo earlier, pull the latest commits first with `git pull origin main`.)*

### 3. Restore and Link the Conversation Session
From the root of your cloned repository, run:

```bash
python antigravity_device_migration/restore_session.py
```

What `restore_session.py` automatically does:
1. Detects `~/.gemini/antigravity/` (`%USERPROFILE%\.gemini\antigravity` on Windows, `$HOME/.gemini/antigravity` on macOS/Linux).
2. Extracts `conversation_db_81089962-53ae-4754-ac53-0a755e441870.zip` into `~/.gemini/antigravity/conversations/`.
3. Extracts `brain_81089962-53ae-4754-ac53-0a755e441870.zip` into `~/.gemini/antigravity/brain/81089962-53ae-4754-ac53-0a755e441870/`.
4. Upserts `session_metadata.json` into `~/.gemini/antigravity/conversation_summaries.db` and automatically inserts your local cloned repository folder URI at the front of `workspace_uris`.

### 4. Open in Antigravity
1. Launch **Antigravity**.
2. Click **Open Folder** and select the cloned `skripsi` or `bab4` directory on your laptop.
3. Open the Agent/Chat sidebar — the conversation **`SKRIPSI`** (`81089962-53ae-4754-ac53-0a755e441870`) will appear with its full history, artifacts, and plans ready to continue.

---

## Moving or Cloning to Another Folder Later

If you later move the repo folder or clone the second repository into a different directory on the same laptop and want this conversation linked there too:

1. Completely close Antigravity.
2. Run inside the new folder (or pass the folder path explicitly):
   ```bash
   python antigravity_device_migration/link_to_workspace.py
   # or:
   python antigravity_device_migration/link_to_workspace.py "D:\path\to\your\cloned\repo"
   ```
3. Reopen Antigravity and open that folder.

---

## API Keys & Local Services Setup on Your Laptop

For security (especially because `Treamyracle/bab4` is a public GitHub repository), **active OpenRouter API keys were intentionally excluded from scripts and scrubbed from the exported conversation archives**.

If you need to re-run verification or IAA scripts on your laptop:
- **OpenRouter scripts** (`verify_nemotron_ultra.py`, `verify_gemma_nemotron_vl.py`):
  ```powershell
  # Windows PowerShell (persistent for your user account):
  [Environment]::SetEnvironmentVariable("OPENROUTER_API_KEY", "sk-or-v1-YOUR-KEY", "User")
  ```
  ```bash
  # macOS / Linux / current shell:
  export OPENROUTER_API_KEY="sk-or-v1-YOUR-KEY"
  ```
- **9router Gateway scripts** (`verify_luna_gemini.py`, `verify_gemma_gemini.py`, `run_independent_audit_iaa.py`):
  Start your local 9router service on `http://localhost:20128/v1` (or set `NINEROUTER_BASE_URL` / `NINEROUTER_API_KEY` if customized).

---

## Contents of `antigravity_device_migration/`

| File | Purpose |
| --- | --- |
| `README.md` | Complete Markdown transfer & recovery guide (this file) |
| `TUTORIAL_MIGRASI_PERANGKAT.txt` | Plain-text Indonesian quickstart guide |
| `restore_session.py` | 1-command cross-platform restore script (`conversations/`, `brain/`, `conversation_summaries.db`) |
| `link_to_workspace.py` | Links the restored session ID to any cloned local repo path |
| `session_metadata.json` | Live `conversation_summaries.db` metadata (`step_count`, `title`, `raw_summary_b64`, timestamps) |
| `conversation_db_81089962-53ae-4754-ac53-0a755e441870.zip` | WAL-flushed, `VACUUM`ed, integrity-checked, secret-scrubbed SQLite conversation history DB |
| `brain_81089962-53ae-4754-ac53-0a755e441870.zip` | Artifacts, reports, figures, uploaded screenshots/PDFs, and transcript logs (excludes large disposable `scratch/` raw dumps so archive stays well within GitHub size limits) |

---

## Verification Checklist After Restoring

1. Check restored files exist:
   - `~/.gemini/antigravity/conversations/81089962-53ae-4754-ac53-0a755e441870.db`
   - `~/.gemini/antigravity/brain/81089962-53ae-4754-ac53-0a755e441870/`
2. Inside the cloned repo, verify all completed datasets, IAA audit files, and tests are intact:
   ```bash
   python scripts/run_independent_audit_iaa.py --status
   python -m unittest discover -s tests
   ```
   Expected IAA status: `A1 cx/gpt-6-luna [high] 300/300 (100.0%)` and `A2 ag/gemini-3.8-flash-high [high] 300/300 (100.0%)`.
