---
title: "What are Coding Principles - The Liskov Substitution Principle (LSP)"
categories:
  - Coding Principles
  - Home Page
bookHidden: true
---

# Liskov Substitution Principle (LSP)

The Liskov Substitution Principle (LSP) is the third principle in the SOLID principles of object-oriented design. It states:

**“Objects of a superclass should be replaceable with objects of a subclass without affecting the correctness of the program.”**

In other words, if class `B` is a subclass of class `A`, then instances of `A` should be replaceable by instances of `B` without altering the program's behavior. LSP ensures that a derived class can stand in for its base class without breaking functionality, making inheritance more predictable and reliable.

## Why Use the Liskov Substitution Principle?

Violations of LSP can lead to unexpected bugs and breakages when subclasses behave differently from their base classes. Adhering to LSP helps:

1. **Ensure Consistency**: Subclasses are expected to behave consistently with their base classes.
2. **Maintain Predictability**: LSP allows for predictable behavior, so consumers of the base class don’t need to know about subclass-specific details.
3. **Enhance Code Reusability**: By ensuring that subclasses don’t violate the expectations of their base classes, we promote reusable code that’s easier to extend.

## Key Concepts of LSP

1. **Behavioral Consistency**: Subclasses should not change the expected behavior of methods inherited from the base class.
2. **Subtype Polymorphism**: LSP enables polymorphism by ensuring that subclasses can be used interchangeably with their base class.
3. **No Weakened Preconditions or Strengthened Postconditions**: Subclasses should not impose stricter conditions than the base class (preconditions) or give stronger guarantees on the result (postconditions).

## LSP in Action

Let’s explore an example to see how LSP works and what happens when it’s violated.

### Without LSP: Violation Example

Consider a `Rectangle` class with `width` and `height` properties, and a `Square` subclass that inherits from it.

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
        this.height = width; // Square has equal width and height
    }

    @Override
    public void setHeight(int height) {
        this.height = height;
        this.width = height; // Square has equal width and height
    }
}
```

In this example:

- The `Square` class overrides `setWidth` and `setHeight` to ensure that the width and height remain equal, as squares require.
- However, this breaks the expected behavior of the `Rectangle` class. For example, if a function expects a `Rectangle` but is passed a `Square`, setting only the `width` or `height` will produce incorrect results.

```java
public void resizeRectangle(Rectangle rectangle) {
    rectangle.setWidth(5);
    rectangle.setHeight(10);
    assert rectangle.getArea() == 50; // This fails for Square
}
```

In this case, using `Square` in place of `Rectangle` causes unexpected behavior, violating LSP.

### With LSP: Corrected Example

To satisfy LSP, we should avoid making `Square` a subclass of `Rectangle` because a square is not a type of rectangle in terms of the expected behavior of width and height properties. Instead, we can create separate classes that share a common interface.

```java
interface Shape {
    int getArea();
}

class Rectangle implements Shape {
    protected int width;
    protected int height;

    public Rectangle(int width, int height) {
        this.width = width;
        this.height = height;
    }

    public int getArea() {
        return width * height;
    }
}

class Square implements Shape {
    private int side;

    public Square(int side) {
        this.side = side;
    }

    public int getArea() {
        return side * side;
    }
}
```

Now:

- `Rectangle` and `Square` implement a common `Shape` interface, rather than `Square` inheriting from `Rectangle`.
- Both classes provide an `getArea` method, so either can be used interchangeably where a `Shape` is expected.
- This approach avoids violating LSP, as the behavior of `Square` and `Rectangle` no longer conflict.

### LSP in Real-World Applications

Let’s consider a practical scenario involving document processing.

Suppose we have a base class `Document` with a method `print` and a derived class `ReadOnlyDocument` that represents read-only documents.

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

In this example:

- `ReadOnlyDocument` violates LSP because it changes the expected behavior of the `save` method.
- If a function that processes `Document` objects tries to save a `ReadOnlyDocument`, it will encounter an exception.

#### Solution

To fix this, we can refactor by separating the behavior using interfaces.

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

This approach ensures that `ReadOnlyDocument` and `EditableDocument` conform to LSP, as each class now has methods that are specific to its functionality.

## Benefits and Challenges of LSP

### Benefits

1. **Improved Predictability**: Clients can use subclasses without needing to know their specific details, as behavior is consistent across the hierarchy.
2. **Enhanced Code Reusability**: By following LSP, subclasses can be seamlessly reused where base classes are expected.
3. **Reduced Bugs**: Violations of LSP can introduce subtle bugs, so adherence to LSP reduces the likelihood of unexpected behavior.

### Challenges

1. **Complex Hierarchies**: LSP can be challenging in complex hierarchies where subclass-specific behaviors conflict with base class expectations.
2. **Increased Design Overhead**: LSP requires careful planning of class hierarchies and interfaces, which can add complexity to the design phase.
3. **Potential for Over-Refactoring**: Strict adherence to LSP can sometimes lead to over-refactoring, where the desire for compliance introduces excessive interfaces or classes.

## Best Practices for Implementing LSP

1. **Test Substitutability**: Regularly test that subclasses can replace base classes without changing behavior, especially if the base class has defined contracts or invariants.
2. **Favor Composition Over Inheritance**: Where LSP is difficult to achieve, consider using composition rather than inheritance to share functionality without inheriting unwanted behavior.
3. **Avoid Overloading Subclass Responsibilities**: Limit the responsibilities of subclasses to avoid conflicts with base class expectations.

## Conclusion

The Liskov Substitution Principle is essential for creating robust, extendable, and reusable class hierarchies. By adhering to LSP, we ensure that subclasses behave in a way that is consistent with their base classes, allowing for predictable and interchangeable code. Though it may require extra design considerations, LSP ultimately leads to software that is more flexible, maintainable, and less prone to errors.
