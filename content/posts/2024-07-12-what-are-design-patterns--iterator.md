---
title: "Iterator Pattern"
draft: false
bookHidden: true
---

# Iterator Pattern

The **Iterator** pattern is a behavioral design pattern that provides a way to access the elements of a collection sequentially without exposing the collection's underlying structure. The Iterator pattern decouples the traversal logic from the collection itself, making it easier to use and extend.

## Intent

**The main intent of the Iterator pattern is to allow sequential access to elements in a collection without exposing its internal structure.** This pattern provides a standard interface for iterating through a collection, enabling different traversal strategies and making collections interchangeable.

## Problem and Solution

### Problem

Suppose you have a complex data structure, such as a custom list or tree. You want to provide a way for clients to access elements in this structure sequentially, but exposing the internal details of the collection would lead to a tightly coupled and inflexible design.

### Solution

The Iterator pattern addresses this by creating a separate iterator object that can traverse the collection. The iterator knows how to navigate the collection and provides methods for accessing elements sequentially, making it easy for the client to interact with the collection without knowing its structure.

## Structure

The Iterator pattern typically includes:

1. **Iterator Interface**: Defines the methods for traversing a collection, such as `next` and `hasNext`.
2. **Concrete Iterator**: Implements the iterator interface, providing the logic for traversing a specific collection.
3. **Aggregate (Collection) Interface**: Defines the method for creating an iterator.
4. **Concrete Aggregate (Concrete Collection)**: Implements the collection interface and returns an iterator for the specific collection.

## UML Diagram

```
+-------------------+           +-------------------------+
|      Iterator     |<----------|       ConcreteIterator  |
|-------------------|           +-------------------------+
| + hasNext()       |           | + hasNext()            |
| + next()          |           | + next()               |
+-------------------+           +-------------------------+
         ^
         |
+-------------------+           +-------------------------+
|    Collection     |<----------|   ConcreteCollection   |
|-------------------|           +-------------------------+
| + createIterator()|           | + createIterator()     |
+-------------------+           +-------------------------+
```

## Example: Custom Collection with Iterator

Let’s implement a custom collection of numbers using the Iterator pattern. We’ll create an `IntegerCollection` with a `NumberIterator` to allow sequential access to the numbers.

### Step 1: Define the Iterator Interface

The `Iterator` interface defines methods for traversal: `hasNext` to check if there are more elements and `next` to retrieve the next element.

```java
// Iterator Interface
interface Iterator<T> {
    boolean hasNext();
    T next();
}
```

### Step 2: Implement the Concrete Iterator

The `NumberIterator` class implements the `Iterator` interface to traverse an `IntegerCollection`.

```java
// Concrete Iterator
class NumberIterator implements Iterator<Integer> {
    private IntegerCollection collection;
    private int position = 0;

    public NumberIterator(IntegerCollection collection) {
        this.collection = collection;
    }

    @Override
    public boolean hasNext() {
        return position < collection.size();
    }

    @Override
    public Integer next() {
        return hasNext() ? collection.get(position++) : null;
    }
}
```

### Step 3: Define the Collection Interface

The `Collection` interface defines a method for creating an iterator, allowing clients to retrieve an iterator for traversing the collection.

```java
// Collection Interface
interface Collection<T> {
    Iterator<T> createIterator();
}
```

### Step 4: Implement the Concrete Collection

The `IntegerCollection` class implements the `Collection` interface, storing integers and returning an iterator for traversal.

```java
// Concrete Collection
class IntegerCollection implements Collection<Integer> {
    private List<Integer> numbers = new ArrayList<>();

    public void add(Integer number) {
        numbers.add(number);
    }

    public Integer get(int index) {
        return numbers.get(index);
    }

    public int size() {
        return numbers.size();
    }

    @Override
    public Iterator<Integer> createIterator() {
        return new NumberIterator(this);
    }
}
```

### Step 5: Client Code Using the Iterator

The client code uses the iterator provided by `IntegerCollection` to access elements sequentially without knowing the collection’s internal structure.

```java
public class Client {
    public static void main(String[] args) {
        IntegerCollection collection = new IntegerCollection();
        collection.add(1);
        collection.add(2);
        collection.add(3);

        Iterator<Integer> iterator = collection.createIterator();

        System.out.println("Iterating through the collection:");
        while (iterator.hasNext()) {
            System.out.println(iterator.next());
        }
    }
}
```

### Output

```plaintext
Iterating through the collection:
1
2
3
```

In this example:

- The `IntegerCollection` class provides the `createIterator` method, allowing the client to obtain a `NumberIterator`.
- The `NumberIterator` traverses the `IntegerCollection` sequentially, implementing the `hasNext` and `next` methods.
- The client code iterates through the collection without knowing its internal structure, relying solely on the iterator.

## Applicability

Use the Iterator pattern when:

1. You need to traverse a collection without exposing its underlying representation.
2. You want to support different types of traversals (e.g., forward, backward) for a collection.
3. You need to provide a uniform interface for traversing different types of collections.

## Advantages and Disadvantages

### Advantages

1. **Encapsulation of Traversal Logic**: The Iterator pattern encapsulates the traversal logic, allowing the collection’s structure to remain hidden from the client.
2. **Simplifies Collection Interaction**: The pattern provides a standard interface for iterating over collections, making it easier to interact with complex data structures.
3. **Supports Multiple Iterations**: Multiple iterators can be created for the same collection, enabling multiple independent traversals.

### Disadvantages

1. **Increased Complexity**: The pattern introduces additional classes (e.g., iterators), which can add complexity, especially for simple collections.
2. **Potential for Concurrent Modification Issues**: Iterators may encounter issues if the collection is modified during iteration, requiring additional safeguards or implementations for concurrent modification handling.

## Best Practices for Implementing the Iterator Pattern

1. **Use the Iterator Pattern for Complex Collections**: Apply this pattern when collections have complex structures or traversal requirements. For simpler collections, native iteration mechanisms may suffice.
2. **Provide Clear Traversal Methods**: Ensure that `hasNext` and `next` methods are intuitive and handle edge cases (e.g., reaching the end of the collection) gracefully.
3. **Handle Concurrent Modifications Carefully**: If the collection might be modified during iteration, implement safeguards like fail-fast or fail-safe iterators.

## Conclusion

The Iterator pattern provides a flexible way to access elements in a collection sequentially without exposing its underlying structure. This pattern enables uniform traversal methods, supporting complex or custom collections while keeping the client code simple and decoupled from collection details.
