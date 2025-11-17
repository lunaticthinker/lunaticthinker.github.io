---
title: "Strategy Pattern"
date: 2024-07-18
categories:
    - Design Patterns
tags:
    - design patterns
    - behavioral patterns
    - strategy
    - algorithms
bookHidden: false
---

Any time you choose between “pay with card”, “pay with PayPal”, or “pay with bank transfer”, you’re bumping into the idea behind the **Strategy** pattern.

Strategy is a behavioral design pattern that lets you define a family of algorithms, encapsulate each one, and switch between them at runtime. The client cares about *what* needs to be done, not *how* each algorithm does it.

## Intent

Enable selecting an algorithm’s behavior at runtime so algorithms can vary independently from the context that uses them. You can add, remove, or swap strategies without editing the code that triggers them.

## Problem and Solution

### Problem

Consider an application that processes payments. Different payment methods — credit card, PayPal, bank transfer — all have slightly different rules and data.

If you put everything into one class with a bunch of `if (type == CREDIT_CARD) ... else if (type == PAYPAL) ...`, the code becomes harder to read, harder to extend, and easy to break.

### Solution

With Strategy, each payment method lives in its own class that implements a shared `PaymentStrategy` interface. The `PaymentProcessor` just holds a reference to a strategy and calls it. Adding a new payment method becomes “add a new class” instead of “edit a big conditional in multiple places”.

## Structure

The Strategy pattern typically includes:

1. **Strategy Interface**: Declares the method(s) that all concrete strategies must implement.
2. **Concrete Strategies**: Implement specific algorithms as classes that conform to the strategy interface.
3. **Context**: Maintains a reference to a strategy and delegates tasks to it, allowing the strategy to be changed at runtime.

## UML Diagram

```text
+------------------+       +----------------------+
|    Context       |       |      Strategy        |
|------------------|       |----------------------|
| - strategy       |       | + executeAlgorithm() |
| + setStrategy()  |       +----------------------+
| + execute()      |                ^
+------------------+                |
         |                          |
         |            +------------------------+
         +----------->|   ConcreteStrategyA    |
                      |------------------------|
                      | + executeAlgorithm()   |
                      +------------------------+
```

## Example: Payment Processing System

Let’s implement a payment processing system using the Strategy pattern. Each payment method (e.g., credit card, PayPal, bank transfer) is encapsulated as a separate strategy.

### Step 1: Define the Strategy Interface

The `PaymentStrategy` interface declares the `pay` method that all concrete strategies must implement.

```java
// Strategy Interface
interface PaymentStrategy {
    void pay(double amount);
}
```

### Step 2: Implement Concrete Strategies

Each payment method is implemented as a concrete strategy, defining its specific behavior for the `pay` method.

```java
// Concrete Strategy for Credit Card Payment
class CreditCardPayment implements PaymentStrategy {
    private String cardNumber;

    public CreditCardPayment(String cardNumber) {
        this.cardNumber = cardNumber;
    }

    @Override
    public void pay(double amount) {
        System.out.println("Processing credit card payment of $" + amount + " with card " + cardNumber);
    }
}

// Concrete Strategy for PayPal Payment
class PayPalPayment implements PaymentStrategy {
    private String email;

    public PayPalPayment(String email) {
        this.email = email;
    }

    @Override
    public void pay(double amount) {
        System.out.println("Processing PayPal payment of $" + amount + " for account " + email);
    }
}

// Concrete Strategy for Bank Transfer Payment
class BankTransferPayment implements PaymentStrategy {
    private String bankAccount;

    public BankTransferPayment(String bankAccount) {
        this.bankAccount = bankAccount;
    }

    @Override
    public void pay(double amount) {
        System.out.println("Processing bank transfer of $" + amount + " to account " + bankAccount);
    }
}
```

### Step 3: Implement the Context

The `PaymentProcessor` class is the context that maintains a reference to a `PaymentStrategy` and delegates the `pay` action to it. This allows the client to choose a payment strategy dynamically.

```java
// Context
class PaymentProcessor {
    private PaymentStrategy paymentStrategy;

    public void setPaymentStrategy(PaymentStrategy paymentStrategy) {
        this.paymentStrategy = paymentStrategy;
    }

    public void processPayment(double amount) {
        if (paymentStrategy == null) {
            throw new IllegalStateException("Payment strategy not set");
        }
        paymentStrategy.pay(amount);
    }
}
```

### Step 4: Client Code Using the Strategy Pattern

The client code chooses a payment strategy and processes a payment, allowing for dynamic selection and switching of strategies.

```java
public class Client {
    public static void main(String[] args) {
        PaymentProcessor processor = new PaymentProcessor();

        // Use Credit Card payment strategy
        processor.setPaymentStrategy(new CreditCardPayment("1234-5678-9012-3456"));
        processor.processPayment(100.0);

        // Switch to PayPal payment strategy
        processor.setPaymentStrategy(new PayPalPayment("user@example.com"));
        processor.processPayment(50.0);

        // Switch to Bank Transfer payment strategy
        processor.setPaymentStrategy(new BankTransferPayment("987654321"));
        processor.processPayment(200.0);
    }
}
```

### Output

```plaintext
Processing credit card payment of $100.0 with card 1234-5678-9012-3456
Processing PayPal payment of $50.0 for account user@example.com
Processing bank transfer of $200.0 to account 987654321
```

In this example:

- `PaymentProcessor` is the context that delegates payment processing to a `PaymentStrategy`.
- `CreditCardPayment`, `PayPalPayment`, and `BankTransferPayment` are concrete strategies, each implementing a specific payment method.
- The client code selects and switches payment strategies dynamically, allowing flexible control over the payment process.

## Applicability

Use the Strategy pattern when:

1. You need multiple variations of an algorithm, and they should be interchangeable.
2. The behavior of a class varies based on some parameter, and you want to avoid complex conditionals.
3. You want to enable clients to dynamically choose from a set of algorithms at runtime.

## Advantages and Disadvantages

### Advantages

1. **Promotes Open-Closed Principle**: New strategies can be added without modifying the existing context, making the code extensible and maintainable.
2. **Eliminates Conditional Logic**: The pattern reduces the need for conditional statements by encapsulating algorithms in separate classes.
3. **Easily Interchangeable Algorithms**: Strategies can be swapped dynamically, providing flexible control over behavior.

### Disadvantages

1. **Increased Number of Classes**: The Strategy pattern requires creating a separate class for each algorithm, which can lead to more classes in the codebase.
2. **Context Awareness**: The context must be aware of available strategies, requiring clients to understand the strategies and choose appropriately.
3. **Potential Overhead**: In some cases, the added flexibility of strategies may introduce overhead, especially if the strategies are simple and rarely change.

## Best Practices for Implementing the Strategy Pattern

1. **Choose the Pattern for Complex Algorithms**: The Strategy pattern is most beneficial for complex algorithms that are likely to vary. Avoid using it for simple behaviors.
2. **Encapsulate Variants Carefully**: Ensure that each strategy encapsulates a specific behavior or algorithm to maintain modularity and simplicity.
3. **Provide a Default Strategy**: In some cases, consider providing a default strategy to handle cases where the client does not specify one.

## Conclusion

The Strategy pattern provides a clean way to define and swap algorithms dynamically, allowing clients to choose behavior at runtime. By encapsulating each algorithm in its own class, the Strategy pattern promotes flexible, reusable code that adheres to the Open-Closed Principle.
