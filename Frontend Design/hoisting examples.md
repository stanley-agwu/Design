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
