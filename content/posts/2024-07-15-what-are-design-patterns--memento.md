---
title: "Memento Pattern"
date: 2024-07-15
categories:
  - Design Patterns
tags:
  - design patterns
  - behavioral patterns
  - memento
  - undo
bookHidden: false
---

Sometimes you just want to hit undo and pretend the last few minutes never happened — in your editor, not in life (unfortunately). That’s exactly the kind of problem the **Memento** pattern is designed to solve.

Memento is a behavioral design pattern that lets an object save and later restore its internal state without exposing how it works inside. It’s the pattern behind familiar features like undo/redo, snapshots, checkpoints, and “restore previous version”.

## Intent

Capture and externalize an object’s internal state so that it can be restored later **without breaking encapsulation**. Instead of sprinkling custom undo logic everywhere, you take snapshots of state and roll back to them when needed.

## Problem and Solution

### Problem

Imagine a text editor where users can type freely and then undo changes. Without a clean way to store and restore state, you’d end up tracking every tiny modification, or worse, hard‑coding “undo” logic into every operation. It quickly becomes a mess.

### Solution

With Memento, the editor simply takes snapshots (mementos) of its state at meaningful points in time. When the user hits undo, the editor restores a previous snapshot. The rest of the system never needs to know what “state” means for the editor — it just stores and passes around opaque memento objects.

## Structure

The Memento pattern typically includes:

1. **Originator**: The object whose state needs to be saved and restored.
2. **Memento**: A snapshot of the originator’s state, stored as an opaque object.
3. **Caretaker**: Responsible for storing and managing mementos without accessing their contents.

## UML Diagram

```text
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

## Example: Text Editor with Undo

Let’s walk through a simple text editor with undo functionality using Memento. The editor saves its content after each important edit and can roll back to previous versions.

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
