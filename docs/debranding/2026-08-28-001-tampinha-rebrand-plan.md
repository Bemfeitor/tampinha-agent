# Debranding plan — Hermes Agent → Tampinha Agent

| Field | Value |
|---|---|
| Source customer | Hermes / Nous Research / NousResearch |
| Target customer | **Tampinha** (org/product), **Tampinha Agent** (product name) — confirmed by user |
| Mode | plan |
| Scope | Entire repository (`C:\Users\flavi\Bemfeitor\tampinha-agent`) |
| Brand scope | Organization **and** product identity (explicit: name, CLI command, package names, logo, all visible references) |
| Release scope | External (fork intended for the user's own distribution as "Tampinha Agent") |
| Tracks | `debranding`, `release` (readiness only, not executed) |
| Run | `2026-08-28-001-tampinha-rebrand` |
| Baseline commit | `99c3cad8570732202907cf71f971fea9ec57df26` (`main`, up to date with `origin/main`) |

## Pre-change baseline

Host: Windows 10, Python 3.14.2, Node v24.13.1, uv 0.10.10. `git status` clean after repairing an interrupted initial checkout (`index.lock` from a killed clone; resolved with `git reset --hard HEAD`, all 10,546 tracked files restored).

A full `uv sync` / `npm install` / build was **not** run in this planning pass — the repo needs three separate toolchains (Python via uv, Node workspaces, and a Nix flake for some checks) and a full build is not the cheapest representative check available for a plan-only pass. Each apply unit below runs its own focused validation instead (import check, script `--help`, JSON/TOML parse, etc.). Recommend a full `uv sync && uv run hermes --help` (pre-rename) as the very first apply step to confirm the fork itself runs before any edits — flagged as **Unit 0** below.

## Assessment

Scanner: `scan-debranding.py --source-customer Hermes --alias "Nous Research" --alias NousResearch --alias "Nous Hermes"`.

```
files        10,557 total · 10,540 product · 0 history · 17 tooling · 89 unread (binary, skipped)
findings     81,342 total · 81,340 blocking · 2 gated
by category  source-customer=78,735 · alias=2,012 · hardcoded-opaque-identifier=593 · suspicious-file=2
```

No `history` surface exists (no `docs/decisions/`, no `CHANGELOG` with source-brand planning content) — nothing to anonymize or exclude there.

**Exposure concentration** (top of 10,540 files by finding count — full list in the scanner's JSON, not reproduced here):

| File | Findings | Why it's hot |
|---|---:|---|
| `hermes_cli/main.py` | 1,003 | CLI entry module |
| `hermes_cli/web_server.py` | 676 | Web/gateway server |
| `apps/desktop/electron/main.ts` | 598 | Desktop app shell |
| `hermes_cli/update_cmd.py` | 543 | Self-update command (checks `hermes-agent` releases) |
| `website/src/data/userStories.json` | 543 | Marketing content |
| `gateway/run.py`, `hermes_cli/gateway.py` | 501 / 484 | Gateway runtime |
| `website/docs/reference/cli-commands.md` | 455 | Generated CLI reference |
| `cli.py` | 449 | Root launcher |
| `tests/**` (multiple files) | 300–400 each | Test fixtures/assertions mirror source names |
| `website/i18n/zh-Hans/**` | 233–303 each | Translated docs (mirror of English docs; regenerate, don't hand-edit) |
| `hermes_constants.py` | 202 | **Canonical identity module — see below** |

**Suspicious files** (`.env.example`, `.envrc`): read in full. No secrets, no live domains — only variable-name and comment references to Hermes (`~/.hermes/config.yaml`, `hermes model`, `hermes setup`). Not blocking.

### Coupling below the surface (why this isn't a find-and-replace job)

`hermes_constants.py` is the single source of truth for identity, but "Hermes" is baked into more than display strings:

* **Filesystem home directory**: `~/.hermes` (Linux/macOS) and `%LOCALAPPDATA%/hermes` (Windows), read by `_get_platform_default_hermes_home()`. Renaming this is a real product decision (Unit 3), not cosmetic — but since this is a fresh fork with zero existing Tampinha installs, there is no migration burden. Flagged `Needs your decision` only to get explicit sign-off on the new path (`~/.tampinha` / `%LOCALAPPDATA%/tampinha`), not because it's risky.
* **Context-local override variable**: `_HERMES_HOME_OVERRIDE` (internal, safe to rename mechanically).
* **CLI entry points** (`pyproject.toml [project.scripts]`): `hermes`, `hermes-agent`, `hermes-acp` → the actual commands a user types. Renaming these is the product decision this whole plan exists to make.
* **Package names**: `hermes-agent` (root `pyproject.toml` + root `package.json`), `hermes-tui` (`ui-tui/package.json`), `hermes` (`apps/desktop/package.json`), plus extras `hermes-agent[cron]`, `[mcp]`, `[honcho]`, `[acp]`, `[termux]`, `[google]`, `[homeassistant]`, `[sms]` in `pyproject.toml`.
* **Self-update mechanism** (`hermes_cli/update_cmd.py`, 543 findings): checks GitHub releases under the `NousResearch/hermes-agent` repo. This is an **external-system dependency**, not a rename — pointed at the wrong upstream, Tampinha Agent would "update" itself from Nous Research's releases. `Blocks release`, routed to the `release` track (Referral, not a debranding unit — needs a real release pipeline for `Bemfeitor/tampinha-agent` first).
* **Visual identity**: `website/static/img/logo.png`, `website/static/img/nous-logo.png`, `favicon.ico/.svg` (in both `web/public/` and `website/static/img/`), `apps/desktop/src/components/ui/connector-logo.tsx`. No replacement logo exists yet — `Needs your decision`.
* **Generated/translated content**: `website/i18n/zh-Hans/**` mirrors the English docs. Edit the English source and regenerate translations through the project's i18n pipeline; hand-editing the translated copy directly would drift from source (rule: don't edit generated content directly when regeneration is correct).

Coupling review (the batch/lens dispatch the skill uses to find coupling that survives a plain rename) was **not run** in this pass given repository size — flagged as a recommended follow-up before any public/external release claim, not before internal use.

## Branding

| Field | Value | Status |
|---|---|---|
| Org/product name | Tampinha | Confirmed |
| Agent product name | Tampinha Agent | Confirmed |
| CLI commands | `hermes`→`tampinha`, `hermes-agent`→`tampinha-agent`, `hermes-acp`→`tampinha-acp` | Proposed, needs sign-off (Unit 4) |
| Home directory | `~/.hermes`→`~/.tampinha`, `%LOCALAPPDATA%/hermes`→`%LOCALAPPDATA%/tampinha` | Proposed, needs sign-off (Unit 3) |
| Package names | `hermes-agent`→`tampinha-agent`, `hermes-tui`→`tampinha-tui`, desktop `hermes`→`tampinha` | Proposed, needs sign-off (Unit 4) |
| Logo / favicon / wordmark | — | **Not provided.** No design decision possible until the user supplies or commissions artwork. |
| Two-profile validation | Not yet applicable — no second brand profile requested | Deferred |

No design system (`DESIGN_SYSTEM`) was named, so no token-provider mapping applies.

## Referrals

| ID | Finding | Track | Urgency | Suggested owner |
|---|---|---|---|---|
| REL-001 | `update_cmd.py` self-update checks `NousResearch/hermes-agent` GitHub releases | `release` | High — must be repointed before any build is distributed, or updates will silently pull Nous Research's binary | Whoever owns the Tampinha release pipeline |
| REL-002 | No coupling review performed (repo scale) | `release` | Medium — do before claiming "fully debranded" for external release | Same |

## Unit ledger

| # | Unit | Disposition | Depends on | Size | Your call |
|---|---|---|---|---|---|
| 0 | Confirm the fork actually builds/runs pre-rename (`uv sync`, `hermes --help`) | `Blocks release` | — | S | No |
| 1 | Supply logo, favicon, wordmark assets (or authorize a placeholder) | `Needs your decision` | — | S | **Yes** |
| 2 | Decide new release pipeline target for self-update (or disable self-update until ready) | `Needs your decision` | — | S | **Yes** |
| 3 | Rename canonical identity in `hermes_constants.py` (home dir path, context var, module docstring) | `Blocks release` | 0 | M | No |
| 4 | Rename CLI entry points + package names (`pyproject.toml`, root/`ui-tui`/`apps/desktop` `package.json`) | `Blocks release` | 3 | M | No |
| 5 | Rename core Python source (`hermes_cli/`, `gateway/`, `tui_gateway/`, `cli.py`, `tools/`) — batched by subsystem | `Blocks release` | 4 | L | No |
| 6 | Align test suite with renamed identifiers | `Blocks release` | 5 | M | No |
| 7 | Desktop app (`apps/desktop/electron/`, `apps/desktop/src/`) | `Blocks release` | 4 | M | No |
| 8 | Docs & website English source (`website/docs/`, `website/src/`) | `Improvement` | 4 | L | No |
| 9 | Regenerate translated docs (`website/i18n/**`) via project i18n pipeline | `Improvement` | 8 | M | No |
| 10 | Docker / Nix / install scripts (`docker/`, `nix/`, `scripts/install.*`) | `Blocks release` | 4 | M | No |
| 11 | Apply chosen logo/favicon assets across `web/`, `website/`, desktop app | `Blocks release` | 1 | S | No |

Referral count: 2 (see `## Referrals`), neither opened as a unit here.

> Working-tree content was reviewed. Git history was not rewritten or certified as debranded.

Recommended order: **1 and 2 first** (their answers gate units 3, 4, 11 and unblock the release track while mechanical work proceeds), then 0 → 3 → 4 → 5/6/7 in sequence, 8/9/10 can run in parallel once 4 lands.

Reply `unit=N` to start one, or give me the logo/asset direction and self-update decision (units 1–2) and I'll queue the mechanical units right after.
