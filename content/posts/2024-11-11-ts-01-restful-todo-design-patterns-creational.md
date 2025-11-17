---
title: "A TypeScript RESTful API Using Design Patterns, Creational"
date: 2024-11-11
categories:
  - Home Page
  - TypeScript
---

Let’s talk about **creational design patterns**—arguably the foundation of any well-architected system. At their core, these patterns focus on how objects are created. Why does this matter? Well, if you’ve ever written code that tightly couples object creation to the logic that depends on those objects, you’ve likely felt the pain of trying to refactor it later.

Creational patterns abstract that creation process, giving us flexibility and reuse. By adopting these patterns, our systems become more scalable, maintainable, and adaptable. In this article, we’ll explore how creational patterns can bring order and elegance to a RESTful API built with TypeScript. And yes, we’ll sprinkle in some practical examples to keep things grounded.

## Abstract Factory

### Overview

The **Abstract Factory** pattern is essentially about creating families of related objects. Imagine a factory—let’s say one for custom error responses. It churns out objects like `404 Not Found` or `500 Internal Server Error`, all following a consistent structure. This pattern ensures we centralize the creation logic for these objects, which makes our code more predictable and, dare I say, pleasant to maintain.

### Implementation

Let’s start simple. Suppose we need to generate error responses. For example, every `404` has the same code but a different message. Instead of repeatedly writing boilerplate code, why not create reusable factories?

Here’s a function-based Abstract Factory—straightforward, clean, and very TypeScript-y:

```typescript
export type CreateErrorResponse = (message?: string) => ErrorResponse;
```

With this template, we define factories for each error type:

```typescript
export const createBadRequestResponse: CreateErrorResponse = (message?: string): ErrorResponse => ({
  code: 400,
  message: message ?? "Bad Request",
});

export const createNotFoundResponse: CreateErrorResponse = (message?: string): ErrorResponse => ({
  code: 404,
  message: message ?? "Not Found",
});

export const createInternalServerErrorResponse: CreateErrorResponse = (message?: string): ErrorResponse => ({
  code: 500,
  message: message ?? "Internal Server Error",
});
```

Now, you might wonder, “What about using classes?” Sure, we can, but—and I’ll admit this is personal preference—I’m a fan of keeping things simple when the situation calls for it. Why complicate something clean with unnecessary abstractions? That said, for those of you who prefer a class-based approach, here’s an example:

```typescript
export interface ErrorResponseFactory {
  create(message?: string): ErrorResponse;
}

export class BadRequestResponseFactory implements ErrorResponseFactory {
  create(message?: string): ErrorResponse {
    return { code: 400, message: message ?? "Bad Request" };
  }
}

export class NotFoundResponseFactory implements ErrorResponseFactory {
  create(message?: string): ErrorResponse {
    return { code: 404, message: message ?? "Not Found" };
  }
}
```

Use this approach if your project demands more extensibility or you want to standardize object creation across various implementations.

## Builder

### Overview

Let’s move to the **Builder** pattern. Imagine you’re assembling a complex object like our `Task` model. It’s not just about instantiating an object—it’s about constructing it piece by piece, ensuring everything is configured correctly. The Builder pattern is perfect for this scenario.

But here’s the twist: our `Task` creation logic has a small oversight. When building the `create` action in the initial RESTful API, we overlooked a key detail—`Task` objects include properties like `id` and `createdAt` that aren’t part of the user’s input. To fix this, we introduce a new `TaskInput` class.

### Implementation

#### Task Input

This lightweight class represents the input expected when creating a task:

```typescript
export default class TaskInput {
  static readonly DefaultTaskInputDescription = "Default Task Description";

  constructor(
    public title: string,
    public description: string = TaskInput.DefaultTaskInputDescription,
  ) {}
}
```

#### Task Model

Now let’s redefine our `Task` model. It extends `TaskInput` and adds properties like `id`, `status`, and timestamps:

```typescript
export default class Task extends TaskInput {
  id: string;
  status: TaskStatus;
  createdAt: number;
  updatedAt: number;

  constructor(
    public title: string,
    public description: string = Task.DefaultTaskInputDescription,
  ) {
    super(title, description);
    this.id = uuid();
    this.status = TaskStatus.Pending;
    this.createdAt = Date.now();
    this.updatedAt = this.createdAt;
  }
}
```

#### Task Builder

Here’s where the Builder pattern shines. It simplifies `Task` creation by handling validation and configuration steps:

```typescript
export default class TaskBuilder {
  private task: Task;

  constructor() {
    this.task = new Task("", Task.DefaultTaskInputDescription);
  }

  fromTaskInput(input: TaskInput) {
    this.setTitle(input.title);
    this.setDescription(input.description);
    return this;
  }

  setId(id: string) {
    this.task.id = id;
    return this;
  }

  setTitle(title: string) {
    this.task.title = title;
    return this;
  }

  setDescription(description: string) {
    this.task.description = description;
    return this;
  }

  setStatus(status: TaskStatus) {
    this.task.status = status;
    return this;
  }

  setCreatedAt(date: Date) {
    this.task.createdAt = date.getTime();
    return this;
  }

  setUpdatedAt(date: Date) {
    this.task.updatedAt = date.getTime();
    return this;
  }

  build(): Task {
    if (this.task.title === "") {
      throw new Error("Title is required.");
    }
    return this.task;
  }
}
```

Notice how `build()` enforces validation. No more wondering if `Task` objects are missing critical properties—this method ensures they’re always valid.

## Factory Method

The **Factory Method** pattern is like the next step after you realize that manually creating objects everywhere in your code is a terrible idea. Think about it—what happens when the way you create an object changes? Do you really want to dive into dozens of files, updating instantiation logic one by one? No, thank you.

The Factory Method pattern centralizes the creation process for a specific object, giving you a single point of truth. It also makes your code easier to extend, because adding new creation logic doesn’t require changing existing code—it just means adding a new factory method.

Let’s start simple and build up.

Remember when we discussed creating error responses in the **Abstract Factory** section? Each of those factories can also be seen as Factory Methods when considered individually. Here’s a super simple Factory Method:

```typescript
export const createErrorResponse = (code: number, message?: string): ErrorResponse => {
  if (!message) {
    switch (code) {
      case 400:
        message = "Bad Request";
        break;
      case 404:
        message = "Not Found";
        break;
      case 500:
        message = "Internal Server Error";
        break;
      default:
        message = "Unknown Error";
    }
  }
  return { code, message };
};
```

This function encapsulates the object creation logic, allowing us to generate consistent error responses without duplicating code. Notice how it defaults to standard messages when none are provided. Simple, effective, and easily extensible.

The **TaskBuilder** class we discussed earlier is a great candidate for a Factory Method. Instead of directly instantiating a builder in multiple places, we create a dedicated method:

```typescript
export function createTaskBuilder(): TaskBuilder {
  return new TaskBuilder();
}
```

Now, wherever we need to build a `Task`, we call `createTaskBuilder()` instead of sprinkling `new TaskBuilder()` all over our codebase. This abstraction makes it easy to adjust the builder instantiation in one place without hunting down instances throughout your code.

If you’re looking to embrace object-oriented principles fully, you can design a factory class that encapsulates the creation logic for builders:

```typescript
export default class TaskBuilderFactory {
  createTaskBuilder(): TaskBuilder {
    return new TaskBuilder();
  }
}
```

Why might you do this? Maybe your project has multiple builder types (e.g., `TaskBuilder`, `SubTaskBuilder`, etc.), and you want a single factory class to manage their creation. This approach keeps things organized and allows for future extensions without altering the existing logic.

The beauty of the Factory Method lies in its simplicity. It centralizes object creation, making your code easier to maintain and extend. And the best part? It’s a small change with a significant impact. Even something as straightforward as a `createTaskBuilder` function can save you headaches down the road.

But keep in mind, not every object needs a factory. Use this pattern when object creation is complex, repetitive, or likely to change.

## Prototype

Let’s move on to the **Prototype** pattern, which is a fascinating one. At its heart, this pattern is all about duplicating objects. Imagine you have an object that took time and effort to set up—maybe it has a bunch of deeply nested properties, or it involved a series of computations. Instead of recreating it from scratch, you simply make a copy.

The Prototype pattern lets us do this efficiently while keeping our code clean and flexible.

In TypeScript, the spread operator is your best friend for shallow cloning:

```typescript
const errorResponse = createErrorResponse(404, "Task Not Found");
const errorResponseDuplicate = { ...errorResponse };
```

This works perfectly for objects composed of primitive types. However, if your object has nested properties or complex references, shallow cloning won’t cut it. That’s when we need a more robust approach.

Inspired by languages like Java, we can introduce a `Cloneable` interface to standardize how cloning is handled:

```typescript
export default interface Cloneable {
  clone(): Cloneable;
}
```

This interface ensures that any class implementing it must provide a `clone` method. Let’s apply this to the `Task` class:

```typescript
import Cloneable from "../utils/Cloneable";
import TaskInput from "./TaskInput";
import TaskStatus from "./TaskStatus";
import { v4 as uuid } from "uuid";

export default class Task extends TaskInput implements Cloneable {
  id: string;
  status: TaskStatus;
  createdAt: number;
  updatedAt: number;

  // Other methods...

  clone(): Cloneable {
    const clone = new Task(this.title, this.description);
    clone.id = this.id;
    clone.status = this.status;
    clone.createdAt = this.createdAt;
    clone.updatedAt = this.updatedAt;
    return clone;
  }
}
```

Here’s what’s happening:

1. The `clone` method creates a new `Task` instance, duplicating all its properties.
2. This approach ensures a deep copy, even if the object contains complex types.

Why go through this effort? Because having a consistent way to clone objects makes your code more predictable and reusable.

## Singleton

Finally, let’s talk about the **Singleton** pattern. This one’s a classic—it ensures a class has only one instance. It’s great for shared resources like a database connection, a configuration manager, or, in our case, the `Database` class.

But let’s get something out of the way: not every single-use instance is a Singleton. To qualify, it must enforce that only one instance can exist and provide global access to it.

Here’s how to implement a Singleton `Database` class:

```typescript
export default class Database {
  private static instance: Database;
  private tasks: Task[] = [];

  private constructor() {}

  public static getInstance(): Database {
    if (!Database.instance) {
      Database.instance = new Database();
    }
    return Database.instance;
  }
}
```

This class ensures that only one `Database` instance exists. Whenever `getInstance` is called, it either returns the existing instance or creates it if it doesn’t already exist.

Sometimes, a full-blown Singleton class feels like overkill. For instance, consider our `taskNotFound404` error response. Do we really need a class to manage a single shared constant? Probably not.

Here’s a simpler approach:

```typescript
export const taskNotFound404 = createNotFoundResponse("Task Not Found");

export const deleteTask = (req: Request, res: Response) => {
  const task = database.getTaskById(req.params.id);
  if (task) {
    database.deleteTask(req.params.id);
    res.status(204).send("");
    return;
  }
  res.status(404).send(JSON.stringify(taskNotFound404));
};
```

The Singleton pattern is powerful but often overused. Before reaching for it, ask yourself: Do I truly need a single, global instance? If the answer is yes, go for it. If not, consider simpler alternatives like module-level constants.

## Conclusion

Creational patterns are all about making object creation predictable, reusable, and flexible. They help us write cleaner, more maintainable code by abstracting away the details of how objects are instantiated. Whether it’s an elegant `TaskBuilder` or a reliable `Database` Singleton, these patterns are invaluable tools in a developer’s toolbox.

For the full implementation of the examples in this article, visit [GitHub](https://github.com/solidref/typescript-todo-restful-dp/tree/01_creational_patterns).

In the next article, we’ll explore **Structural** patterns and how they can simplify complex relationships in our RESTful API. See you there!
