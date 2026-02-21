// Currying

/*
Currying transforms a function with multiple arguments into a sequence of 
functions, each taking one argument.
*/
// Normal Function
function add(a, b, c) {
  return a + b + c;
}

add(1, 2, 3); // 6

// Curried Version
function addC(a) {
  return function (b) {
    return function (c) {
      return a + b + c;
    };
  };
}

add(1)(2)(3); // 6

/*
Thus, instead of f(a, b, c), we have f(a)(b)(c)
*/
