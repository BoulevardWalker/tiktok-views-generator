# Security Policy — tiktok-views-generator

## Supported versions

| Version | Supported |
| ------- | --------- |
| 2.6.x   | yes       |
| 2.5.x   | yes       |
| < 2.5   | no        |

## Reporting a vulnerability

Open a **private** security advisory on GitHub, or mail `security@fridgegate.dev` (PGP key in `docs/pgp.asc`). Do not open a public issue for anything that lets an attacker:

- Read or exfiltrate session cookies from `sessions/`
- RCE via a malicious proxy file or config YAML
- Leak proxy credentials from `proxies/pool.txt`
- Escape the sandboxed request builder

We aim to triage in 72h.

## Threat model

This tool runs on a user's own Windows desktop. It makes outbound HTTPS to TikTok endpoints. It stores minted sessions on disk in `sessions/`. The primary threats:

1. **Proxy credential leakage** — `proxies/pool.txt` is plaintext. If you sync this repo, redact it.
2. **Session cookie theft** — sessions are written with `0o600` on POSIX; on Windows ACLs are inherited from the user profile. Don't run as a shared account.
3. **Untrusted config** — YAML is loaded with `safe_load`. Do not switch to `full_load`.
4. **Driver injection** — only drivers registered in `drivers/__init__.py` are loadable. Do not add a `driver: python:` config key.

## Non-goals

We don't defend against a user who deliberately wants to harm their own account. Rate-limit abuse is a user problem.