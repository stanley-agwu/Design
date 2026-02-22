# Hoisting

### Javascript Execution Context

When we try to execution javascript code, execution occurs in two phases:
1. Creation Phase ->
    - First it creates a global Window object.
    - Second it creates a memory heap for storing variables and fucntions references.
    - Third it initializes the variables and functions declarations with undefined.

2. Execution Phase
During the executon phase, Javascript Engine executes the codes line by line, 
assigning values to variables and executing the function calls.
For every new function created, the Javascript Engine creates a new execution 
context altogether.

### Temporal Dead Zone (TDZ) -> 
It is the time between the declaration and initialization of variables 
using "let" and "const".


### What is JavaScript Execution Context
An Execution Context is the environment in which JavaScript code is evaluated and executed.

Think of it as:
    A box that contains everything needed to run a piece of code.

There are three types:

1. Global Execution Context (GEC)
2. Function Execution Context (FEC)
3. Eval Execution Context (rarely used)

#### Two Phases of Execution Context
Every execution context is created in two phases:

-> Phase 1: Creation Phase (Memory Phase) ->
JavaScript scans the code and:

1. Allocates memory for variables
2. Allocates memory for functions
3. Sets up `this`
4. Creates scope chain

-> Phase 2: Execution Phase
1. Code runs line by line
2. Values are assigned
3. Functions are invoked


#### Example to Understand Execution Context
Creation Phase and Execution Phase ->

console.log(a);
var a = 10;

function test() {
    console.log("Hello");
}


- Creation Phase (Global Context)
Memory is allocated like this:

a → undefined
test → function definition

So internally, JS sees:
var a = undefined;

function test() {
    console.log("Hello");
}


- Execution Phase
Now code runs:
console.log(a); undefined
a = 10;

So output:
undefined

#### The Call Stack
Execution contexts are managed using a Call Stack (LIFO).

Example:

function one() {
    two();
}

function two() {
    console.log("Two");
}

one();

Call Stack Order:

1. Global Context pushed
2. `one()` pushed
3. `two()` pushed
4. `two()` popped
5. `one()` popped
6. Global popped


#### Hoisting Explained Properly
Hoisting means:
    -> During the creation phase, declarations are moved to memory before execution.

NOTE: Important:
-> Only declarations are hoisted, not initializations.
-> Hoisting happens before code execution.

#### Example 1. var Hoisting
console.log(a);
var a = 5;

Internally becomes:

var a;          // hoisted
console.log(a); // undefined
a = 5;

Output:
undefined

Because `a` is hoisted and initialized with `undefined` during creation phase.

#### Example 2. let and const Hoisting

console.log(a);
let a = 5;

This throws:
ReferenceError

Why?

Because `let` and `const` are hoisted BUT NOT initialized.

They stay in something called:
    Temporal Dead Zone (TDZ)

TDZ is the time between:
    Start of scope → until variable initialization

Example:
{
    console.log(a); ReferenceError
    let a = 10;
}

Even though `a` is hoisted, it’s in TDZ until execution reaches:
    let a = 10;

#### Example 3. Function Hoisting
1. Function Declaration

sayHi();

function sayHi() {
    console.log("Hi");
}

Works because:
    -> Entire function is hoisted with body.

2. Function Expression

sayHi();

var sayHi = function() {
    console.log("Hi");
};

Internally:

var sayHi;   // undefined
sayHi();     // TypeError

Because only the variable is hoisted, not the function body.

#### Deep Internal Structure of Execution Context
Each Execution Context contains:
    1. Variable Environment
    2. Lexical Environment
    3. This Binding

1. Variable Environment
Stores:
    1. var variables
    2. function declarations

2. Lexical Environment
Stores:
    1. let
    2. const
    3. block scope

3. Scope Chain
Used to resolve variables from outer scopes.

#### Advanced Example
var x = 1;

function foo() {
    console.log(x);
    var x = 2;
}

foo();

What happens?

1. Creation Phase of `foo`:
x → undefined

2. Execution:
console.log(x) → undefined
x = 2

Output:
undefined

NOT `1`.

Because local `x` shadows global `x`.

Visual Timeline

For:
console.log(a);
let a = 10;

Timeline:
Creation Phase:
a → uninitialized (TDZ)

Execution Phase:
console.log(a) → ReferenceError

#### JavaScript works like this:
1. Parse file
2. Create Global Execution Context
3. Hoist declarations into memory
4. Execute code line by line
5. Push new contexts on function calls
6. Pop them when finished

#### Summary Table
|---------------------------------------------------------------------------------------|
| Type                 | Hoisted?      | Initialized?  | Accessible before declaration? |
| -------------------- | ------------- | ------------- | ------------------------------ |
| var                  | Yes           | undefined     | Yes                            |
| let                  | Yes           | No (TDZ)      | No                             |
| const                | Yes           | No (TDZ)      | No                             |
| function declaration | Yes           | Full function | Yes                            |
| function expression  | Only variable | undefined     | No                             |
|---------------------------------------------------------------------------------------|

#### Summary
Execution Context is the environment in which JavaScript code runs. It is 
created in two phases (creation and execution), managed via the call stack, 
and during the creation phase, variable and function declarations are hoisted 
into memory.

#### Advanced Example Solution ->
var x = 1;

function foo() {
    console.log(x);
    var x = 2;
}

foo();


- Solution
- Explanation using execution context + hoisting.

Step 1: Global Execution Context (Creation Phase)

var x = 1;

function foo() {
    console.log(x);
    var x = 2;
}

During the creation phase of the Global Execution Context:
Memory becomes:

x → undefined
foo → function definition

Then execution phase assigns:
x = 1

Step 2: Calling `foo()`

When:
foo();

A new Function Execution Context (FEC) is created for `foo`.

1. Creation Phase of `foo`
Inside `foo`, JavaScript scans:

function foo() {
    console.log(x);
    var x = 2;
}

It sees:
var x;

So in memory inside `foo`:
x → undefined

NOTE: This "shadows" the global `x`.

Important:
    The function internally becomes:

function foo() {
    var x;          hoisted
    console.log(x);
    x = 2;
}

Step 3: Execution Phase of `foo`

Now line by line:
Line 1:
    console.log(x);
Which `x`?
    The "local x", not global.
And local `x` is currently:
    undefined
So it prints:
    undefined

Line 2:
    x = 2;
Now local `x` becomes 2.

Function ends.


NOTE: -> Why NOT 1?

Because of "variable shadowing".
The local `var x` inside `foo` takes priority over the global `x`.
Even though the assignment happens later, the declaration is hoisted to the 
top of the function.

#### Summary
Inside `foo`, JS treats it like:

function foo() {
    var x = undefined; hoisted
    console.log(x);
    x = 2;
}

Final Solution
    undefined
Because the local `var x` is hoisted and shadows the global `x`.
