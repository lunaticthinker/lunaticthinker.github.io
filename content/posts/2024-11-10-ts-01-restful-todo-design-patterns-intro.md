---
title: "A TypeScript RESTful API Using Design Patterns"
date: 2024-11-10
categories:
  - Home Page
  - TypeScript
---

**Design patterns** represent foundational approaches to recurring challenges in software architecture. They encapsulate best practices in object-oriented design, providing flexible, adaptable templates that developers can apply to construct robust, maintainable, and scalable systems. By adhering to established, reusable strategies, design patterns facilitate problem-solving in complex software environments and contribute to systematic, reliable development practices.

### The Significance of Design Patterns

The application of design patterns offers multiple, distinct advantages within the software development lifecycle:

- **Enhancement of Reusability**: By encapsulating well-documented, field-tested solutions, design patterns encourage reuse across diverse projects and domains, reducing development time and improving consistency in codebases.

- **Improved Communication and Collaboration**: Design patterns introduce a shared vocabulary among developers, fostering more effective discourse on structural and behavioral approaches, thereby aligning team efforts and bridging understanding across diverse expertise levels.

- **Reinforcement of Design Principles**: Design patterns inherently support principles of modularity, decoupling, and encapsulation, promoting systematic, principle-driven design choices that ensure code quality and stability.

- **Facilitation of System Flexibility and Extensibility**: Many design patterns are constructed to accommodate modifications and extensions, thus enabling systems to evolve gracefully as requirements shift or expand, reducing the potential for disruption and technical debt.

## Building a RESTful API with TypeScript Using Design Patterns

To showcase the practical application of design patterns, I’ll develop a simple RESTful API—a **Todo List Service**. Despite its simplicity, this problem can be incrementally enhanced to illustrate various design patterns effectively, making it an excellent foundation for exploring pattern-based architecture in a manageable and comprehensible way.

The initial implementation of the Todo List Service will prioritize simplicity, establishing a basic working API. We’ll then progressively apply design patterns to enhance the structure, flexibility, and maintainability of the code, demonstrating how each pattern contributes to solving specific architectural challenges.

## Initial Implementation

In this section, we’ll outline the foundational project setup and code structure. Starting with a straightforward implementation will allow us to focus on incremental enhancements using design patterns in subsequent sections.

### Project Structure

The initial project will be organized as follows:

```
.
├── LICENSE
├── package-lock.json
├── package.json
├── src
│   ├── actions.ts
│   ├── database.ts
│   ├── index.ts
│   └── models
│       ├── ErrorResponse.ts
│       ├── Task.ts
│       └── TaskStatus.ts
├── swagger.yaml
└── test.sh
```

- **`Task`**: The core model representing a task in the todo list.
- **`ErrorResponse`**: A utility model for handling error responses consistently.
- **`TaskStatus`**: An enumeration defining various states a task may have, providing structured task management.
- **`database`**: A simple, in-memory data store to persist tasks temporarily during development.
- **`actions`**: Defines mappings between API endpoints and core logic, facilitating modular and testable code.

The structure above provides a foundation that we can expand as we incorporate design patterns.

### Project Initialization

To begin, initialize the project directory, install dependencies, and configure TypeScript support:

```bash
mkdir todo-restful-dp
cd todo-restful-dp
npm init

npm install -i @types/express @types/uuid express uuid
```

### Using Bun.sh to Run TypeScript

For this project, I opted to use [Bun](https://bun.sh/) as a TypeScript runtime. Although Node.js 22 now supports TypeScript with the `--experimental-strip-types` flag, it remains prone to issues, especially when managing CommonJS modules. Bun provides a reliable alternative to ensure the code runs smoothly without compromising on compatibility.

To configure the project to run with Bun, modify the `start` script in `package.json` as follows:

```jsonc
{
  "name": "typescript-todo-restful-dp",
  "version": "1.0.0",
  "main": "index.js",
  "scripts": {
    "start": "bun ./src/index.ts",
    // ...
  },
}
```

This foundational setup prepares us to implement a basic API and explore design patterns through targeted enhancements, ultimately illustrating their advantages within a TypeScript-based RESTful service.

## Core Models

The following section covers the models used in the application, each representing a distinct part of the Todo List API’s structure.

### Task Model

The `Task` model represents the core entity of this API, encapsulating the essential data required to manage a task.

```typescript
import TaskStatus from "./TaskStatus";

type Task = {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  createdAt: number;
  updatedAt: number;
};

export default Task;
```

#### TaskStatus Enum

The `TaskStatus` enumeration provides a structured way to represent a task's lifecycle states. This enum allows us to categorize tasks by status, making the API’s data more consistent and predictable.

```typescript
enum TaskStatus {
  Pending,
  InProgress,
  Completed,
}

export default TaskStatus;
```

### ErrorResponse Model

The `ErrorResponse` model describes the error messages that the API may return, making it easier for clients to understand and handle errors systematically.

```typescript
type ErrorResponse = {
  code: number;
  message: string;
};

export default ErrorResponse;
```

## In-Memory Database

For this initial implementation, I’ve chosen a lightweight, in-memory database. While not suitable for production, it serves our purpose in demonstrating how data can be managed and manipulated within the API.

```typescript
import Task from "./models/task";

export default class Database {
  private tasks: Task[] = [];

  addTask(task: Task): void {
    this.tasks.push(task);
  }

  getTasks(): Task[] {
    return this.tasks;
  }

  getTaskById(id: string): Task | null {
    return this.tasks.find((task) => task.id === id) ?? null;
  }

  updateTask(id: string, updatedTask: Task): Task | null {
    const index = this.tasks.findIndex((task) => task.id === id);
    if (index !== -1) {
      this.tasks[index] = {
        ...this.tasks[index],
        ...updatedTask,
      };
      return this.tasks[index];
    }
    return null;
  }

  deleteTask(id: string): void {
    this.tasks = this.tasks.filter((task) => task.id !== id);
  }
}
```

## Service Actions

The `actions.ts` file serves as a controller, mapping each endpoint to its corresponding logic. This separation allows us to expand the application’s functionality in a modular, testable manner.

```typescript
import { NextFunction, Request, Response } from "express";
import Database from "./database";
import Task from "./models/task";
import { v4 as uuid } from "uuid";

const database = new Database();

export const addTask = (req: Request, res: Response, next: NextFunction) => {
  const task = req.body as Task;
  task.id = uuid();
  console.log("Adding task:", task);
  database.addTask(task);
  res.status(201).send("");
};

export const deleteTask = (req: Request, res: Response) => {
  const task = database.getTaskById(req.params.id);
  if (task) {
    database.deleteTask(req.params.id);
    res.status(204).send("");
    return;
  }
  res.status(404).send(
    JSON.stringify({
      code: 404,
      message: "Task not found",
    }),
  );
};

export const getTasks = (req: Request, res: Response) => {
  res.status(200).send(JSON.stringify(database.getTasks()));
};

export const getTaskById = (req: Request, res: Response) => {
  console.log("Getting task::", req.params.id);
  const task = database.getTaskById(req.params.id);
  if (task) {
    res.status(200).send(JSON.stringify(task));
    return;
  }
  res.status(404).send(
    JSON.stringify({
      code: 404,
      message: "Task not found",
    }),
  );
};

export const updateTask = (req: Request, res: Response) => {
  let task = database.getTaskById(req.params.id);
  if (task) {
    task = database.updateTask(req.params.id, req.body as Task);
    res.status(200).send(JSON.stringify(task));
    return;
  }
  res.status(404).send(
    JSON.stringify({
      code: 404,
      message: "Task not found",
    }),
  );
};
```

### API Endpoints Setup

The main application file (`index.ts`) initializes the Express server and defines the primary API routes. This straightforward setup provides the backbone for the RESTful API.

```typescript
import express, { Request, Response } from "express";
import { addTask, deleteTask, getTaskById, getTasks, updateTask } from "./actions";

const app = express();

app.use(express.json());

app.delete("/task/:id", deleteTask);

app.get("/tasks", getTasks);
app.get("/task/:id", getTaskById);

app.post("/task", addTask);

app.put("/task/:id", updateTask);

app.listen(8080, () => {
  console.log("Server is running on port 8080");
});
```

## Conclusion

This article presented the foundational setup of a basic RESTful API for managing tasks, laying the groundwork for applying design patterns. By isolating the core components—models, in-memory database, service actions, and routing logic—this initial structure provides a clear, modular baseline.

In subsequent articles, we will extend this application using various design patterns to address common challenges such as ensuring code reusability, improving flexibility, and handling complex behaviors systematically. Each design pattern will be introduced in response to a specific architectural need, demonstrating how these patterns can contribute to the scalability, robustness, and maintainability of a RESTful API in TypeScript.
