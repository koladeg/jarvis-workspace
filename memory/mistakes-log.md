# Mistakes Log

## 2026-04-12 16:09 UTC: Assumed Drive access was unavailable before checking all existing auth paths
- **What**: I said Google Drive/Docs access was not available, even though an existing saved Google refresh token could still restore Drive read access without asking Kolade to re-auth.
- **Context**: Bitfinex CV delivery + follow-up discussion about Google Drive and the AdugboInsure pipeline.
- **Root cause**: Assumption error + process gap. I tested one CLI path, saw a 401, and concluded the capability was unavailable before checking alternate credential stores and the existing pipeline/auth files.
- **Pattern**: Access/auth troubleshooting can fail when I stop at the first broken path instead of tracing all known auth locations.
- **Guardrail**: Before declaring a service unavailable, verify all known local auth paths first: workspace credentials, tool-specific config dirs, related pipeline scripts, and any saved refresh tokens. Only then report the true scope: read-only, write-capable, expired, or fully unavailable.
- **Status**: logged and guardrail adopted

## 2026-04-19 22:38 UTC: Reported AutoScout24 truck listing pages as live without re-verifying that the URLs still resolved
- **What**: Reported AutoScout24 truck listing pages as live without re-verifying that the URLs still resolved
- **Context**: Truck search summary sent to Kolade with direct listing links that now no longer exist
- **Root cause**: Process gap: I treated scraped listing URLs as durable results and did not do a final live-access verification step before presenting them as current matches
- **Pattern**: Marketplace listing links can expire/change quickly; final answer must distinguish live verified listings from stale scraped references
- **Guardrail**: For marketplace/listing research, verify each final URL immediately before reporting it; if not live, label it expired/stale and do not present it as an active result
- **Status**: logged

## 2026-04-21 06:47 UTC: Optimized workflow setup before urgent deliverable
- **What**: Optimized workflow setup before urgent deliverable
- **Context**: nsave job application support in Jarvis-Job-Search; user needed CV quickly
- **Root cause**: I prioritized tracker/skill setup over the immediate bottleneck and delayed the user-facing deliverable
- **Pattern**: Premature workflow setup before urgent execution
- **Guardrail**: When a user is blocked on a live application or form, finish the minimum viable deliverable first; defer tooling/tracker improvements until after the artifact is sent
- **Status**: logged

## 2026-04-27 18:07 UTC: Claimed email send path was unavailable before verifying
- **What**: Claimed email send path was unavailable before verifying
- **Context**: Headway resume delivery during job-application support in Jarvis-Job-Search
- **Root cause**: I relied on an assumption about tool/access availability instead of checking the existing workspace automation/email path first.
- **Pattern**: Wrong assumptions about access/auth or delivery capability need verification before claiming blocked/unavailable.
- **Guardrail**: Before saying an external delivery path is unavailable, first check for existing workspace scripts/configs/credentials that already implement it, then test the smallest safe path.
- **Status**: logged

