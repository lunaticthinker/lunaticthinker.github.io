---
title: "What Are Coding Principles"
date: 2024-06-15
slug: what-are-coding-principles
description: High-level overview of core coding principles and why they matter before diving into individual deep dives.
summary: Coding principles are shared heuristics that preserve clarity, flexibility, and delivery velocity. This article introduces their purpose, families, pros, and trade‑offs.
categories:
  - Coding Principles
  - Home Page
tags:
  - principles
  - architecture
---

I’ve spent enough hours untangling legacy code to see how quietly entropy spreads: a duplicated validation, a helper that knows too much, a 200‑line function nobody wants to touch. The principles below are habits that keep change local and predictable. Reach for one when a concrete symptom shows up—duplicate logic, volatile dependencies, unreadable flow—not for the comfort of ticking a box.

For each principle you get: intent, indicators, refactor moves, examples, and trade‑offs. Use what solves the pain in front of you; ignore the rest until it hurts.

So what are coding principles, exactly? In this article, I’m using the term to mean shared heuristics for writing and shaping code: compact rules of thumb that help multiple people on a team make compatible design decisions over time. They are not laws or style‑guide pedantry; they are reusable decision patterns that reduce surprise, keep behavior consistent, and make change cheaper. A good principle gives you a way to name a kind of problem ("this is a DRY violation", "this is YAGNI") and a default direction for fixing it.∂

Practice:

1. Implement for current, confirmed requirements.
2. Introduce pattern only after distinct variants appear.
3. Cull unused scaffolding periodically.

<!--more-->

## 1. DRY (Don't Repeat Yourself)

Here's what I'm after: one single source of truth for each business rule. When a tax rate changes, I want to edit it in one place—not hunt through six files wondering which ghosts I've missed.

What tells me I need this:

- I see the same validation logic copy-pasted in multiple spots.
- The same magic number or policy value appears in different places.
- Every bug fix requires identical edits across several files.

How I typically fix it:

1. Look for semantic duplication, not just identical code. Sometimes the pattern is hidden.
2. Extract it into a well-named function, constant, or value object.
3. Wait for the third occurrence before generalizing (the "rule of three").
4. Resist the urge to build speculative frameworks.

Example (JavaScript → Python):

```javascript
// Before
function register(email) {
  if (!/^[^@]+@[^@]+$/.test(email)) throw Error("email");
}

// After: shared pattern + validation helper
const EMAIL_PATTERN = /^[^@]+@[^@]+$/;

function ensureEmail(e) {
  if (!EMAIL_PATTERN.test(e)) throw Error("email");
}

function register(email) {
  ensureEmail(email);
}
```

Speculative smells I watch for:

- Interfaces with a single implementation and no foreseeable variation.
- Configuration flags without active code paths.
- Abstractions named "Base", "Manager", or "Factory" without multiple real consumers.

```python
import re

EMAIL_PATTERN = re.compile(r"^[^@]+@[^@]+$")

def ensure_email(e: str) -> None:
    if not EMAIL_PATTERN.match(e):
        raise ValueError("email")
```

When I break this rule: During early exploratory work when I'm still figuring things out, or when I need a performance optimization that requires duplication. Always leave a comment explaining why—your teammates (and future you) will need it.

| Dimension | Effect | Notes |
function sort(data: number[]): number[] { return [...data].sort((a,b)=>a-b) }
|-----------|--------|-------|
| Change Amplification | ↓ | Single edit site for business rule. |
| Defect Probability | ↓ | Divergent clones eliminated. |

```python
# Anti-Pattern: hidden duplication of tax rate
def gross(price): return price * 1.19
def vat_component(price): return price * 0.19

VAT_RATE = 0.19
def gross_clean(price): return price * (1 + VAT_RATE)
def vat_component_clean(price): return price * VAT_RATE
```

```go
// Domain constant centralization
const Vat = 0.19
func Gross(p float64) float64 { return p * (1+Vat) }
func VatPart(p float64) float64 { return p * Vat }
```

Where it can go wrong: premature unification (false DRY) creates leaky, awkward abstractions. I hold off until the third occurrence proves the pattern.

Smells I flag:

- Same constant/value touched in multiple commits.
  class AvatarStore:
  def **init**(self, s3): self.\_s3 = s3
  def save(self, user_id, bytes):
  self.\_s3.put_object(Bucket=BUCKET, Key=f"avatars/{user_id}", Body=bytes)
- Divergent logic differing only by a literal.
- Copy‑paste edits with tiny deltas.

Moves I reach for:

- Inline identical logic, then parameterize differences.
- Extract domain constants to a focused module.
- Centralize validation rules in a declarative schema.

If I bend it:

- During exploration when abstraction cost outweighs clarity.
- For performance specialization where two versions legitimately diverge (and I document it).

Multi‑Language Example (Validation Duplication → Centralization):

```javascript
function invite(email) {
  if (!/^[^@]+@[^@]+$/.test(email)) throw Error("bad"); /* ... */
}

// After: single semantic source
function register(email) {
  enforceEmail(email);
}
function invite(email) {
  enforceEmail(email);
}
```

```python
# Centralized validation callable
EMAIL_PATTERN = re.compile(r"^[^@]+@[^@]+$")
def validate_email(e: str) -> None:
  if not EMAIL_PATTERN.match(e): raise ValueError("invalid")
```

## 2. KISS (Keep It Simple, Stupid)

My goal here is simple: strip away the accidental complexity so the essential logic can breathe. Let the unavoidable hard parts stand out clearly instead of drowning in ceremony.

What tells me something's too complex:

- Deep nesting that forces me to track mental stack frames.
- Conditional ladders that go on forever.
- Clever one-liners that make me pause and decode.

How I simplify:

1. Add guard clauses at the top to flatten the structure.
2. Delete indirection layers that add no value.
3. Expand cryptic expressions into named, readable steps.

Example (Java):

```java
// Before: nested maze
public User load(Id id){
  if(id != null){
    User u = repo.find(id);
    if(u != null){
      if(u.isActive()){
        return u;
      }
    }
  }
  throw new IllegalStateException("inactive or missing");
}

// After: guard clauses
public User load(Id id){
  if(id == null) throw new IllegalArgumentException("id");
  User u = repo.find(id);
  if(u == null || !u.isActive()) throw new IllegalStateException("inactive or missing");
  return u;
}
```

When complexity is unavoidable: Some domain logic is genuinely complex—think tax calculations or regulatory requirements. Simplifying would distort the rules. In these cases, embrace the complexity but make invariants explicit and back them with solid tests.

Complexity Metrics: Cyclomatic Complexity (CC), nesting depth, parameter count. Rising metrics correlate with elevated defect discovery latency.

```javascript
// Over-engineered classification
function grade(score) {
  if (score < 0 || score > 100) throw new Error("range");
  return ["F", "D", "C", "B", "A"][score === 100 ? 4 : Math.min(4, Math.floor(score / 20))];
}

// Simpler, proportional logic
function gradeSimple(score) {
  if (score < 0 || score > 100) throw new Error("range");
  const bands = ["F", "D", "C", "B", "A"];
  return bands[Math.min(4, Math.floor(score / 20))];
}
```

Heuristic: If readability improves more than added lines, favor explicitness.

Complexity drivers I look for:

- Layer stacking without necessity.
- Reflection / meta‑programming overuse.
- Excessive nesting vs. simple guard exits.

My usual moves:

- Replace nested conditionals with early returns.
- Delete pure pass‑through layers.
- Flatten data transforms into a readable pipeline.

Guard Clause Example (Java):

```java
// Before
public User load(Id id){
  if(id != null){
    User u = repo.find(id);
    if(u != null){
      if(u.isActive()){
        return u;
      }
    }
  }
  throw new IllegalStateException("not found or inactive");
}
// After
public User load(Id id){
  if(id == null) throw new IllegalArgumentException("id");
  User u = repo.find(id);
  if(u == null || !u.isActive()) throw new IllegalStateException("not found or inactive");
  return u;
}
```

When I accept complexity:

- Domain logic is inherently nuanced (tax rules)—I document invariants instead of forcing false simplicity.
- A proven hot path needs tighter code—isolated and commented.
  Speculative smells I trim:

- Single‑implementation interfaces.
- Dormant flags/toggles.
- "Base/Manager/Factory" names without consumers.

Cleanup steps:

- Inline unused abstractions.
- Delete stale toggles beyond deprecation window.
- Replace unused polymorphism with a simple function.

Multi‑Lang Over‑Engineering Example → Simplification:

```typescript
// Before: premature strategy pattern
interface SortStrategy {
  sort(data: number[]): number[];
}
class QuickSort implements SortStrategy {
  sort(d) {
    /* ... */ return d;
  }
}
class MergeSort implements SortStrategy {
  sort(d) {
    /* ... */ return d;
  }
}
function sort(data: number[], strat: SortStrategy) {
  return strat.sort(data);
}

// After: single observed need
function sort(data: number[]): number[] {
  return [...data].sort((a, b) => a - b);
}
```

When to Bend It:

- Library / framework design anticipating extension by third parties.
- Regulatory / compliance readiness where delaying adds audit risk.
  Indicators of Low Cohesion:

- Class methods share few common fields.
- Module where functions operate on unrelated concepts.

Coupling Smells:

- Wide imports (grabbing entire packages for one small function).
- Circular dependencies.

Refactor Patterns:

- Split “utility” grab‑bags into concept modules (e.g., `date_utils`, `string_utils`).
- Introduce adapters to reduce direct dependency on unstable concrete services.

Python Example (Coupling Reduction):

```python
# Before: direct AWS SDK calls sprinkled everywhere
def upload_avatar(user_id, bytes):
  s3 = boto3.client('s3')
  s3.put_object(Bucket=BUCKET, Key=f"avatars/{user_id}", Body=bytes)

# After: cohesive storage gateway
class AvatarStore:
  def __init__(self, s3): self._s3 = s3
  def save(self, user_id, bytes):
    self._s3.put_object(Bucket=BUCKET, Key=f"avatars/{user_id}", Body=bytes)
```

When to Bend It:

- Performance micro‑optimizations merging previously separate concerns (document trade‑off and plan revert).
  Common Layers (Generic):

- Interface / Transport (HTTP, CLI)
- Application Service (use‑case orchestration)
- Domain (pure business invariants)
- Infrastructure (persistence, messaging, external APIs)

Refactor Patterns:

- Extract inline SQL from controller into repository.
- Convert business rules embedded in UI templates into domain services.

JavaScript Example:

```javascript
// Before: mixed concerns in route handler
app.post("/users", async (req, res) => {
  const exists = await db.user.find({ email: req.body.email });
  if (exists) return res.status(409).end();
  await db.user.insert(req.body);
  mailer.sendWelcome(req.body.email);
  res.status(201).end();
});
// After: application service
async function registerUser(dto) {
  userService.ensureUnique(dto.email);
  userService.create(dto);
  userService.welcome(dto.email);
}
app.post("/users", async (req, res) => {
  await registerUser(req.body);
  res.status(201).end();
});
```

When to Bend It:

- Extremely small scripts where introducing layers increases ceremony without clear benefit.
  Smells:

- Chained calls `a.b().c().d()` spanning multiple different domain objects.
- Functions accessing grandchildren objects to mutate them.

Refactor Patterns:

- Add façade / convenience method exposing needed derived value.
- Relocate behavior into owning aggregate root.

Example (C#):

```csharp
// Before
var street = order.Customer.Address.Street;
// After (encapsulated)
var street = order.CustomerStreet();
```

When to Bend It:

- Fluent APIs intentionally designed for chaining (ensure immutability or clear boundaries).
  Fragile Base Smells:

- Overridden methods requiring knowledge of parent internal state.
- Base class growing conditional logic for child variants.

Refactor Patterns:

- Replace inheritance with delegating field.
- Use small interfaces + struct/record wrappers.

Example (Java):

```java
// Inheritance
class TimedHashMap<K,V> extends HashMap<K,V>{
  long hits=0; @Override public V get(Object k){ hits++; return super.get(k); }
}
// Composition
class TimedMap<K,V>{
  private final Map<K,V> inner; private long hits=0;
  TimedMap(Map<K,V> inner){ this.inner = inner; }
  V get(K k){ hits++; return inner.get(k); }
}
```

When to Bend It:

- Framework callback inheritance (e.g., test base classes) where conventions reduce boilerplate.
  Patterns:

- Guard arguments in public API boundaries.
- Introduce value objects enforcing invariants on construction.
- Use assertions in internal code paths for impossible states.

Example (TypeScript):

```typescript
function createUser(email: string) {
  if (!/^[^@]+@[^@]+$/.test(email)) throw new Error("email");
  return { email };
}
```

When to Bend It:

- Performance-critical hot loops where prevalidation cost dominates (ensure upstream sanitized input instead).
  Smells:

- Public mutable fields.
- “Getter” returning internal collection directly (exposed mutability).

Refactor Patterns:

- Return defensive copies / read‑only views.
- Replace primitive obsession with domain value types.

Java Example:

```java
class Basket{ private final List<Item> items = new ArrayList<>();
  public List<Item> getItems(){ return Collections.unmodifiableList(items); }
  public void add(Item i){ items.add(i); }
}
```

When to Bend It:

- DTOs / serialization objects intentionally exposing structure for mapping.
  Heuristics:

- Aim for <= ~15 lines per function for cognitive chunking (contextual).
- Prefer verbs for commands, nouns for queries.
- Eliminate misleading metaphors (e.g., `manager`, `util`).

Refactor Pattern:

- Rename plus extract: rename ambiguous variables, then extract logic into well‑named helpers.

Bad vs Good (PHP):

```php
// Bad
function proc($a,$b){ if($a>0){ return $a*$b; } return $b; }
// Good
function computeWeightedScore(int $base, int $weight): int {
  if ($base <= 0) return $weight;
  return $base * $weight;
}
```

When to Bend It:

- Extremely performance‑critical code where micro‑optimizations (bit tricks) required; accompany with clarifying comments.
  Testability Enablers:

- Pure functions for deterministic logic.
- Dependency injection for side‑effectful collaborators.
- Clear seams (ports/adapters) for infrastructure.

Refactor Patterns:

- Extract external calls into injected interfaces.
- Break long procedures into composable testable steps.

Example (Go):

```go
type Clock interface { Now() time.Time }
type RealClock struct{}
func (RealClock) Now() time.Time { return time.Now() }

func Expired(created time.Time, ttl time.Duration, clk Clock) bool {
  return clk.Now().After(created.Add(ttl))
}
```

When to Bend It:

- Tiny glue code whose behavior is trivially covered by integration tests.
  Additional Advanced Metrics:
  | Metric | Insight |
  |--------|--------|
  | Instability (afferent/efferent coupling ratio) | Predicts resilience to change. |
  | Churn vs Complexity | High churn + high CC marks refactor hotspots. |
  | Mutation Score | Quality of tests beyond raw coverage. |
  | Review Latency | Organizational friction; rising suggests clarity issues. |

## 3. YAGNI (You Aren't Gonna Need It)

I've learned this the hard way: don't build abstractions until you actually need them. Real variation should drive your design choices, not hypothetical future scenarios. Unused scaffolding isn't preparation—it's technical debt waiting to confuse someone.

Signs you're over-engineering:

- Interfaces with only one implementation and no concrete plans for more.
- Feature flags sitting dormant in the codebase.
- Generic base types with zero consumers.

What works for me:

1. Build for the requirements you have now, not the ones you imagine.
2. Introduce patterns only after you've seen the variation appear at least twice.
3. Regularly prune unused abstractions—they age poorly.

Example (TypeScript):

```typescript
// Before: speculative strategy pattern
interface SortStrategy {
  sort(data: number[]): number[];
}
class QuickSort implements SortStrategy {
  sort(d) {
    return d.sort((a, b) => a - b);
  }
}
function sort(data: number[], strat: SortStrategy) {
  return strat.sort(data);
}

// After: needed only ascending sort
function sort(data: number[]): number[] {
  return [...data].sort((a, b) => a - b);
}
```

When Bending Is Acceptable: Public API surface design or compliance preparation where delay raises external risk.

```csharp
// Premature abstraction
public interface IDiscountStrategy { decimal Apply(decimal p); }

// Lean concrete logic; strategy only added when variation emerges
public static decimal ApplyDiscount(decimal price, decimal rate) => price * (1 - rate);
```

Metric: Track orphan classes/functions (no references). Reduce their half‑life.

Speculative Smells:

- Interfaces with a single implementation and no foreseeable variation.
- Configuration flags without active code paths.
- Abstraction naming using “Base”, “Manager”, “Factory” absent multiple consumers.

Refactor Patterns:

- Inline unused abstractions back into calling code.
- Delete feature toggles older than deprecation window.
- Replace unused polymorphism with a simple function.

Multi‑Lang Over‑Engineering Example → Simplification:

```typescript
// Before: premature strategy pattern
interface SortStrategy {
  sort(data: number[]): number[];
}
class QuickSort implements SortStrategy {
  sort(d) {
    /* ... */ return d;
  }
}
class MergeSort implements SortStrategy {
  sort(d) {
    /* ... */ return d;
  }
}
function sort(data: number[], strat: SortStrategy) {
  return strat.sort(data);
}

// After: single observed need
function sort(data: number[]): number[] {
  return [...data].sort((a, b) => a - b);
}
```

When to Bend It:

- Library / framework design anticipating extension by third parties.
- Regulatory / compliance readiness where delaying adds audit risk.

## 4. Cohesion & Coupling

I group closely related behavior and keep modules from leaning on unstable details so a small change doesn’t ripple everywhere.

Low Cohesion Signs: A class with methods that touch completely different fields. Utility modules that are “junk drawers.”

High Coupling Signs: Wide imports (pulling huge packages for one helper), circular dependencies, or needing to change 5 files for one small tweak.

Improvement Moves:

1. Organize around domain concepts (e.g., `InvoiceNotifier`).
2. Wrap unstable externals behind adapters.
3. Split multi‑purpose modules into focused units.

Example (Python):

```python
# Before: direct AWS usage everywhere
def upload_avatar(user_id, bytes):
  s3 = boto3.client('s3')
  s3.put_object(Bucket=BUCKET, Key=f"avatars/{user_id}", Body=bytes)

# After: cohesive gateway
class AvatarStore:
  def __init__(self, s3): self._s3 = s3
  def save(self, user_id, bytes):
    self._s3.put_object(Bucket=BUCKET, Key=f"avatars/{user_id}", Body=bytes)
```

When It’s OK to Bend: Micro‑optimizations merging layers for performance—document the trade‑off.

```java
// Mixed responsibilities (low cohesion)
class BillingService { void pdf(){} void emailInvoice(){} void tax(){} }

class InvoicePdf { void pdf(){} }
class TaxCalculator { void tax(){} }
class InvoiceNotifier { void emailInvoice(){} }
```

Measures: Fan‑out (outgoing dependencies) and fan‑in (incoming). Outliers prompt review.

Low cohesion indicators:

- Methods touch unrelated fields.
- Modules feel like junk drawers.

Coupling smells:

- Wide imports for a single helper.
- Circular dependencies.

To improve:

- Split utility grab‑bags into concept modules.
- Introduce adapters around unstable externals.

Python Example (Coupling Reduction):

```python
# Before: direct AWS SDK calls sprinkled everywhere
def upload_avatar(user_id, bytes):
  s3 = boto3.client('s3')
  s3.put_object(Bucket=BUCKET, Key=f"avatars/{user_id}", Body=bytes)

# After: cohesive storage gateway
class AvatarStore:
  def __init__(self, s3): self._s3 = s3
  def save(self, user_id, bytes):
    self._s3.put_object(Bucket=BUCKET, Key=f"avatars/{user_id}", Body=bytes)
```

When to Bend It:

- Performance micro‑optimizations merging previously separate concerns (document trade‑off and plan revert).

## 5. Separation of Concerns (SoC)

The idea is straightforward: separate your UI from orchestration, domain rules from infrastructure. When you do this well, you can evolve or swap any layer without causing collateral damage elsewhere.

The layers typically look like this: Transport (HTTP/UI), Application (use case orchestration), Domain (business rules), Infrastructure (database, external APIs).

My process for extracting concerns:

1. Spot where responsibilities are tangled together—like persistence mixed with notifications.
2. Pull each concern into its own dedicated component.
3. Keep your orchestration layer thin and declarative, like a table of contents.

Example (JavaScript):

```javascript
// Before
app.post("/users", async (req, res) => {
  const exists = await db.user.find({ email: req.body.email });
  if (exists) return res.status(409).end();
  await db.user.insert(req.body);
  mailer.sendWelcome(req.body.email);
  res.status(201).end();
});

// After
async function registerUser(dto) {
  userService.ensureUnique(dto.email);
  userService.create(dto);
  userService.welcome(dto.email);
}
app.post("/users", async (req, res) => {
  await registerUser(req.body);
  res.status(201).end();
});
```

When It’s OK to Bend: Tiny scripts or one‑off tooling where ceremony outweighs benefit.

```typescript
class UserApplicationService {
  constructor(private repo: UserRepository) {}
  register(dto: RegisterUser) {
    /* validation */ return this.repo.save(dto);
  }
}
interface UserRepository {
  save(dto: RegisterUser): User;
}
class PgUserRepository implements UserRepository {
  /* SQL impl */
}
```

Outcome: Replace `PgUserRepository` with another store without touching business flow.

Common Layers (Generic):

- Interface / Transport (HTTP, CLI)
- Application Service (use‑case orchestration)
- Domain (pure business invariants)
- Infrastructure (persistence, messaging, external APIs)

Refactor Patterns:

- Extract inline SQL from controller into repository.
- Convert business rules embedded in UI templates into domain services.

JavaScript Example:

```javascript
// Before: mixed concerns in route handler
app.post("/users", async (req, res) => {
  const exists = await db.user.find({ email: req.body.email });
  if (exists) return res.status(409).end();
  await db.user.insert(req.body);
  mailer.sendWelcome(req.body.email);
  res.status(201).end();
});
// After: application service
async function registerUser(dto) {
  userService.ensureUnique(dto.email);
  userService.create(dto);
  userService.welcome(dto.email);
}
app.post("/users", async (req, res) => {
  await registerUser(req.body);
  res.status(201).end();
});
```

When to Bend It:

- Extremely small scripts where introducing layers increases ceremony without clear benefit.

## 6. Law of Demeter (LoD)

I avoid spelunking through long object chains; I’d rather ask an object for what I need and let it own its internals.

Improvement Moves:

1. Add convenience methods exposing required derived values.
2. Relocate behavior to data owners (tell, don’t ask).

Example (Ruby):

```ruby
# Before
total = order.cart.items.sum(&:price)
# After
total = order.total_price
```

When It’s OK to Bend: Fluent APIs designed for chaining (ensure they’re stable and documented).

```ruby
# Train wreck chain
total = order.cart.items.sum(&:price)

# Encapsulated
total = order.total_price
```

Benefit: Internal structure can refactor without global search/replace.

Smells:

- Chained calls `a.b().c().d()` spanning multiple different domain objects.
- Functions accessing grandchildren objects to mutate them.

Refactor Patterns:

- Add façade / convenience method exposing needed derived value.
- Relocate behavior into owning aggregate root.

Example (C#):

```csharp
// Before
var street = order.Customer.Address.Street;
// After (encapsulated)
var street = order.CustomerStreet();
```

When to Bend It:

- Fluent APIs intentionally designed for chaining (ensure immutability or clear boundaries).

## 7. Composition Over Inheritance

Inheritance trees get messy fast. I prefer composing small, focused parts instead of climbing fragile class hierarchies. Delegation gives you flexibility without the brittleness of parent-child coupling.

My refactoring approach:

1. Identify the new behavior you added in a subclass.
2. Replace that inheritance relationship with delegation to a separate component.
3. Keep your interfaces minimal—expose only what's needed.

Example (Java):

```java
// Inheritance
class TimedHashMap<K,V> extends HashMap<K,V>{
  long hits=0; @Override public V get(Object k){ hits++; return super.get(k); }
}

// Composition
class TimedMap<K,V>{
  private final Map<K,V> inner; private long hits=0;
  TimedMap(Map<K,V> inner){ this.inner = inner; }
  V get(K k){ hits++; return inner.get(k); }
}
```

When It’s OK to Bend: Framework hooks (e.g. test base classes) that deliberately reduce boilerplate.

```go
type Cache interface { Get(string) (string,bool); Set(string,string) }
type MetricsCache struct { inner Cache; hits int }
func (m *MetricsCache) Get(k string)(string,bool){ v,ok := m.inner.Get(k); if ok { m.hits++ }; return v,ok }
```

Swappable `inner` enables cross‑cutting concerns (metrics, tracing) without deep hierarchies.

Fragile Base Smells:

- Overridden methods requiring knowledge of parent internal state.
- Base class growing conditional logic for child variants.

Refactor Patterns:

- Replace inheritance with delegating field.
- Use small interfaces + struct/record wrappers.

Example (Java):

```java
// Inheritance
class TimedHashMap<K,V> extends HashMap<K,V>{
  long hits=0; @Override public V get(Object k){ hits++; return super.get(k); }
}
// Composition
class TimedMap<K,V>{
  private final Map<K,V> inner; private long hits=0;
  TimedMap(Map<K,V> inner){ this.inner = inner; }
  V get(K k){ hits++; return inner.get(k); }
}
```

When to Bend It:

- Framework callback inheritance (e.g., test base classes) where conventions reduce boilerplate.

## 8. Fail Fast

I want failures to show themselves immediately, at clear boundaries, before they can propagate. When you catch problems early, downstream code gets to make a beautiful assumption: its inputs are valid.

What I do:

1. Validate rigorously at public entry points—your API surface.
2. Use value objects that enforce their own invariants on construction.
3. Add assertions for states that should be impossible internally.

Example (Rust):

```rust
fn parse_port(s: &str) -> Result<u16, &'static str> {
  let p: u16 = s.parse().map_err(|_| "not a number")?;
  if p == 0 { return Err("zero invalid") }
  Ok(p)
}
```

When It’s OK to Bend: Ultra‑hot loops where validation cost is proven to dominate (ensure upstream sanitation).

```rust
fn parse_port(s: &str) -> Result<u16, &'static str> {
  let p: u16 = s.parse().map_err(|_| "not a number")?;
  if p == 0 { return Err("zero invalid") }
  Ok(p)
}
```

Result: Downstream logic need not defensively revalidate.

Patterns:

- Guard arguments in public API boundaries.
- Introduce value objects enforcing invariants on construction.
- Use assertions in internal code paths for impossible states.

Example (TypeScript):

```typescript
function createUser(email: string) {
  if (!/^[^@]+@[^@]+$/.test(email)) throw new Error("email");
  return { email };
}
```

When to Bend It:

- Performance-critical hot loops where prevalidation cost dominates (ensure upstream sanitized input instead).

## 9. Encapsulation / Information Hiding

Hide your internal representation. This gives you freedom to strengthen invariants or refactor internals later without triggering a cascade of edits across your entire codebase.

Example (Kotlin):

```kotlin
class Money private constructor(private val cents: Long){
  companion object { fun of(cents: Long): Money { require(cents>=0); return Money(cents) } }
  fun add(other: Money) = Money(this.cents + other.cents)
}
```

When It’s OK to Bend: Simple DTOs for serialization where mutability and visibility are expected.

```kotlin
class Money private constructor(private val cents: Long){
  companion object { fun of(cents: Long): Money { require(cents>=0); return Money(cents) } }
  fun add(other: Money) = Money(this.cents + other.cents)
}
```

External code cannot create negative amounts.

Smells:

- Public mutable fields.
- “Getter” returning internal collection directly (exposed mutability).

Refactor Patterns:

- Return defensive copies / read‑only views.
- Replace primitive obsession with domain value types.

Java Example:

```java
class Basket{ private final List<Item> items = new ArrayList<>();
  public List<Item> getItems(){ return Collections.unmodifiableList(items); }
  public void add(Item i){ items.add(i); }
}
```

When to Bend It:

- DTOs / serialization objects intentionally exposing structure for mapping.

## 10. Readability & Intent

I optimize for scan speed—if future me has to pause to decode a name, it’s too expensive.

Helpful Habits:

- Use verbs for actions (`calculateInvoiceTotal`), nouns for data (`invoiceRepository`).
- Avoid filler words (`Utils`, `Manager`, `Helper`).
- Limit function length so the whole idea fits on one screen.

Example (PHP):

```php
// Before
function proc($a,$b){ if($a>0){ return $a*$b; } return $b; }
// After
function computeWeightedScore(int $base, int $weight): int {
  if ($base <= 0) return $weight;
  return $base * $weight;
}
```

When It’s OK to Bend: Low‑level bit twiddling or math optimizations—add a clarifying comment.

Guideline: Replace encoded terms with domain nouns; limit horizontal span to aid visual chunking.

Heuristics:

- Aim for <= ~15 lines per function for cognitive chunking (contextual).
- Prefer verbs for commands, nouns for queries.
- Eliminate misleading metaphors (e.g., `manager`, `util`).

Refactor Pattern:

- Rename plus extract: rename ambiguous variables, then extract logic into well‑named helpers.

Bad vs Good (PHP):

```php
// Bad
function proc($a,$b){ if($a>0){ return $a*$b; } return $b; }
// Good
function computeWeightedScore(int $base, int $weight): int {
  if ($base <= 0) return $weight;
  return $base * $weight;
}
```

When to Bend It:

- Extremely performance‑critical code where micro‑optimizations (bit tricks) required; accompany with clarifying comments.

## 11. Testability

I design code to be easily testable because fast, clear tests are my safety net for aggressive refactoring. Without them, I'm paralyzed—afraid to touch anything.

What enables this:

- Pure functions for your core logic—no hidden state or side effects.
- Inject collaborators (like clocks or databases) instead of hardcoding them.
- Draw clear boundaries: wrap external effects, isolate your business logic.

Example (Go):

```go
type Clock interface { Now() time.Time }
type RealClock struct{}
func (RealClock) Now() time.Time { return time.Now() }

func Expired(created time.Time, ttl time.Duration, clk Clock) bool {
  return clk.Now().After(created.Add(ttl))
}
```

When It’s OK to Bend: Tiny glue functions already covered by higher‑level tests.

```python
def price_with_tax(price: float, tax_rate: float, round_fn=round):
    return round_fn(price * (1 + tax_rate), 2)

def test_price_with_tax():
    assert price_with_tax(10, 0.2, lambda v: v) == 12.0
```

Injected `round_fn` removes need for monkeypatching global rounding.

Testability Enablers:

- Pure functions for deterministic logic.
- Dependency injection for side‑effectful collaborators.
- Clear seams (ports/adapters) for infrastructure.

Refactor Patterns:

- Extract external calls into injected interfaces.
- Break long procedures into composable testable steps.

Example (Go):

```go
type Clock interface { Now() time.Time }
type RealClock struct{}
func (RealClock) Now() time.Time { return time.Now() }

func Expired(created time.Time, ttl time.Duration, clk Clock) bool {
  return clk.Now().After(created.Add(ttl))
}
```

When to Bend It:

- Tiny glue code whose behavior is trivially covered by integration tests.

## 12. Metrics to Watch

I use a handful of lightweight metrics as smoke detectors for entropy; I don’t chase numbers for vanity.

| Metric                | Why It Matters                                     |
| --------------------- | -------------------------------------------------- |
| Duplication %         | Shows where DRY is slipping.                       |
| Cyclomatic Complexity | More paths = more tests & potential bugs.          |
| Fan‑out / Fan‑in      | Extreme connectivity signals fragile architecture. |
| Mutation Score        | Tells you if tests really catch changes.           |
| Review Time           | Long reviews hint at readability issues.           |

Advanced (use when team matures): Instability (coupling ratio), churn vs complexity (hotspot), and flaky test rate.

## Pros (Net Advantages)

- Changes stay small and safe.
- Fewer surprise bugs.
- Architecture can evolve instead of being “rewritten from scratch.”
- New team members ramp faster.
- Tests actually support refactoring instead of blocking it.

## Cons / Trade‑Offs (When Misapplied)

- Premature abstraction creates confusing layers.
- Checklist thinking (“must apply every principle”) slows delivery.
- Chasing metrics for their own sake leads to unnatural code.
- Over‑engineered interfaces add noise.

## Mitigations

1. Apply a principle when you feel pain (duplication, confusion), not just because it exists.
2. Schedule periodic “cleanup passes” to delete obsolete code.
3. Write a short note (ADR) when bending a rule—future you will thank you.
4. Start with reversible changes; commit only when patterns prove stable.
5. Track one metric per quarter; improve it modestly.

## SOLID (At a Glance)

These five principles collectively enhance evolvability:

| Principle | Definition                                                                                                                                   |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| SRP       | A unit has exactly one reason to change. [Deep dive →](/posts/2024-06-16-what-are-coding-principles--single-responsibility/)                 |
| OCP       | Extend behavior without modifying stable code. [Deep dive →](/posts/2024-06-17-what-are-coding-principles--open-closed/)                     |
| LSP       | Subtypes honor the contracts of supertypes. [Deep dive →](/posts/2024-06-18-what-are-coding-principles--liskov-substitution/)                |
| ISP       | Clients depend only on methods they actually use. [Deep dive →](/posts/2024-06-20-what-are-coding-principles--interface-segregation/)        |
| DIP       | High-level policy depends on abstractions, not concretes. [Deep dive →](/posts/2024-06-22-what-are-coding-principles--dependency-inversion/) |

Treat SOLID as a cohesion and dependency stabilizing scaffold; deeper analysis deferred to focused articles.

## Conclusion

Treat these principles as tools, not destinations. Start with a specific pain point: duplicated validation, a 150-line function, an unstable dependency. Apply just enough principle-driven pressure to reduce the cost of future changes. Measure success by shorter review times and fewer files touched per change.

Here's a simple exercise: Pick one module. Shorten its longest function. Centralize one duplicated constant. Rename the least clear identifier. Then get a peer review and see if clarity improved.

Small improvements, applied consistently, compound into significant gains. Start small. Stay steady. The results will speak for themselves.
