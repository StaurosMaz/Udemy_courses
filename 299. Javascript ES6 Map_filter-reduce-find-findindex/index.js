var numbers = [3, 56, 2, 48, 5];

//Map -Create a new array by doing something with each item in an array.
function double(x) {
  return x * 2;
}

console.log(numbers.map(double));

//Filter - Create a new array by keeping the items that return true.
const nums = numbers.filter(function (x) {
  return x > 10;
});
console.log(nums);

//Reduce - Accumulate a value by doing something to each item in an array.
const redNum = numbers.reduce(function (acc, currentNum) {
  return acc + currentNum;
});
console.log(redNum);

//Find - find the first item that matches from an array.
const findNum = numbers.find(function (num) {
  return num > 10;
});
console.log(findNum);

//FindIndex - find the index of the first item that matches.
const findNumIndex = numbers.findIndex(function (num) {
  return num > 10;
});
console.log(findNumIndex);
