# [SYSTEM]

You are a senior organizational architect closing fragile connection F1 from Review Part 2 Phase 1. The OTA chain has per-hop SLAs but no chain-level timeout owner — no single role monitors the end-to-end wall-clock time from model registration to fleet ACTIVE status. You will assign this ownership to the Backend/Cloud Engineer, whose device twin synchronization monitoring already provides cross-fleet visibility of model version distribution. This is a small, precise surgical edit. Output one block.

# [TASK]

Add OTA chain-level timeout ownership to [[BACKEND_CLOUD_ENGINEER_SKILL]] §3.6 (Post-Launch/Market) activities and add a corresponding metric to §10.

# [CONTEXT]

The [[REVIEW_V2_PHASE1_VALUE_CHAIN|Phase 1]] found that while the OTA Model Artifact Contract defines per-hop status transition timeouts and an end-to-end timeout (24h staged / 1h hotfix), no single role owns the wall-clock monitoring of the full chain. Individual hops have SLAs but the chain-level transaction time is unmonitored. F1 recommended assigning this to [[BACKEND_CLOUD_ENGINEER_SKILL|Backend]] because Backend already monitors device twin desired-vs-reported state drift across the fleet — the same mechanism that detects OTA campaign health can be extended to own chain-level timeout alerting.

# [OUTPUT FORMAT]

One block.

## BLOCK 1: OTA Chain-Level Timeout Ownership for [[BACKEND_CLOUD_ENGINEER_SKILL]]

**(a) Add to §3.6 Post-Launch/Market activities:**

- **OTA chain-level timeout monitoring:** Own the end-to-end OTA transaction time across the full OTA chain ([[MLOPS_ENGINEER_SKILL|MLOps]] registration → [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]] distribution → [[FIRMWARE_ENGINEER_SKILL|Firmware]] download/apply → Backend ACTIVE status). Monitor the wall-clock time from MLOps model artifact registration to Firmware ACTIVE status for every OTA campaign. Alert if: (a) any device exceeds the end-to-end timeout defined in the OTA Model Artifact Contract (24 hours for staged rollout, 1 hour for urgent hotfix) without reaching ACTIVE or ROLLED_BACK, (b) any stage fails to complete within its allocated window, or (c) the campaign-level completion rate stalls (no progress for >2 hours during active rollout). Chain-level timeout alerts notify [[MLOPS_ENGINEER_SKILL|MLOps]], [[DEVOPS_PLATFORM_ENGINEER_SKILL|DevOps]], and [[PRODUCT_OWNER_TECHNICAL_PROJECT_MANAGER_SKILL|PO/TPM]] within 5 minutes. Publish an OTA Chain Performance Report within 1 business day of campaign completion including: per-hop latency distribution, chain-level timeout incidents, and root causes of any timeout

**(b) Add to §10 Technical metrics:**

- **OTA chain-level timeout compliance:** ≥99% of OTA campaigns complete within the end-to-end timeout (24h staged / 1h hotfix). Zero devices exceed the timeout without alerting. Measured per campaign; reported in the OTA Chain Performance Report. #ota-chain-timeout #F1

# [CONSTRAINTS]

- [[wiki-links]], #ota-chain-timeout #F1 tags
- Acronyms defined on first use
- Match existing BACKEND SKILL.md tone
- Append to existing §3.6 and §10 content — do not replace
