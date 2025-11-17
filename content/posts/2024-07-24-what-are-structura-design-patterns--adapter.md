---
title: "Adapter Pattern"
draft: false
bookHidden: true
---

# Adapter Pattern

The **Adapter** pattern is a structural design pattern that enables objects with incompatible interfaces to work together. It acts as a bridge between two incompatible interfaces by converting the interface of a class into another interface that the client expects. This pattern is useful when integrating components that were not designed to work together.

## Intent

**The main intent of the Adapter pattern is to allow classes with incompatible interfaces to communicate by providing a wrapper that adapts one interface to another.** This pattern lets developers reuse existing code with new systems without modifying the original codebase.

## Problem and Solution

### Problem

Suppose you are building a payment processing system that needs to integrate with multiple third-party payment providers. Each provider has its own API with a unique set of methods and parameter structures. This incompatibility makes it difficult to switch between providers or support multiple providers simultaneously.

### Solution

The Adapter pattern addresses this by creating a common interface that the application can use for all payment providers. Each provider then has its own adapter that implements the common interface and translates calls to the third-party provider’s API.

## Structure

The Adapter pattern typically includes:

1. **Target Interface**: Defines the interface expected by the client.
2. **Adapter Class**: Implements the target interface and wraps an adaptee, translating calls from the target to the adaptee.
3. **Adaptee**: The class with an incompatible interface that needs to be adapted.

## UML Diagram

```
+--------------------+       +--------------------+
|   Target          |       |    Adaptee         |
|------------------- |       |--------------------|
| + request()       |       | + specificRequest()|
+--------------------+       +--------------------+
         ^                          ^
         |                          |
         +--------------------------+
                  Adapter
```

## Example: Payment Processing System

Let’s implement an example of integrating different payment providers using the Adapter pattern. We’ll create a common `PaymentProcessor` interface that each provider’s adapter will implement, allowing the application to interact with various payment providers in a uniform way.

### Step 1: Define the Target Interface

The `PaymentProcessor` interface defines the method that the client expects to use for processing payments.

```java
// Target Interface
interface PaymentProcessor {
    void processPayment(double amount);
}
```

### Step 2: Define the Adaptees

Each payment provider has its own interface, which is incompatible with the `PaymentProcessor` interface. Here are two example providers, `Stripe` and `PayPal`.

```java
// Adaptee 1: Stripe Payment API
class StripePayment {
    public void makeStripePayment(double amount) {
        System.out.println("Processing payment with Stripe: $" + amount);
    }
}

// Adaptee 2: PayPal Payment API
class PayPalPayment {
    public void sendPayment(double amount) {
        System.out.println("Processing payment with PayPal: $" + amount);
    }
}
```

### Step 3: Create Adapter Classes

The `StripeAdapter` and `PayPalAdapter` classes implement the `PaymentProcessor` interface, allowing the client to use these adapters interchangeably. Each adapter translates the `processPayment` call to the appropriate method in the adaptee.

```java
// Adapter for Stripe
class StripeAdapter implements PaymentProcessor {
    private StripePayment stripePayment;

    public StripeAdapter(StripePayment stripePayment) {
        this.stripePayment = stripePayment;
    }

    @Override
    public void processPayment(double amount) {
        stripePayment.makeStripePayment(amount);
    }
}

// Adapter for PayPal
class PayPalAdapter implements PaymentProcessor {
    private PayPalPayment payPalPayment;

    public PayPalAdapter(PayPalPayment payPalPayment) {
        this.payPalPayment = payPalPayment;
    }

    @Override
    public void processPayment(double amount) {
        payPalPayment.sendPayment(amount);
    }
}
```

### Step 4: Client Code Using the Adapter

The client code interacts with the `PaymentProcessor` interface, allowing it to process payments through different providers without being aware of their specific implementations.

```java
public class Client {
    public static void main(String[] args) {
        PaymentProcessor stripeProcessor = new StripeAdapter(new StripePayment());
        stripeProcessor.processPayment(50.0);  // Output: Processing payment with Stripe: $50.0

        PaymentProcessor payPalProcessor = new PayPalAdapter(new PayPalPayment());
        payPalProcessor.processPayment(75.0);  // Output: Processing payment with PayPal: $75.0
    }
}
```

### Explanation

In this example:

- The `PaymentProcessor` interface is the target interface that the client expects.
- Each adapter (`StripeAdapter` and `PayPalAdapter`) adapts the incompatible interfaces (`StripePayment` and `PayPalPayment`) to the `PaymentProcessor` interface.
- The client code can process payments using any payment provider without knowing the specific details of each provider’s API.

## Applicability

Use the Adapter pattern when:

1. You want to integrate classes with incompatible interfaces.
2. You need to reuse existing classes in a system that requires a specific interface.
3. You need to work with a third-party library or legacy system whose interface cannot be modified.

## Advantages and Disadvantages

### Advantages

1. **Increased Reusability**: Adapter allows existing classes to be reused in new contexts without modification.
2. **Decouples Code**: The client code is decoupled from specific implementations, making it easier to switch between different implementations.
3. **Improved Flexibility**: The pattern enables seamless integration of components that were not originally designed to work together.

### Disadvantages

1. **Increased Complexity**: The Adapter pattern introduces an additional layer, which can increase code complexity.
2. **Potential Overhead**: In some cases, adapting an interface may add slight performance overhead, especially if many adapters are involved.

## Best Practices for Implementing the Adapter Pattern

1. **Use Composition Over Inheritance**: Adapters are often implemented using composition (holding an instance of the adaptee) rather than inheritance, making them more flexible.
2. **Apply Adapter to External or Legacy Systems**: The Adapter pattern is particularly useful when dealing with third-party APIs or legacy code.
3. **Avoid Overusing**: If classes are already compatible or can be made compatible with minor modifications, consider simpler integration strategies instead.

## Conclusion

The Adapter pattern is a powerful way to bridge incompatible interfaces, allowing for more flexible and reusable code. By using adapters, you can integrate legacy or third-party code seamlessly into new systems, facilitating modularity and adaptability.
