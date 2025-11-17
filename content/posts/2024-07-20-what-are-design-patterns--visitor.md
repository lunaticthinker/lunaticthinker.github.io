---
title: "Visitor Pattern"
date: 2024-07-20
categories:
    - Design Patterns
tags:
    - design patterns
    - behavioral patterns
    - visitor
    - extensibility
bookHidden: false
---

Every time you think “I need to run a bunch of different operations over this object hierarchy, but I really don’t want to keep changing those classes”, you’re in Visitor territory.

The **Visitor** pattern is a behavioral design pattern that lets you add new operations to a group of related classes *without* modifying their source. Operations live in visitor classes; your data structures just agree to “accept” them.

## Intent

Separate algorithms from the object structure they operate on so you can add new operations without changing existing classes. The classes stay stable; visitors carry the evolving behavior.

## Problem and Solution

### Problem

Imagine a tax engine that needs to calculate taxes on different types of assets: stocks, real estate, bonds, maybe more in the future. Each asset has its own rules.

If you keep adding tax methods directly onto asset classes, every new rule means editing every relevant class. Over time, those classes become bloated with unrelated logic.

### Solution

With Visitor, you move those tax calculations into a separate visitor class. Assets just implement an `accept` method that calls back into the visitor. When tax rules change or new reporting features show up, you add a new visitor instead of touching each asset type.

## Structure

The Visitor pattern typically includes:

1. **Visitor Interface**: Declares a visit method for each type of concrete element in the structure.
2. **Concrete Visitor**: Implements specific operations to perform on each type of element.
3. **Element Interface**: Defines an `accept` method to allow visitors to operate on the element.
4. **Concrete Elements**: Implement the `accept` method, which calls the appropriate `visit` method on the visitor.

## UML Diagram

```text
+-------------------+            +-------------------+
|     Visitor       |<-----------|  ConcreteVisitor  |
|-------------------|            +-------------------+
| + visitA()        |            | + visitA()        |
| + visitB()        |            | + visitB()        |
+-------------------+            +-------------------+
         ^
         |
+-------------------+            +-------------------+
|     Element       |<-----------|  ConcreteElement  |
|-------------------|            +-------------------+
| + accept()        |            | + accept()        |
+-------------------+            +-------------------+
```

## Example: Tax Calculation on Different Assets

Let’s implement a tax calculation system using the Visitor pattern. We’ll create different asset types (e.g., `Stock`, `RealEstate`) and a visitor for tax calculation. Each asset accepts the visitor to perform tax calculations without knowing the specific tax logic.

### Step 1: Define the Visitor Interface

The `Visitor` interface declares `visit` methods for each concrete element type (i.e., `Stock`, `RealEstate`), enabling the visitor to perform specific operations.

```java
// Visitor Interface
interface Visitor {
    void visit(Stock stock);
    void visit(RealEstate realEstate);
}
```

### Step 2: Implement Concrete Visitor

The `TaxCalculator` class is a concrete visitor that implements tax calculation for each type of asset.

```java
// Concrete Visitor for Tax Calculation
class TaxCalculator implements Visitor {
    @Override
    public void visit(Stock stock) {
        double tax = stock.getValue() * 0.15; // Assume 15% tax on stocks
        System.out.println("Tax on stock: $" + tax);
    }

    @Override
    public void visit(RealEstate realEstate) {
        double tax = realEstate.getValue() * 0.1; // Assume 10% tax on real estate
        System.out.println("Tax on real estate: $" + tax);
    }
}
```

### Step 3: Define the Element Interface

The `Asset` interface defines an `accept` method, allowing the visitor to operate on it.

```java
// Element Interface
interface Asset {
    void accept(Visitor visitor);
}
```

### Step 4: Implement Concrete Elements

Each concrete asset (e.g., `Stock`, `RealEstate`) implements the `accept` method, which calls the corresponding `visit` method on the visitor.

```java
// Concrete Element for Stock
class Stock implements Asset {
    private double value;

    public Stock(double value) {
        this.value = value;
    }

    public double getValue() {
        return value;
    }

    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}

// Concrete Element for Real Estate
class RealEstate implements Asset {
    private double value;

    public RealEstate(double value) {
        this.value = value;
    }

    public double getValue() {
        return value;
    }

    @Override
    public void accept(Visitor visitor) {
        visitor.visit(this);
    }
}
```

### Step 5: Client Code Using the Visitor Pattern

The client code creates assets and applies the `TaxCalculator` visitor to each asset, calculating tax without modifying the asset classes.

```java
public class Client {
    public static void main(String[] args) {
        Asset stock = new Stock(1000.0);
        Asset realEstate = new RealEstate(5000.0);

        Visitor taxCalculator = new TaxCalculator();

        // Calculate tax for each asset
        stock.accept(taxCalculator);       // Output: Tax on stock: $150.0
        realEstate.accept(taxCalculator);   // Output: Tax on real estate: $500.0
    }
}
```

### Output

```plaintext
Tax on stock: $150.0
Tax on real estate: $500.0
```

In this example:

- `TaxCalculator` is the visitor that calculates tax for each type of asset.
- `Stock` and `RealEstate` are concrete elements that implement the `accept` method.
- The client code applies `TaxCalculator` to each asset, calculating tax without modifying asset classes.

## Applicability

Use the Visitor pattern when:

1. You need to perform operations on a set of objects with varying types, and you want to keep the operations separate from the object structure.
2. The object structure rarely changes, but you expect to add new operations frequently.
3. You want to avoid modifying classes each time a new operation is required, maintaining adherence to the Open-Closed Principle.

## Advantages and Disadvantages

### Advantages

1. **Extensibility**: The Visitor pattern makes it easy to add new operations without modifying the classes on which they operate.
2. **Separation of Concerns**: Operations are separated from the object structure, leading to cleaner and more maintainable code.
3. **Open-Closed Principle**: New functionality can be added without changing existing code, as operations are handled by visitors.

### Disadvantages

1. **Increased Complexity**: The pattern introduces multiple classes (visitors and elements), which may increase complexity.
2. **Dependency on Object Structure**: The pattern relies on a stable object structure, as changes to the structure require updating all visitors.
3. **Not Ideal for Frequently Changing Structures**: If the object structure changes frequently, the Visitor pattern can become cumbersome, as each visitor needs to account for the changes.

## Best Practices for Implementing the Visitor Pattern

1. **Use When Object Structure Is Stable**: The pattern is most effective when the object structure remains stable, allowing new operations to be added easily.
2. **Avoid If Structure Changes Frequently**: If the structure changes often, consider alternative patterns that are less reliant on a stable hierarchy.
3. **Consider Double Dispatch**: The Visitor pattern uses double dispatch to enable the correct visitor method to be called based on both the visitor and the element type.

## Conclusion

The Visitor pattern provides a powerful way to add operations to object structures without modifying the objects themselves. By decoupling operations from the object structure, the Visitor pattern supports open-ended extensibility, making it ideal for scenarios with stable structures but frequently changing operations.
