---
title: "Liskov Substitution Principle: Don’t Surprise Your Callers"
date: 2024-06-18
categories:
  - Coding Principles
tags:
  - solid
  - clean code
  - software design
  - inheritance
  - best practices
---

The Liskov Substitution Principle (LSP) is the quiet backbone of safe inheritance. It’s the “L” in SOLID, and it answers one simple question:

> If I swap a base class instance with a subclass instance, does everything still behave correctly?

Formally, LSP says: objects of a superclass should be replaceable with objects of a subclass **without** breaking the program. In practice, it’s about making sure your subclasses don’t surprise anyone who already understands the base type.

## Why LSP Matters

When LSP is violated, things break in ways that are frustrating and subtle. The type system says “this is fine,” but reality says otherwise.

Following LSP helps you:

**Keep behavior consistent.** If something claims to be a `Rectangle`, it should act like one. Callers shouldn’t need to know which specific subtype they’re holding.

**Preserve predictability.** Code that depends on a base type should not need special cases for particular subclasses.

**Improve reuse.** When subclasses truly honor the base contract, you can plug them into existing code paths with confidence instead of defensive checks everywhere.

## The Core Ideas Behind LSP

You can think of LSP as a behavioral contract layered on top of the type system:

**Behavioral consistency.** Subclasses shouldn’t change what methods _mean_. They can extend behavior, but not break expectations.

**Polymorphism that actually works.** The whole point of polymorphism is being able to treat different implementations the same way. LSP is what makes that safe.

**Don’t tighten preconditions or promises.** Subclasses shouldn’t require _more_ from callers (stricter preconditions) or promise something fundamentally _different_ in return (stronger or incompatible postconditions).

## A Classic Violation: Rectangle vs Square

Let’s start with the textbook example and see where things go wrong.

```java
class Rectangle {
    protected int width;
    protected int height;

    public void setWidth(int width) {
        this.width = width;
    }

    public void setHeight(int height) {
        this.height = height;
    }

    public int getArea() {
        return width * height;
    }
}

class Square extends Rectangle {
    @Override
    public void setWidth(int width) {
        this.width = width;
        this.height = width; // force equality
    }

    @Override
    public void setHeight(int height) {
        this.height = height;
        this.width = height; // force equality
    }
}
```

The `Square` class is trying to enforce its invariant: equal sides. But it’s doing so by silently changing how `setWidth` and `setHeight` behave compared to `Rectangle`.

Now consider a function that works with `Rectangle`:

```java
public void resizeRectangle(Rectangle rectangle) {
    rectangle.setWidth(5);
    rectangle.setHeight(10);
    assert rectangle.getArea() == 50; // expectation for rectangles
}
```

Pass in a `Rectangle` and the assertion holds. Pass in a `Square` and it fails, because the calls force both sides to be 10. The type system is happy, but behavior is broken.

That’s an LSP violation: a `Square` cannot safely stand in for a `Rectangle` in code that relies on the base type’s contract.

## Fixing It: Separate Types, Shared Abstraction

The root issue is the inheritance relationship itself. A square isn’t a rectangle _in terms of this API’s expectations_. So we model them as separate shapes sharing a common interface.

```java
interface Shape {
    int getArea();
}

class Rectangle implements Shape {
    private final int width;
    private final int height;

    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    public int getArea() {
        return width * height;
    }
}

class Square implements Shape {
    private final int side;

    public Square(int side) {
        this.side = side;
    }

    public int getArea() {
        return side * side;
    }
}
```

Now both `Rectangle` and `Square` are honest about what they are. They implement the same `Shape` contract, and any function that needs “something with an area” can accept `Shape` without worrying about the details.

Instead of inheriting and fighting the base class behavior, we introduce an abstraction that matches the shared semantics.

## A More Realistic Violation: Read‑Only Documents

Here’s a scenario that’s closer to day‑to‑day work.

```java
class Document {
    public void print() {
        System.out.println("Printing document...");
    }

    public void save() {
        System.out.println("Saving document...");
    }
}

class ReadOnlyDocument extends Document {
    @Override
    public void save() {
        throw new UnsupportedOperationException("Cannot save a read-only document");
    }
}
```

`ReadOnlyDocument` compiles and technically “is a” `Document`, but it blows up when you call `save`. Any code that relies on `Document` being saveable now has to tiptoe around this subclass.

You’ve created a type that advertises behavior it doesn’t actually support.

### Refactoring Toward LSP

We can fix this by expressing capabilities as separate interfaces instead of baking them into a single base class.

```java
interface Printable {
    void print();
}

interface Saveable {
    void save();
}

class EditableDocument implements Printable, Saveable {
    public void print() {
        System.out.println("Printing document...");
    }

    public void save() {
        System.out.println("Saving document...");
    }
}

class ReadOnlyDocument implements Printable {
    public void print() {
        System.out.println("Printing read-only document...");
    }
}
```

Now a piece of code that expects something `Saveable` can rely on `save()` working. A `ReadOnlyDocument` no longer pretends to support saving, so it can’t violate the contract.

LSP is restored by aligning types with what they truly guarantee.

## Benefits and Trade‑Offs

### What You Gain

**Predictable behavior.** Callers can trust that a subtype won’t secretly break base type promises.

**Safer reuse.** You can introduce new implementations without sprinkling special‑case logic everywhere.

**Fewer subtle bugs.** Many painful defects come from “it compiled, but the behavior changed.” LSP pushes you to surface those mismatches at design time.

### What It Costs

**More design thought.** You need to think about contracts, invariants, and whether inheritance is even the right tool.

**Refactoring complex hierarchies.** Fixing long‑lived inheritance trees to respect LSP can be non‑trivial.

**Risk of over‑abstraction.** In the name of purity, it’s easy to invent too many interfaces and indirections. As always, balance matters.

## Working With LSP Day to Day

You don’t need formal proofs to benefit from LSP. A few habits go a long way:

**Ask “can this really substitute?”** When you add a subclass, mentally run through how existing code uses the base type. Would anything break in surprising ways?

**Favor composition when in doubt.** If you’re struggling to make a subclass obey the base contract, that’s a strong signal to stop inheriting and start composing.

**Keep subclass responsibilities narrow.** The more extra behavior you pile on, the easier it is to accidentally violate expectations.

**Test substitutability.** Write tests that exercise your code using the base type, then run them with each subtype. If only some subclasses pass, you’ve likely got an LSP problem.

## The Bottom Line

LSP is about honesty in your type relationships.

If a class claims to be usable wherever its base type is expected, it should behave accordingly. When it doesn’t, you get surprising failures, defensive code, and hierarchies that no one fully trusts.

When you respect LSP—often by reshaping inheritance into better abstractions or composition—your code becomes more reliable, more reusable, and easier to reason about. Subtypes stop being landmines and start being genuine drop‑in alternatives.
