---
title: "Decorator Pattern"
date: 2024-07-27
categories:
  - Design Patterns
tags:
  - design patterns
  - structural patterns
  - decorator
  - composition
bookHidden: false
---

Think of adding toppings to a pizza or filters to a photo: you start with something simple, then wrap it with extra behavior. You don’t need a new “class” of pizza for every possible combination.

The **Decorator** pattern is a structural pattern that lets you dynamically add responsibilities to objects by wrapping them in other objects. It’s a flexible alternative to subclassing for extending behavior.

## Intent

Add new functionality to an object dynamically, without changing its class or affecting other instances, by wrapping it in decorators that implement the same interface.

## Problem and Solution

### Problem

Imagine a `TextEditor` that should support bold, italic, underline, strikethrough, links, and more. If you model each combination as a subclass, you quickly end up with a combinatorial explosion of types.

### Solution

Decorator lets you keep a simple `PlainText` implementation and wrap it with decorators like `BoldTextDecorator`, `ItalicTextDecorator`, etc. Each decorator adds one behavior and forwards the rest. You can stack them in any order at runtime to compose behavior.

## Structure

The Decorator pattern typically includes:

1. **Component Interface**: Defines the interface for objects that can have responsibilities added to them dynamically.
2. **Concrete Component**: The original object to which new functionality is added.
3. **Decorator**: Abstract class that implements the component interface and contains a reference to a component.
4. **Concrete Decorators**: Subclasses of the decorator that add specific behaviors to the component.

## UML Diagram

```text
+-------------------+     +-----------------------+
|   Component       |<----|     Decorator        |
|-------------------|     |-----------------------|
| + operation()     |     | - component: Component|
+-------------------+     | + operation()         |
        ^                 +-----------------------+
        |                          ^
        |                          |
+------------------+      +----------------------+
|ConcreteComponent |      |   ConcreteDecorator  |
|------------------|      +----------------------+
| + operation()    |      | + operation()        |
+------------------+      +----------------------+
```

## Example: Text Editor with Formatting

Let’s implement an example of a text editor using the Decorator pattern. We’ll have a basic `TextEditor` that can display plain text, and we’ll add decorators for different formatting options, such as bold and italic.

### Step 1: Define the Component Interface

The `Text` interface defines the `render` method that all text components and decorators must implement.

```java
// Component Interface
interface Text {
    String render();
}
```

### Step 2: Implement the Concrete Component

The `PlainText` class implements the `Text` interface and represents the base component that can display plain text.

```java
// Concrete Component
class PlainText implements Text {
    private String content;

    public PlainText(String content) {
        this.content = content;
    }

    @Override
    public String render() {
        return content;
    }
}
```

### Step 3: Create the Abstract Decorator

The `TextDecorator` class implements the `Text` interface and holds a reference to a `Text` object, allowing it to act as a wrapper.

```java
// Decorator
abstract class TextDecorator implements Text {
    protected Text text;

    public TextDecorator(Text text) {
        this.text = text;
    }

    @Override
    public String render() {
        return text.render();
    }
}
```

### Step 4: Implement Concrete Decorators

Each concrete decorator adds specific behavior to the `Text` object, such as bold or italic formatting.

```java
// Concrete Decorator for Bold Text
class BoldTextDecorator extends TextDecorator {
    public BoldTextDecorator(Text text) {
        super(text);
    }

    @Override
    public String render() {
        return "<b>" + text.render() + "</b>";
    }
}

// Concrete Decorator for Italic Text
class ItalicTextDecorator extends TextDecorator {
    public ItalicTextDecorator(Text text) {
        super(text);
    }

    @Override
    public String render() {
        return "<i>" + text.render() + "</i>";
    }
}
```

### Step 5: Client Code Using the Decorator

The client code can now create text with different combinations of decorators by wrapping the `PlainText` object with various decorators.

```java
public class Client {
    public static void main(String[] args) {
        Text plainText = new PlainText("Hello, World!");

        // Apply bold formatting
        Text boldText = new BoldTextDecorator(plainText);
        System.out.println(boldText.render()); // Output: <b>Hello, World!</b>

        // Apply italic formatting
        Text italicText = new ItalicTextDecorator(plainText);
        System.out.println(italicText.render()); // Output: <i>Hello, World!</i>

        // Apply both bold and italic formatting
        Text boldItalicText = new BoldTextDecorator(new ItalicTextDecorator(plainText));
        System.out.println(boldItalicText.render()); // Output: <b><i>Hello, World!</i></b>
    }
}
```

### Explanation

In this example:

- The `Text` interface defines the `render` method that all text objects and decorators implement.
- `PlainText` is the base component that displays plain text.
- `BoldTextDecorator` and `ItalicTextDecorator` are concrete decorators that add bold and italic formatting, respectively.
- The client can combine multiple decorators to create complex formatting dynamically.

## Applicability

Use the Decorator pattern when:

1. You need to add responsibilities to objects dynamically and flexibly.
2. You want to avoid subclassing, as it would lead to a large number of classes for every possible combination of behaviors.
3. You need to add different combinations of behaviors to objects without modifying the base class or the client code.

## Advantages and Disadvantages

### Advantages

1. **Flexible Behavior Extension**: Decorator allows you to add or remove behaviors at runtime without modifying the original object.
2. **Adheres to Open-Closed Principle**: New behaviors can be added by creating new decorators, rather than modifying existing classes.
3. **Combining Multiple Behaviors**: You can stack multiple decorators around an object to create complex behaviors dynamically.

### Disadvantages

1. **Increased Complexity**: The Decorator pattern introduces additional classes, which may increase complexity, especially when many decorators are combined.
2. **Hard to Debug**: Multiple layers of decorators can make it difficult to debug and trace the flow of execution.
3. **Order Sensitivity**: The order in which decorators are applied can impact the final behavior, requiring careful attention.

## Best Practices for Implementing the Decorator Pattern

1. **Use Composition Over Inheritance**: Decorators should wrap objects instead of extending them, making the pattern more flexible.
2. **Limit Decorator Stacking**: While multiple decorators can be stacked, avoid overuse, as this can lead to confusion and increased complexity.
3. **Use Naming Conventions**: Clear naming for decorators helps in understanding the chain of decorators applied to an object.

## Conclusion

The Decorator pattern provides a flexible and dynamic way to add behaviors to objects without modifying their structure. This pattern enables you to enhance the functionality of objects at runtime, creating a modular and extensible design that adheres to the Open-Closed Principle.
