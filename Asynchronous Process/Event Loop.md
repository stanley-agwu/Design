# Asynchronous Javascript

### Event Loop
The Event Loop is the mechanism that allows JavaScript (which is single-threaded) to handle asynchronous operations without blocking execution.

JavaScript runtime (Browser or Node.js) consists of:
1. Call Stack
2. Web APIs / Node APIs
3. Task Queue (Macrotask Queue)
4. Microtask Queue
5. Event Loop

##### 1. Call Stack (Synchronous Execution)
JS executes one function at a time
Functions are pushed onto the stack and popped when done
If the stack is busy → nothing else runs

"""
function a() {
  b();
}
function b() {
  console.log("Hello");
}
a();
"""

Execution order:
a → b → console.log → pop → pop

-> Blocking: long-running code freezes everything.

##### 2. Web APIs (Async Offloading)
When JS encounters async operations, they are delegated to the environment:
1. setTimeout
2. setInterval
3. fetch
4. DOM events
5. Promises (resolution handled specially)

setTimeout(() => console.log("Done"), 1000);

What happens:
Timer is handled outside the Call Stack
JS continues immediately

##### 3. Task Queue (Macrotask Queue)
Also called Callback Queue or Macrotask Queue.

It Contains callbacks from:
1. setTimeout
2. setInterval
3. DOM events
4. setImmediate (Node)

Example:
setTimeout(() => console.log("Macrotask"), 0);

-> Executed after Call Stack is empty.

##### 4. Microtask Queue (HIGH PRIORITY)
Microtasks run before macrotasks.

Sources:
1. Promise.then / catch / finally
2. queueMicrotask
3. MutationObserver

Promise.resolve().then(() => console.log("Microtask"));

##### 5. The Event Loop (The Orchestrator)
The Event Loop constantly checks:
1. Is the Call Stack empty?
2. If yes → run all microtasks
3. Then → run one macrotask
4. Repeat forever

###### Priority Order
Call Stack
↓
Microtask Queue (ALL)
↓
Macrotask Queue (ONE)
↓
Render (browser)
↓
Repeat

##### Classic Example:
console.log("Start");
setTimeout(() => console.log("Timeout"), 0);
Promise.resolve().then(() => console.log("Promise"));
console.log("End");

##### Execution Order
Start
End
Promise
Timeout

##### Why?
Step	                      Explanation
Start	                      Sync → Call Stack
setTimeout	                Goes to Web API
Promise.then	              Goes to Microtask Queue
End	                        Sync
Microtasks	                Promise executes
Macrotasks	                Timeout executes

##### Infinite Microtask Starvation (Important!)
function loop() {
  Promise.resolve().then(loop);
}
loop();


- Macrotasks never run
- Browser UI freezes
- This is why microtasks are dangerous if abused

##### Browser Rendering vs Event Loop
In browsers:
- Rendering happens between macrotasks
- Microtasks block rendering

Promise.resolve().then(() => {
  while (true) {} // freezes UI
});

#### Node.js Event Loop
Node.js has phases:
1. Timers
2. I/O callbacks
3. Idle / prepare
4. Poll
5. Check (setImmediate)
6. Close callbacks

- NOTE: process.nextTick runs before microtasks (highest priority)

##### Mental Model (Best Way to Remember)
JavaScript runs synchronous code first, then empties microtasks, then runs one macrotask, repeat process forever.

##### When You should Actually CARE About the Event Loop
1. Debugging async bugs
2. Promise vs setTimeout ordering
3. Performance optimization
4. Avoiding UI freezes
5. Writing libraries / frameworks

##### Summary
The Event Loop enables non-blocking asynchronous behavior in JavaScript by coordinating the Call Stack, Microtask Queue, and Macrotask Queue in a strict priority order.