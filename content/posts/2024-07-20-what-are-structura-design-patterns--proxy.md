---
title: "Proxy Pattern"
draft: false
bookHidden: true
---

# Proxy Pattern

The **Proxy** pattern is a structural design pattern that provides a surrogate or placeholder for another object. By controlling access to the underlying object, the Proxy pattern allows additional functionality, such as lazy initialization, access control, logging, or caching, to be added without modifying the original object.

## Intent

**The main intent of the Proxy pattern is to control access to an object by acting as a stand-in for it, allowing additional functionality to be added transparently.** This pattern is particularly useful when working with resource-intensive objects, objects that need controlled access, or objects that need enhanced functionality.

## Problem and Solution

### Problem

Suppose you’re building an image viewer that can display high-resolution images from a remote server. Loading every image in full resolution at once can be slow and resource-intensive. Without a mechanism to manage the loading process, the application might become sluggish or unresponsive.

### Solution

The Proxy pattern can address this by creating an `ImageProxy` class that stands in for the actual image. The `ImageProxy` can handle loading the image only when it’s actually needed (lazy loading), making the application more responsive. Once loaded, the proxy forwards requests to the real image, making the process seamless to the client.

## Structure

The Proxy pattern typically includes:

1. **Subject**: Defines the common interface for both the Real Subject and the Proxy.
2. **Real Subject**: The actual object that performs the work and to which access is controlled.
3. **Proxy**: Controls access to the Real Subject and may add additional functionality before or after forwarding requests to it.

## UML Diagram

```
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
