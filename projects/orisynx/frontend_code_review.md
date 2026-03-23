# Orisynx Frontend Code Review

_Date:_ 2026-03-22  
_Repo reviewed:_ `Audit-IS/fe`  
_Reviewed commit:_ `1f7f747` (`main`)

## Executive Summary

Orisynx FE is currently a **high-fidelity frontend prototype with partial data wiring**, not yet an MVP aligned to the 2026-03-22 product brief. The app has a solid visual foundation—Next.js App Router, shadcn/ui, Tailwind, reusable form primitives, and broad route coverage—but the implementation is still **page-centric, mock-heavy, and inconsistent at the architecture level**.

The biggest frontend issues are:

1. **Architecture drift**: the codebase mixes three competing models—backend API, IndexedDB/local-first, and hardcoded page-level mock data.
2. **Overgrown route components**: many pages are 400–750 lines and contain UI, data orchestration, derived state, mock content, and action handlers in one file.
3. **Weak domain alignment**: the current product is an audit-management dashboard, while the brief calls for concepts like **Canvas metaphor**, **Workspace isolation**, and **read-only dashboard behaviors** that do not yet exist in the frontend architecture.
4. **Pattern inconsistency**: repeated helper functions, repeated create-and-log flows, inconsistent naming/status handling, and several “coming soon” placeholders inside production routes.
5. **Testing quality is mixed**: there is decent test coverage breadth, but multiple Jest tests are failing and some tests appear to reflect older storage assumptions.

### Overall assessment

- **Visual/UI maturity:** good
- **Architecture maturity:** fair to weak
- **Maintainability:** moderate risk
- **MVP brief alignment:** low
- **Refactor urgency:** high

---

## 1. Architecture Assessment

### 1.1 Folder structure evaluation

### What is good

The top-level structure is recognizable and generally clean:

- `app/` for routes
- `components/ui/` for shadcn primitives
- `components/common/` for reusable app pieces
- `components/layout/` for shell/navigation/header
- `hooks/` for data hooks
- `lib/` for API, auth, DB, and utilities
- `e2e/` and colocated `.test.tsx` files for testing

This is a reasonable starting structure for a Next.js App Router app.

### What is weak

The structure is **organized physically, but not architecturally**.

The codebase is grouped mostly by framework conventions and UI buckets, but the actual feature logic is still concentrated in route files. The result is:

- route files becoming mini-monoliths
- feature behavior spread across `app/`, `hooks/`, `lib/`, and inline mock arrays
- no stable feature module boundaries
- weak separation between domain logic, UI state, and transport/storage

### Evidence

Large route files include:

- `app/(main)/audit/[id]/page-client.tsx` — 756 lines
- `app/(main)/tasks/[id]/page-client.tsx` — 685 lines
- `app/(main)/users/[id]/page-client.tsx` — 626 lines
- `app/(main)/findings/[id]/page-client.tsx` — 584 lines
- `app/(main)/capa/[id]/page-client.tsx` — 583 lines
- `app/(main)/users/page-client.tsx` — 567 lines
- `app/(main)/profile/page.tsx` — 555 lines
- `app/(main)/capa/page-client.tsx` — 538 lines
- `app/(main)/findings/page-client.tsx` — 531 lines

### Recommendation

Move from the current route-first structure to **feature modules**, e.g.:

```text
features/
  audits/
    components/
    hooks/
    services/
    mappers/
    types/
  findings/
  tasks/
  capa/
  workspaces/
  dashboard/
```

Then keep `app/.../page.tsx` thin and compositional.

---

### 1.2 Component hierarchy

### Good

There is a healthy primitive layer:

- `components/ui/*`
- reusable form controls in `components/common/form/*`
- layout pieces like `PageHeader`, `AppSidebar`

This suggests the team is already thinking in reusable UI building blocks.

### Weak

The hierarchy breaks down above the primitive layer.

Instead of assembling pages from feature-level sections/components, many pages inline everything:

- filter bars
n- stat cards
- dialog forms
- list item rendering
- color/status helpers
- action orchestration
- temporary placeholders

This makes pages hard to test, hard to reuse, and expensive to refactor.

### Recommendation

Break pages into feature components such as:

- `AuditSummaryCards`
- `AuditFilters`
- `AuditList`
- `AuditListItem`
- `CreateAuditDialog`
- `FindingsStats`
- `FindingsFilters`
- `FindingsTable` or `FindingsBoard`

---

### 1.3 State management approach

Current approach:

- page-local `useState` for filters and dialogs
- generic fetch hooks in `hooks/use-store.ts`
- transport via `ApiService`
- auth state via `AuthService` + `localStorage`
- optional IndexedDB infrastructure via `db.ts`, `db-service.ts`, `db-seed.ts`

### Main issue: state model is contradictory

The repo currently implies three different architectural directions:

1. **Backend API app**
   - `lib/api-client.ts`
   - `lib/api-service.ts`
   - `lib/auth-service.ts`
   - README says backend + MongoDB

2. **Local-first IndexedDB app**
   - `lib/db.ts`
   - `lib/db-service.ts`
   - `lib/db-seed.ts`
   - `conductor/product.md` emphasizes local-first and IndexedDB

3. **Page-level mock data app**
   - hardcoded arrays and extended mock objects embedded inside page components

These models are not reconciled.

### Why it matters

This ambiguity will block the brief requirements:

- workspace isolation needs a first-class boundary in data/state
- read-only dashboard views need capability-aware selectors and route guards
- canvas metaphor needs app-wide interaction/state composition

None of that is easy while storage and state ownership remain unclear.

### Recommendation

Choose one explicit frontend data architecture for MVP:

- **Preferred for MVP**: API-backed app with typed frontend repositories + query layer
- Or, if local-first is intentional: IndexedDB-first with a sync adapter abstraction

Either way, introduce a stable abstraction like:

```ts
interface AuditRepository {
  list(): Promise<Audit[]>;
  getById(id: string): Promise<Audit | null>;
  create(input: CreateAuditInput): Promise<Audit>;
}
```

Then let pages consume repositories/hooks, not raw transport assumptions.

---

### 1.4 Routing and navigation setup

### Good

- App Router route grouping is sensible: `(auth)` and `(main)`
- Detail routes exist for core modules
- shared shell via `app/(main)/layout.tsx`

### Weak

Routing is still shaped around a classic admin dashboard, not the brief.

Current navigation centers on:

- Dashboard
- Create Audit
- Task Manager
- Calendar
- Findings
- CAPA
- Users
- Documents
- Templates
- Reports
- Analytics
- Audit History
- Notifications

This is fine for the current audit product, but does **not map to**:

- Canvas metaphor
- Workspace isolation
- read-only dashboard mode per role/workspace
- clearer object hierarchy implied by the new brief

### Additional issue

`ProtectedRoute` is client-side only and checks `AuthService.isAuthenticated()` from a token in localStorage. From a frontend architecture perspective, this is fragile for route composition and role-aware rendering.

### Recommendation

Refactor navigation around primary product objects and context:

- Workspace switcher / selector
- Canvas / board / editor entry point
- contextual left nav per workspace
- dashboard as a read-only overview within selected workspace

---

### 1.5 Asset/config organization

### Issues found

- `next.config.mjs` still includes deprecated/unsupported `eslint` config behavior for Next 16
- `typescript.ignoreBuildErrors = true`
- README, docs, and implementation disagree on storage architecture
- brand naming is inconsistent: README/product/docs still say **Audicity**, UI says **Orisynx**

### Recommendation

Standardize:

- one product name
- one architecture story
- one environment setup story
- one source of truth for app behavior assumptions

---

## 2. Code Quality Review

### 2.1 Naming conventions

### Good

- TypeScript types are generally well named (`Audit`, `Finding`, `CAPA`, `HistoryLog`)
- file names are mostly conventional
- route names are understandable

### Issues

1. **Brand inconsistency**
   - `Audicity` in docs/types/db names/README
   - `Orisynx` in UI branding

2. **Status vocabulary inconsistency**
   - statuses differ by module and are often mapped ad hoc
   - some filters slugify statuses inline (`replace(' ', '-')`)
   - some pages define local `getStatusColor`, some use shared helpers

3. **Mixed naming semantics**
   - `use-store.ts` is not actually a store; it is a group of fetch hooks
   - `api-service` vs `db-service` vs inline mocks create naming confusion around source of truth

### Recommendation

Create shared enums/constants, e.g.:

```ts
export const TASK_STATUS = ['To Do', 'In Progress', 'In Review', 'Completed'] as const;
export type TaskStatus = (typeof TASK_STATUS)[number];
```

And centralize label ↔ slug ↔ color mapping.

---

### 2.2 Code duplication

There is meaningful duplication across the app.

### Examples

- repeated `getStatusColor` helpers in multiple pages
- repeated create form submission pattern:
  - create entity
  - get current user
  - call `ApiService.createHistory`
  - toast success/error
  - refetch
- repeated filter/search card layout
- repeated stat-card layout patterns
- repeated page scaffolding instead of using `PageLayout`

`PageLayout`/`TwoColumnLayout` exist but are effectively unused in application routes.

### Recommendation

Extract shared feature patterns:

- `createEntityWithAuditLog(...)`
- `EntityListFilters`
- `StatusBadge`
- `MetricCard`
- `EmptyState`
- `DetailSidebar`
- `EntityCommentsPanel`

---

### 2.3 Component reusability

### Good

- reusable validated form components are a strong foundation
- `PageHeader` is broadly reusable
- UI primitives are properly centralized

### Weak

Most feature-level UIs are still too page-specific to be reused. For example:

- audit detail sections are embedded in `audit/[id]/page-client.tsx`
- findings list cards are embedded in `findings/page-client.tsx`
- user list cards and role views are embedded in `users/page-client.tsx`

The app has **reusable primitives**, but not enough **reusable domain components**.

---

### 2.4 Performance and maintainability bottlenecks

Primary risks:

1. **Huge client components**
   - expensive to understand and rerender
   - difficult to memoize selectively
   - difficult to test surgically

2. **Derived data recomputed inline**
   - lots of `.filter()`, `.map()`, `.reduce()` inside render paths
   - acceptable now at small scale, but weak for growth

3. **Debug logging inside UI render paths**
   - examples in `app/(main)/history/page-client.tsx`
   - multiple `console.log(...)` usages in `audit/new/page-client.tsx`

4. **Mock expansion inside detail routes**
   - detail pages augment real entities with large hardcoded objects/arrays on every render

5. **Build safety disabled**
   - `typescript.ignoreBuildErrors = true`
   - deprecated Next config usage

### Recommendation

- split heavy pages
- memoize derived selectors where needed
- remove render-time logging
- move fixtures/mocks into explicit mock/fixture files
- stop suppressing type/build failures

---

### 2.5 TypeScript usage

### Strengths

- TypeScript is used across the codebase
- shared domain types exist in `lib/types.ts`
- form schemas with Zod are in use

### Weaknesses

1. Types are broad and stringly in places where domain enums should be tighter.
2. `Partial<T>` is used heavily in create flows without dedicated input types.
3. Build-time type safety is undermined by:
   - `typescript.ignoreBuildErrors = true`
4. Generic store typing in `db-service.ts` relies on `any` escapes.
5. Some route code mixes real and synthetic fields without clear DTO/view-model boundaries.

### Recommendation

Introduce:

- `CreateAuditInput`, `UpdateAuditInput`, etc.
- view-model mappers for UI-only fields
- tighter status/type enums
- explicit `AuditDetailViewModel` rather than mutating raw API records in-component

---

### 2.6 Test coverage insights

### Coverage breadth is decent

Detected:

- **26** unit/integration test files
- **5** Playwright E2E files

That is a good signal.

### But test health is not stable

Observed issues:

- `corepack pnpm test -- --runInBand` failed due to incorrect CLI forwarding and matched no tests
- `corepack pnpm test` surfaced failing Jest tests
- at least some tests appear coupled to old UI labels or older DB-based implementation assumptions

Examples from observed test failures:

- `app/(main)/findings/findings-validation.test.tsx`
  - expects button name `Log New Finding`
  - rendered UI exposes `Log Finding`
- `app/(main)/capa/capa-validation.test.tsx`
  - expects DB service interaction, but current page flow uses API service

### Assessment

Tests exist, but the suite is partially **drifted from implementation**. That reduces confidence significantly.

---

## 3. MVP Brief Alignment

## Bottom line

The current frontend does **not align closely** with the 2026-03-22 MVP brief.

It aligns to a **traditional audit/admin dashboard**, not a workspace/canvas-centered product.

### 3.1 Current screens vs likely brief requirements

### What exists today

Current implemented screens/routes include:

- login/register
- dashboard
- audit list/detail/create
- findings list/detail
- tasks list/detail
- CAPA list/detail
- users list/detail
- templates list/create
- documents
- reports
- analytics
- history
- notifications
- profile
- calendar

### What appears missing relative to the brief

Based on the requested review criteria, the frontend is missing or not structurally prepared for:

- **Canvas metaphor** as a primary interaction surface
- **Workspace isolation** as a first-class app boundary
- **Dashboard read-only behavior** per workspace/role/context
- likely clearer role/context-aware content partitioning
- architecture that treats workspaces as top-level routing/state entities

---

### 3.2 Missing implementation: Canvas metaphor

No route, component hierarchy, or layout system suggests a canvas-first UI.

Current interaction style is:

- list pages
- detail pages
- form dialogs
- dashboard cards
- admin-sidebar navigation

That is fundamentally different from a canvas model.

### Impact

This is not a “small missing feature”; it is an **interaction paradigm mismatch**.

### What needs refactoring

To support a canvas metaphor, the frontend likely needs:

- a dedicated canvas route/shell
- spatial/board-style layout components
- composable panels/cards/nodes
- drag/rearrange/selection state
- workspace-scoped object loading
- non-page-centric interaction flows

---

### 3.3 Missing implementation: Workspace isolation

There is currently no clear workspace concept in routing, state, or data contracts.

No evidence of:

- workspace ID in route structure
- workspace-scoped repositories/hooks
- workspace selector or switcher
- workspace-aware permissions/view filtering
- workspace-aware cache partitioning

### Why it matters

Workspace isolation should affect:

- navigation
- data loading
- visibility rules
- dashboard contents
- mutation permissions
- shared components and query keys

Right now, the app is globally scoped.

---

### 3.4 Missing implementation: Dashboard read-only mode

The dashboard today is action-oriented:

- `New Audit`
- detail/edit flow orientation
- “View Report” / “Export” actions
- module-wide actionable cards

There is no clear mode boundary for read-only behavior by role/workspace.

A proper brief-aligned dashboard would need:

- explicit read-only route or mode
- capability-based hiding/disabling of actions
- passive insight-first layout
- consistent “view-only” affordances

---

### 3.5 Current placeholder/unimplemented UI affecting MVP

There are many route-level placeholders and “coming soon” behaviors in core pages, including:

- task tabs still placeholder text
- findings secondary tabs placeholder text
- CAPA effectiveness view placeholder
- report generation/sharing placeholders
- document upload/view/share placeholders
- audit detail upload/share/team actions placeholders
- history export placeholders
- template preview/use placeholders
- calendar scheduling placeholder
- various page-header actions using toast-only behavior

This means even within the current audit-dashboard concept, the frontend is not yet functionally complete.

---

### 3.6 Prioritized list of frontend changes needed for brief alignment

#### P0 — Required before claiming MVP alignment

1. Introduce **workspace-aware routing and state model**
2. Define and implement the **Canvas** shell / primary interaction model
3. Refactor dashboard into **read-only workspace overview**
4. Remove architecture ambiguity between API / IndexedDB / mock data
5. Replace page-level hardcoded mock detail sections with repository-backed view models

#### P1 — Strongly recommended next

6. Break large route files into feature modules/components
7. Add role/capability-aware UI rendering rules
8. Standardize status enums, filters, badges, and action models
9. Replace placeholder tabs/actions with real states or remove from MVP
10. Fix failing test suite and align tests to current architecture

#### P2 — Quality and scale improvements

11. Introduce app-wide query/cache strategy
12. Introduce workspace switcher and persisted context
13. Improve design system usage at feature level
14. Normalize docs, naming, and environment expectations

---

## 4. Specific Files / Components That Need Attention

## Highest priority

### 1. `app/(main)/audit/[id]/page-client.tsx`
Why:
- 756-line page component
- mixes live data with large hardcoded mock arrays
- detail route is carrying too much presentation and temporary domain logic

### 2. `app/(main)/findings/page-client.tsx`
Why:
- overloaded page
- inline form dialog + stats + filters + list + placeholder tabs
- not aligned to reusable feature composition

### 3. `app/(main)/tasks/page-client.tsx`
Why:
- repeated patterns from findings/CAPA
- placeholder tabs still visible in main UX
- hardcoded defaults in create flow

### 4. `app/(main)/capa/page-client.tsx`
Why:
- repeated create/log/list pattern
- placeholder effectiveness tab blocks real workflow credibility

### 5. `hooks/use-store.ts`
Why:
- generic hook bundle has grown too large
- naming suggests state store, but it is a collection of fetch hooks
- should be split by feature and data source abstraction

### 6. `lib/api-client.ts`
Why:
- central transport is fine, but overall architecture depends on it while docs/db layer imply other sources
- no typed repository boundary above it

### 7. `next.config.mjs`
Why:
- deprecated `eslint` config path for Next 16
- `ignoreBuildErrors` weakens engineering discipline

### 8. `components/layout/app-sidebar.tsx`
Why:
- current IA is product-misaligned for workspace/canvas brief
- static admin navigation will likely need redesign

### 9. `app/(main)/page-client.tsx`
Why:
- dashboard is currently action-heavy and classic-admin in structure
- not read-only/workspace-aware

### 10. `README.md`, `conductor/product.md`, `.docs/unimplemented_features.md`
Why:
- architecture/product naming drift
- team will keep building against conflicting assumptions unless docs are normalized

---

## 5. Recommendations

### Quick wins — low effort, high impact

1. **Standardize brand naming** across docs and UI
2. **Remove render-time `console.log` / dev logs** from route components
3. **Replace repeated local `getStatusColor` helpers** with shared status maps
4. **Use `PageLayout` consistently** or remove it if not needed
5. **Hide placeholder tabs/actions from MVP routes** instead of shipping “coming soon” everywhere
6. **Rename `hooks/use-store.ts`** to reflect actual role, or split it by feature
7. **Fix failing Jest tests** and rebaseline snapshots/assertions
8. **Remove unsupported Next config entries**

### Refactoring priorities

1. **Feature modularization** of routes
2. **Repository/service abstraction** over transport/storage
3. **Workspace-aware app shell**
4. **Dashboard redesign for read-only mode**
5. **Canvas-first interaction surface**

### Pattern standardization

Introduce shared patterns for:

- statuses, labels, and colors
- list filter bars
- metric cards
- create/edit dialog workflows
- activity log creation
- detail page sidebars/panels
- empty/loading/error states

---

## 6. Ticket Recommendations for ClickUp

### Epic A — Frontend Architecture Realignment
- Create feature-module structure for audits/findings/tasks/CAPA/users
- Move route logic into feature components/hooks/services
- Introduce repository abstraction layer
- Split `hooks/use-store.ts` by feature

### Epic B — MVP Brief Alignment
- Add workspace-aware route model
- Add workspace selector/switcher UX
- Implement read-only dashboard mode
- Design and implement Canvas shell

### Epic C — Core UI Quality
- Standardize status badges, filters, and shared list patterns
- Remove placeholder actions from MVP scope
- Replace inline mocks with repository-backed view models
- Normalize empty/loading/error states

### Epic D — Test Stabilization
- Fix broken Jest tests
- Align tests to API-backed architecture
- Add feature-level integration tests for key create/list/detail flows
- Validate dashboard/read-only/workspace behavior once introduced

### Suggested ticket list

#### P0 tickets
1. **Define frontend source-of-truth architecture (API vs local-first adapter) and remove mixed data patterns**
2. **Add workspace entity and workspace-scoped routing/state**
3. **Implement read-only dashboard variant for MVP**
4. **Create Canvas shell and first canvas-based interaction flow**
5. **Refactor audit detail page into modular sections and remove embedded mock arrays**

#### P1 tickets
6. **Refactor findings/tasks/CAPA list pages into shared list patterns**
7. **Create shared activity-log mutation helper**
8. **Centralize status enums, slugs, and color mappings**
9. **Fix failing Jest tests and remove outdated DB-based assumptions**
10. **Remove Next.js build config deprecations and stop ignoring type errors**

#### P2 tickets
11. **Create role/capability-aware action policy for buttons and menus**
12. **Introduce feature-level view models and selectors**
13. **Consolidate documentation around product name and storage model**
14. **Add real empty-state/product-state decisions to replace “coming soon” tabs**

---

## 7. Before / After Examples

### Example 1 — Repeated page-local status mapping

#### Before

```ts
const getStatusColor = (status: string) => {
  switch (status) {
    case 'Completed':
      return 'bg-emerald-500/10 text-emerald-700 ...';
    case 'In Progress':
      return 'bg-blue-500/10 text-blue-700 ...';
    default:
      return 'bg-slate-500/10 text-slate-700 ...';
  }
};
```

#### After

```ts
export const taskStatusMeta: Record<TaskStatus, { label: string; className: string }> = {
  'To Do': { label: 'To Do', className: 'bg-slate-500/10 text-slate-700 ...' },
  'In Progress': { label: 'In Progress', className: 'bg-blue-500/10 text-blue-700 ...' },
  'In Review': { label: 'In Review', className: 'bg-indigo-500/10 text-indigo-700 ...' },
  Completed: { label: 'Completed', className: 'bg-emerald-500/10 text-emerald-700 ...' },
};

export function StatusBadge({ status }: { status: TaskStatus }) {
  return <Badge className={taskStatusMeta[status].className}>{taskStatusMeta[status].label}</Badge>;
}
```

### Example 2 — Mixed data shaping inside route component

#### Before

```ts
const auditExtended = audit
  ? {
      ...audit,
      ownerAvatar: '/placeholder.svg?height=40&width=40',
      description: 'Comprehensive audit focusing on compliance requirements...',
      objectives: [...],
      scope: 'All systems...',
      complianceScore: 87,
    }
  : null;
```

#### After

```ts
export interface AuditDetailViewModel {
  audit: Audit;
  team: AuditTeamMember[];
  findings: FindingSummary[];
  tasks: TaskSummary[];
  documents: AuditDocument[];
}

export async function getAuditDetailViewModel(id: string): Promise<AuditDetailViewModel | null> {
  const audit = await auditRepository.getById(id);
  if (!audit) return null;

  return {
    audit,
    team: await auditRepository.getTeam(id),
    findings: await findingRepository.listByAudit(id),
    tasks: await taskRepository.listByAudit(id),
    documents: await documentRepository.listByAudit(id),
  };
}
```

### Example 3 — Repeated create + history logging flow

#### Before

```ts
const createdTask = await ApiService.createTask(newTask);
await ApiService.createHistory({
  entityType: 'Task',
  entityId: createdTask.id,
  action: 'Created',
  user: user?.name || 'System User',
  timestamp: new Date().toISOString(),
  details: `Task "${data.title}" created and assigned to ${data.assignee}`,
});
```

#### After

```ts
await createEntityWithHistory({
  create: () => taskRepository.create(input),
  entityType: 'Task',
  action: 'Created',
  details: ({ entity }) => `Task "${entity.title}" created and assigned to ${entity.assignee}`,
  actor: currentUser,
});
```

---

## Final Verdict

Orisynx FE has a solid UI base and enough breadth to prove the product direction visually, but it is **not yet structurally ready for the brief-defined MVP**. The main blocker is not styling or route count—it is the mismatch between the current **admin-dashboard implementation** and the required **workspace/canvas/read-only** product model.

If the team addresses architecture first, the existing design system and route coverage can be reused. If not, feature work will continue to pile onto unstable page-level patterns and make the eventual MVP pivot more expensive.

## Review notes from validation runs

- `corepack pnpm test` was run and surfaced failing Jest tests, including at least:
  - `app/(main)/findings/findings-validation.test.tsx`
  - `app/(main)/capa/capa-validation.test.tsx`
- `corepack pnpm build` surfaced Next 16 config warnings about unsupported `eslint` config in `next.config.mjs`
- build config currently suppresses type failures via `typescript.ignoreBuildErrors = true`
