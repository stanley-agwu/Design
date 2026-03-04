# Promises Examples

#### Example 1 -> what will the following code output:

```js
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

wait(0).then(() => console.log(4));
Promise.resolve()
  .then(() => console.log(2))
  .then(() => console.log(3));

console.log(1);
```
##### Output
// 1, 2, 3, 4
-----------------------------------------------------------------------------
#### Example 2 -> what will the following code output:

```js
const wait = (ms) => new Promise((resolve) => {
    console.log(0);
    setTimeout(resolve, ms);
});

(async () => {
    wait(0).then(() => console.log(4));
    Promise.resolve()
    .then(() => console.log(2))
    .then(() => console.log(3));

    console.log(1);
})();
```

##### Solution
1. Promise executor (callback) → runs now (immediately like sync task)
2. .then → are pushed/moved to Microtask queue to be executed
3. setTimeout → are moved to Web API/timers to complete its time before being moved to the Task Queue where it runs as a macrotask
4. All microtasks always run before the next macrotask

##### Output
// 0, 1, 2, 3, 4
----------------------------------------------------------------------------
#### Example 3 -> Task queues vs. microtasks
Promise callbacks are handled as a microtask whereas setTimeout() callbacks are handled as macrotasks in the Task queue.

```js
const promise = new Promise((resolve, reject) => {
  console.log("Promise callback");
  resolve();
}).then(() => {
  console.log("Promise callback (.then)");
});

setTimeout(() => {
  console.log("event-loop cycle: Promise (fulfilled)", promise);
}, 0);

console.log("Promise (pending)", promise);
```

##### Output
Promise callback
Promise (pending) Promise {<pending>}
Promise callback (.then)
event-loop cycle: Promise (fulfilled) Promise {<fulfilled>}
----------------------------------------------------------------------------
#### Example 4

```js
const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

wait(0).then(() => console.log(4));
Promise.resolve()
  .then(() => console.log(2))
  .then(() => console.log(3));

console.log(1);
```

##### Output
1, 2, 3, 4
-----------------------------------------------------------------------------
#### Example 5 -> How long will the Promise.all resolve?

```js
function fib(n){
    table = new Array(n + 1).fill(0)
    table[1] = 1
    for (let i = 0; i < n - 1; i += 1) {
        table[i + 2] = table[i] + table[i + 1]
    }
    return table[n]
}

function getFib(num){
    return new Promise((resolve) => {
        setTimeout(() =>
    {
        resolve(fib(num))
    }, 2000)
})};

const result = Promise.all([
    getFib(20),
    getFib(30),
    getFib(25),
]);
```

#### Output
`~2 second`

All three `getFib` calls are started immediately and in parallel.

Promise.all:
1. Waits for all promises
2. Resolves when the slowest one resolves
3. Rejects if any reject

Since all three:
    Take 2 seconds
    Start at the same time
    The total time = `max(2s, 2s, 2s) = 2s`


### Important Concept
There are two types of **waiting**:

1. Non-blocking wait (like setTimeout)
JS delegates waiting to Web APIs → timers run concurrently.

2. Blocking CPU work
If fib() was extremely heavy like:

`while(true) {}`

That would block the single thread.
-----------------------------------------------------------------------------
### Example 6 -> How long will the Promise.all resolve?

```js
function delay(ms) {
  return new Promise(resolve => setTimeout(() => {
    console.log("Run delay!");
    resolve();
  }, ms));
}

async function run() { 
    console.log("Start"); 
    await delay(1000); 
    console.log("After 1 second"); 
} 
    
run();
```

#### Output
Start
(1 second later)
Run delay!
After 1 second

**NOTE**: await pauses execution until resolution.
Because await pauses the async function, even though JavaScript itself is single-threaded.

**Important Concept**
Inside an async function:
    - Everything after await is no longer part of the current synchronous execution.
It is moved into a microtask.
-----------------------------------------------------------------------------
### Even If Promise Resolves Immediately

```js
async function test() {
    console.log("A");
    await Promise.resolve();
    console.log("B");
}

test();
console.log("C");
```

#### Output
A
C
B

Why?
Because even resolved promises resume in a microtask, not immediately.

**Core Insight**
await does NOT block JavaScript.

It:
1. Pauses only the async function
2. Schedules continuation as a microtask
3. Lets other code run
--------------------------------------------------------------------------
