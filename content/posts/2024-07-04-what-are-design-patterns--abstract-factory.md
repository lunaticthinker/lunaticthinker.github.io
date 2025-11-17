---
title: "Abstract Factory Pattern"
draft: false
bookHidden: true
---

# Abstract Factory Pattern

The **Abstract Factory** pattern is a creational design pattern that provides an interface for creating families of related or dependent objects without specifying their concrete classes. This pattern is particularly useful when we need to enforce consistency across multiple products or components that belong to the same family.

## Intent

**The main intent of the Abstract Factory pattern is to encapsulate a group of individual factories with a common interface.** This allows clients to create families of related objects without coupling the code to specific implementations. It promotes a more modular and scalable design by allowing the creation of product families independently of the client code.

## Problem and Solution

### Problem

Imagine you’re building a cross-platform GUI application that needs different sets of UI components (e.g., buttons, text fields) for Windows, macOS, and Linux. You want the application to remain consistent on each platform but don’t want to hard-code the specifics of each platform in the main application code.

### Solution

The Abstract Factory pattern allows you to define an interface (`GUIFactory`) that provides methods to create a family of related objects, such as `Button` and `TextField`. Each platform (Windows, macOS, Linux) has its own factory implementation that provides platform-specific instances of these components.

## Structure

The Abstract Factory pattern typically includes:

1. **Abstract Factory Interface**: Declares methods for creating abstract product types.
2. **Concrete Factories**: Implementations of the abstract factory interface that return specific types of products.
3. **Abstract Product Interfaces**: Interfaces or abstract classes for each type of product created by the factory.
4. **Concrete Products**: Implementations of the abstract product interfaces.

## UML Diagram

```
+-------------------+       +---------------------+
|   GUIFactory      |       |   Button           |
|-------------------|       |---------------------|
| + createButton()  |       | + render()         |
| + createTextField()|      |---------------------|
+-------------------+       |  LinuxButton       |
                            |  WindowsButton     |
                            +---------------------+
```

## Example: Cross-Platform UI Components

Let’s implement a simplified cross-platform UI system with the Abstract Factory pattern in Java. We’ll create an interface `GUIFactory` that provides factory methods for creating `Button` and `TextField` objects. Each platform (Windows and Linux) has its own factory that produces platform-specific components.

### Step 1: Define Abstract Product Interfaces

```java
// Abstract Product for Buttons
interface Button {
    void render();
}

// Abstract Product for TextFields
interface TextField {
    void render();
}
```

### Step 2: Define Concrete Products

```java
// Concrete Button for Windows
class WindowsButton implements Button {
    public void render() {
        System.out.println("Rendering Windows Button");
    }
}

// Concrete TextField for Windows
class WindowsTextField implements TextField {
    public void render() {
        System.out.println("Rendering Windows TextField");
    }
}

// Concrete Button for Linux
class LinuxButton implements Button {
    public void render() {
        System.out.println("Rendering Linux Button");
    }
}

// Concrete TextField for Linux
class LinuxTextField implements TextField {
    public void render() {
        System.out.println("Rendering Linux TextField");
    }
```

### Step 3: Define the Abstract Factory Interface

```java
// Abstract Factory
interface GUIFactory {
    Button createButton();
    TextField createTextField();
}
```

### Step 4: Implement Concrete Factories

```java
// Concrete Factory for Windows
class WindowsFactory implements GUIFactory {
    public Button createButton() {
        return new WindowsButton();
    }

    public TextField createTextField() {
        return new WindowsTextField();
    }
}

// Concrete Factory for Linux
class LinuxFactory implements GUIFactory {
    public Button createButton() {
        return new LinuxButton();
    }

    public TextField createTextField() {
        return new LinuxTextField();
    }
}
```

### Step 5: Client Code

The client code uses the factory to create objects without needing to know about specific implementations. This makes it easy to switch between different families of products.

```java
class Application {
    private Button button;
    private TextField textField;

    public Application(GUIFactory factory) {
        button = factory.createButton();
        textField = factory.createTextField();
    }

    public void renderUI() {
        button.render();
        textField.render();
    }
}

// Client code
public class Client {
    public static void main(String[] args) {
        GUIFactory factory;
        String os = System.getProperty("os.name");

        if (os.contains("Windows")) {
            factory = new WindowsFactory();
        } else {
            factory = new LinuxFactory();
        }

        Application app = new Application(factory);
        app.renderUI();
    }
}
```

### Explanation

In this example:

- `Application` depends on the `GUIFactory` interface, not specific implementations, which adheres to the Dependency Inversion Principle.
- We can easily switch between different platforms by providing different factory implementations (e.g., `WindowsFactory` or `LinuxFactory`) without changing `Application`’s code.
- This design makes the system open for extension but closed for modification, aligning with the Open-Closed Principle.

## Applicability

Use the Abstract Factory pattern when:

1. You need to create families of related objects, such as UI components that should be consistent across an application.
2. You want to isolate the client code from concrete implementations and enforce consistency among related objects.
3. Your application needs to be scalable with minimal modification to existing code.

## Advantages and Disadvantages

### Advantages

1. **Encapsulates Object Creation**: Abstract Factory centralizes object creation, making the code more organized and easier to manage.
2. **Promotes Consistency**: Ensures that related products are consistent and can work together.
3. **Improves Scalability**: Adding new product families requires only creating new factory implementations, without altering existing code.

### Disadvantages

1. **Increased Complexity**: Using multiple interfaces and classes can make the code more complex, especially for small projects.
2. **Limited Flexibility with Families**: Each concrete factory produces a specific family of products, so adding new products outside of existing families may require additional modifications.

## Summary

The Abstract Factory pattern is a powerful tool for creating families of related objects in a consistent and scalable way. By encapsulating object creation and enforcing consistent product families, this pattern helps decouple the client code from specific implementations, making the system more modular and adaptable to change.
