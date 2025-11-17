---
title: "Memento Pattern"
draft: false
bookHidden: true
---

# Memento Pattern

The **Memento** pattern is a behavioral design pattern that allows an object to save and restore its state without exposing its internal structure. This pattern is particularly useful for implementing undo/redo functionality, as it captures an object’s state at a specific moment and allows it to be restored later.

## Intent

**The main intent of the Memento pattern is to capture and externalize an object’s internal state so that it can be restored later without violating encapsulation.** By storing snapshots of an object’s state, this pattern enables undo and redo operations, making it ideal for applications like text editors or graphical editors.

## Problem and Solution

### Problem

Imagine a text editor where users can type text and use the undo function to revert to a previous state. Without a way to store and restore the state of the editor, implementing an undo function would be difficult, requiring complex logic to track every change.

### Solution

The Memento pattern solves this problem by capturing snapshots (mementos) of the editor’s state at specific points in time. When the user performs an undo, the editor can restore a previous state from its saved mementos. This design keeps the internal details of the editor hidden from external objects, adhering to the principle of encapsulation.

## Structure

The Memento pattern typically includes:

1. **Originator**: The object whose state needs to be saved and restored.
2. **Memento**: A snapshot of the originator’s state, stored as an opaque object.
3. **Caretaker**: Responsible for storing and managing mementos without accessing their contents.

## UML Diagram

```
+-------------------+       +-------------------+
|    Originator     |       |    Memento        |
|-------------------|       |-------------------|
| - state           |       | - state           |
| + saveState()     |       |-------------------|
| + restoreState()  |       | + getState()      |
+-------------------+       +-------------------+
         ^
         |
+-------------------+
|    Caretaker      |
|-------------------|
| + addMemento()    |
| + getMemento()    |
+-------------------+
```

## Example: Text Editor with Undo Functionality

Let’s implement a simple text editor with undo functionality using the Memento pattern. The editor will save states after each edit and allow users to undo changes by restoring previous states.

### Step 1: Define the Memento Class

The `Memento` class holds a snapshot of the `TextEditor`’s state. This class is immutable, with no public methods to modify its contents.

```java
// Memento
class Memento {
    private final String state;

    public Memento(String state) {
        this.state = state;
    }

    public String getState() {
        return state;
    }
}
```

### Step 2: Implement the Originator

The `TextEditor` class acts as the originator, with methods to save and restore its state. It uses the `Memento` class to create snapshots and restore its state.

```java
// Originator
class TextEditor {
    private String content;

    public void setContent(String content) {
        this.content = content;
    }

    public String getContent() {
        return content;
    }

    public Memento saveState() {
        return new Memento(content);
    }

    public void restoreState(Memento memento) {
        this.content = memento.getState();
    }
}
```

### Step 3: Implement the Caretaker

The `History` class acts as the caretaker, storing a list of mementos and managing the undo functionality. It doesn’t interact with the internal state of `Memento` or `TextEditor`.

```java
// Caretaker
class History {
    private List<Memento> mementos = new ArrayList<>();

    public void addMemento(Memento memento) {
        mementos.add(memento);
    }

    public Memento getMemento(int index) {
        return mementos.get(index);
    }

    public Memento getLastMemento() {
        if (mementos.isEmpty()) return null;
        return mementos.remove(mementos.size() - 1);
    }
}
```

### Step 4: Client Code Using the Memento Pattern

The client code demonstrates setting content, saving states, and undoing changes by restoring previous states from the history.

```java
public class Client {
    public static void main(String[] args) {
        TextEditor editor = new TextEditor();
        History history = new History();

        // Set initial content and save state
        editor.setContent("Hello");
        history.addMemento(editor.saveState());

        // Modify content and save state
        editor.setContent("Hello, World!");
        history.addMemento(editor.saveState());

        // Modify content again without saving
        editor.setContent("Hello, World! How are you?");

        System.out.println("Current content: " + editor.getContent()); // Output: Hello, World! How are you?

        // Undo changes by restoring last saved state
        editor.restoreState(history.getLastMemento());
        System.out.println("After undo: " + editor.getContent()); // Output: Hello, World!

        // Undo to previous saved state
        editor.restoreState(history.getLastMemento());
        System.out.println("After another undo: " + editor.getContent()); // Output: Hello
    }
}
```

### Output

```plaintext
Current content: Hello, World! How are you?
After undo: Hello, World!
After another undo: Hello
```

In this example:

- `TextEditor` is the originator, capable of saving and restoring its state through mementos.
- `Memento` stores the state of `TextEditor` as an immutable snapshot.
- `History` acts as the caretaker, managing the list of mementos and enabling undo functionality by providing previous states when needed.

## Applicability

Use the Memento pattern when:

1. You want to provide undo or rollback functionality without exposing the internal structure of the object.
2. You need to save snapshots of an object’s state, but the object’s internal details should remain hidden from other objects.
3. The state to be saved is complex or changes frequently, making a centralized snapshot mechanism beneficial.

## Advantages and Disadvantages

### Advantages

1. **Encapsulation of State**: Memento captures and stores an object’s state while keeping it private and hidden from other objects.
2. **Supports Undo Functionality**: The pattern provides a simple way to implement undo/redo features by storing previous states.
3. **Decouples State Management**: By externalizing the saved state, Memento separates state management from the object’s main logic, keeping the code clean and organized.

### Disadvantages

1. **Memory Usage**: Storing multiple states can consume significant memory, especially for large objects or frequent snapshots.
2. **Increased Complexity**: The Memento pattern introduces additional classes (memento and caretaker), which can add complexity to the system.
3. **Potential Privacy Issues**: If the caretaker has too much access to mementos, it may lead to unintended exposure of an object’s state.

## Best Practices for Implementing the Memento Pattern

1. **Limit Memento Access**: Keep mementos immutable and avoid giving the caretaker or other objects direct access to internal state.
2. **Manage Memory Usage Carefully**: Be mindful of the memory impact when saving multiple mementos, and consider limiting the number of saved states.
3. **Use with Complex State Changes**: Apply this pattern when dealing with complex or frequently changing states that benefit from snapshot-based management.

## Conclusion

The Memento pattern provides an effective way to save and restore an object’s state, enabling functionality like undo/redo without compromising encapsulation. By externalizing snapshots, the Memento pattern allows flexible state management while preserving the internal details of the originator.
