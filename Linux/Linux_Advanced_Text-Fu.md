# Linux Advanced Text-Fu

---

# Part 1 — Regular Expressions (Regex)

---

## 1. What is Regex?

Regular expressions (regex) are **patterns** used to match character combinations in strings. They are one of the most powerful tools in Linux for searching, filtering, and manipulating text. Regex is used heavily with `grep`, `sed`, `awk`, and `tr`.

Sample text used in examples throughout this section:
```
sally sells seashells
by the seashore
```

**Three regex modes in grep:**

| Mode | Flag | Description |
|---|---|---|
| Basic (BRE) | default | `?`, `+`, `{`, `\|` must be escaped with `\` |
| Extended (ERE) | `grep -E` | Meta-characters work without escaping |
| Perl-Compatible (PCRE) | `grep -P` | Most powerful — supports lookaheads etc. |

> Always wrap regex patterns in **single quotes** `' '` to prevent the shell from misinterpreting special characters.

---

## 2. Anchors — Matching Position

Anchors match a **position** in a line, not a character.

| Anchor | Meaning |
|---|---|
| `^` | Start of line |
| `$` | End of line |
| `\b` | Word boundary |

```bash
grep "^by" file.txt         # Matches "by the seashore" (starts with "by")
grep "seashore$" file.txt   # Matches line ending with "seashore"
grep "^$" file.txt          # Matches empty lines
grep '\bsells\b' file.txt   # Matches whole word "sells" only
```

---

## 3. The Dot — Any Character

`.` matches **any single character** except a newline.

```bash
grep "s.lly" file.txt       # Matches "sally", "s1lly", "s lly" etc.
grep "\." file.txt          # Matches a literal dot (escape with \)
```

---

## 4. Character Classes `[ ]`

Square brackets match **any one** of the characters listed inside.

| Pattern | Matches |
|---|---|
| `[abc]` | Any one of: a, b, or c |
| `[a-z]` | Any lowercase letter |
| `[A-Z]` | Any uppercase letter |
| `[0-9]` | Any digit |
| `[^abc]` | Any character NOT a, b, or c |

```bash
grep "[aeiou]" file.txt         # Lines containing any vowel
grep "[^a-z]" file.txt          # Lines with a non-lowercase character
grep "[Ss]ells" file.txt        # Matches "Sells" or "sells"
```

**POSIX classes (inside `[ ]`):**

| Class | Matches |
|---|---|
| `[:alpha:]` | Any letter |
| `[:digit:]` | Any digit |
| `[:alnum:]` | Any letter or digit |
| `[:space:]` | Space, tab, newline |
| `[:upper:]` | Uppercase letters |
| `[:lower:]` | Lowercase letters |

```bash
grep "[[:digit:]]" file.txt     # Lines containing a digit
grep "[[:upper:]]" file.txt     # Lines containing an uppercase letter
```

---

## 5. Quantifiers — How Many Times?

| Quantifier | Meaning |
|---|---|
| `*` | 0 or more times |
| `+` | 1 or more times (ERE) |
| `?` | 0 or 1 time — optional (ERE) |
| `{n}` | Exactly n times |
| `{n,}` | At least n times |
| `{n,m}` | Between n and m times |

```bash
grep "se*" file.txt             # "s", "se", "see", "seee" etc.
grep -E "se+" file.txt          # "se", "see" etc. (at least one e)
grep -E "colou?r" file.txt      # "color" or "colour"
grep -E "s{2}" file.txt         # Exactly 2 s's: "ss"
grep -E "se{1,3}" file.txt      # "se", "see", or "seee"
```

> In BRE (default), `+`, `?`, `{` need escaping: `\+`, `\?`, `\{n\}`. Use `grep -E` to avoid this.

---

## 6. Alternation `|` and Grouping `( )`

**Alternation `|`** — OR matching. Requires `-E`.

```bash
grep -E "cat|dog" file.txt              # Lines with "cat" OR "dog"
grep -E "sells|seashells" file.txt      # Lines with either word
```

**Grouping `( )`** — Group patterns together. Requires `-E`.

```bash
grep -E "(sea)+" file.txt               # "sea", "seasea" etc.
grep -E "^(sally|by)" file.txt          # Lines starting with "sally" or "by"
grep -E "(sea)(shell|shore)" file.txt   # "seashell" or "seashore"
```

---

## 7. Quick Reference — Regex Cheat Sheet

| Pattern | Meaning |
|---|---|
| `^` | Start of line |
| `$` | End of line |
| `.` | Any single character |
| `[abc]` | Any one of a, b, c |
| `[^abc]` | NOT a, b, or c |
| `[a-z]` | Any lowercase letter |
| `[0-9]` | Any digit |
| `*` | 0 or more |
| `+` | 1 or more (ERE) |
| `?` | 0 or 1 (ERE) |
| `{n,m}` | Between n and m times |
| `\|` | OR (ERE: no backslash needed) |
| `( )` | Group patterns |
| `\` | Escape a special character |

**grep flags:**

| Flag | Meaning |
|---|---|
| `-E` | Extended regex (ERE) |
| `-i` | Case-insensitive |
| `-v` | Invert match |
| `-n` | Show line numbers |
| `-c` | Count matching lines |
| `-w` | Match whole word only |
| `-r` | Recursive search |
| `-C n` | Show n lines of context |

---

---

# Part 2 — Text Editors

---

## 8. Text Editors Overview

On Linux, the two most dominant terminal text editors are **Vim** and **Emacs**. Both are pre-installed on most Linux distributions.

| Editor | Best for | Learning curve |
|---|---|---|
| **Vim** | Fast, lightweight editing; always available on servers | Moderate |
| **Emacs** | Extensible, all-in-one environment | Steeper |

> If you want to navigate your system like a ninja, you need to learn at least one of these editors.

---

---

# Part 3 — Vim

---

## 9. Vim (Vi Improved)

Vim is pre-installed on nearly **every** Linux distribution. Incredibly lightweight and fast — starts instantly and handles very large files.

**Open Vim:**
```bash
vim                     # Open blank buffer
vim filename.txt        # Open a file (creates it if it doesn't exist)
```

**Vim is a modal editor** — what your keys do depends on which mode you're in:

| Mode | How to enter | Purpose |
|---|---|---|
| **Normal mode** | Default / press `Esc` | Navigate, run commands. Keys are commands NOT text |
| **Insert mode** | Press `i` | Type and edit text like a normal editor |
| **Visual mode** | Press `v` | Select blocks of text |
| **Command-line mode** | Press `:` from Normal | Save, quit, search & replace |

> ⚠️ Press `Esc` whenever unsure — it always safely returns you to Normal mode.

---

## 10. Vim Navigation (Normal mode)

| Key | Movement |
|---|---|
| `h` or `←` | Left one character |
| `l` or `→` | Right one character |
| `j` or `↓` | Down one line |
| `k` or `↑` | Up one line |
| `w` | Forward to start of next word |
| `b` | Back to start of previous word |
| `0` | Start of current line |
| `$` | End of current line |
| `gg` | First line of file |
| `G` | Last line of file |
| `:n` | Jump to line number n |
| `Ctrl+f` | Page down |
| `Ctrl+b` | Page up |

---

## 11. Vim Search Patterns (Normal mode)

```bash
/pattern        # Search forward — jumps to first match
?pattern        # Search backward
n               # Jump to next match
N               # Jump to previous match (reverse direction)
```

**Search and replace (Command-line mode):**

```bash
:s/old/new          # Replace first occurrence on current line
:s/old/new/g        # Replace all on current line
:%s/old/new/g       # Replace all in entire file
:%s/old/new/gc      # Replace all, confirm each time
```

---

## 12. Vim Inserting and Appending Text

All keys below switch you from Normal to **Insert mode**:

| Key | Action |
|---|---|
| `i` | Insert **before** the cursor |
| `a` | Append **after** the cursor |
| `I` | Insert at **beginning** of line |
| `A` | Append at **end** of line |
| `o` | New line **below** and enter insert mode |
| `O` | New line **above** and enter insert mode |

Press **`Esc`** to return to Normal mode when done typing.

---

## 13. Vim Editing (Normal mode)

**Deleting:**

| Command | Action |
|---|---|
| `x` | Delete character under cursor |
| `dw` | Delete to end of word |
| `dd` | Delete entire line |
| `2dd` | Delete 2 lines |
| `d$` | Delete to end of line |

**Copying (Yank) and Pasting (Put):**

| Command | Action |
|---|---|
| `yy` | Copy current line |
| `3yy` | Copy 3 lines |
| `p` | Paste below / after cursor |
| `P` | Paste above / before cursor |

**Undo and Redo:**

| Command | Action |
|---|---|
| `u` | Undo |
| `Ctrl+r` | Redo |

**Replacing:**

| Command | Action |
|---|---|
| `r` | Replace single character under cursor |
| `R` | Enter Replace mode — overwrite until `Esc` |

---

## 14. Vim Saving and Exiting (Command-line mode)

Press `:` from Normal mode to enter Command-line mode, then type:

| Command | Action |
|---|---|
| `:w` | Save the file |
| `:w filename` | Save as new filename |
| `:q` | Quit (only if no unsaved changes) |
| `:wq` | Save and quit |
| `:x` | Save and quit (same as `:wq`) |
| `:q!` | Force quit WITHOUT saving |
| `:qa!` | Force quit all open files |

**Typical Vim workflow:**
```
vim filename.txt    → open file
i                   → enter insert mode and type
Esc                 → return to normal mode
:wq                 → save and quit
```

---

## 15. Quick Reference — Vim

| Key | Action |
|---|---|
| `Esc` | Return to Normal mode |
| `i / a / o` | Insert before / after / new line |
| `h j k l` | Navigate left / down / up / right |
| `w / b` | Next / previous word |
| `gg / G` | Start / end of file |
| `x` | Delete character |
| `dd` | Delete line |
| `yy` | Copy line |
| `p` | Paste |
| `u` | Undo |
| `Ctrl+r` | Redo |
| `/pattern` | Search forward |
| `n / N` | Next / previous match |
| `:%s/old/new/g` | Replace all in file |
| `:w` | Save |
| `:q` | Quit |
| `:wq` | Save and quit |
| `:q!` | Quit without saving |

---

---

# Part 4 — Emacs

---

## 16. Emacs

Emacs is an extremely powerful, extensible text editor. You can do code editing, file management, and more — all within Emacs. Steeper learning curve than Vim but very rewarding.

**Key notation:**
- `C-` = hold **Ctrl**
- `M-` = hold **Meta/Alt**

**Open Emacs:**
```bash
emacs                   # Open Emacs
emacs filename.txt      # Open a specific file
```

**Buffers** — Text in Emacs lives in a "buffer". Each open file has its own buffer. Multiple buffers can be open simultaneously.

---

## 17. Emacs Manipulate Files

| Command | Action |
|---|---|
| `C-x C-f` | Open / create a file |
| `C-x C-s` | Save current file |
| `C-x C-w` | Save file as (new name) |
| `C-x s` | Save all open buffers |

---

## 18. Emacs Buffer Navigation

**Moving the cursor:**

| Command | Action |
|---|---|
| Arrow keys | Move as expected |
| `C-←` | Move one word left |
| `C-→` | Move one word right |
| `C-↑` | Move up one paragraph |
| `C-↓` | Move down one paragraph |
| `M-<` | Jump to beginning of buffer |
| `M->` | Jump to end of buffer |

**Managing windows and buffers:**

| Command | Action |
|---|---|
| `C-x 2` | Split screen horizontally (two windows) |
| `C-x o` | Move cursor to the other window |
| `C-x 1` | Make current window the only one (close splits) |
| `C-x k` | Kill (close) a buffer |
| `C-x b` | Switch to another buffer |

---

## 19. Emacs Editing

In Emacs, **cutting = "killing"** and **pasting = "yanking"**.

**Selecting text:**

| Command | Action |
|---|---|
| `C-Space` | Set mark (start of selection) then move cursor to extend |

**Cut, Copy, Paste:**

| Command | Action |
|---|---|
| `C-w` | Kill (cut) selected region |
| `M-w` | Copy selected region |
| `C-y` | Yank (paste) |
| `C-k` | Kill from cursor to end of line |

**Undo:**

| Command | Action |
|---|---|
| `C-x u` | Undo |
| `C-/` | Undo (alternative) |

---

## 20. Emacs Exiting and Help

| Command | Action |
|---|---|
| `C-x C-c` | Exit Emacs (prompts to save unsaved buffers) |
| `C-h C-h` | Open help menu |
| `C-h k` | Describe what a key does |
| `C-h f` | Describe a function |

---

## 21. Quick Reference — Emacs

**Files:**

| Command | Action |
|---|---|
| `C-x C-f` | Open / create file |
| `C-x C-s` | Save |
| `C-x C-w` | Save as |
| `C-x s` | Save all |
| `C-x C-c` | Exit |

**Navigation:**

| Command | Action |
|---|---|
| `C-← / C-→` | Word left / right |
| `C-↑ / C-↓` | Paragraph up / down |
| `M-<` / `M->` | Start / end of buffer |

**Editing:**

| Command | Action |
|---|---|
| `C-Space` | Start selection |
| `C-w` | Cut |
| `M-w` | Copy |
| `C-y` | Paste |
| `C-k` | Cut to end of line |
| `C-x u` | Undo |

**Windows/Buffers:**

| Command | Action |
|---|---|
| `C-x 2` | Split horizontally |
| `C-x o` | Switch window |
| `C-x 1` | Close other windows |
| `C-x k` | Close buffer |
| `C-x b` | Switch buffer |

**Help:**

| Command | Action |
|---|---|
| `C-h C-h` | Help menu |
| `C-h k` | Describe key |
