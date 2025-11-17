---
title: "Mediator Pattern"
draft: false
bookHidden: true
---

# Mediator Pattern

The **Mediator** pattern is a behavioral design pattern that promotes loose coupling between objects by encapsulating their communication within a mediator. The mediator centralizes interactions between objects, making them easier to modify and reuse independently.

## Intent

**The main intent of the Mediator pattern is to reduce dependencies between communicating objects by introducing a mediator that handles their interactions.** This pattern is especially useful in scenarios where multiple objects need to communicate, and direct coupling would create a complex web of dependencies.

## Problem and Solution

### Problem

Suppose you’re designing a chat application where multiple users can send messages to each other. Without a centralized way to manage communication, each user would need to be aware of all other users, resulting in tightly coupled code that is difficult to maintain and extend. Adding new users or changing communication behavior would require modifying all related classes.

### Solution

The Mediator pattern solves this problem by creating a mediator object (e.g., `ChatRoom`) that manages the communication between users. Each user communicates only with the mediator, which then relays messages to the appropriate recipients. This setup decouples users from each other, making the system easier to maintain, modify, and extend.

## Structure

The Mediator pattern typically includes:

1. **Mediator Interface**: Defines methods for communication between colleagues.
2. **Concrete Mediator**: Implements the mediator interface, coordinating interactions between colleagues.
3. **Colleague Interface**: Defines a common interface for all participants that communicate through the mediator.
4. **Concrete Colleagues**: Implement the colleague interface and interact with each other through the mediator.

## UML Diagram

```
+-------------------+          +-----------------------+
|    Mediator       |<---------|   ConcreteMediator    |
|-------------------|          |-----------------------|
| + sendMessage()   |          | + sendMessage()       |
+-------------------+          +-----------------------+
         ^
         |
+-------------------+          +-----------------------+
|   Colleague       |<---------|   ConcreteColleague   |
|-------------------|          |-----------------------|
| + send()          |          | + send()             |
| + receive()       |          | + receive()          |
+-------------------+          +-----------------------+
```

## Example: Chat Application

Let’s implement a simple chat application using the Mediator pattern. We’ll create a `ChatRoom` mediator to handle communication between users, allowing them to send messages to each other without being directly aware of one another.

### Step 1: Define the Mediator Interface

The `ChatMediator` interface defines a method for sending messages. The mediator will coordinate message delivery between users.

```java
// Mediator Interface
interface ChatMediator {
    void sendMessage(String message, User user);
}
```

### Step 2: Implement the Concrete Mediator

The `ChatRoom` class implements the `ChatMediator` interface, managing a list of users and relaying messages between them.

```java
// Concrete Mediator
class ChatRoom implements ChatMediator {
    private List<User> users = new ArrayList<>();

    public void addUser(User user) {
        users.add(user);
    }

    @Override
    public void sendMessage(String message, User user) {
        for (User u : users) {
            if (u != user) {
                u.receive(message);
            }
        }
    }
}
```

### Step 3: Define the Colleague Interface

The `User` class represents a participant in the chat. Each user has methods to send and receive messages and interacts with others through the `ChatRoom`.

```java
// Colleague Interface
abstract class User {
    protected ChatMediator mediator;
    protected String name;

    public User(ChatMediator mediator, String name) {
        this.mediator = mediator;
        this.name = name;
    }

    public abstract void send(String message);
    public abstract void receive(String message);
}
```

### Step 4: Implement Concrete Colleagues

Each `ConcreteUser` class represents a specific user in the chat and interacts only through the mediator.

```java
// Concrete Colleague
class ConcreteUser extends User {
    public ConcreteUser(ChatMediator mediator, String name) {
        super(mediator, name);
    }

    @Override
    public void send(String message) {
        System.out.println(this.name + " sends: " + message);
        mediator.sendMessage(message, this);
    }

    @Override
    public void receive(String message) {
        System.out.println(this.name + " received: " + message);
    }
}
```

### Step 5: Client Code Using the Mediator

The client code creates users and a chat room, adding users to the chat room and allowing them to send messages.

```java
public class Client {
    public static void main(String[] args) {
        ChatMediator chatRoom = new ChatRoom();

        User user1 = new ConcreteUser(chatRoom, "Alice");
        User user2 = new ConcreteUser(chatRoom, "Bob");
        User user3 = new ConcreteUser(chatRoom, "Charlie");

        ((ChatRoom) chatRoom).addUser(user1);
        ((ChatRoom) chatRoom).addUser(user2);
        ((ChatRoom) chatRoom).addUser(user3);

        user1.send("Hello, everyone!");
        user2.send("Hi, Alice!");
    }
}
```

### Output

```plaintext
Alice sends: Hello, everyone!
Bob received: Hello, everyone!
Charlie received: Hello, everyone!
Bob sends: Hi, Alice!
Alice received: Hi, Alice!
Charlie received: Hi, Alice!
```

In this example:

- The `ChatRoom` mediator handles communication between users, with each user sending and receiving messages only through the mediator.
- `ConcreteUser` represents a user in the chat, sending and receiving messages through the `ChatRoom`.
- The client code interacts with the users through the mediator, which manages all message delivery.

## Applicability

Use the Mediator pattern when:

1. You need to reduce coupling between multiple classes that communicate with each other.
2. You want to simplify complex communication patterns or workflows by centralizing interactions.
3. You need flexibility to modify communication between objects without modifying the objects themselves.

## Advantages and Disadvantages

### Advantages

1. **Reduces Coupling**: The Mediator pattern reduces direct dependencies between objects, promoting loose coupling and improving maintainability.
2. **Centralized Control**: By managing interactions in one place, the mediator simplifies complex communication and makes it easier to understand and modify.
3. **Enhanced Flexibility**: New colleagues can be added or removed easily, and communication behavior can be changed by modifying the mediator.

### Disadvantages

1. **Increased Complexity in the Mediator**: As more communication logic is centralized, the mediator can become complex, potentially turning into a “god object.”
2. **Potential Performance Bottleneck**: Since all interactions go through the mediator, it can become a performance bottleneck, especially in high-traffic scenarios.

## Best Practices for Implementing the Mediator Pattern

1. **Limit Mediator Complexity**: Avoid turning the mediator into an overly complex object. If the mediator becomes too complex, consider splitting its responsibilities.
2. **Use Mediator to Manage High Interdependencies**: Apply the Mediator pattern in systems where multiple objects interact frequently, as it simplifies managing these dependencies.
3. **Encapsulate Communication Patterns**: Use the mediator to encapsulate communication patterns, making it easier to modify behavior without affecting the colleagues.

## Conclusion

The Mediator pattern provides a centralized way to manage communication between objects, reducing coupling and making the system easier to extend and maintain. By isolating communication logic, the Mediator pattern enhances flexibility and scalability in complex systems.
