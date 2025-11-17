---
title: "Command Pattern"
draft: false
bookHidden: true
---

---

title: "Command Pattern"
date: 2024-07-11
categories: - Design Patterns
tags: - design patterns - behavioral patterns - command - architecture
bookHidden: false

---

The **Command** pattern is what you use when you want to treat a user action or operation as a first‑class object—something you can queue, log, undo, or replay later.

It’s a behavioral pattern that wraps a request (what to do, with which arguments, against which receiver) into a stand‑alone object. Once the action is packaged this way, it becomes easy to schedule, buffer, or reverse without hard‑wiring everything into a single method call.

## Problem and Solution

### Problem

Suppose you’re building a text editor that supports various operations, such as writing text, deleting text, and copying text. If you want to implement features like undo, redo, or macro recording, handling these actions directly in the client code can become complex and rigid, especially when operations are dependent on previous states.

### Solution

The Command pattern addresses this by creating command objects for each action (e.g., `WriteTextCommand`, `DeleteTextCommand`). Each command encapsulates the action and can be executed, stored, or reversed independently. This design simplifies adding new commands and enables undoable operations.

## Structure

The Command pattern typically includes:

1. **Command Interface**: Defines the `execute` method, which all commands must implement.
2. **Concrete Command**: Implements the command interface and performs specific actions on a receiver.
3. **Receiver**: The object that performs the actual work when a command is executed.
4. **Invoker**: Initiates the command and keeps track of commands to support actions like undo.
5. **Client**: Configures the invoker with specific commands.

## UML Diagram

```text
+-------------------+       +----------------------+
|    Command        |<------|   ConcreteCommand    |
|-------------------|       |----------------------|
| + execute()       |       | + execute()          |
+-------------------+       +----------------------+
         ^
         |
+-------------------+       +----------------------+
|   Invoker         |       |     Receiver         |
|-------------------|       |----------------------|
| + setCommand()    |       | + action()           |
| + executeCommand()|       +----------------------+
+-------------------+
```

## Example: Text Editor with Undo Functionality

Let’s implement a simple text editor using the Command pattern. We’ll create commands for writing and deleting text, each of which can be undone.

### Step 1: Define the Command Interface

The `Command` interface defines the `execute` and `undo` methods, which all commands must implement.

```java
// Command Interface
interface Command {
    void execute();
    void undo();
}
```

### Step 2: Implement the Receiver

The `TextEditor` class is the receiver that performs the actual operations on the text (e.g., adding or deleting text).

```java
// Receiver
class TextEditor {
    private StringBuilder text = new StringBuilder();

    public void writeText(String newText) {
        text.append(newText);
    }

    public void deleteText(int length) {
        text.delete(text.length() - length, text.length());
    }

    public String getText() {
        return text.toString();
    }
}
```

### Step 3: Implement Concrete Commands

Each command encapsulates a specific action on the `TextEditor`. For example, `WriteCommand` writes text, while `DeleteCommand` removes text. Each command also implements `undo` to reverse its action.

```java
// Concrete Command for Writing Text
class WriteCommand implements Command {
    private TextEditor editor;
    private String text;

    public WriteCommand(TextEditor editor, String text) {
        this.editor = editor;
        this.text = text;
    }

    @Override
    public void execute() {
        editor.writeText(text);
    }

    @Override
    public void undo() {
        editor.deleteText(text.length());
    }
}

// Concrete Command for Deleting Text
class DeleteCommand implements Command {
    private TextEditor editor;
    private String deletedText;

    public DeleteCommand(TextEditor editor, int length) {
        this.editor = editor;
        this.deletedText = editor.getText().substring(editor.getText().length() - length);
    }

    @Override
    public void execute() {
        editor.deleteText(deletedText.length());
    }

    @Override
    public void undo() {
        editor.writeText(deletedText);
    }
}
```

### Step 4: Implement the Invoker

The `CommandManager` class acts as an invoker, executing commands and keeping a history to support undo functionality.

```java
// Invoker
class CommandManager {
    private Stack<Command> commandHistory = new Stack<>();

    public void executeCommand(Command command) {
        command.execute();
        commandHistory.push(command);
    }

    public void undoLastCommand() {
        if (!commandHistory.isEmpty()) {
            commandHistory.pop().undo();
        }
    }
}
```

### Step 5: Client Code Using the Command Pattern

The client creates commands and executes them through the `CommandManager`, allowing actions to be undone if needed.

```java
public class Client {
    public static void main(String[] args) {
        TextEditor editor = new TextEditor();
        CommandManager commandManager = new CommandManager();

        // Execute write commands
        Command writeHello = new WriteCommand(editor, "Hello ");
        Command writeWorld = new WriteCommand(editor, "World!");

        commandManager.executeCommand(writeHello);
        commandManager.executeCommand(writeWorld);
        System.out.println("Text after writing: " + editor.getText());  // Output: Hello World!

        // Undo the last command
        commandManager.undoLastCommand();
        System.out.println("Text after undo: " + editor.getText());     // Output: Hello

        // Redo the command
        commandManager.executeCommand(writeWorld);
        System.out.println("Text after redoing: " + editor.getText());  // Output: Hello World!
    }
}
```

### Output

```plaintext
Text after writing: Hello World!
Text after undo: Hello
Text after redoing: Hello World!
```

In this example:

- The `TextEditor` class performs operations on the text and serves as the receiver.
- `WriteCommand` and `DeleteCommand` encapsulate text operations and allow them to be undone.
- `CommandManager` executes commands and keeps a history of commands for undo functionality.

## Applicability

Use the Command pattern when:

1. You need to parameterize objects with operations, such as in menu items, buttons, or macro recording.
2. You want to support undo/redo functionality, where each command can reverse its action.
3. You need to queue or log requests for execution, allowing actions to be replayed or stored.

## Advantages and Disadvantages

### Advantages

1. **Decouples Sender and Receiver**: Command encapsulates requests, decoupling the object that initiates the request from the one that performs it.
2. **Supports Undo/Redo**: The Command pattern makes it easy to implement undoable operations by tracking executed commands.
3. **Easily Extensible**: Adding new commands is straightforward, as each command is self-contained and does not affect existing code.

### Disadvantages

1. **Increased Complexity**: The pattern can introduce extra classes, increasing code complexity, especially when many commands are involved.
2. **Potential Overhead**: In some cases, storing and tracking all commands for undo/redo can lead to memory overhead.

## Best Practices for Implementing the Command Pattern

1. **Use Command History for Undo/Redo**: Maintain a history stack to allow easy implementation of undo/redo functionality.
2. **Limit Command Complexity**: Avoid overly complex commands to keep the design simple and maintainable.
3. **Consider Reversible Actions**: Implement `undo` only for commands that can be logically reversed, ensuring each command is self-contained.

## Conclusion

The Command pattern provides a powerful way to encapsulate requests, allowing flexible handling of operations, including support for undo, redo, and macro recording. By decoupling the invoker from the executor, this pattern enhances flexibility and modularity in the system.
