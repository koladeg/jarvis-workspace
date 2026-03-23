# Orisynx Frontend Prioritized Recommendations

## Priority 0 — Must do before MVP alignment

### 1. Pick and enforce one frontend data architecture
**Problem**
- Repo currently mixes backend API, IndexedDB/local-first infrastructure, and page-level mock data.

**Files**
- `lib/api-client.ts`
- `lib/api-service.ts`
- `lib/db.ts`
- `lib/db-service.ts`
- `lib/db-seed.ts`
- `README.md`
- `conductor/product.md`

**Action**
- Decide MVP source of truth
- Put all entity reads/writes behind repositories
- Remove or isolate the non-MVP path

**Acceptance criteria**
- Pages no longer import mixed persistence assumptions
- No inline mock arrays in core routes
- Architecture docs match implementation

---

### 2. Introduce workspace-aware routing and state
**Problem**
- No workspace isolation exists in routes, hooks, or UI shell.

**Action**
- Add workspace-aware route model, e.g. `/workspaces/[workspaceId]/...`
- Scope data hooks and cache keys to workspace
- Add workspace selector in shell

**Acceptance criteria**
- Workspace ID is visible in route/state model
- Lists/details are workspace-scoped
- UI actions respect selected workspace context

---

### 3. Redesign dashboard as read-only workspace overview
**Problem**
- Current dashboard is action-heavy and global, not read-only and not workspace-based.

**Files**
- `app/(main)/page-client.tsx`
- `components/layout/app-sidebar.tsx`

**Action**
- Convert dashboard into passive overview
- Move mutations into contextual workflows
- Hide/disable create/edit actions in read-only mode

**Acceptance criteria**
- Dashboard can render in read-only mode
- Actions are capability-gated
- Dashboard content is workspace-specific

---

### 4. Create the Canvas shell
**Problem**
- No canvas metaphor exists in current architecture.

**Action**
- Add a dedicated canvas route and layout
- Define panel/card/node primitives
- Create the first real canvas flow instead of a standard admin page

**Acceptance criteria**
- Canvas exists as a first-class route/shell
- At least one core workflow is canvas-driven
- Canvas state is workspace-aware

---

### 5. Refactor oversized route components
**Top files**
- `app/(main)/audit/[id]/page-client.tsx`
- `app/(main)/tasks/[id]/page-client.tsx`
- `app/(main)/users/[id]/page-client.tsx`
- `app/(main)/findings/[id]/page-client.tsx`
- `app/(main)/capa/[id]/page-client.tsx`
- `app/(main)/users/page-client.tsx`
- `app/(main)/findings/page-client.tsx`
- `app/(main)/tasks/page-client.tsx`

**Action**
- Split each into feature sections/components/hooks/view-model mappers

**Acceptance criteria**
- No route component >300 lines unless strongly justified
- Detail pages composed from modular sections
- Route files act mainly as composition shells

---

## Priority 1 — High impact follow-up

### 6. Standardize domain enums and badge/filter mappings
**Problem**
- Repeated local `getStatusColor` helpers and ad hoc label/slug transforms.

**Action**
- Create shared enums/constants/status metadata
- Introduce shared `StatusBadge` components

**Acceptance criteria**
- No local `getStatusColor` helpers in pages
- Filters use shared status definitions

---

### 7. Extract shared create-and-log mutation helpers
**Problem**
- Repeated create entity + create history + toast + refetch pattern.

**Files**
- `app/(main)/audit/new/page-client.tsx`
- `app/(main)/tasks/page-client.tsx`
- `app/(main)/findings/page-client.tsx`
- `app/(main)/capa/page-client.tsx`
- `app/(main)/users/page-client.tsx`

**Action**
- Create mutation helper or feature service wrapper

**Acceptance criteria**
- Repeated mutation boilerplate removed
- History logging standardized

---

### 8. Remove or replace placeholder UX in core routes
**Problem**
- Many “coming soon” actions still appear in main user paths.

**Action**
- Either implement them or hide them from MVP

**Acceptance criteria**
- No dead-end buttons in primary flows
- Tabs either work or are removed

---

### 9. Stabilize the test suite
**Problem**
- Tests exist but are partially drifted from current implementation.

**Observed failures**
- `app/(main)/findings/findings-validation.test.tsx`
- `app/(main)/capa/capa-validation.test.tsx`

**Action**
- Update tests to current architecture
- Separate unit tests from integration assumptions
- Add smoke coverage for workspace/dashboard changes

**Acceptance criteria**
- `pnpm test` passes reliably
- test intent matches current source of truth

---

### 10. Stop suppressing build/type issues
**Files**
- `next.config.mjs`

**Problem**
- Unsupported Next 16 eslint config
- `typescript.ignoreBuildErrors = true`

**Action**
- Remove deprecated config
- restore build-time type safety

**Acceptance criteria**
- build is clean without ignored type failures
- Next config warnings removed

---

## Priority 2 — Quality and maintainability improvements

### 11. Normalize docs and branding
- Make `Orisynx` vs `Audicity` consistent
- Align README with actual architecture
- Decide whether local-first is still intended

### 12. Split `hooks/use-store.ts` by feature
- `useAudit*`, `useFinding*`, `useTask*`, etc. should live with their feature domains
- rename away from “store” unless a real store is introduced

### 13. Use shared page layouts consistently
- `PageLayout` and `TwoColumnLayout` exist but are not used in app pages
- either adopt them or delete them

### 14. Remove render-time debug logging
- remove `console.log` from `audit/new/page-client.tsx`
- remove repeated dev logging in route render logic

### 15. Introduce view models for detail pages
- stop fabricating UI-only fields inline in route components
- map raw entities to `DetailViewModel`s in services/selectors

---

## Suggested implementation sequence

### Sprint 1
- Decide architecture source of truth
- Clean Next config/build safety
- Fix failing tests
- Standardize status enums and shared badges

### Sprint 2
- Introduce workspace-aware route model
- Refactor dashboard into read-only workspace overview
- Split `audit/[id]` and `findings/page-client` into feature modules

### Sprint 3
- Implement canvas shell
- migrate one key workflow to canvas interaction
- add workspace-aware action gating

### Sprint 4
- remove remaining placeholder flows
- finish page modularization for tasks/CAPA/users
- stabilize tests for new architecture

---

## Quick wins shortlist

1. Remove `typescript.ignoreBuildErrors`
2. Remove deprecated `eslint` config from `next.config.mjs`
3. Fix failing Jest tests
4. Replace repeated status helpers with shared metadata
5. Remove visible “coming soon” tabs/buttons from core screens
6. Normalize product naming across docs and UI
7. Split `hooks/use-store.ts`
