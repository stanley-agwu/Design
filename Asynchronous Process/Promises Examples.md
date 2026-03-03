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
