---
title: "Observer Pattern"
date: 2024-07-16
categories:
  - Design Patterns
tags:
  - design patterns
  - behavioral patterns
  - observer
  - events
bookHidden: false
---

Any time you subscribe to something — a newsletter, a Twitch stream, a weather app — you’re living in the world of the **Observer** pattern.

Observer is a behavioral design pattern that defines a one‑to‑many relationship between objects so that when one object’s state changes, all dependent objects are notified automatically. It’s the backbone of event systems, GUIs, and many reactive APIs.

## Intent

Establish a clean relationship where changes to one object (the **subject**) automatically propagate to many **observers** — without the subject hard‑coding who those observers are. Everyone interested gets notified; no one is tightly coupled.

## Problem and Solution

### Problem

Suppose you’re building a weather station system that gathers data and shows it on phones, tablets, TVs, maybe even a wall display. Without a proper mechanism, each device would have to constantly poll the station for updates, or the station would need hard‑coded references to every device.

Both approaches are ugly: either you burn CPU on polling, or you create tight coupling and brittle dependencies.

### Solution

With Observer, the `WeatherStation` acts as the subject and each device becomes an observer. Devices subscribe once; when the station updates, it simply notifies all registered observers. You can add or remove observers at runtime without changing the station’s code.

## Structure

The Observer pattern typically includes:

1. **Subject**: Maintains a list of observers and provides methods for attaching, detaching, and notifying observers.
2. **Observer Interface**: Defines the update method that all observers must implement.
3. **Concrete Observer**: Implements the observer interface and responds to updates from the subject.

## UML Diagram

```text
+------------------+       +-------------------+
|    Subject       |       |    Observer       |
|------------------|       |-------------------|
| + attach()       |       | + update()        |
| + detach()       |       +-------------------+
| + notify()       |                ^
+------------------+                |
         ^                          |
         |                          |
+------------------+       +----------------------+
| ConcreteSubject  |       |  ConcreteObserver    |
|------------------|       +----------------------+
| - state          |       | + update()           |
+------------------+       +----------------------+
```

## Example: Weather Station and Devices

Let’s implement a weather station system using the Observer pattern. The `WeatherStation` is the subject that maintains weather data and notifies devices (observers) when the data changes.

### Step 1: Define the Observer Interface

The `Observer` interface defines the `update` method, which all observers must implement to receive updates.

```java
// Observer Interface
interface Observer {
    void update(float temperature, float humidity);
}
```

### Step 2: Implement the Subject

The `WeatherStation` class acts as the subject. It maintains a list of observers and notifies them when the weather data changes.

```java
// Subject
class WeatherStation {
    private List<Observer> observers = new ArrayList<>();
    private float temperature;
    private float humidity;

    public void attach(Observer observer) {
        observers.add(observer);
    }

    public void detach(Observer observer) {
        observers.remove(observer);
    }

    public void setWeatherData(float temperature, float humidity) {
        this.temperature = temperature;
        this.humidity = humidity;
        notifyObservers();
    }

    private void notifyObservers() {
        for (Observer observer : observers) {
            observer.update(temperature, humidity);
        }
    }
}
```

### Step 3: Implement Concrete Observers

Each device (e.g., `PhoneDisplay`, `TVDisplay`) acts as a concrete observer and implements the `update` method to respond to changes in weather data.

```java
// Concrete Observer for Phone Display
class PhoneDisplay implements Observer {
    @Override
    public void update(float temperature, float humidity) {
        System.out.println("Phone Display: Temperature = " + temperature + ", Humidity = " + humidity);
    }
}

// Concrete Observer for TV Display
class TVDisplay implements Observer {
    @Override
    public void update(float temperature, float humidity) {
        System.out.println("TV Display: Temperature = " + temperature + ", Humidity = " + humidity);
    }
}
```

### Step 4: Client Code Using the Observer Pattern

The client code creates a weather station and attaches various displays to it. When the weather data changes, all displays receive the update.

```java
public class Client {
    public static void main(String[] args) {
        WeatherStation weatherStation = new WeatherStation();

        Observer phoneDisplay = new PhoneDisplay();
        Observer tvDisplay = new TVDisplay();

        // Attach observers to the weather station
        weatherStation.attach(phoneDisplay);
        weatherStation.attach(tvDisplay);

        // Update weather data
        weatherStation.setWeatherData(25.0f, 65.0f);
        weatherStation.setWeatherData(27.0f, 70.0f);
    }
}
```

### Output

```plaintext
Phone Display: Temperature = 25.0, Humidity = 65.0
TV Display: Temperature = 25.0, Humidity = 65.0
Phone Display: Temperature = 27.0, Humidity = 70.0
TV Display: Temperature = 27.0, Humidity = 70.0
```

In this example:

- `WeatherStation` is the subject that maintains weather data and notifies observers.
- `PhoneDisplay` and `TVDisplay` are observers that respond to changes in the weather data by implementing the `update` method.
- The client code attaches observers to the weather station, allowing them to receive updates whenever the weather data changes.

## Applicability

Use the Observer pattern when:

1. An object needs to notify other objects without making assumptions about who or what those objects are.
2. There is a need to create a one-to-many dependency between objects, so that changes in one object are automatically propagated to others.
3. The set of objects that depend on the subject changes dynamically, and you want to allow for flexible addition or removal of observers.

## Advantages and Disadvantages

### Advantages

1. **Loose Coupling**: The Observer pattern promotes loose coupling by decoupling subjects from their observers, allowing them to vary independently.
2. **Easy Addition/Removal of Observers**: Observers can be added or removed dynamically at runtime, providing flexibility in managing dependencies.
3. **Supports Event-Driven Architecture**: This pattern is well-suited for event-driven systems, allowing objects to respond to changes in other objects automatically.

### Disadvantages

1. **Potential Memory Leaks**: Observers that are not detached may lead to memory leaks if they are no longer needed but still hold references to the subject.
2. **Unpredictable Execution Order**: The order in which observers are notified is not guaranteed, which may lead to unexpected behavior in certain cases.
3. **Performance Overhead**: If there are many observers or frequent notifications, the Observer pattern may introduce performance overhead.

## Best Practices for Implementing the Observer Pattern

1. **Use Weak References to Avoid Memory Leaks**: Consider using weak references or other techniques to avoid memory leaks when observers are no longer needed.
2. **Notify Observers Asynchronously if Necessary**: If notifications may take time, consider notifying observers asynchronously to avoid blocking the main execution.
3. **Provide Detachment Mechanisms**: Ensure that observers can be easily detached to allow for flexible management of observer lifecycles.

## Conclusion

The Observer pattern provides a structured way to handle one-to-many dependencies, allowing objects to subscribe to changes in other objects without tightly coupling them. This pattern is essential for building flexible, decoupled systems where events need to be propagated to multiple components.
