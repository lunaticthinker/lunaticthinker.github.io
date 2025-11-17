---
title: "Composite Pattern"
date: 2024-07-26
categories:
  - Design Patterns
tags:
  - design patterns
  - structural patterns
  - composite
  - tree structures
bookHidden: false
---

Files and folders. Menu items and submenus. Shapes and groups of shapes. We constantly work with part–whole hierarchies, and we’d really like to treat “a single item” and “a group of items” in the same way.

The **Composite** pattern is a structural pattern that lets you compose objects into tree‑like structures and treat individual objects and groups uniformly.

## Intent

Allow clients to treat individual objects and compositions of objects uniformly by giving them a common interface and arranging them in a tree structure.

## Problem and Solution

### Problem

Suppose you’re building a graphics editor where shapes can be grouped into larger shapes, and those groups can be grouped again. You want to call `draw()` on _anything_ — a single circle or a big nested group — and have it “just work”.

Without a consistent model, you end up writing special‑case code that checks “is this a single shape or a group?” everywhere.

### Solution

Composite defines a common `Component` interface (for example, `Graphic`) that both simple shapes and groups implement. A `Composite` stores children (which can be leaves or other composites) and forwards operations like `draw()` to them. The client doesn’t care whether it’s dealing with a leaf or a subtree.

## Structure

The Composite pattern typically includes:

1. **Component**: An interface or abstract class defining common operations for both individual and composite objects.
2. **Leaf**: Represents individual objects in the composition (e.g., Circle, Rectangle).
3. **Composite**: Represents groups of `Leaf` objects and other `Composite` objects, managing children and implementing operations on the group.

## UML Diagram

```text
+-------------------+
|     Component     |<-----------------------------+
|-------------------|                              |
| + operation()     |                              |
+-------------------+                              |
        ^                                        |
        |                                        |
+------------------+               +-------------------+
|     Leaf         |               |    Composite     |
+------------------+               +-------------------+
| + operation()    |               | + add(Component) |
|                  |               | + remove(Component) |
+------------------+               | + operation()     |
                                    +-------------------+
```

## Example: Graphic Shapes Hierarchy

Let’s implement an example of a graphic shapes editor using the Composite pattern. In this example, we’ll have individual shapes (e.g., `Circle`, `Rectangle`) and groups of shapes that we can treat uniformly.

### Step 1: Define the Component Interface

The `Graphic` interface defines common operations that both individual shapes and groups of shapes should implement.

```java
// Component
interface Graphic {
    void draw();
}
```

### Step 2: Implement Leaf Classes

Each concrete shape (e.g., `Circle`, `Rectangle`) implements the `Graphic` interface, representing individual objects in the composition.

```java
// Leaf for Circle
class Circle implements Graphic {
    @Override
    public void draw() {
        System.out.println("Drawing a circle");
    }
}

// Leaf for Rectangle
class Rectangle implements Graphic {
    @Override
    public void draw() {
        System.out.println("Drawing a rectangle");
    }
}
```

### Step 3: Implement the Composite Class

The `CompositeGraphic` class represents groups of shapes. It implements the `Graphic` interface and can contain other `Graphic` objects, allowing it to hold both individual shapes and groups of shapes.

```java
// Composite
class CompositeGraphic implements Graphic {
    private List<Graphic> children = new ArrayList<>();

    public void add(Graphic graphic) {
        children.add(graphic);
    }

    public void remove(Graphic graphic) {
        children.remove(graphic);
    }

    @Override
    public void draw() {
        for (Graphic graphic : children) {
            graphic.draw();
        }
    }
}
```

### Step 4: Client Code Using the Composite

The client can treat individual shapes and groups of shapes uniformly, using the same interface (`Graphic`) for all operations.

```java
public class Client {
    public static void main(String[] args) {
        // Create individual shapes
        Graphic circle = new Circle();
        Graphic rectangle = new Rectangle();

        // Create a composite group of shapes
        CompositeGraphic group = new CompositeGraphic();
        group.add(circle);
        group.add(rectangle);

        // Create another group with nested composites
        CompositeGraphic nestedGroup = new CompositeGraphic();
        nestedGroup.add(group);
        nestedGroup.add(new Circle());

        // Draw all graphics
        System.out.println("Drawing individual group:");
        group.draw();

        System.out.println("\nDrawing nested group:");
        nestedGroup.draw();
    }
}
```

### Output

```plaintext
Drawing individual group:
Drawing a circle
Drawing a rectangle

Drawing nested group:
Drawing a circle
Drawing a rectangle
Drawing a circle
```

In this example:

- The `Graphic` interface defines a `draw` method that both `Circle` and `Rectangle` implement.
- The `CompositeGraphic` class represents a group of `Graphic` objects and also implements the `draw` method by iterating over its children.
- The client code can use `draw` on both individual shapes and groups of shapes without needing to know whether each element is a single shape or a composite.

## Applicability

Use the Composite pattern when:

1. You need to represent part-whole hierarchies, such as graphical objects, menus, or file directories.
2. You want clients to treat individual objects and groups of objects uniformly, without needing to distinguish between them.
3. You have complex structures that benefit from being managed as nested groups or trees.

## Advantages and Disadvantages

### Advantages

1. **Unified Interface**: Composite provides a unified interface for handling individual and composite objects, simplifying client code.
2. **Easier Tree Structures**: The pattern enables easy creation and management of complex, hierarchical structures, such as directories or UI components.
3. **Scalability**: Composite allows you to add new types of components and composites without changing the existing code, following the Open-Closed Principle.

### Disadvantages

1. **Complex Management**: Managing composite hierarchies can become complex, especially with deep or large tree structures.
2. **Limited Safety with Leaf-Specific Operations**: In certain cases, leaf nodes may need specific operations that don’t apply to composites, which can complicate the design.
3. **Overhead for Simple Structures**: For simpler scenarios, using the Composite pattern may add unnecessary complexity.

## Best Practices for Implementing the Composite Pattern

1. **Avoid Assumptions About Components**: Ensure that client code does not make assumptions about whether a `Graphic` is a leaf or a composite.
2. **Use Recursion for Composite Operations**: Composite structures often benefit from recursive operations, allowing each element to perform its action in a tree structure.
3. **Consider Interface Segregation**: If some operations apply only to specific components, consider using smaller interfaces or segregated operations to prevent unexpected behavior.

## Conclusion

The Composite pattern provides a powerful way to work with complex hierarchical structures, enabling clients to treat individual objects and compositions of objects uniformly. By leveraging this pattern, you can build flexible and scalable structures for applications involving tree-like relationships.
