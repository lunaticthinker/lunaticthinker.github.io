---
title: "Composite Pattern"
draft: false
bookHidden: true
---

# Composite Pattern

The **Composite** pattern is a structural design pattern that allows you to compose objects into tree-like structures to represent part-whole hierarchies. This pattern enables clients to treat individual objects and groups of objects uniformly, making it particularly useful for handling complex structures such as directories, menus, and graphical objects.

## Intent

**The main intent of the Composite pattern is to allow clients to treat individual objects and compositions of objects uniformly.** This pattern enables the creation of a tree structure, where both simple and complex elements implement the same interface, making it easier to work with complex object hierarchies.

## Problem and Solution

### Problem

Suppose you are developing a graphical editor where each shape can contain other shapes, such as groups of circles, rectangles, and lines. You want the application to treat single shapes and groups of shapes uniformly, allowing operations like drawing, resizing, and moving to apply to both individual shapes and groups.

### Solution

The Composite pattern allows you to define an abstract interface for all shapes, with methods like `draw` and `resize`. Individual shapes and groups of shapes (composites) both implement this interface. The composite (group) can contain other shapes or groups, enabling the creation of a recursive tree structure.

## Structure

The Composite pattern typically includes:

1. **Component**: An interface or abstract class defining common operations for both individual and composite objects.
2. **Leaf**: Represents individual objects in the composition (e.g., Circle, Rectangle).
3. **Composite**: Represents groups of `Leaf` objects and other `Composite` objects, managing children and implementing operations on the group.

## UML Diagram

```
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
