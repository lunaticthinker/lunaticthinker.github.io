---
title: "Proxy Pattern"
date: 2024-07-20
categories:
  - Design Patterns
tags:
  - design patterns
  - structural patterns
  - proxy
  - lazy loading
bookHidden: false
---

Any time you click something and **it looks like** the real object, but behind the scenes there’s access control, caching, logging, or lazy loading happening — that’s the **Proxy** pattern at work.

Proxy is a structural design pattern that provides a stand‑in (a proxy) for another object. The client talks to the proxy as if it were the real thing; the proxy decides when and how to forward calls to the real subject, and can add behavior around those calls.

## Intent

Control access to an object by acting as its stand‑in, so you can add behavior (lazy loading, caching, security, logging) **without** changing the original class or the client code.

## Problem and Solution

### Problem

Suppose you’re building an image viewer that displays high‑resolution images from disk or a remote server. If you eagerly load every image in full resolution, startup becomes slow and memory usage explodes.

You want the UI to feel snappy, but you also don’t want to rewrite your whole rendering code every time requirements change.

### Solution

Introduce an `ImageProxy` that implements the same interface as the real image. The proxy only loads the heavy `RealImage` the first time it’s actually needed (lazy loading), then forwards calls to it. The client just calls `display()` and doesn’t care whether it’s talking to the proxy or the real object.

## Structure

The Proxy pattern typically includes:

1. **Subject**: Defines the common interface for both the Real Subject and the Proxy.
2. **Real Subject**: The actual object that performs the work and to which access is controlled.
3. **Proxy**: Controls access to the Real Subject and may add additional functionality before or after forwarding requests to it.

## UML Diagram

```text
+------------------+     +------------------+
|     Subject      |<----|  RealSubject     |
|------------------|     |------------------|
| + request()      |     | + request()      |
+------------------+     +------------------+
        ^
        |
+------------------+
|      Proxy      |
|-----------------|
| + request()     |
+-----------------+
```

## Example: Image Viewer with Lazy Loading

Let’s implement an image viewer using the Proxy pattern. We’ll create an `ImageProxy` that controls access to the high-resolution `RealImage` object, loading it only when necessary.

### Step 1: Define the Subject Interface

The `Image` interface defines the `display` method that both the real image and the proxy must implement.

```java
// Subject Interface
interface Image {
    void display();
}
```

### Step 2: Implement the Real Subject

The `RealImage` class represents a high-resolution image that takes time and resources to load.

```java
// Real Subject
class RealImage implements Image {
    private String filename;

    public RealImage(String filename) {
        this.filename = filename;
        loadImageFromDisk();
    }

    private void loadImageFromDisk() {
        System.out.println("Loading image from disk: " + filename);
    }

    @Override
    public void display() {
        System.out.println("Displaying image: " + filename);
    }
}
```

### Step 3: Implement the Proxy

The `ImageProxy` class controls access to the `RealImage`, only loading it when the `display` method is called for the first time.

```java
// Proxy
class ImageProxy implements Image {
    private RealImage realImage;
    private String filename;

    public ImageProxy(String filename) {
        this.filename = filename;
    }

    @Override
    public void display() {
        if (realImage == null) {
            realImage = new RealImage(filename); // Load only when needed
        }
        realImage.display();
    }
}
```

### Step 4: Client Code Using the Proxy

The client interacts with `ImageProxy` just as it would with `RealImage`, without knowing if the image has been loaded yet.

```java
public class Client {
    public static void main(String[] args) {
        Image image1 = new ImageProxy("high_res_image1.jpg");
        Image image2 = new ImageProxy("high_res_image2.jpg");

        // The image is loaded only when display() is called for the first time
        System.out.println("Displaying images:");
        image1.display();  // Loads and displays high_res_image1.jpg
        image1.display();  // Displays high_res_image1.jpg without loading again
        image2.display();  // Loads and displays high_res_image2.jpg
    }
}
```

### Output

```plaintext
Displaying images:
Loading image from disk: high_res_image1.jpg
Displaying image: high_res_image1.jpg
Displaying image: high_res_image1.jpg
Loading image from disk: high_res_image2.jpg
Displaying image: high_res_image2.jpg
```

In this example:

- `RealImage` is the resource-intensive object that loads an image from disk.
- `ImageProxy` controls access to `RealImage`, only creating it when `display` is called for the first time (lazy loading).
- The client interacts with `ImageProxy`, which behaves like `RealImage` and loads the image only when necessary.

## Types of Proxy

The Proxy pattern can be implemented in different ways, depending on the additional functionality needed:

1. **Virtual Proxy**: Manages access to a resource-intensive object by creating it only when necessary (e.g., lazy loading).
2. **Remote Proxy**: Manages interaction with an object located on a remote server, handling communication details.
3. **Protection Proxy**: Controls access to an object by enforcing permissions or authentication checks.
4. **Cache Proxy**: Provides temporary storage to improve performance by caching responses from a resource-intensive or remote object.

## Applicability

Use the Proxy pattern when:

1. You need to control access to a resource-intensive or remote object.
2. You want to add additional functionality, such as lazy loading, caching, or access control, to an object without modifying it.
3. You want to separate concerns in your code, allowing a proxy to manage specific tasks independently of the real subject.

## Advantages and Disadvantages

### Advantages

1. **Controlled Access**: Proxy allows controlled access to the real subject, enhancing security, performance, or resource management.
2. **Lazy Initialization**: The pattern supports lazy loading, reducing resource usage by delaying object creation until necessary.
3. **Decoupling**: Proxy separates client code from specific functionalities (e.g., caching, loading), making the system more modular and maintainable.

### Disadvantages

1. **Increased Complexity**: Proxy introduces additional layers, which may increase code complexity.
2. **Potential Performance Overhead**: Depending on implementation, proxies can add some latency, especially if multiple layers are involved.
3. **May Lead to Over-Engineering**: Proxy should be used judiciously, as adding unnecessary proxies can lead to a complex and difficult-to-understand codebase.

## Best Practices for Implementing the Proxy Pattern

1. **Identify Core Functionality and Additional Concerns**: Use Proxy to separate additional concerns like security, caching, or logging from the main functionality.
2. **Use Lazy Loading and Caching Carefully**: Ensure that lazy loading and caching improve performance without introducing excessive delays or stale data.
3. **Keep Proxy Interface Consistent**: Maintain consistency between the Proxy and Real Subject interfaces to avoid confusion and unexpected behavior.

## Conclusion

The Proxy pattern provides a flexible way to control access to objects, allowing you to add functionality such as lazy loading, caching, or access control transparently. This pattern enhances modularity and performance in systems with resource-intensive, remote, or protected objects.
