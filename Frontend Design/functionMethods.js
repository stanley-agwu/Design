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

// 2. Function.prototype.apply
// apply() -> functionName.apply(thisArg, [arg1, arg2, ...])

// Works just like call(), but arguments are passed as an array.
/*
1. Calls the function immediately.
2. Arguments are passed as an array.
3. Explicitly sets this.
*/

function sayWeather(temperature, windSpeed, humidity){
    return `Hello ${this.name}!, the weather says, temperature is 
        ${temperature}°C, wind speed is ${windSpeed} and a humidity of ${humidity}.`
}

console.log(sayWeather(32, '42mph', '30 g/m³'))
console.log(sayWeather.apply(person, [32, '42mph', '30 g/m³']))

// 3. Function.prototype.bind
// bind() -> const newFunction = functionName.bind(thisArg, arg1, arg2, ...)


// Returns a new function with this permanently set. It does NOT execute immediately.
/*
1. Does NOT run immediately
2. Returns a new function
3. Can preset arguments (partial application)
*/
function locationTemperature(temperature, location){
    return `Hello ${this.name}!, the temperature in ${location} today is ${temperature}°C.`
}

const bindFunc = locationTemperature.bind(person);

console.log(bindFunc(-12, 'France'));
console.log(bindFunc(25, 'Barcelona'));
