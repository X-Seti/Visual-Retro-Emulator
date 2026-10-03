### 🧠 AI Directives for Project: Visual-Retro-Emulator

---

#### 1. File Naming

- Keep filenames simple and unchanged.
- Avoid using words like **"enhanced"** or **"fixed"**.
- Overwrite existing files unless creating a new module with a distinct name.

---

#### 2. Code Structure & Refactoring

- When appropriate, organize functions into smaller logical files (e.g., `ui/`, `manager/`).
- Follow developer in-line tags:
  - `#this belongs in ui/`
  - `#this goes in manager/`
- These tags must **never be altered or removed**.

---

#### 3. Handling Script Continuation

- If interrupted with a prompt like **"Continue"**, do **not regenerate the full script**.
- Instead, append or insert only the **missing or remaining** portion to the existing content.
- Resume from the last complete logical block (e.g., function or class).

---

#### 4. Comments and Directives

- Preserve all in-line tags and developer notes as-is.
- Do not change wording of directive comments like `#this belongs in ...`.

---

#### 5. Output Format

- Use proper syntax highlighting in code blocks (e.g., ` ```python `).
- Keep explanations minimal unless clarification is requested.

---

#### 6. AI Role & Boundaries

- Behave as an **assistant developer**, not the lead architect.
- Seek confirmation before making high-level design decisions or structural rewrites.

---

#### 7. UI Behavior – Chip Packages

- Allow chips placed on the canvas to remain abstract until a package type is chosen.
- Package type (e.g., DIP, QFP) should be **selectable post-placement** via UI options.
- Link package metadata to chip objects for future layout processing.

---

#### 8. Script Updates & Preservation

- When **editing, updating, or regenerating** any part of a script:
  - **Preserve existing changes**.
  - Do **not overwrite custom logic or manually-added sections** unless explicitly instructed.
  - Assume edits should **merge into** the existing code, respecting previous modifications and structure.

---

**Note**: In this context, ASI stands for **Artificial Super Intelligence**.

