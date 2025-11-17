---
title: "Template Method Pattern"
date: 2024-07-19
categories:
    - Design Patterns
tags:
    - design patterns
    - behavioral patterns
    - template method
    - inheritance
bookHidden: false
---

If you’ve ever created a base class with a `run()` method that calls a series of steps, then let subclasses override only a few of those steps, you’ve already reinvented the **Template Method** pattern.

Template Method is a behavioral pattern that defines the skeleton of an algorithm in a superclass, while allowing subclasses to customize specific steps. The overall flow stays the same; the details can vary.

## Intent

Define an algorithm’s structure in one place (a template method) and let subclasses override selected steps without changing the overall flow. You get consistent workflows with customizable hooks.

## Problem and Solution

### Problem

Imagine a reporting system that generates PDF, HTML, and CSV reports. Every report follows the same high‑level steps:

1. Gather data
2. Format it
3. Export it

Without a shared template, each report class tends to re‑implement the full workflow, duplicating logic and making changes painful.

### Solution

Template Method moves the shared workflow into an abstract base class and defines a `generateReport()` method that calls the steps in order. Concrete reports only override what’s different — for example, how they format or export. The algorithm lives in one place; behavior differences live in subclasses.

## Structure

The Template Method pattern typically includes:

1. **Abstract Class**: Defines the template method (the skeleton of the algorithm) and provides methods that subclasses can override.
2. **Template Method**: A method in the abstract class that defines the sequence of steps in the algorithm, calling other methods that subclasses can customize.
3. **Concrete Classes**: Implement or override specific steps of the algorithm.

## UML Diagram

```text
+---------------------------+
|      AbstractClass        |
|---------------------------|
| + templateMethod()        |
| + primitiveOperation1()   |
| + primitiveOperation2()   |
+---------------------------+
         ^
         |
+---------------------------+
|      ConcreteClassA       |
|---------------------------|
| + primitiveOperation1()   |
| + primitiveOperation2()   |
+---------------------------+

+---------------------------+
|      ConcreteClassB       |
|---------------------------|
| + primitiveOperation1()   |
| + primitiveOperation2()   |
+---------------------------+
```

## Example: Report Generation System

Let’s implement a report generation system using the Template Method pattern. We’ll create a base class `Report` that defines the steps for generating a report. Each specific report type (e.g., `PDFReport`, `HTMLReport`) can override certain steps while maintaining the overall structure.

### Step 1: Define the Abstract Class with the Template Method

The `Report` class defines the template method `generateReport`, which outlines the sequence of steps for generating a report. Each step can be customized by subclasses.

```java
// Abstract Class
abstract class Report {
    public final void generateReport() {
        gatherData();
        formatReport();
        exportReport();
    }

    protected abstract void gatherData();

    protected abstract void formatReport();

    protected abstract void exportReport();
}
```

### Step 2: Implement Concrete Classes

Each concrete report class overrides the specific steps of the algorithm to provide its unique behavior for formatting and exporting.

```java
// Concrete Class for PDF Report
class PDFReport extends Report {
    @Override
    protected void gatherData() {
        System.out.println("Gathering data for PDF report.");
    }

    @Override
    protected void formatReport() {
        System.out.println("Formatting report in PDF format.");
    }

    @Override
    protected void exportReport() {
        System.out.println("Exporting report as a PDF file.");
    }
}

// Concrete Class for HTML Report
class HTMLReport extends Report {
    @Override
    protected void gatherData() {
        System.out.println("Gathering data for HTML report.");
    }

    @Override
    protected void formatReport() {
        System.out.println("Formatting report in HTML format.");
    }

    @Override
    protected void exportReport() {
        System.out.println("Exporting report as an HTML file.");
    }
}

// Concrete Class for CSV Report
class CSVReport extends Report {
    @Override
    protected void gatherData() {
        System.out.println("Gathering data for CSV report.");
    }

    @Override
    protected void formatReport() {
        System.out.println("Formatting report in CSV format.");
    }

    @Override
    protected void exportReport() {
        System.out.println("Exporting report as a CSV file.");
    }
}
```

### Step 3: Client Code Using the Template Method Pattern

The client code uses the `generateReport` method of each report type, which follows the same sequence of steps but customizes them as needed.

```java
public class Client {
    public static void main(String[] args) {
        Report pdfReport = new PDFReport();
        System.out.println("Generating PDF Report:");
        pdfReport.generateReport();

        Report htmlReport = new HTMLReport();
        System.out.println("\nGenerating HTML Report:");
        htmlReport.generateReport();

        Report csvReport = new CSVReport();
        System.out.println("\nGenerating CSV Report:");
        csvReport.generateReport();
    }
}
```

### Output

```plaintext
Generating PDF Report:
Gathering data for PDF report.
Formatting report in PDF format.
Exporting report as a PDF file.

Generating HTML Report:
Gathering data for HTML report.
Formatting report in HTML format.
Exporting report as an HTML file.

Generating CSV Report:
Gathering data for CSV report.
Formatting report in CSV format.
Exporting report as a CSV file.
```

In this example:

- `Report` defines the `generateReport` template method, outlining the steps for generating a report.
- `PDFReport`, `HTMLReport`, and `CSVReport` are concrete classes that override specific steps, allowing each report type to customize behavior as needed.
- The client code calls `generateReport` on each report, and the overall sequence of steps remains consistent.

## Applicability

Use the Template Method pattern when:

1. You want to define the skeleton of an algorithm in one place, with some steps left for subclasses to implement.
2. You have multiple classes that share a common structure but require different implementations for specific steps.
3. You want to enforce a consistent workflow or process across subclasses, with flexible customization.

## Advantages and Disadvantages

### Advantages

1. **Promotes Code Reuse**: The Template Method pattern centralizes the common steps of an algorithm, promoting reuse and reducing redundancy.
2. **Ensures Consistent Workflow**: The template method enforces a consistent structure for the algorithm, making the process predictable and maintainable.
3. **Easy to Extend**: New subclasses can define custom behavior for specific steps without changing the core algorithm.

### Disadvantages

1. **Increased Number of Classes**: The pattern requires creating a subclass for each specific behavior, which can increase the number of classes.
2. **Potentially Inflexible**: Since the template method is defined in the abstract class, any changes to the algorithm’s structure require modifications to the superclass, impacting all subclasses.

## Best Practices for Implementing the Template Method Pattern

1. **Encapsulate Invariant Behavior**: Use the Template Method pattern to encapsulate the steps of an algorithm that are invariant across subclasses, centralizing them in the base class.
2. **Limit the Template Method’s Scope**: Avoid making the template method overly complex. Define only the essential steps, and leave details to the subclasses.
3. **Use Hook Methods (Optional)**: Consider adding optional steps (hooks) in the template method that subclasses can override if needed. This approach provides more flexibility.

## Conclusion

The Template Method pattern provides an effective way to define a sequence of steps in an algorithm while allowing subclasses to customize specific parts. By centralizing the structure of the algorithm in a base class, this pattern promotes consistency and reduces duplication.
