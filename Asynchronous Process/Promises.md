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

