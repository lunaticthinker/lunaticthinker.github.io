---
title: "Prototype Pattern"
draft: false
bookHidden: true
---

# Prototype Pattern

The **Prototype** pattern is a creational design pattern that enables object creation by cloning existing instances. Instead of creating new instances from scratch, the Prototype pattern allows objects to be duplicated, reducing the need to repeat expensive initialization processes. This pattern is ideal when object creation is costly, complex, or involves significant configuration.

## Intent

**The main intent of the Prototype pattern is to specify the kinds of objects to create using a prototypical instance, allowing new objects to be created by copying this prototype.** This pattern helps reduce the overhead of creating new instances by cloning pre-configured objects.

## Problem and Solution

### Problem

Imagine you’re developing a graphic editor where you need to create multiple shapes with similar properties (e.g., colors, dimensions, coordinates). Each shape requires configuration, which can be repetitive and resource-intensive if created from scratch each time.

### Solution

The Prototype pattern lets you define a prototype object (e.g., `Circle`, `Rectangle`) with pre-configured properties. New shapes can be created by cloning these prototypes, inheriting the configuration of the original and making adjustments as needed. This approach minimizes the need for repetitive configuration and reduces object creation overhead.

## Structure

The Prototype pattern typically includes:

1. **Prototype Interface**: Declares a `clone` method for cloning objects.
2. **Concrete Prototypes**: Classes implementing the prototype interface, providing their own cloning mechanisms.
3. **Client Code**: Uses the prototype objects to create new instances by cloning.

## UML Diagram

```
+-------------------+
|   Prototype       |
|-------------------|
| + clone()         |
+-------------------+
        ^
        |
+------------------+       +------------------+
|   Circle         |       |   Rectangle      |
|------------------|       |------------------|
| + clone()        |       | + clone()        |
+------------------+       +------------------+
```

## Example: Graphic Editor with Shapes

Let’s implement a graphic editor that creates various shapes by cloning prototypes. We’ll define a `Shape` interface with a `clone` method, and concrete shapes (`Circle` and `Rectangle`) that implement this interface.

### Step 1: Define the Prototype Interface

```java
// Prototype interface
interface Shape {
    Shape clone();
}
```

### Step 2: Implement Concrete Prototypes

Each concrete shape class (`Circle` and `Rectangle`) implements the `clone` method, allowing new instances to be created by copying existing ones.

```java
// Concrete Prototype for Circle
class Circle implements Shape {
    private int radius;
    private String color;

    public Circle(int radius, String color) {
        this.radius = radius;
        this.color = color;
    }

    public void setRadius(int radius) {
        this.radius = radius;
    }

    @Override
    public Shape clone() {
        return new Circle(radius, color); // Creates a copy with the same properties
    }

    @Override
    public String toString() {
        return "Circle with radius " + radius + " and color " + color;
    }
}

// Concrete Prototype for Rectangle
class Rectangle implements Shape {
    private int width;
    private int height;
    private String color;

    public Rectangle(int width, int height, String color) {
        this.width = width;
        this.height = height;
        this.color = color;
    }

    public void setDimensions(int width, int height) {
        this.width = width;
        this.height = height;
    }

    @Override
    public Shape clone() {
        return new Rectangle(width, height, color); // Creates a copy with the same properties
    }

    @Override
    public String toString() {
        return "Rectangle with width " + width + ", height " + height + " and color " + color;
    }
}
```

### Step 3: Client Code

The client can create new shapes by cloning prototypes, making adjustments as needed.

```java
public class Client {
    public static void main(String[] args) {
        // Create initial prototypes
        Circle baseCircle = new Circle(5, "Red");
        Rectangle baseRectangle = new Rectangle(4, 7, "Blue");

        // Clone the prototypes to create new instances
        Circle circleClone = (Circle) baseCircle.clone();
        circleClone.setRadius(10);  // Adjust properties if necessary

        Rectangle rectangleClone = (Rectangle) baseRectangle.clone();
        rectangleClone.setDimensions(8, 10);

        System.out.println(baseCircle);      // Output: Circle with radius 5 and color Red
        System.out.println(circleClone);     // Output: Circle with radius 10 and color Red
        System.out.println(baseRectangle);   // Output: Rectangle with width 4, height 7 and color Blue
        System.out.println(rectangleClone);  // Output: Rectangle with width 8, height 10 and color Blue
    }
}
```

### Explanation

In this example:

- `Shape` defines a `clone` method that each concrete shape class (`Circle`, `Rectangle`) implements.
- `Circle` and `Rectangle` provide their own cloning mechanisms, creating copies with the same properties.
- The client can create new shapes by cloning the prototypes, making adjustments as necessary.

## Applicability

Use the Prototype pattern when:

1. Object creation is resource-intensive, complex, or requires significant configuration.
2. You want to avoid duplicating code to initialize objects with similar properties.
3. You need to create new instances by copying existing instances rather than creating them from scratch.

## Advantages and Disadvantages

### Advantages

1. **Reduced Overhead**: Prototypes can be cloned rather than recreated from scratch, reducing initialization costs for complex objects.
2. **Easier Object Creation**: Prototype cloning simplifies object creation when similar configurations are needed.
3. **Flexibility**: New objects can be created dynamically by cloning prototypes, providing flexibility without modifying the underlying code.

### Disadvantages

1. **Deep vs. Shallow Copying**: Cloning may require deep copying if the object contains references to mutable objects, which can increase complexity.
2. **Complex Cloning Logic**: For objects with complex structures, implementing a reliable `clone` method can be challenging.
3. **Limited Use Case**: Prototype is not suitable for objects that are simple or where instantiation from scratch is straightforward.

## Best Practices for Implementing the Prototype Pattern

1. **Consider Deep Cloning**: For objects with nested structures, ensure that deep copies are made to avoid shared references.
2. **Use `clone` Carefully**: In Java, the `clone` method from `Object` can lead to issues if not properly implemented. Consider custom `clone` methods or use external libraries when necessary.
3. **Avoid Overusing**: The Prototype pattern is best suited for scenarios where object creation is costly or complex; for simpler cases, regular instantiation is sufficient.

## Conclusion

The Prototype pattern provides a way to create new objects by duplicating existing instances, making it ideal for scenarios where objects require costly or complex configuration. By cloning prototypes, you can reduce object creation overhead and simplify the construction process, leading to cleaner and more flexible code.
