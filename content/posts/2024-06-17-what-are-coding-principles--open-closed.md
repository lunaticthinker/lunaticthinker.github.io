---
title: "Open-Closed Principle: Extend Without Breaking Things"
date: 2024-06-17
categories:
  - Coding Principles
tags:
  - solid
  - clean code
  - software design
  - architecture
  - best practices
bookHidden: false
---

The Open-Closed Principle (OCP) sits second in SOLID, but it’s usually the one you feel when requirements start shifting under your feet.

The idea is captured in a single sentence:

> Software entities (classes, modules, functions, etc.) should be open for extension, but closed for modification.

In practical terms, that means you should be able to add new behavior without constantly cracking open and rewriting the code that already works. Done well, OCP lets your system grow by addition instead of surgery.

## Why Bother With OCP?

If you’ve ever shipped a feature, then nervously edited old code to support the next one, you already know the pain OCP tries to avoid.

When you follow it, a few good things happen:

**You get modular pieces.** Code that’s closed for modification tends to form clear, separate components. Each part has its own role instead of accumulating “just one more” responsibility.

**You touch less, break less.** Every time you edit existing, battle‑tested code, you open the door to regressions. Extending instead of modifying keeps those risks smaller.

**You can actually scale the design.** As new requirements appear, you plug in new behaviors rather than reshaping the foundation. The codebase becomes more like a growing library than a constantly rewritten script.

## What OCP Really Means

Two phrases sit at the heart of it:

**Closed for modification.** Once a class or module is stable and tested, you shouldn’t have to keep patching it every time a new variant appears. Instead of editing it, you build around it.

**Open for extension.** The design still needs to breathe. You make it easy to inject new behavior—through interfaces, composition, or polymorphism—so the system can adapt without ripping out what’s already there.

This isn’t about never changing code. It’s about shaping core parts so they can stay mostly stable while the edges evolve.

## OCP in Real Code

Let’s walk through a concrete example.

### The Fragile Version: Hard‑Coded Conditions

Imagine a service that calculates discounts based on customer type:

```java
class DiscountService {
    public double calculateDiscount(String customerType, double amount) {
        if (customerType.equals("Regular")) {
            return amount * 0.05;
        } else if (customerType.equals("Premium")) {
            return amount * 0.1;
        } else {
            return 0;
        }
    }
}
```

It works—for now. But every time marketing invents a new customer category (“VIP”, “Partner”, “Seasonal”), you have to go back into `DiscountService` and wedge in another `if`.

That’s a direct violation of OCP: the class isn’t closed to modification. It keeps changing as the business changes, and every edit risks breaking existing behavior.

### The Extensible Version: One Contract, Many Behaviors

Now let’s lean into OCP by separating the “how to calculate discount” decision from the service that uses it.

```java
// Contract for discount calculation
interface DiscountCalculator {
    double calculate(double amount);
}

// Concrete implementations
class RegularDiscount implements DiscountCalculator {
    public double calculate(double amount) {
        return amount * 0.05;
    }
}

class PremiumDiscount implements DiscountCalculator {
    public double calculate(double amount) {
        return amount * 0.1;
    }
}

class VipDiscount implements DiscountCalculator {
    public double calculate(double amount) {
        return amount * 0.15;
    }
}

// Service depending on abstraction
class DiscountService {
    private DiscountCalculator discountCalculator;

    public DiscountService(DiscountCalculator discountCalculator) {
        this.discountCalculator = discountCalculator;
    }

    public double calculateDiscount(double amount) {
        return discountCalculator.calculate(amount);
    }
}
```

`DiscountService` now depends on an abstraction, not on specific customer types. To support a new category, you add a new `DiscountCalculator` implementation—no changes to `DiscountService` required.

The service is effectively closed to modification but remains open to extension through new strategies.

## Strategy Pattern: OCP in Disguise

The **Strategy Pattern** is one of the clearest expressions of OCP in everyday code. It lets you swap algorithms without rewriting the context that uses them.

```java
// Strategy interface
interface SortingStrategy {
    void sort(List<Integer> items);
}

// Concrete strategies
class QuickSortStrategy implements SortingStrategy {
    public void sort(List<Integer> items) {
        // Quick sort implementation
    }
}

class MergeSortStrategy implements SortingStrategy {
    public void sort(List<Integer> items) {
        // Merge sort implementation
    }
}

// Context
class Sorter {
    private SortingStrategy strategy;

    public Sorter(SortingStrategy strategy) {
        this.strategy = strategy;
    }

    public void setStrategy(SortingStrategy strategy) {
        this.strategy = strategy;
    }

    public void sortItems(List<Integer> items) {
        strategy.sort(items);
    }
}
```

`Sorter` stays stable. You can introduce `HeapSortStrategy`, `RadixSortStrategy`, or something exotic without touching the `Sorter` class at all. That’s OCP: the context is closed, the set of strategies is open.

## The Upsides—and the Cost

### Where OCP Shines

**Flexibility without fear.** New features arrive as new classes, not as edits to fragile switch statements scattered through the code.

**Maintainability improves.** Tested components stay intact. You’re less likely to ship regressions when old code remains untouched.

**Scaling feels natural.** As business rules multiply, you extend via additional implementations instead of inflating a single god method.

### Where It Can Hurt

**The design gets heavier.** Interfaces, extra classes, and wiring logic add overhead—especially when the domain is still in flux.

**Small projects can feel over‑engineered.** For a tiny script, introducing abstractions “for future flexibility” can actually make things harder to understand.

**Performance trade‑offs.** Layers of indirection can add cost in hot paths. Usually it’s negligible, but in tight loops you may need to be more direct.

## Using OCP Without Overdoing It

You don’t need to architect everything like a plugin system from day one. Instead:

**Spot evolving areas.** Look for parts of the code that keep changing—pricing rules, workflows, feature toggles. Those are good candidates for OCP‑friendly design.

**Favor composition over inheritance.** Inject behavior as collaborators rather than building deep class hierarchies. It’s easier to reason about and test.

**Lean on interfaces where they help.** Define contracts around variable behavior, not around everything. The goal is targeted flexibility.

**Use patterns as tools, not trophies.** Strategy, Factory, and others are helpful when they solve real variation. If there’s only one implementation and no concrete demand for more, you may not need the abstraction yet.

## Wrapping It Up

The Open-Closed Principle is about evolving systems without constantly rewriting their foundations.

When your core classes are closed to casual modification but designed to be extended in clear, well‑defined ways, your codebase starts to feel less fragile. Features get added as new pieces, not as risky changes to old ones.

You won’t apply OCP everywhere, and you shouldn’t try. But in the parts of your system that change often, it can be the difference between calm, incremental growth and endless, nerve‑wracking edits.
