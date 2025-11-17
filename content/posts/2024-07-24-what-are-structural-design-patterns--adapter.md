---
title: "Adapter Pattern"
date: 2024-07-24
categories:
  - Design Patterns
tags:
  - design patterns
  - structural patterns
  - adapter
  - integration
bookHidden: false
---

We run into adapters in real life all the time: power‑plug adapters, HDMI–to–USB‑C dongles, language interpreters. Software has the same problem — two sides that need to talk, but speak different “interfaces”.

The **Adapter** pattern is a structural design pattern that lets incompatible interfaces work together. It wraps one object and exposes a different interface that the client actually expects.

## Intent

Let classes with incompatible interfaces collaborate by inserting a small wrapper that translates one interface into another, so you can reuse existing code without changing it.

## Problem and Solution

### Problem

Suppose you’re building a payment system that needs to integrate with several third‑party providers. Each provider has its own API surface, naming, and quirks. Your app now has `makeStripePayment`, `sendPayment`, and a dozen other method names scattered everywhere.

Switching providers or supporting more than one becomes painful, and your core code ends up tightly coupled to vendor APIs.

### Solution

Define a clean `PaymentProcessor` interface that your application uses everywhere. For each provider, create an adapter that implements `PaymentProcessor` but internally delegates to the provider’s own API. The rest of the app only knows about `processPayment(amount)`.

## Structure

The Adapter pattern typically includes:

1. **Target Interface**: Defines the interface expected by the client.
2. **Adapter Class**: Implements the target interface and wraps an adaptee, translating calls from the target to the adaptee.
3. **Adaptee**: The class with an incompatible interface that needs to be adapted.

## UML Diagram

```text
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
