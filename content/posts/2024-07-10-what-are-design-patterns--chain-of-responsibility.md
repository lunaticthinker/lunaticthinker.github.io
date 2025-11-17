---
title: "Chain of Responsibility Pattern"
date: 2024-07-10
categories:
  - Design Patterns
tags:
  - design patterns
  - behavioral patterns
  - chain of responsibility
  - architecture
bookHidden: false
---

The **Chain of Responsibility** pattern is what you reach for when you want to send a request into a pipeline and let whoever can handle it, handle it.

It’s a behavioral pattern that lets a request travel through a chain of handlers. Each handler decides whether to process the request or pass it along, which keeps senders decoupled from specific receivers and makes it easy to extend the chain over time.

## Intent

**The main intent of the Chain of Responsibility pattern is to decouple the sender of a request from its receiver by giving more than one object a chance to handle the request.** The pattern creates a chain of handlers, where each handler has the opportunity to process the request or pass it along the chain.

## Problem and Solution

### Problem

Suppose you’re designing a system for processing user support requests. Depending on the type of request, it may need to be handled by different levels of support staff (e.g., Level 1, Level 2, or Level 3). Without the Chain of Responsibility, you would have to tightly couple the request handling process with specific handler classes, making the system rigid and difficult to extend.

### Solution

The Chain of Responsibility pattern solves this problem by creating a chain of support levels (handlers). Each level can either process the request if it has the required permission or pass it to the next level in the chain. This approach allows for dynamic and flexible request handling, where new levels can be added without changing the existing code.

## Structure

The Chain of Responsibility pattern typically includes:

1. **Handler Interface**: Defines the method for processing requests and sets the reference to the next handler.
2. **Concrete Handlers**: Classes that implement the handler interface. Each concrete handler decides whether to process the request or pass it to the next handler.
3. **Client**: Initiates the request and sends it to the first handler in the chain.

## UML Diagram

```text
+-------------------+           +------------------+
|    Handler        |<----------| ConcreteHandler1 |
|-------------------|           +------------------+
| - nextHandler     |           | + handleRequest()|
| + setNext()       |           +------------------+
| + handleRequest() |
+-------------------+
        ^
        |
        +--------------------------+
                                 |
                        +--------------------+
                        |  ConcreteHandler2  |
                        +--------------------+
                        | + handleRequest()  |
                        +--------------------+
```

## Example: Support Request Handling System

Let’s implement a support request handling system using the Chain of Responsibility pattern. We’ll create different support levels (e.g., Level 1, Level 2, Level 3) that can process requests based on priority.

### Step 1: Define the Handler Interface

The `SupportHandler` interface defines methods for setting the next handler in the chain and handling the request.

```java
// Handler Interface
abstract class SupportHandler {
    protected SupportHandler nextHandler;

    public void setNext(SupportHandler nextHandler) {
        this.nextHandler = nextHandler;
    }

    public abstract void handleRequest(String request, int priority);
}
```

### Step 2: Implement Concrete Handlers

Each `SupportLevel` class represents a support level with specific permissions. If a request’s priority is within the handler’s threshold, it processes the request; otherwise, it forwards it to the next handler.

```java
// Concrete Handler for Level 1 Support
class Level1Support extends SupportHandler {
    @Override
    public void handleRequest(String request, int priority) {
        if (priority <= 1) {
            System.out.println("Level 1 Support: Handling request '" + request + "'");
        } else if (nextHandler != null) {
            nextHandler.handleRequest(request, priority);
        }
    }
}

// Concrete Handler for Level 2 Support
class Level2Support extends SupportHandler {
    @Override
    public void handleRequest(String request, int priority) {
        if (priority <= 2) {
            System.out.println("Level 2 Support: Handling request '" + request + "'");
        } else if (nextHandler != null) {
            nextHandler.handleRequest(request, priority);
        }
    }
}

// Concrete Handler for Level 3 Support
class Level3Support extends SupportHandler {
    @Override
    public void handleRequest(String request, int priority) {
        if (priority <= 3) {
            System.out.println("Level 3 Support: Handling request '" + request + "'");
        } else {
            System.out.println("Request '" + request + "' cannot be handled.");
        }
    }
}
```

### Step 3: Client Code Using the Chain of Responsibility

The client code creates a chain of support levels and submits requests to the first handler in the chain.

```java
public class Client {
    public static void main(String[] args) {
        // Create support levels
        SupportHandler level1 = new Level1Support();
        SupportHandler level2 = new Level2Support();
        SupportHandler level3 = new Level3Support();

        // Set up the chain of responsibility
        level1.setNext(level2);
        level2.setNext(level3);

        // Send requests with varying priorities
        System.out.println("Processing requests:");
        level1.handleRequest("Basic issue", 1);   // Handled by Level 1
        level1.handleRequest("Intermediate issue", 2);   // Handled by Level 2
        level1.handleRequest("Complex issue", 3);   // Handled by Level 3
        level1.handleRequest("Critical issue", 4);   // Cannot be handled
    }
}
```

### Output

```plaintext
Processing requests:
Level 1 Support: Handling request 'Basic issue'
Level 2 Support: Handling request 'Intermediate issue'
Level 3 Support: Handling request 'Complex issue'
Request 'Critical issue' cannot be handled.
```

In this example:

- `SupportHandler` is the handler interface that defines `handleRequest`.
- `Level1Support`, `Level2Support`, and `Level3Support` are concrete handlers that process requests based on priority.
- The client creates a chain by setting the `nextHandler` for each support level and submits requests to the first handler in the chain.

## Applicability

Use the Chain of Responsibility pattern when:

1. Multiple objects can handle a request, and the handler is determined dynamically.
2. You want to decouple the sender from the receiver by allowing more than one handler for a request.
3. You need to implement multiple handlers with similar interfaces or shared responsibilities.

## Advantages and Disadvantages

### Advantages

1. **Reduced Coupling**: Chain of Responsibility decouples the sender from the receiver, promoting a more flexible and scalable system.
2. **Dynamic Request Processing**: Handlers can be added, removed, or rearranged at runtime, enabling dynamic request processing.
3. **Single Responsibility Principle**: Each handler focuses on a specific responsibility, making the code easier to maintain and extend.

### Disadvantages

1. **Uncertain Request Handling**: There’s no guarantee that a request will be handled if it doesn’t match any handler in the chain.
2. **Potential Performance Overhead**: If the chain is long, a request may need to pass through multiple handlers, which can lead to performance overhead.
3. **Complexity with Long Chains**: Managing long chains or complex sequences of handlers can make debugging and tracking requests challenging.

## Best Practices for Implementing the Chain of Responsibility Pattern

1. **Ensure Chain Order**: The order of handlers in the chain can affect how requests are processed, so arrange handlers carefully.
2. **Use Null Object for End of Chain**: Consider using a null object to represent the end of the chain, eliminating the need for null checks.
3. **Avoid Long Chains**: Keep chains manageable, as long chains can lead to performance issues and complex code.

## Conclusion

The Chain of Responsibility pattern provides a flexible approach to handling requests, allowing multiple objects to process a request independently. This pattern is highly beneficial when multiple handlers could potentially handle a request, and it supports easy extension and modification by adding or rearranging handlers.
