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

## 2026-05-01 02:04 UTC: Accidental invalid read path during heartbeat
- **What**: Accidental invalid read path during heartbeat
- **Context**: Heartbeat handling on 2026-05-01 00:04 UTC
- **Root cause**: I fired an unnecessary read call with a bad path before the real HEARTBEAT.md read, instead of using the known exact workspace path directly.
- **Pattern**: Minor workflow slip: unnecessary first tool call before the intended exact-path read.
- **Guardrail**: For heartbeat prompts, use only the exact HEARTBEAT.md path from the prompt/workspace and avoid any exploratory pre-read calls.
- **Status**: logged

## 2026-05-14 08:03 UTC: Sent a scheduled reminder before its actual due time
- **What**: Sent a scheduled reminder before its actual due time
- **Context**: Heartbeat handling for Thursday dev sync reminder
- **Root cause**: I matched the reminder to the day but failed to verify the exact scheduled UTC time before replying
- **Pattern**: TBD
- **Guardrail**: For heartbeat reminders, compare the current UTC timestamp against the exact scheduled UTC time before sending any reminder
- **Status**: logged

## 2026-05-19 19:50 UTC: Treated the first-class browser tool as unavailable and switched messaging to 'cannot submit' before checking the local agent-browser path
- **What**: Treated the first-class browser tool as unavailable and switched messaging to 'cannot submit' before checking the local agent-browser path
- **Context**: Job application automation during Anthropic/Holepunch application work on 2026-05-19
- **Root cause**: I anchored on one browser path failing and claimed a capability limitation before checking the alternative local browser path already documented in TOOLS.md
- **Pattern**: Same family as wrong assumptions about access/capability before verification
- **Guardrail**: When browser automation appears unavailable, verify the documented local browser path (agent-browser) before telling Kolade submission cannot be automated
- **Status**: logged

## 2026-05-22 17:51 UTC: Robin long-running requests timed out in foreground
- **What**: Robin long-running requests timed out in foreground
- **Context**: Private Robin listener handling substantive 'run the lanes' requests on 2026-05-22
- **Root cause**: The listener routed long-running research work through the short foreground path with a 300s timeout instead of acknowledging immediately and delegating to a longer background runner
- **Pattern**: Avoid using the same synchronous reply path for both lightweight chat and substantive multi-lane execution
- **Guardrail**: Any request likely to exceed quick-reply latency must be acknowledged first and moved to a background worker with lane-appropriate timeout before the reply path starts the heavy work
- **Status**: logged

## 2026-05-24 19:51 UTC: Used ambiguous portfolio screenshot columns as if they were verified position values
- **What**: Used ambiguous portfolio screenshot columns as if they were verified position values
- **Context**: US stock update sent after reading a Bamboo screenshot on 2026-05-24
- **Root cause**: I inferred market values and ranking from unclear screenshot columns instead of first reconstructing explicit ticker, market value, and portfolio-percent fields
- **Pattern**: Same family as acting on unverified structure from screenshots or UI summaries
- **Guardrail**: For portfolio screenshots, do not send allocation or rebalance guidance until each row is mapped to explicit ticker, market value, and weight columns; if any column meaning is ambiguous, label the summary provisional and ask for the raw screenshot or cleaner data
- **Status**: logged

## 2026-05-25 13:51 UTC: Claimed browser automation was unavailable before fully verifying the documented agent-browser path
- **What**: Claimed browser automation was unavailable before fully verifying the documented agent-browser path
- **Context**: Germany visa portal research and Robin follow-up on 2026-05-24/25
- **Root cause**: I treated one browser route failing on this host as a capability limit and let that shape the user-facing message before exhausting the documented local browser path and its constraints
- **Pattern**: Repeat of the browser-capability assumption family already logged on 2026-05-19
- **Guardrail**: When a web task is blocked by one browser path, verify the documented local agent-browser route and report the exact failing step before saying browsing or submission is unavailable
- **Status**: logged

## 2026-06-07 09:51 UTC: Robin foreground path retriggered a known research timeout pattern
- **What**: Robin foreground path retriggered a known research timeout pattern
- **Context**: Robin private research request on 2026-06-07 to run a news link and show results timed out after 330 seconds before the listener was patched
- **Root cause**: The listener still allowed some run/check-this-link style research prompts onto the short-lived inline path instead of treating them as long-running work and delegating immediately
- **Pattern**: Repeat of the Robin foreground-timeout family logged on 2026-05-22
- **Guardrail**: Route any request to run, check, or inspect a link for substantive results through the background runner when browsing/research may exceed quick-reply latency; keep the inline path for lightweight chat only
- **Status**: logged

