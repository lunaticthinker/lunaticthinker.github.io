---
title: "Flyweight Pattern"
draft: false
bookHidden: true
---

# Flyweight Pattern

The **Flyweight** pattern is a structural design pattern that focuses on minimizing memory usage by sharing as much data as possible with similar objects. This pattern is especially effective in systems where a large number of similar objects are created, such as in graphics applications or document editing software.

## Intent

**The main intent of the Flyweight pattern is to reduce memory usage by sharing parts of the object state that are common to many objects, allowing many instances to share the same data.** This pattern promotes the reuse of objects that have shared properties, saving memory and improving performance.

## Problem and Solution

### Problem

Imagine you’re building a graphical editor that needs to display thousands of characters with different font types, sizes, and colors. Creating an object for each character could lead to high memory usage, as many characters share similar properties. Without Flyweight, you’d end up with redundant data stored in each character object.

### Solution

The Flyweight pattern addresses this problem by splitting the state of objects into **intrinsic** (shared) and **extrinsic** (unique) states:

1. **Intrinsic State**: Common, unchanging data that can be shared (e.g., font type, font size).
2. **Extrinsic State**: Data that is unique to each instance and cannot be shared (e.g., position on screen).

By storing the intrinsic state in a shared object, we can reduce the number of objects and overall memory usage.

## Structure

The Flyweight pattern typically includes:

1. **Flyweight**: Declares the interface through which flyweights can receive and act on extrinsic state.
2. **Concrete Flyweight**: Implements the flyweight interface and stores intrinsic state.
3. **Flyweight Factory**: Manages a pool of flyweight objects, returning existing instances if they match the requested intrinsic state.
4. **Client**: Maintains and provides extrinsic state to flyweights when needed.

## UML Diagram

```
+-------------------+     +----------------------+
|    Flyweight      |<----|   ConcreteFlyweight  |
|-------------------|     |----------------------|
| + operation()     |     | + operation()        |
+-------------------+     +----------------------+
         ^
         |
+-------------------------+
|      FlyweightFactory   |
|-------------------------|
| + getFlyweight()        |
+-------------------------+
```

## Example: Character Display in a Text Editor

Let’s implement an example of a text editor using the Flyweight pattern. Each character will have intrinsic properties (e.g., font and size) and extrinsic properties (e.g., position), allowing the editor to reuse character objects for similar fonts and sizes.

### Step 1: Define the Flyweight Interface

The `Character` interface defines the `draw` method, which accepts extrinsic state as parameters.

```java
// Flyweight Interface
interface Character {
    void draw(int x, int y);
}
```

### Step 2: Implement the Concrete Flyweight

The `ConcreteCharacter` class represents a specific character with intrinsic state (e.g., font and size). The `draw` method uses extrinsic state (position) provided by the client.

```java
// Concrete Flyweight
class ConcreteCharacter implements Character {
    private char symbol;
    private String font;
    private int size;

    public ConcreteCharacter(char symbol, String font, int size) {
        this.symbol = symbol;
        this.font = font;
        this.size = size;
    }

    @Override
    public void draw(int x, int y) {
        System.out.println("Drawing '" + symbol + "' at (" + x + "," + y + ") in font " + font + " with size " + size);
    }
}
```

### Step 3: Implement the Flyweight Factory

The `CharacterFactory` class manages a pool of characters based on intrinsic state (character symbol, font, and size). If a character with the same intrinsic state exists, it returns the existing instance; otherwise, it creates a new one.

```java
// Flyweight Factory
class CharacterFactory {
    private Map<String, Character> characters = new HashMap<>();

    public Character getCharacter(char symbol, String font, int size) {
        String key = symbol + font + size;
        if (!characters.containsKey(key)) {
            characters.put(key, new ConcreteCharacter(symbol, font, size));
            System.out.println("Creating new character: " + symbol);
        } else {
            System.out.println("Reusing existing character: " + symbol);
        }
        return characters.get(key);
    }
}
```

### Step 4: Client Code Using the Flyweight

The client code creates characters through the `CharacterFactory`, passing in the extrinsic state (position) when drawing each character.

```java
public class Client {
    public static void main(String[] args) {
        CharacterFactory factory = new CharacterFactory();

        // Creating and reusing characters
        Character a1 = factory.getCharacter('A', "Arial", 12);
        a1.draw(10, 20);

        Character a2 = factory.getCharacter('A', "Arial", 12);
        a2.draw(30, 20);

        Character b1 = factory.getCharacter('B', "Arial", 12);
        b1.draw(50, 20);

        // a1 and a2 share the same intrinsic state and are the same instance
        System.out.println("a1 and a2 are the same instance: " + (a1 == a2));
    }
}
```

### Output

```plaintext
Creating new character: A
Drawing 'A' at (10,20) in font Arial with size 12
Reusing existing character: A
Drawing 'A' at (30,20) in font Arial with size 12
Creating new character: B
Drawing 'B' at (50,20) in font Arial with size 12
a1 and a2 are the same instance: true
```

In this example:

- The `CharacterFactory` ensures that each unique combination of intrinsic state (symbol, font, size) is only created once, reusing it when needed.
- The `ConcreteCharacter` class stores intrinsic state, while extrinsic state is provided during the `draw` call.
- `a1` and `a2` share the same intrinsic state, so they are the same instance, reducing memory usage.

## Applicability

Use the Flyweight pattern when:

1. You need a large number of objects, and most of their properties can be shared, saving memory.
2. You want to reduce memory usage by sharing common data across multiple objects.
3. Your objects have both intrinsic (shared) and extrinsic (unique) properties, allowing for partial reuse.

## Advantages and Disadvantages

### Advantages

1. **Reduced Memory Usage**: Flyweight saves memory by sharing intrinsic data across multiple objects.
2. **Efficient Object Management**: Flyweight reduces the need for duplicate objects, making it easier to manage large collections of similar objects.
3. **Improved Performance**: By reducing memory usage, Flyweight can improve performance, especially in memory-constrained applications.

### Disadvantages

1. **Increased Complexity**: The Flyweight pattern can add complexity to code due to the separation of intrinsic and extrinsic state.
2. **Dependency on Client for Extrinsic State**: The client is responsible for passing extrinsic state, which can lead to errors if not managed correctly.
3. **Limited Use Case**: The pattern is primarily useful in situations with many similar objects. For unique objects, the pattern provides little benefit.

## Best Practices for Implementing the Flyweight Pattern

1. **Clearly Separate Intrinsic and Extrinsic State**: Clearly define which parts of the object state are shared and which are unique to ensure the pattern is applied effectively.
2. **Use a Factory for Object Management**: Use a factory class to manage and reuse flyweight instances, avoiding direct instantiation by clients.
3. **Evaluate Memory Trade-offs**: Apply the Flyweight pattern only when memory savings are significant, as it can add complexity to your design.

## Conclusion

The Flyweight pattern provides an efficient way to manage memory usage by sharing intrinsic state across similar objects. This pattern is particularly useful in systems where many objects share common data, allowing for flexible, optimized object creation while reducing overall memory consumption.
