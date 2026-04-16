"""
Remove RAG chunks from chunks.json and chunks.faiss by source path prefix.

Chunks whose 'source' field starts with the given prefix are removed.
The FAISS index is rebuilt from the surviving vectors (extracted via reconstruct_n).
Both files are backed up before any modification.

Usage:
    python scripts/remove_chunks.py <source-path-prefix>

Examples:
    python scripts/remove_chunks.py "Vault/raw/books/some-book.md"
    python scripts/remove_chunks.py "Vault/raw/some-folder/"
    python scripts/remove_chunks.py "E:/OtherProject/raw/"

Path matching is case-insensitive and normalised to forward slashes.
"""

import sys
import json
import shutil
from pathlib import Path

import numpy as np

try:
    import faiss
except ImportError:
    print("Error: faiss not installed.  Run: pip install faiss-cpu")
    sys.exit(1)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
WEBAPP_DATA  = PROJECT_ROOT / "webapp" / "data"
CHUNKS_JSON  = WEBAPP_DATA / "chunks.json"
FAISS_PATH   = WEBAPP_DATA / "chunks.faiss"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _norm(path: str) -> str:
    """Normalise a path for prefix comparison: forward slashes, lowercase."""
    return path.replace("\\", "/").lower()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    prefix = _norm(sys.argv[1])
    # Ensure a trailing slash when the prefix looks like a directory
    # (no extension) so we don't accidentally match "foo-bar.md" when
    # the user meant to target "foo/" only.
    if not prefix.endswith("/") and "." not in Path(prefix).name:
        prefix += "/"

    print(f"Source prefix  : {prefix!r}")
    print(f"chunks.json    : {CHUNKS_JSON}")
    print(f"chunks.faiss   : {FAISS_PATH}\n")

    # ---- Load chunks.json --------------------------------------------------
    if not CHUNKS_JSON.exists():
        print(f"Error: {CHUNKS_JSON} not found.")
        sys.exit(1)

    chunks = json.loads(CHUNKS_JSON.read_text(encoding="utf-8"))
    print(f"Loaded {len(chunks)} chunks from chunks.json")

    # ---- Classify ----------------------------------------------------------
    keep_idx   = []
    remove_idx = []
    for i, chunk in enumerate(chunks):
        src = _norm(chunk.get("source", ""))
        if src.startswith(prefix):
            remove_idx.append(i)
        else:
            keep_idx.append(i)

    if not remove_idx:
        print(f"No chunks match source prefix {prefix!r}  — nothing to do.")
        sys.exit(0)

    # Show affected sources
    affected_sources = sorted({_norm(chunks[i].get("source", "")) for i in remove_idx})
    print(f"\nChunks to remove : {len(remove_idx)}")
    print(f"Chunks to keep   : {len(keep_idx)}")
    print(f"Affected sources ({len(affected_sources)}):")
    for s in affected_sources:
        count = sum(1 for i in remove_idx if _norm(chunks[i].get("source", "")) == s)
        print(f"  [{count:>4} chunks]  {s}")

    # ---- Load FAISS and sanity-check alignment -----------------------------
    faiss_index = None
    all_vecs    = None

    if not FAISS_PATH.exists():
        print(f"\nWarning: {FAISS_PATH} not found — only chunks.json will be updated.")
    else:
        faiss_index = faiss.read_index(str(FAISS_PATH))
        n_vecs   = faiss_index.ntotal
        n_chunks = len(chunks)

        if n_vecs != n_chunks:
            print(
                f"\nERROR: FAISS has {n_vecs} vectors but chunks.json has {n_chunks} entries."
                f"\nThey are out of sync — cannot safely remove by position."
                f"\nRe-run export_for_web.py to rebuild both from scratch, then retry."
            )
            sys.exit(1)

        print(f"\nFAISS index      : {n_vecs} vectors  dim={faiss_index.d}")
        # Reconstruct all vectors up front (IndexFlatIP supports this)
        all_vecs = faiss_index.reconstruct_n(0, n_vecs)   # shape (n, dim)

    # ---- Confirm -----------------------------------------------------------
    print()
    answer = input("Proceed? [y/N] ").strip().lower()
    if answer != "y":
        print("Aborted — no files changed.")
        sys.exit(0)

    # ---- Backup ------------------------------------------------------------
    bak_json  = CHUNKS_JSON.with_suffix(".json.bak")
    shutil.copy2(CHUNKS_JSON, bak_json)
    print(f"\nBacked up → {bak_json.name}")

    if faiss_index is not None:
        bak_faiss = FAISS_PATH.with_suffix(".faiss.bak")
        shutil.copy2(FAISS_PATH, bak_faiss)
        print(f"Backed up → {bak_faiss.name}")

    # ---- Write filtered chunks.json ----------------------------------------
    kept_chunks = [chunks[i] for i in keep_idx]
    CHUNKS_JSON.write_text(json.dumps(kept_chunks, indent=2), encoding="utf-8")
    size_kb = CHUNKS_JSON.stat().st_size / 1024
    print(f"\nSaved {len(kept_chunks)} chunks → chunks.json  ({size_kb:.0f} KB)")

    # ---- Rebuild FAISS from kept vectors -----------------------------------
    if faiss_index is not None:
        kept_vecs = all_vecs[np.array(keep_idx)].astype(np.float32)  # fancy indexing
        new_index = faiss.IndexFlatIP(kept_vecs.shape[1])
        new_index.add(kept_vecs)
        faiss.write_index(new_index, str(FAISS_PATH))
        size_mb = FAISS_PATH.stat().st_size / 1024 / 1024
        print(f"Rebuilt FAISS    → chunks.faiss  ({new_index.ntotal} vectors, {size_mb:.1f} MB)")

    print(f"\nDone. Removed {len(remove_idx)} chunk(s).")
    print("Restart the server (or re-deploy) to pick up the changes.\n")
    print("To restore backups if needed:")
    print(f"  copy {bak_json.name} chunks.json")
    if faiss_index is not None:
        print(f"  copy {bak_faiss.name} chunks.faiss")


if __name__ == "__main__":
    main()
