// Function.prototype methods

// Call, Bind and Apply

// 1. Function.prototype.call
// call() -> functionName.call(thisArg, arg1, arg2, ...)

// Invokes (executes) a function immediately, and lets you set the value of this.
/*
1. Calls the function immediately.
2. Arguments are passed one by one.
3. Explicitly sets this.
*/

const person = { name: 'Teddy' };

function sayTemperature(temperature){
    return `Hello ${this.name}!, the temperature is ${temperature}°C.`
}

console.log(sayTemperature(32))
console.log(sayTemperature.call(person, 32))
console.log(this)
