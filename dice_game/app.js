const n = 5;
let rad1 = Math.floor(Math.random() * n);
let rad2 = Math.floor(Math.random() * n);
const radArry = [
  "images/dice1.png",
  "images/dice2.png",
  "images/dice3.png",
  "images/dice4.png",
  "images/dice5.png",
  "images/dice6.png",
];
console.log(radArry);
document.querySelector(".img1").setAttribute("src", radArry[rad1]);
document.querySelector(".img2").setAttribute("src", radArry[rad2]);
console.log(rad1, rad2);

if (rad1 > rad2) {
  document.querySelector("h1").innerHTML = "player 1 wins";
} else if (rad2 > rad1) {
  document.querySelector("h1").innerHTML = "player 2 wins";
} else {
  document.querySelector("h1").innerHTML = "draw";
}
