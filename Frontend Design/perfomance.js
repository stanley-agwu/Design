// Debouncing and Throttling

/*
Some events fire too frequently (scroll, resize, keypress, mousemove), and 
thus, running expensive logic that each time significantly impacts (reduce) 
performance.
*/
// Debouncing
/*
Debouncing ensures a function runs only after a specified delay has passed 
since the last event.
If the event keeps firing, the timer resets.
Think of it as:
    “Wait until the user stops doing something.”
*/

// Design Use cases
/*
---------------------------------------------------------------------|
S/N   | Scenario            | Why Debounce?                          |
------|-------------------- |----------------------------------------|
 1.   | Search input        | Avoid API call on every keystroke      |
 2.   | Window resize       | Recalculate layout once after resizing |
 3.   | Auto-save draft     | Save only after user stops typing      |
 4.   | Live filtering      | Reduce unnecessary computation         |
----------------------------------------------------------------------
*/
// Implementation
function debounce(fn, delay) {
  let timer;

  return function (...args) {
    clearTimeout(timer);

    timer = setTimeout(() => {
      fn.apply(this, args);
    }, delay);
  };
}

// Debounce (Leading + Trailing)
/*
1. Execute immediately
2. Then ignore until delay passes
*/
function debounceI(fn, delay, immediate = false) {
  let timer;

  return function (...args) {
    const callNow = immediate && !timer;

    clearTimeout(timer);

    timer = setTimeout(() => {
      timer = null;
      if (!immediate) fn.apply(this, args);
    }, delay);

    if (callNow) fn.apply(this, args);
  };
}


// Throttling
/*
Throttling ensures a function runs at most once every specified interval.
1. It doesn’t wait for silence.
2. It limits frequency.

Think:
    “Run this at most once every 200ms.”
*/

// Design Use cases
/*
-----------------------------------------------------|
S/N | Scenario              | Why Throttle?          |
----|-----------------------|------------------------|
1.  | Scroll tracking       | Update progress bar    |
2.  | Mouse move            | Track pointer position |
3.  | Analytics events      | Avoid spamming logs    |
4.  | Realtime dashboard    | Controlled refresh     |
-----------------------------------------------------|
*/

// Implementation
function throttle(fn, interval) {
  let lastTime = 0;

  return function (...args) {
    const now = Date.now();

    if (now - lastTime >= interval) {
      lastTime = now;
      fn.apply(this, args);
    }
  };
}

// Example Throttle

function handleScroll() {
  console.log("Scroll Y:", window.scrollY);
}

window.addEventListener("scroll", throttle(handleScroll, 200));


// Throttle (Trailing Option)
/*
This ensures:
1. Leading execution
2. Trailing execution
*/
function throttleT(fn, interval) {
  let lastTime = 0;
  let timer;

  return function (...args) {
    const now = Date.now();
    const remaining = interval - (now - lastTime);

    if (remaining <= 0) {
      clearTimeout(timer);
      timer = null;
      lastTime = now;
      fn.apply(this, args);
    } else if (!timer) {
      timer = setTimeout(() => {
        lastTime = Date.now();
        timer = null;
        fn.apply(this, args);
      }, remaining);
    }
  };
}


// Performance Enhancements -> With debounce/throttle:
/*
1. CPU usage drops (From reduced scroll, mousemove, keypress events).
2. Network usage drops (From unneccessary/multitude of API calls).
3. Layout thrashing reduced.
4. Battery usage reduced.
*/

// Summary
/*
Debouncing delays execution until activity stops.
Throttling limits execution rate during activity.
*/
