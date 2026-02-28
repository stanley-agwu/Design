# Frontend Design Fundamentals

### 1. Virtual DOM (VDOM)
The Virtual DOM (VDOM) is a lightweight JavaScript representation of the real DOM.

Instead of updating the real DOM directly (which is slow), frameworks update the Virtual DOM first, compare changes, and then efficiently update only the necessary parts of the real DOM.

#### Why Not Update the Real DOM Directly?
Real DOM operations are expensive because they:

1. Trigger layout recalculation (reflow)
2. Trigger repaint
3. Block the main thread

Frequent direct updates = poor performance.

#### How Virtual DOM Works (Step-by-Step)
Let’s take how it works in frameworks like React:

1. Initial Render
- UI is converted into a Virtual DOM tree (JS objects).
- That tree is rendered to the real DOM.

2. State Changes
- When state updates, a `new Virtual DOM tree` is created.

3. Diffing (Reconciliation)
- The new tree is compared with the old tree.
- Only differences are identified.

4. Efficient DOM Update
- Only changed nodes are updated in the real DOM.

#### Simple Example

##### Without Virtual DOM

```js
document.getElementById("counter").innerText = count;
```

Every update touches the real DOM.

##### With Virtual DOM (Conceptual)

```js
function render() {
  return {
    type: "div",
    children: [`Count: ${count}`]
  };
}
```

Framework:
- Compares old vs new virtual tree
- Updates only changed text node

#### Key Benefits
- Faster UI updates
- Reduced direct DOM manipulation
- Predictable rendering
- Better developer experience

#### Important Clarification
Virtual DOM is **not faster than the real DOM itself**.

It is faster because:
- It minimizes expensive real DOM operations.

The optimization comes from:
- Batching updates
- Diffing algorithm
- Smart reconciliation

#### Used In:
1. React
2. Vue.js (uses VDOM)
3. Preact

(Not used in Angular — Angular uses change detection differently.)

#### Summary
The Virtual DOM is an in-memory JavaScript representation of the real DOM that allows frameworks to efficiently compute UI changes and apply minimal updates to the actual DOM for better performance.


### 2. IIFE
IIFE (Immediately Invoked Function Expression) is deeply connected to scope, closures, and encapsulation — especially important before ES6 modules existed.

#### What is an IIFE?
An **IIFE** is a function that:

1. Is defined as an expression
2. Is executed immediately after it is created

##### Basic Syntax

```js
(function () {
    console.log("I run immediately!");
})();
```

Or with arrow function:

```js
(() => {
    console.log("I also run immediately!");
})();
```

##### Why Do We Need the Parentheses?
Normally this is a **function declaration**:

```js
function greet() {}
```

But this is a **function expression**:

```js
(function greet() {})
```

Wrapping it in parentheses forces JavaScript to treat it as an expression.
Then the final `()` executes it immediately.

So structurally:

```js
(function() {})()
```

means:
1. Create function expression
2. Immediately call it

#### Core Purpose of IIFE
The main purpose:
1. Create a private scope
2. Avoid polluting the global scope
3. Simulate modules (before ES6 modules)

##### Use Case #1 — Avoid Global Scope Pollution
Without IIFE:

```js
var counter = 0;

function increment() {
    counter++;
}
```

Everything is global.

Now with IIFE:

```js
(function () {
    var counter = 0;

    function increment() {
        counter++;
        console.log(counter);
    }

    increment();
})();
```

Now:
- `counter` is private
- `increment` is private
- Nothing leaks to global scope

This was extremely important before ES6 `let`, `const`, and modules.

##### Use Case #2 — Data Privacy (Encapsulation)
You can return only what you want exposed:

```js
const Counter = (function () {
    let count = 0;

    return {
        increment() {
            count++;
        },
        getCount() {
            return count;
        }
    };
})();

Counter.increment();
console.log(Counter.getCount()); // 1
```

Here:
- `count` is private
- Only selected methods are public

This is the **Module Pattern**.

##### Use Case #3 — Capture Loop Variables (Before let)
Before `let`, `var` caused scope problems.

Problem:

```js
for (var i = 0; i < 3; i++) {
    setTimeout(() => {
        console.log(i);
    }, 100);
}
```

Output:

```
3
3
3
```

Fix with IIFE:

```js
for (var i = 0; i < 3; i++) {
    (function (index) {
        setTimeout(() => {
            console.log(index);
        }, 100);
    })(i);
}
```

Output:

```
0
1
2
```

The IIFE creates a new scope for each iteration.

Today, we use:

```js
for (let i = 0; i < 3; i++) {
```

But historically, IIFE was critical.

##### Use Case #4 — Initialization Code
Sometimes you want code to run once immediately:

```js
(function initApp() {
    console.log("App initialized");
})();
```

Used in:
1. Script bootstrapping
2. Configuration setup
3. Environment detection

##### IIFE With Parameters
You can pass arguments:

```js
(function (name) {
    console.log(`Hello ${name}`);
})("Stammer");
```

##### IIFE and Closures
IIFE creates closure naturally:

```js
const add = (function () {
    let base = 10;

    return function (num) {
        return base + num;
    };
})();

console.log(add(5)); // 15
```

`base` stays alive due to closure.

##### Async IIFE (Modern Use Case)
Useful when using `await` outside of modules:

```js
(async function () {
    const response = await fetch("https://api.example.com");
    const data = await response.json();
    console.log(data);
})();
```

Very common in:
1. Node.js scripts
2. Testing
3. REPL environments

#### Execution Context View
When an IIFE runs:

1. A new execution context is created
2. It gets its own:
   - Variable Environment
   - Lexical Environment
3. After execution:
   - The function scope disappears
   - Unless closures reference it

This is why it’s powerful for isolation.

#### Comparison With Modern Alternatives
|-------------------------------------------------------|
| Feature           | IIFE              | ES6 Modules   |
| ----------------- | ------------------|---------------|
| Scope isolation   | YES               | YES           |
| Private variables | YES               | YES           |
| Import/export     | NO                | YES           |
| Recommended today | NO, Mostly legacy | YES           |
|-------------------------------------------------------|

Today:
1. Prefer ES Modules
2. Prefer `let` / `const`
3. Prefer block scope

But IIFE is still useful for:
1. Immediate async execution
2. Legacy codebases
3. Script isolation in browsers

#### Common Variations
These are all valid:

```js
(function(){})()
(function(){}())
!function(){}()
+function(){}()
```

They all force expression context.

##### Summary
An IIFE is a function expression that executes immediately after creation. It is used to create a private scope, avoid global namespace pollution, implement the module pattern, and manage closures — especially before ES6 modules and block scoping were introduced.


### 3. ES Modules
**ES Modules (ECMAScript Modules)** are the official JavaScript standard for organizing and sharing code between files using `import` and `export`.

They allow you to split code into reusable, maintainable modules with **explicit dependencies**.

#### Basic Syntax

##### Exporting

```js
// math.js
export const add = (a, b) => a + b;

export function multiply(a, b) {
  return a * b;
}
```

##### Importing

```js
// app.js
import { add, multiply } from "./math.js";

console.log(add(2, 3));
```

#### Default Export

```js
// logger.js
export default function log(message) {
  console.log(message);
}
```

Import:

```js
import log from "./logger.js";
```

#### Key Characteristics
1. Static structure (imports are resolved at compile time)
2. Supports tree-shaking
3. Strict mode by default
4. File-based modularity
5. Asynchronous loading in browsers

#### Tree-shaking
Tree-shaking is a build-time optimization that removes unused exports from your final JavaScript bundle.

It works with ES Modules because their static import/export structure lets bundlers (like Webpack, Rollup, Vite) analyze which code is actually used.

In short:
Tree-shaking eliminates dead code to reduce bundle size and improve performance.

#### ES Modules vs CommonJS
|------------------------------------------------------------------|
| Feature      | ES Modules             | CommonJS                 |
| ------------ | ---------------------- | ------------------------ |
| Syntax       | `import/export`        | `require/module.exports` |
| Loading      | Static                 | Dynamic                  |
| Execution    | Asynchronous (browser) | Synchronous              |
| Tree-shaking | YES                    | NO                       |
| Default in   | Modern JS, browsers    | Node.js (legacy)         |
|------------------------------------------------------------------|

#### In Browsers

```html
<script type="module" src="app.js"></script>
```

#### In Node.js
Enable via:

* `.mjs` extension
* or `"type": "module"` in `package.json`

#### Why ES Modules Matter
1. Better code organization
2. Better performance via tree-shaking
3. Cleaner dependency graph
4. Standardized across browsers and Node

#### Summary
ES Modules are the standardized JavaScript module system that uses `import` and `export` to structure code into reusable, maintainable, and statically analyzable modules.


### 4. Scope

#### What is Scope in JavaScript?

**Scope** defines **where variables are accessible** in your code.

In simple terms:
Scope determines the visibility and lifetime of variables.

JavaScript has **lexical scope**, meaning scope is determined by where code is written, not where it is executed.

#### Types of Scopes

##### Global Scope
Variables declared outside any function or block.

```js
const appName = "MyApp";

function printApp() {
  console.log(appName);
}

printApp(); // "MyApp"
```

- Accessible everywhere
- Can cause global name space pollution

##### Function Scope
Variables declared inside a function are accessible only within that function.

```js
function greet() {
  const message = "Hello";
  console.log(message);
}

greet(); // Hello
console.log(message); // ReferenceError
```

`message` exists only inside `greet`.

##### Block Scope (let / const)
Introduced in ES6.
Variables declared with `let` or `const` inside `{}` are block-scoped.

```js
if (true) {
  let count = 10;
  const name = "Grant";
}

console.log(count); // ReferenceError
```

NOTE: `var` does NOT respect block scope:

```js
if (true) {
  var x = 5;
}

console.log(x); // 5 (leaks out)
```

#### Lexical Scope (Important Concept)
Scope is determined by **where a function is defined**, not where it is called.

```js
function outer() {
  const a = 10;

  function inner() {
    console.log(a);
  }

  return inner;
}

const fn = outer();
fn(); // 10
```

`inner` remembers the scope it was created in → this is also a **closure**.

#### Scope Chain
When accessing a variable, JS looks:

1. Inside current scope
2. Then outer scope
3. Then outer of outer
4. Until global scope

```js
const a = 1;

function first() {
  const b = 2;

  function second() {
    const c = 3;
    console.log(a, b, c);
  }

  second();
}

first(); // 1 2 3
```

This lookup process is called the **scope chain**.

#### Shadowing
A variable in inner scope can override outer scope variable.

```js
const value = 100;

function test() {
  const value = 50;
  console.log(value);
}

test(); // 50
```

Inner `value` shadows outer one.

#### Temporal Dead Zone (TDZ)
Applies to `let` and `const`.

```js
console.log(a); // ReferenceError
let a = 10;
```

Between the start of scope and variable declaration → TDZ.

#### Common Pitfall (Closures + Loops)

```js
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
```

Output:

```
3
3
3
```

Because `var` is function-scoped.

Fix:

```js
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
```

Output:

```
0
1
2
```

#### Scope vs Context (Important Difference)
Scope → Where variables are accessible
Context (`this`) → How a function is invoked

They are different concepts.

#### Best Practices
1. Prefer `const` by default
2. Use `let` only when reassignment is needed
3. Avoid `var`
3. Avoid global variables
4. Keep scope small

#### Summary
Scope in JavaScript defines where variables are accessible. JavaScript uses lexical scoping, meaning a function’s scope is determined by where it is defined, forming a scope chain that resolves variables from inner to outer environments.

#### Side effects improper scope usage

1. **Global namespace pollution** → Variables accidentally accessible everywhere, causing conflicts.
2. **Variable shadowing bugs** → Inner variables override outer ones unexpectedly.
3. **Memory leaks via closures** → Variables kept alive longer than intended.
4. **Unexpected mutation** → Shared scoped variables modified from multiple     places.


### 5. Closure

#### What is a Closure in JavaScript?
A **closure** is created when a function **remembers variables from its lexical scope**, even after the outer function has finished executing.

In simple terms:
A closure allows a function to access variables from its outer scope even after that outer function has returned.

JavaScript has **lexical scoping**, so closures are a natural result of how scope works.

#### Basic Example

```js
function outer() {
  let count = 0;

  function inner() {
    count++;
    console.log(count);
  }

  return inner;
}

const counter = outer();

counter(); // 1
counter(); // 2
counter(); // 3
```

#### What happened?
1. `outer()` runs
2. Normally `count` should disappear after `outer` finishes
3. But `inner` still references `count`
4. JavaScript keeps `count` alive in memory

That preserved environment is the **closure**.

#### How It Works Internally
When `outer()` executes:
1. A new execution context is created
2. `count` is stored in its lexical environment
3. `inner` keeps a reference to that environment
4. Even after `outer()` finishes, the environment remains alive

This is why closures can preserve state.

#### Practical Use Case — Private Variables
Closures enable data encapsulation:

```js
function createBankAccount(initialBalance) {
  let balance = initialBalance;

  return {
    deposit(amount) {
      balance += amount;
    },
    getBalance() {
      return balance;
    }
  };
}

const account = createBankAccount(100);

account.deposit(50);
console.log(account.getBalance()); // 150
```

`balance` is private — it cannot be accessed directly.

This is the foundation of the **Module Pattern**.

#### Closure in Loops
Problem:

```js
for (var i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
```

Output:

```
3
3
3
```

Why?

- `var` is function-scoped
- All callbacks close over the same `i`

Fix using `let` (block scope):

```js
for (let i = 0; i < 3; i++) {
  setTimeout(() => console.log(i), 100);
}
```

Output:

```
0
1
2
```

Or fix using closure manually:

```js
for (var i = 0; i < 3; i++) {
  (function(index) {
    setTimeout(() => console.log(index), 100);
  })(i);
}
```

#### Real-World Example
Closures are heavily used in:

1. React hooks
2. Event handlers
3. Memoization
4. Debounce/throttle
5. Factory functions

Example (Debounce):

```js
function debounce(fn, delay) {
  let timer;

  return function (...args) {
    clearTimeout(timer);
    timer = setTimeout(() => {
      fn(...args);
    }, delay);
  };
}
```

`timer` persists between function calls because of closure.

#### Memory Implications
Closures can cause **memory leaks** if:

1. They reference large objects
2. They persist longer than needed
3. They are attached to long-lived listeners

Because the outer variables remain in memory as long as the inner function exists.

#### Summary
A closure is a function that retains access to variables from its lexical scope even after the outer function has finished execution. It allows state preservation and data encapsulation in JavaScript.

#### Important Clarification
Closure is NOT:

1. A special syntax
2. A feature you “enable”
3. Something separate from scope

It is simply:
A function + its preserved lexical environment.


