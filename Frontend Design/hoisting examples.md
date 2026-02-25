# Hoisting Examples

### Hoisting Q1
What is result of the following code execution?

```js
var x = 1;

function foo() {
    console.log(x);
    x = 2;
}

foo();
console.log(x);
```

### Solution Q1
There is "no local declaration" inside `foo`.

So during execution:

1. `console.log(x)` → looks for `x` in local scope → not found
2. Looks in outer (global) scope → finds `x = 1`

So it prints:
    `1`
Then:
    `x = 2;``

It updates the "global variable".
So final output:
    `1`
    `2`

Final Result
    `1`
    `2`
Because no shadowing happens.

### Hoisting Q2.
What is result of the following code execution?

```js
var x = 1;

function foo() {
    console.log(x);
    let x = 2;
}

foo();
```

### Solution Q2.
This throws:
ReferenceError: Cannot access 'x' before initialization

Why?
This is because `let` is:
    1. Hoisted
    2. But "NOT initialized"
    3. Placed in the **Temporal Dead Zone (TDZ)**

Inside `foo`, JS sees:
`let x;`

But it is in TDZ until this line runs:
    `let x = 2;`

So when we do:
    `console.log(x);`
JS finds the "local `x` first" (due to lexical scope),
but it is in TDZ → ReferenceError.

Key Difference ->
With `var` → prints `undefined`
With `let` → throws `ReferenceError`

### Hoisting Q3.
What is result of the following code execution?

```js
var x = 1;

function foo() {
    console.log(x);
    if (true) {
        var x = 2;
    }
}

foo();
```

### Solution Q3.
Output:
    `undefined`
Why?
    Because `var` is "function-scoped", not block-scoped.
JS internally transforms it to:

```js
function foo() {
    var x;        // hoisted to function top
    console.log(x);
    if (true) {
        x = 2;
    }
}
```

So `x` inside `foo` shadows global `x`.
At time of logging:

`x === undefined`


### Hoisting Q4.
What is result of the following code execution?

```js
var x = 1;

function foo(x) {
    console.log(x);
    var x = 2;
}

foo();
```

### Solution Q4.
output
    `undefined`
Why?
    Because parameters are also part of function scope.

Internally becomes:

```js
function foo(x) {
    var x;       // ignored because already declared
    console.log(x);
    x = 2;
}
```

Since no argument is passed:
`x === undefined`

### Hoisting Q5.
What is result of the following code execution?

```js
let x = 1;

function foo() {
    console.log(x);
    {
        let x = 2;
    }
}

foo();
```

### Solution Q5.
Output:
    `1`
Because block-scoped `x` does NOT affect outer one.


### Hoisting Q6.
What is result of the following code execution?

```js
var x = 1;

function foo() {
    console.log(x);
    x = 2;
    var x;
}

foo();
```

### Solution Q6.
Output:
    `undefined`
Even though assignment comes before `var`.
Because hoisting makes it:

```js
function foo() {
    var x;
    console.log(x);
    x = 2;
}
```

*NOTE: ->*
-> JavaScript resolves variables lexically.

-> `var` → function-scoped
-> `let/const` → block-scoped
-> Hoisting happens before code execution.
