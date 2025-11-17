---
title: The controversy of JavaScript runtime environments
date: 2024-05-16T23:39:51+00:00
url: /the-controversy-of-javascript-runtime-environments/
featured_image: /media/2015/11/dna-structure.jpg
categories:
  - Home Page
  - JavaScript
---

For nearly a decade, I have honed my skills as both a frontend and backend developer. Over the past five years, my focus has primarily been on backend development, specializing exclusively in [JavaScript][1].

"Hold on, isn't JavaScript both a programming language and a standard? Actually, no. [ECMAScript][2] is the [standard][3], and [JavaScript][1] is just an implementation of that standard.

Do I, as a programmer, need to concern myself with the distinction above? Perhaps I should. However, my intent isn't to debate the nuances of the programming language or the standard that underpins this elegant and versatile language. I'm also not here to delve into the complexities and debates surrounding [**JavaScript Engines**][4] and the emerging concept of **JavaScript Runtime Environments** (_admittedly, I haven't found a definitive source that encapsulates what I'm about to discuss, but let's dive in anyway, shall we?_).

## JavaScript Engines

I'll start with JavaScript Engines. This seems like the right place to start, right? You see, the engine is essentially the language interpreter. But there's more to it than that. There are actually multiple implementations of the ECMAScript standard: JavaScript, JScript (by Microsoft), and ActionScript (by Macromedia, now Adobe). Each of these had its own purpose (or lack thereof) at some point in time. I understand the need for ActionScript, but JScript? Why Microsoft?

That's not necessarily a bad thing. After all, with an open standard, such diversity is to be expected. Some implementations arise from innovative ideas, while others are driven by more corporate goals (which is a polite way of saying they might be motivated by profit).

So, if we travel back in time, we find that [a very smart individual][5] established the foundation for the standard, and subsequently, various entities felt compelled to implement it. Among all these engines (focusing solely on JavaScript), here is a short list of the honorable mentions.

### [V8](https://v8.dev/)

An open-source, high-performance JavaScript and WebAssembly engine developed by Google (perhaps the most popular at the moment), used in the Google Chrome browser, Node.js, and various other runtime environments.

- Just-In-Time (JIT) compilation for improved performance.
- Modern ECMAScript support.<br /> Written in C++.

### [SpiderMonkey](https://spidermonkey.dev/)

Mozilla's JavaScript and WebAssembly engine (perhaps the first of its kind), used in the Firefox web browser, Thunderbird, and other Mozilla projects.

- Implements the latest ECMAScript standards.
- Includes a JIT compiler, interpreter, and garbage collector.
- Written in C++.

### JavaScriptCore (JSC)

Also known as Nitro, this is Apple's JavaScript engine, used in the Safari web browser, WebKit, and other Apple software.

- Supports the latest ECMAScript standards.
- Includes a JIT compiler and a low-level interpreter.
- Written in C++.

### ChakraCore

The open-source core of Microsoft's Chakra JavaScript engine, used in the Microsoft Edge browser (pre-Chromium) and other Microsoft applications.

- Implements modern ECMAScript features.
- Includes a JIT compiler and garbage collector.
- Written in C++.

### Hermes

An open-source JavaScript engine optimized for running React Native, used primarily in React Native mobile applications.

- Optimized for fast startup and memory efficiency.
- Bytecode precompilation to reduce startup time.
- Written in C++.

_And others..._

Is it acceptable that multiple engines exist? Absolutely. They are designed to implement (or should be implementing) the standard. Their purpose is to serve the standard and enable users to run the language. **In browsers.** After all, that's what both the standard and the language were created for, isn't it?

Do you see any issues so far? I don't. The engine serves its purpose, the browser requires the language, and we developers are equipped with a highly capable tool to provide our customers with an excellent experience. There are no problems here.

## JavaScript Runtime Environments

The problem arises when the browser is no longer the sole runtime environment for this language. Notice that I've shifted the focus here. I'm no longer discussing engines; I'm now addressing runtime environments. Historically, the browser was the first runtime environment for JavaScript. Its scope was very limited, offering only minimal capabilities.

At some point, we wondered: why should we use JavaScript for frontend development and a different language for the backend? Why should we need to learn more than one language to develop our applications? I won't debate whether this was a good or bad idea. The bad ideas came later.

For now, let's introduce our culprits. The most popular JavaScript Runtime Environments:

### [Node.js](https://nodejs.org/)

The first and widely-used, open-source, cross-platform runtime environment for executing JavaScript server-side, built on the [V8 engine](https://v8.dev/), used for server-side scripting, building scalable network applications, command-line tools and... why not... the development base for pretty much any frontend app.

### [Deno](https://deno.land/)

The next-gen secure runtime for JavaScript and TypeScript, created by [Ryan Dahl](https://en.wikipedia.org/wiki/Ryan_Dahl) (the original creator of Node.js) and used for modern web development with TypeScript support and secure execution with restricted permissions by default.

### [Bun](https://bun.sh/)

The wonder child of runtime environments, built using [JavaScriptCore](https://docs.webkit.org/Deep%20Dive/JSC/JavaScriptCore.html) Engine, capable of running both JavaScript and TypeScript and designed for speed.

#### Other Mentions

##### [Winterjs][6]

A lightweight runtime environment focused on simplicity and performance, minimalistic and performance-oriented applications.

##### Cloudflare Workers

A serverless platform for running JavaScript on Cloudflare's edge network, low-latency edge computing, serverless functions, and API endpoints.

##### [Hermes][7] (by Facebook)

A JavaScript engine optimized for running React Native applications, used for mobile application development and with a focus on performance and startup time.

_And the list can continue..._

Having multiple runtime environments is beneficial, right? Right? Well, competition is always healthy. However, intentionally hindering progress is not. And I'm not talking about runtime environments sabotaging each other; I'm talking about them sabotaging us, the developers.

When OpenJDK emerged from Java SE, the developers retained the same language syntax. Similarly, when Mono was introduced as a .NET C# alternative, particularly to support Linux, it adhered to the official .NET syntax. These examples illustrate a consistent approach to preserving language syntax across different implementations.

But now, let's take a look at JavaScript Runtime Environments. I'll focus on just one example (_how to read a file_), though the list of differences is extensive.

### Node.js Implementation

[Node.js API Docs](https://nodejs.org/docs/latest/api/fs.html#fspromisesreadfilepath-options)

```javascript
const { readFile } = require("node:fs/promises");

(async function logFile() {
  const contents = await readFile("/foo/bar.txt", { encoding: "utf8" });
  console.log(contents);
})();
```

### Deno Implementation

[Deno API Docks](https://deno.land/api@v1.43.3?s=Deno.read)

```javascript
(async function logFile() {
  using f = await Deno.open("/foo/bar.txt");
  const buf = new Uint8Array(100);
  const numberOfBytesRead = await Deno.read(f.rid, buf);
  const text = new TextDecoder().decode(buf);
  console.log(contents);
})();
```

```javascript
// or using the more direct approach

(async function logFile() {
  const content = Deno.readTextFile("/foo/bar.txt");
  console.log(contents);
})();
```

### Bun Implementation

[Bun API Docs](https://bun.sh/docs/api/file-io#reading-files-bun-file)

```javascript
(async function logFile() {
  const content = await Bun.file("/foo/bar.txt").text();
  console.log(contents);
})();
```

```javascript
// or using the Bun.fs compatibility module for Node.js

(async function logFile() {
  const content = await Bun.fs.readFile("/foo/bar.txt", "utf-8");
  console.log(contents);
})();
```

Now, let me explain the purpose of this article. I work for a company that, over the past few years, has chosen to embrace JavaScript for both backend and frontend development. Why? The reason is clear: the simplicity of switching between frontend and backend while using the same language.

As a technical lead in this company, I am beginning to find Node.js a bit too slow for the performance we desire (or require) for our application. So I became curious whether there are better solutions available for us. Additionally, I constantly read about new and impressive engines (and runtime environments) that are setting new speed records for running JavaScript.

However, I'm stuck on one major issue. Over the past four years, the project I've been working on has accumulated millions of lines of code. Deno isn't a viable solution because it was launched with a new concept in mind and I respect that. Bun… could be an option, but it presents numerous compatibility issues. Rewriting a significant amount of code to use the correct syntax would be required. And then, what if we decide that Bun isn't suitable and need to switch back to Node.js?

Now, let's say I decide to develop a small feature (a microservice) from our application to run on all three major JavaScript runtime environments. This would allow us to determine which one performs better.

```javascript
async function readFile(filePath) {
  // Check for Node.js and Bun (which supports require and import.meta.url)
  if (typeof require !== "undefined" && typeof module !== "undefined") {
    const { readFile: cjsReadFile } = require("node:fs").promises;
    return await cjsReadFile(filePath, "utf8");
  }
  // For Deno
  else if (typeof Deno !== "undefined") {
    return await Deno.readTextFile(filePath);
  }
  // For Bun
  else if (typeof Bun !== "undefined") {
    return await Bun.file(filePath).text();
  }
  // Fallback for unsupported environments
  else {
    console.error("This runtime environment is not supported.");
  }
}

(async function logFile() {
  const contents = await readFile(filePath);
  console.log(contents);
})();
```

Here is a read file method compatible with all three runtime environments. However, it still doesn't cover Node.js's ESM mode. What do you think of this approach? How do you think the majority of developers would react to it?

One potential solution could be Bun. They claim to have good compatibility with Node.js (they're not quite there yet, but they're working hard on it). However, syntax compatibility remains an issue. Even if I'm willing to give it a shot, convincing over 50 developers on the team might be a different story.

In conclusion, while I appreciate the interest in developing newer and better engines or runtime environments, I also understand why they don't gain popularity overnight among developers. As long as syntax varies from one runtime to another, or even from one engine to another, migrating our code is far from simple. Convincing a team to develop new projects on a newer, supposedly better runtime environment while maintaining legacy code on the older one is, in my opinion, nearly impossible. And then there's the issue of expenses, which I don't even want to get into.

While the drive to innovate and create better JavaScript engines and runtime environments is commendable, the reality of adoption is much more complex. Syntax inconsistencies between runtimes and engines make code migration a daunting task. For a project with millions of lines of code and a large team of developers, the cost and effort involved in transitioning to a new runtime environment are significant barriers.

Although new runtime environments like Bun (or, the latest, WinterJs) show promise with claims of improved performance and compatibility, the practical challenges of integrating these into existing projects cannot be ignored. The technical and financial hurdles, combined with the need to maintain legacy systems, make such transitions impractical for many organizations.

Ultimately, the stability and consistency provided by established environments like Node.js, despite its performance limitations, offer a safer and more predictable path for development. As we continue to explore and evaluate new technologies, it's crucial to balance innovation with practicality, ensuring that the tools we choose align with the needs and capabilities of our teams and projects.

[1]: https://en.wikipedia.org/wiki/JavaScript
[2]: https://en.wikipedia.org/wiki/ECMAScript
[3]: https://tc39.es/ecma262/
[4]: https://en.wikipedia.org/wiki/List_of_ECMAScript_engines
[5]: https://en.wikipedia.org/wiki/Brendan_Eich
[6]: https://github.com/wasmerio/winterjs
[7]: https://github.com/facebook/hermes
