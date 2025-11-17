---
title: "Factory Method Pattern"
date: 2024-07-06
categories:
  - Design Patterns
tags:
  - design patterns
  - creational patterns
  - factory method
  - architecture
bookHidden: false
---

The **Factory Method** pattern is the one you use when you want to say “give me a transport,” not “new Truck()” or “new Ship()”.

It defines an interface for creating objects but lets subclasses decide which concrete type to produce. Instantiation is deferred to specific factories, which keeps your high-level code less entangled with concrete classes and more open to extension.

## Intent

**The main intent of Factory Method is to move the “which concrete type?” decision into dedicated creators.** Your core logic works with the `Transport` interface; factories decide whether that’s a truck, ship, or something new.

## Problem and Solution

### Problem

Suppose you are building a logistics application that needs to create various types of transport vehicles, such as `Truck` and `Ship`. The exact type of transport might depend on the logistics route (land or sea). If you try to instantiate each type within the main application logic, you risk tightly coupling the code to specific classes, making it harder to extend or maintain.

### Solution

The Factory Method pattern enables you to define a `TransportFactory` interface with a `createTransport` method. Subclasses can implement this interface to create specific transport types, such as `Truck` or `Ship`, without modifying the main application logic.

## Structure

The Factory Method pattern typically includes:

1. **Creator (Abstract Class or Interface)**: Declares a factory method that returns new objects of a certain type.
2. **Concrete Creators**: Implement the factory method to create specific types of objects.
3. **Product (Interface or Abstract Class)**: Defines the interface for the objects the factory method creates.
4. **Concrete Products**: Concrete classes implementing the product interface, created by the factory.

## UML Diagram

```text
+------------------+           +--------------------+
|    Transport     |           |    TransportFactory|
|------------------|           |--------------------|
| + deliver()      |           | + createTransport()|
+------------------+           +--------------------+
        ^                              ^
        |                              |
+----------------+             +----------------+
|     Truck      |             |      Ship      |
+----------------+             +----------------+
```

## Example: Logistics Transport System

Let’s implement a logistics transport system using the Factory Method pattern. We’ll create a `TransportFactory` that provides a method to create different transport types, such as `Truck` for land transport and `Ship` for sea transport.

### Step 1: Define the Product Interface

```java
// Product interface
interface Transport {
    void deliver();
}
```

### Step 2: Define Concrete Products

```java
// Concrete Product for Truck
class Truck implements Transport {
    public void deliver() {
        System.out.println("Delivering by land with a truck.");
    }
}

// Concrete Product for Ship
class Ship implements Transport {
    public void deliver() {
        System.out.println("Delivering by sea with a ship.");
    }
}
```

### Step 3: Define the Creator Class with Factory Method

The `TransportFactory` defines a factory method `createTransport` that will be overridden by subclasses to create specific transport types.

```java
// Creator (Abstract Class with Factory Method)
abstract class TransportFactory {
    public abstract Transport createTransport();

    public void planDelivery() {
        Transport transport = createTransport();
        transport.deliver();
    }
}
```

### Step 4: Implement Concrete Factories

Each concrete factory implements the `createTransport` method to produce specific transport objects (`Truck` or `Ship`).

```java
// Concrete Factory for Truck
class TruckFactory extends TransportFactory {
    @Override
    public Transport createTransport() {
        return new Truck();
    }
}

// Concrete Factory for Ship
class ShipFactory extends TransportFactory {
    @Override
    public Transport createTransport() {
        return new Ship();
    }
}
```

### Step 5: Client Code

The client code can use any concrete factory to create and deliver transport without knowing the specific type of transport.

```java
public class Client {
    public static void main(String[] args) {
        TransportFactory truckFactory = new TruckFactory();
        truckFactory.planDelivery();  // Output: Delivering by land with a truck.

        TransportFactory shipFactory = new ShipFactory();
        shipFactory.planDelivery();   // Output: Delivering by sea with a ship.
    }
}
```

### Explanation

In this example:

- `TransportFactory` defines a `createTransport` method that subclasses override to specify the type of transport to be created.
- `TruckFactory` and `ShipFactory` are concrete factories that produce `Truck` and `Ship` objects, respectively.
- The client code can create and use transport objects without knowing their exact type, adhering to the Open-Closed Principle and promoting loose coupling.

## Applicability

Use the Factory Method pattern when:

1. You want to allow subclasses to alter the type of object created.
2. You have a common interface or base class but want to delegate instantiation to subclasses.
3. You want to reduce dependencies between a main class and specific classes, especially when types may change over time.

## Advantages and Disadvantages

### Advantages

1. **Promotes Loose Coupling**: The Factory Method pattern decouples client code from specific implementations, making the system more flexible and modular.
2. **Supports Open-Closed Principle**: New types of products can be added without modifying the client code.
3. **Increases Extensibility**: Adding new factories and products is straightforward and doesn’t disrupt existing code.

### Disadvantages

1. **Increased Complexity**: The Factory Method pattern introduces additional classes and complexity, which can be excessive for simple projects.
2. **Requires Subclassing**: To add new product types, new subclasses must be created, which may lead to a more complex hierarchy.

## Best Practices for Implementing the Factory Method Pattern

1. **Use Factory Method for Complex Object Creation**: For simple objects, this pattern might be overkill. Reserve it for cases where the construction process benefits from being centralized and managed by subclasses.
2. **Favor Interface-Based Products**: Define a common interface for products to keep client code consistent and make adding new products easier.
3. **Consider Alternative Patterns for Object Creation**: In cases where only one type of object is needed, simpler patterns like the **Simple Factory** or **Singleton** might be more appropriate.

## Conclusion

The Factory Method pattern provides a flexible and modular way to create objects, allowing subclasses to control the instantiation process. By deferring object creation to subclasses, this pattern promotes loose coupling and extensibility, making it easier to add new product types without modifying existing code.
