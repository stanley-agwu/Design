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

