# Callback, Promise, Async-Await

### Callback
A callback is a function passed into another function to be executed later.

##### Example

```js
function greet(name, callback) {
    console.log("Hello " + name);
    callback();
}

function sayBye() {
    console.log("Goodbye!");
}

greet("Stanley", sayBye);
```

### Callback Problem -> Callback Hell

```js
getUser(userId, function(user) {
    getOrders(user.id, function(orders) {
        getPayment(orders[0], function(payment) {
            console.log(payment);
        });
    });
});
```

This becomes:
1. Hard to read.
2. Hard to maintain.
3. Hard to handle errors.

That’s why Promises were introduced.

### Promise
A Promise represents a value that may be available now, later, or never.
A Promise has 3 states:
1. Pending
2. Fulfilled
3. Rejected

#### Creating a Promise

```js
const examplePromise = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve("Success!");
        // reject("Error!");
    }, 1000);
});
```

#### Consuming a Promise

```js
examplePromise
    .then((result) => {
        console.log(result);
    })
    .catch((error) => {
        console.log(error);
    })
    .finally(() => {
        console.log("Done");
    });
```

#### Promise Chain
Much cleaner than callback hell.

```js
fetchUser()
    .then(user => fetchOrders(user.id))
    .then(orders => fetchPayment(orders[0]))
    .then(payment => console.log(payment))
    .catch(err => console.error(err));
```

### Promise Static Methods
These are methods on the Promise constructor.

#### Promise.resolve()
Creates resolved promise.

```js
Promise.resolve(42)
    .then(value => console.log(value));
```

#### Promise.reject()

```js
Promise.reject("Error")
    .catch(err => console.log(err));
```

#### Promise.all()
1. Waits for all promises to succeed.
2. If one fails → entire thing fails.

```js
Promise.all([
    fetchUser(),
    fetchOrders(),
    fetchPayments()
])
.then(results => console.log(results))
.catch(err => console.log(err));
```

#### Promise.allSettled()
Waits for all promises, regardless of success/failure.

```js
Promise.allSettled([
    Promise.resolve("A"),
    Promise.reject("B")
])
.then(results => console.log(results));
```

##### Output

```js
[
  { status: "fulfilled", value: "A" },
  { status: "rejected", reason: "B" }
]
```

#### Promise.race()
Returns first settled promise (success or fail).

```js
Promise.race([
    slowRequest(),
    fastRequest()
])
.then(result => console.log(result));
```

#### Promise.any()
1. Returns first fulfilled promise.
2. Fails only if ALL fail.

```js
Promise.any([
    Promise.reject("A"),
    Promise.resolve("B"),
])
.then(result => console.log(result));
```

##### Output
B

### Async / Await
async/await is syntactic sugar over Promises.

#### Basic Example

```js
async function fetchData() {
    return "Hello";
}

fetchData().then(console.log);
```

An async function always returns a Promise.

#### Using Await

```js
function delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function run() {
    console.log("Start");
    await delay(1000);
    console.log("After 1 second");
}

run();
```

### Error Handling

```js
async function test() {
    try {
        const data = await fetchUser();
        console.log(data);
    } catch (err) {
        console.error(err);
    }
}
```

- Equivalent to .then().catch().

### Important: Async Execution Model
JavaScript is:
    Single-threaded, non-blocking, event-loop driven.

There are:
1. Call Stack
2. Web APIs
3. Callback Queue/Task Queue/Macro-task Queue
4. Microtask Queue (Promises live here)

#### Example -> What will be the output

```js
console.log("1");

setTimeout(() => console.log("2"), 0);

Promise.resolve().then(() => console.log("3"));

console.log("4");
```

#### Output:
1
4
3
2

Why?

#### Order of execution:
Synchronous code → 1
Synchronous code → 4
Microtasks (Promises) → 3
Macrotasks (setTimeout) → 2

NOTE: Promise callbacks run before setTimeout.

### Advanced Interview Comparison
------------------------------------------------------------------|
| Feature            | Callback | Promise     | Async/Await       |
| ------------------ | -------- | ----------- | ----------------- |
| Readability        | Low      | Medium      | High              |
| Error handling     | Manual   | .catch()    | try/catch         |
| Chaining           | Nested   | Flat chain  | Sequential        |
| Parallel execution | Hard     | Promise.all | await Promise.all |
------------------------------------------------------------------|

### When to Use What?
1. Simple async → Callback
2. Complex chaining → Promise
3. Clean readable async code → Async/Await
4. Parallel tasks → Promise.all + await

### Quick Ultimate Mental Model
1. Callback → "Call me later"
2. Promise → "I promise to give you result"
3. Async/Await → "Wait here until promise resolves"
