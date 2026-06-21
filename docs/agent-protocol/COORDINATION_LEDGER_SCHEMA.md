---
title: "Coordination Ledger Schema — Append-Only SHA-256 Chain"
version: "1.0.0"
date_created: "2026-06-21"
status: draft
owning_roles:
  - "[[QA_TEST_AUTOMATION_ENGINEER_SKILL]]"
  - "[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"
consuming_roles:
  - "All 14 roles (as instantiated AI agents)"
  - "ARB (Architecture Review Board)"
  - "[[SECURITY_ENGINEER_SKILL]]"
cssclass: protocol-spec
tags:
  - multi-agent
  - coordination-protocol
  - MACP
  - autonomy
  - coordination-ledger
  - audit-trail
  - machine-parseable
---

# Coordination Ledger Schema — Append-Only SHA-256 Chain

> **Pillar 4 of the [[MULTI_AGENT_COORDINATION_PROTOCOL|MACP]].** Closes the Phase-3 gap *"No coordination ledger exists … making coordination invisible and un-auditable."* The ledger is the **agent equivalent of the ADR/CCR log** — it makes agent-to-agent coordination visible, auditable, and correctable.

#multi-agent #coordination-protocol #MACP #autonomy

**Acronyms (defined on first use):** MACP (Multi-Agent Coordination Protocol), SHA-256 (Secure Hash Algorithm, 256-bit), A2A (Agent-to-Agent), JSONL (JSON Lines — one JSON object per line), UUID (Universally Unique Identifier), ADR (Architecture Decision Record), CCR (Contract Clarification Record), AID (Agent Identity Document), ISO 8601 (date/time standard), Ed25519 (Edwards-curve Digital Signature Algorithm), UTC (Coordinated Universal Time).

---

## 1. Purpose

Every agent-to-agent interaction that results in a **decision**, an **artifact exchange**, or a **dispute** is recorded in the Coordination Ledger. The ledger gives the ecosystem three properties it currently lacks:

1. **Visibility** — a human (or auditing agent) can reconstruct exactly what agents coordinated, when, and why.
2. **Auditability** — the ledger is **append-only with cryptographic integrity** (a SHA-256 hash chain), so entries cannot be silently altered or removed after the fact.
3. **Correctability** — like the ADR log, errors are corrected by *appending a reversing/superseding entry*, never by mutating history.

The ledger does **not** replace the durable governance artifacts (ADRs, CCRs); it *references* them. The ADR/CCR registries hold the authoritative decision text; the ledger holds the tamper-evident record that the coordination happened.

---

## 2. Storage Model

- **Format:** append-only JSONL file at `docs/agent-protocol/ledger/COORDINATION_LEDGER.jsonl` — one ledger entry (one JSON object) per line.
- **Append-only enforcement:** the file is write-append; the CI guard rejects any commit whose diff *modifies or deletes* an existing line (only additions at end-of-file are permitted). Git history plus the hash chain gives two independent tamper-evidence layers.
- **Genesis:** line 1 is the genesis entry (`seq: 0`, `prev_hash` = 64 zeros).
- **Sharding (optional):** for scale, the ledger may roll to monthly files (`COORDINATION_LEDGER_2026-06.jsonl`), each opening with a checkpoint entry whose `prev_hash` is the `entry_hash` of the previous shard's last entry — preserving one continuous chain.

---

## 3. Ledger Entry Schema

```yaml
# Coordination Ledger Entry Schema v1.0.0

schema_version: "1.0.0"

# ── Chain Position ────────────────────────────────────────────────────────────
seq: integer                        # (required) monotonically increasing, starts at 0 (genesis)
timestamp: string                   # (required) ISO 8601 UTC, e.g. "2026-06-21T09:14:35Z"
prev_hash: string                   # (required) SHA-256 hex (64 chars) of the previous entry's entry_hash; genesis = 64 zeros
entry_hash: string                  # (required) SHA-256 hex of canonical(this entry WITHOUT entry_hash) — see §4

# ── Event Classification ──────────────────────────────────────────────────────
entry_type:                         # (required) enum
  type: string
  allowed_values:
    - COORDINATION_DECISION   # a CONFIRM/REJECT that resolved a coordination
    - ARTIFACT_EXCHANGE       # an artifact passed and was accepted across a boundary
    - DISPUTE                 # a deadlock / rejection requiring escalation
    - ESCALATION              # handed to a human or ARB
    - GOVERNANCE_VOTE         # a non-binding ballot was cast/tallied
    - CONTRACT_UPDATE         # registry contract version changed (from CCR/ADR feedback loop)
    - IDENTITY_EVENT          # agent ACTIVE/SUSPENDED/RETIRED or key rotation
    - CORRECTION              # reverses/supersedes a prior entry (append-only correction)
    - CHECKPOINT              # shard boundary / periodic chain checkpoint

# ── Actors ────────────────────────────────────────────────────────────────────
actors:
  initiator: string                 # (required) agent_id (did:macp:...)
  counterpart: string               # (optional) agent_id; null for single-actor events
  human_role_holder: string         # (optional) wikilink — present for ESCALATION/governance-ratification

# ── Coordination Reference ────────────────────────────────────────────────────
correlation_id: string              # (required for coordination events) ties to the A2A conversation
message_ids: list[string]           # (optional) A2A message_ids comprising this coordination
contract_ref:
  contract_id: string               # (optional) e.g. "FW↔DATA-001"
  contract_version: string          # (optional)
decision_tier: string               # (optional) Tier-1|Tier-2|Tier-3|Tier-4

# ── Outcome ───────────────────────────────────────────────────────────────────
outcome:
  result: string                    # (required) CONFIRMED | REJECTED | COUNTERED | ESCALATED | RATIFIED | RECORDED
  summary: string                   # (required) ≥30 chars — human-readable one-line outcome
  confidence: number                # (optional) 0.0–1.0 of the deciding agent
  payload_hash: string              # (optional) content_sha256 of the exchanged artifact (links to A2A message)

# ── Governance Linkage ────────────────────────────────────────────────────────
linked_artifacts:                   # (optional) durable governance artifacts this coordination produced/used
  adr: string                       # ADR-NNNN
  ccr: string                       # CCR-NNNN
  escalation: string                # ESC-NNNN
  irc: string                       # IRD-NNNN (Integration Readiness Declaration)

# ── Correction (required when entry_type = CORRECTION) ────────────────────────
corrects:
  target_seq: integer               # seq of the entry being corrected
  target_entry_hash: string         # entry_hash of the target (immutable pointer)
  reason: string                    # ≥30 chars — why the prior entry was wrong

# ── Signature ─────────────────────────────────────────────────────────────────
signature:
  signer: string                    # (required) agent_id that wrote this entry
  algorithm: string                 # (required) "Ed25519"
  value: string                     # (required) Ed25519 signature over entry_hash
```

---

## 4. Hash Chain Construction

The chain is what makes the ledger tamper-evident. Each entry's hash binds it to its predecessor, so altering any historical entry invalidates every entry after it.

### 4.1 Canonicalization

1. Take the entry object **excluding** the `entry_hash` field (and excluding `signature.value`, which signs the hash).
2. Serialize it with **deterministic canonical JSON**: keys sorted lexicographically, no insignificant whitespace, UTF-8, numbers in canonical form (this matches the canonicalization used for `content_sha256` in [[A2A_MESSAGE_SCHEMA]]).

### 4.2 Hash Computation

```
entry_hash = SHA-256( prev_hash_bytes || canonical_json_bytes(entry_without_entry_hash) )
```

- `prev_hash` for `seq = 0` (genesis) is `0000…0000` (64 zero hex chars).
- `prev_hash` for `seq = n` is the `entry_hash` of `seq = n-1`.
- The signer then signs `entry_hash` with its Ed25519 private key (verifiable against its AID public key, [[AGENT_IDENTITY_SCHEMA]]).

### 4.3 Reference Pseudocode

```python
import hashlib, json

def canonical(entry: dict) -> bytes:
    e = {k: v for k, v in entry.items() if k != "entry_hash"}
    e = strip_signature_value(e)                      # keep signer/algorithm, drop value
    return json.dumps(e, sort_keys=True, separators=(",", ":")).encode("utf-8")

def compute_entry_hash(prev_hash_hex: str, entry: dict) -> str:
    h = hashlib.sha256()
    h.update(bytes.fromhex(prev_hash_hex))
    h.update(canonical(entry))
    return h.hexdigest()

def verify_chain(entries: list[dict]) -> bool:
    prev = "0" * 64
    for e in entries:
        if e["prev_hash"] != prev:
            return False                              # broken link
        if compute_entry_hash(prev, e) != e["entry_hash"]:
            return False                              # tampered content
        if not ed25519_verify(public_key_of(e["signature"]["signer"]),
                              e["entry_hash"], e["signature"]["value"]):
            return False                              # bad/forged signature
        prev = e["entry_hash"]
    return True
```

Any auditor (human or agent) runs `verify_chain` over the whole file; a single byte changed anywhere makes the verification fail at that entry and every entry after it.

---

## 5. Example Entries

**Genesis (seq 0):**
```json
{"schema_version":"1.0.0","seq":0,"timestamp":"2026-06-21T00:00:00Z","prev_hash":"0000000000000000000000000000000000000000000000000000000000000000","entry_type":"CHECKPOINT","actors":{"initiator":"did:macp:architect:primary"},"outcome":{"result":"RECORDED","summary":"MACP coordination ledger genesis block initialized."},"entry_hash":"3b1f...a92c","signature":{"signer":"did:macp:architect:primary","algorithm":"Ed25519","value":"eyJ...g0"}}
```

**Coordination decision — Tier-3 Auto-Confirm (the non-breaking branch of `FW↔DATA-001`):**
```json
{"schema_version":"1.0.0","seq":4127,"timestamp":"2026-06-21T09:14:35Z","prev_hash":"9c2e...11ab","entry_type":"COORDINATION_DECISION","actors":{"initiator":"did:macp:firmware:primary","counterpart":"did:macp:data:primary"},"correlation_id":"c0ffee-...-0001","message_ids":["5f2a-...-9c01","8d3b-...-2f10"],"contract_ref":{"contract_id":"FW↔DATA-001","contract_version":"2.1.0"},"decision_tier":"Tier-3","outcome":{"result":"CONFIRMED","summary":"Additive optional field battery_mv accepted; Tier-3 Auto-Confirm; transition window 2 sprints.","confidence":0.91,"payload_hash":"a17b...e9"},"linked_artifacts":{"ccr":"CCR-0031"},"entry_hash":"7a44...c0d1","signature":{"signer":"did:macp:data:primary","algorithm":"Ed25519","value":"eyJ...g4"}}
```

**Dispute + escalation — Tier-2 breaking branch:**
```json
{"schema_version":"1.0.0","seq":4128,"timestamp":"2026-06-21T09:15:02Z","prev_hash":"7a44...c0d1","entry_type":"ESCALATION","actors":{"initiator":"did:macp:firmware:primary","counterpart":"did:macp:data:primary","human_role_holder":"[[EMBEDDED_SYSTEMS_ARCHITECT_SKILL]]"},"correlation_id":"c0ffee-...-0007","contract_ref":{"contract_id":"FW↔DATA-001","contract_version":"2.1.0"},"decision_tier":"Tier-2","outcome":{"result":"ESCALATED","summary":"timestamp uint32→uint64 is breaking; routed to ADR with Architect approver.","confidence":0.94},"linked_artifacts":{"escalation":"ESC-0009","adr":"ADR-0051"},"entry_hash":"b9f0...7e22","signature":{"signer":"did:macp:firmware:primary","algorithm":"Ed25519","value":"eyJ...g5"}}
```

**Correction (append-only):**
```json
{"schema_version":"1.0.0","seq":4140,"timestamp":"2026-06-21T11:02:10Z","prev_hash":"d1c2...90ff","entry_type":"CORRECTION","actors":{"initiator":"did:macp:data:primary"},"corrects":{"target_seq":4127,"target_entry_hash":"7a44...c0d1","reason":"battery_mv range corrected to 0–4200 mV to match cell chemistry; prior 0–5000 superseded."},"outcome":{"result":"RECORDED","summary":"Supersedes seq 4127 ingest validation range."},"linked_artifacts":{"ccr":"CCR-0031"},"entry_hash":"f5aa...3b18","signature":{"signer":"did:macp:data:primary","algorithm":"Ed25519","value":"eyJ...g6"}}
```

Note the correction **does not edit seq 4127** — it appends seq 4140 pointing back at it. History stays intact; the current truth is computed by applying corrections.

---

## 6. What Gets Recorded (and What Does Not)

| Recorded (an entry is mandatory) | Not recorded (no entry) |
|----------------------------------|--------------------------|
| Any CONFIRM/REJECT/COUNTER that resolves a coordination | Bare `ACK` delivery receipts |
| Any artifact accepted across a boundary (ARTIFACT_EXCHANGE) | `QUERY` reads of the registries |
| Any deadlock/dispute and its escalation | Heartbeats |
| Any governance vote cast or tally produced | Intra-agent reasoning steps |
| Any contract version change (CONTRACT_UPDATE) | Draft messages never sent |
| Any agent status change or key rotation (IDENTITY_EVENT) | |

This keeps the ledger focused on **consequential** coordination — the same threshold the ADR/CCR logs use (significant decisions, not every keystroke).

---

## 7. Validation Rules

| Rule | Condition |
|------|-----------|
| V-LED-01 | `seq` is a non-negative integer, strictly increasing by 1 per entry |
| V-LED-02 | `seq = 0` entry has `prev_hash` = 64 zeros and `entry_type = CHECKPOINT` |
| V-LED-03 | For `seq = n > 0`, `prev_hash` equals the `entry_hash` of `seq = n-1` |
| V-LED-04 | `entry_hash` equals `SHA-256(prev_hash_bytes ‖ canonical(entry_without_entry_hash))` |
| V-LED-05 | `entry_type` ∈ the 9 allowed values |
| V-LED-06 | `signature.value` verifies (Ed25519) against `signature.signer`'s AID public key over `entry_hash` |
| V-LED-07 | `signature.signer` resolves to an AID that was `ACTIVE` (or whose `previous_public_keys` covers) at `timestamp` |
| V-LED-08 | For COORDINATION_DECISION/DISPUTE/ESCALATION, `correlation_id` is present and a valid UUID |
| V-LED-09 | `linked_artifacts.adr` / `.ccr` / `.escalation` / `.irc` match their ID regexes and exist in the respective registries |
| V-LED-10 | For `entry_type = CORRECTION`, `corrects.target_seq` < this `seq` and `corrects.target_entry_hash` matches that entry |
| V-LED-11 | No existing line is modified or deleted in any commit (append-only CI guard) |
| V-LED-12 | A Tier-1 decision is never recorded with `outcome.result = CONFIRMED` by an agent signer (must be RATIFIED with a `human_role_holder`) |
| V-LED-13 | `outcome.summary` ≥30 chars |

---

## 8. Audit & Query Operations

| Operation | Use |
|-----------|-----|
| `verify_chain()` | full tamper-evidence check (§4.3) — run on every audit and before any governance review |
| `trail(correlation_id)` | reconstruct one coordination end-to-end (messages → outcome → linked ADR/CCR) |
| `history(contract_id)` | every coordination touching a contract, in order |
| `disputes(window)` | all DISPUTE/ESCALATION entries in a time window — feeds the Engineering Process Review |
| `current_truth(seq)` | apply CORRECTION entries to resolve the effective state of a prior entry |
| `agent_activity(agent_id)` | all entries signed by an agent — accountability review |
| `tier1_audit()` | confirm zero Tier-1 entries were agent-CONFIRMED (safety invariant, V-LED-12) |

The `disputes(window)` and `tier1_audit()` operations feed directly into the [[AGENT_GOVERNANCE_PARTICIPATION|Engineering Process Review]] and the [[EVALUATION_HARNESS_SPEC|evaluation harness]], turning previously invisible coordination into a measurable signal.

---

## 9. Machine-Actionability Notes

An agent interacting with the ledger should:

1. **Append, never amend** — write new lines only; correct errors with CORRECTION entries.
2. **Chain correctly** — read the last entry's `entry_hash`, set it as `prev_hash`, compute and sign `entry_hash`.
3. **Verify on read** — when consuming the ledger for a decision, run `verify_chain` over at least the relevant `trail` before trusting it.
4. **Link governance artifacts** — populate `linked_artifacts` so the ledger and the ADR/CCR registries stay cross-navigable.
5. **Respect the Tier-1 invariant** — never write a `CONFIRMED` Tier-1 outcome; Tier-1 resolutions are `RATIFIED` and carry a `human_role_holder`.
6. **Record consequential events only** — follow the §6 inclusion list; do not pollute the ledger with reads/heartbeats.

---

## 10. Related Documents

- [[MULTI_AGENT_COORDINATION_PROTOCOL]] — master specification (Pillar 4 lives here)
- [[A2A_MESSAGE_SCHEMA]] — `correlation_id`, `message_ids`, and `payload_hash` originate here
- [[AGENT_IDENTITY_SCHEMA]] — entry signatures verify against AID public keys; key rotation is an IDENTITY_EVENT
- [[CONTRACT_REGISTRY_SCHEMA]] — CONTRACT_UPDATE entries record version bumps
- [[ADR_SCHEMA]], [[CCR_SCHEMA]] — durable artifacts the ledger references
- [[AGENT_GOVERNANCE_PARTICIPATION]] — consumes `disputes()` and `tier1_audit()`
- [[REVIEW_V2_PHASE3_AI_AGENT]] — §6.5 (audit-trail absence this closes)

#multi-agent #coordination-protocol #MACP #autonomy #coordination-ledger
