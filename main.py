"""One-liner entry for u-puan-describe-your-ex-in-one-word-9fc6ebe7.

Competition: "Describe Your Ex in One Word" — the entry must be exactly one
word, 1-111 UTF-8 characters, not only whitespace. The judge brief rewards a
verdict on an ex with comic punch, surprise, craft and recognition: the word
should land instantly, sting a little, and feel universally true.

Candidate words weighed:
  - "Clingy"     — vivid, but one-note; describes behaviour, not the story.
  - "Ghost"      — punchy and topical, yet too familiar; the surprise is gone.
  - "Ex-pensive" — a pun, but hyphenated wordplay risks reading as two words
                   and the joke is thinner than the pain.
  - "Recurring"  — the winner: it turns the ex into a subscription nobody
                   cancelled, a plot twist that keeps coming back. Comic
                   punch (the ex as an unwanted renewal), surprise (a
                   billing word applied to a person), craft (one clean
                   dictionary word, no gimmick), recognition (everyone has
                   felt the ex resurface). It is the verdict, not a label.

Entry word: "Recurring".
"""

import os

WORD = "Recurring"


def validate(word):
    """Check the entry word against the competition gate."""
    if not isinstance(word, str):
        raise ValueError("entry must be a string")
    if word != word.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if not word:
        raise ValueError("entry must not be empty")
    if len(word) > 111:
        raise ValueError("entry must be at most 111 characters")
    if len(word.split()) != 1:
        raise ValueError("entry must be exactly one word")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in word):
        raise ValueError("entry must not contain control characters")
    word.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8 text
    return True


def main():
    validate(WORD)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    if os.path.exists(path):
        with open(path, "rb") as f:
            existing = f.read()
        if existing != WORD.encode("utf-8"):
            raise RuntimeError(
                "refusing to overwrite entry.txt: it already holds "
                "different content (%d bytes)" % len(existing)
            )
        return  # already written correctly; nothing to do
    # Write atomically via a temp file in the same directory so a crash
    # can never leave a half-written entry.txt behind.
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8", newline="") as f:
        f.write(WORD)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp_path, path)
    # Post-write verification: read the file back and confirm it holds
    # exactly the validated entry word, byte for byte.
    with open(path, "rb") as f:
        written = f.read()
    if written != WORD.encode("utf-8"):
        raise RuntimeError(
            "post-write verification failed: entry.txt holds %r, "
            "expected %r" % (written, WORD.encode("utf-8"))
        )


if __name__ == "__main__":
    main()
