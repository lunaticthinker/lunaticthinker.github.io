---
title: "Builder Pattern"
date: 2024-07-05
categories:
  - Design Patterns
tags:
  - design patterns
  - creational patterns
  - builder
  - architecture
bookHidden: false
---

The **Builder** pattern is what you reach for when a constructor has become a small novel of parameters and optional flags.

It’s a creational pattern that lets you construct complex objects step by step, separating _how_ you assemble them from _what_ the final representation looks like. That way you can support multiple configurations without turning your constructors into unreadable beasts.

## Intent

**The main intent of the Builder pattern is to separate the construction of a complex object from its representation.** You keep the process consistent while allowing the result to vary.

## Problem and Solution

### Problem

Suppose you’re creating a `House` object that can have multiple configurable components, like `windows`, `doors`, `floors`, and a `roof`. Using a constructor with numerous parameters can quickly become unreadable and prone to errors, especially if many parameters are optional.

### Solution

The Builder pattern lets you create a `HouseBuilder` class that builds `House` objects step by step, only including the properties needed for each particular instance. This approach is more readable and manageable, as it clearly defines each part of the construction.

## Structure

The Builder pattern typically includes:

1. **Builder Interface**: Declares methods to set each attribute or part of the complex object.
2. **Concrete Builder**: Implements the builder interface, constructing and assembling parts of the product.
3. **Product**: The complex object being built.
4. **Director (optional)**: Oversees the construction process, ensuring the correct order or steps are followed to create the final object.

## UML Diagram

```text
+-------------------+       +-------------------+
|   HouseBuilder    |       |    House         |
|-------------------|       |-------------------|
| + setWindows()    |       | - windows        |
| + setDoors()      |       | - doors          |
| + setRoof()       |       | - roof           |
| + build()         |       | - floors         |
+-------------------+       +-------------------+
        |                           ^
        |                           |
        +---------------------------+
```

## Example: Building a House

Let’s implement a simplified example of building a `House` with a `HouseBuilder`. The `HouseBuilder` class allows us to construct different house configurations without using a long list of parameters.

### Step 1: Define the Product

The product class `House` represents the final object we want to build.

```java
class House {
    private int windows;
    private int doors;
    private int floors;
    private String roofType;

    public House(int windows, int doors, int floors, String roofType) {
        this.windows = windows;
        this.doors = doors;
        this.floors = floors;
        this.roofType = roofType;
    }

    @Override
    public String toString() {
        return "House with " + windows + " windows, " + doors + " doors, " + floors + " floors, and a " + roofType + " roof.";
    }
}
```

### Step 2: Define the Builder Interface

The builder interface `HouseBuilder` defines the methods required to build each part of a `House`.

```java
interface HouseBuilder {
    HouseBuilder setWindows(int windows);
    HouseBuilder setDoors(int doors);
    HouseBuilder setFloors(int floors);
    HouseBuilder setRoofType(String roofType);
    House build();
}
```

### Step 3: Implement the Concrete Builder

The concrete builder class `ConcreteHouseBuilder` implements the `HouseBuilder` interface and provides methods to set each attribute.

```java
class ConcreteHouseBuilder implements HouseBuilder {
    private int windows;
    private int doors;
    private int floors;
    private String roofType;

    @Override
    public HouseBuilder setWindows(int windows) {
        this.windows = windows;
        return this;
    }

    @Override
    public HouseBuilder setDoors(int doors) {
        this.doors = doors;
        return this;
    }

    @Override
    public HouseBuilder setFloors(int floors) {
        this.floors = floors;
        return this;
    }

    @Override
    public HouseBuilder setRoofType(String roofType) {
        this.roofType = roofType;
        return this;
    }

    @Override
    public House build() {
        return new House(windows, doors, floors, roofType);
    }
}
```

### Step 4: Using the Builder in Client Code

The client code uses the builder to construct different configurations of a `House` without needing to modify the `House` class directly.

```java
public class Client {
    public static void main(String[] args) {
        HouseBuilder builder = new ConcreteHouseBuilder();

        // Building a simple house
        House simpleHouse = builder
                .setWindows(4)
                .setDoors(2)
                .setFloors(1)
                .setRoofType("Gable")
                .build();

        System.out.println(simpleHouse);

        // Building a complex house
        House complexHouse = builder
                .setWindows(10)
                .setDoors(5)
                .setFloors(3)
                .setRoofType("Hip")
                .build();

        System.out.println(complexHouse);
    }
}
```

### Output

```plaintext
House with 4 windows, 2 doors, 1 floors, and a Gable roof.
House with 10 windows, 5 doors, 3 floors, and a Hip roof.
```

In this example:

- The `HouseBuilder` interface defines methods for setting each property of the `House`.
- `ConcreteHouseBuilder` implements the `HouseBuilder` interface, allowing properties to be set one by one.
- The client can build `House` objects with different configurations, such as a single-story house or a complex multi-story house, without modifying the `House` class directly.

## Applicability

Use the Builder pattern when:

1. You need to create complex objects with multiple configurations or optional parts.
2. You want to avoid using a long list of constructor parameters.
3. You need a way to construct objects with clear, step-by-step instructions.

## Advantages and Disadvantages

### Advantages

1. **Increased Readability**: Builders provide a more readable way to construct complex objects, with each attribute clearly defined.
2. **Flexibility in Object Creation**: The Builder pattern allows different configurations of an object without modifying its structure.
3. **Immutability**: Once a product is built, it can be made immutable, ensuring consistent state across the application.

### Disadvantages

1. **Increased Complexity**: The Builder pattern introduces additional classes, which can increase complexity, especially in simpler scenarios.
2. **Limited Use for Simple Objects**: If an object has only a few attributes or doesn’t require multiple configurations, the Builder pattern may be unnecessary.

## Best Practices for Implementing the Builder Pattern

1. **Use Fluent Interfaces**: Design builder methods to return the builder object itself, allowing for method chaining and improved readability.
2. **Use Director Class (Optional)**: When building complex products with specific construction steps, consider adding a Director class to manage the sequence and enforce rules for object construction.
3. **Consider Inner Builder Classes**: In languages like Java, it’s common to use an inner static Builder class to simplify the structure when the Builder is tightly coupled to the product.

## Conclusion

The Builder pattern provides a structured approach for constructing complex objects with multiple configurations, avoiding bloated constructors and improving code readability. By separating the construction process from the representation, the Builder pattern allows for a modular, flexible, and maintainable design, especially useful when creating objects with optional or numerous properties.
