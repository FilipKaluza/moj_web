let doorImage1 = document.getElementById("door1");
let doorImage2 = document.getElementById("door2");
let doorImage3 = document.getElementById("door3");
let botDoorPath = "https://s3.amazonaws.com/codecademy-content/projects/chore-door/images/robot.svg";

let beachDoorPath = "https://s3.amazonaws.com/codecademy-content/projects/chore-door/images/beach.svg";

let spaceDoorPath = "https://s3.amazonaws.com/codecademy-content/projects/chore-door/images/space.svg";

let closedDoorPath = "https://s3.amazonaws.com/codecademy-content/projects/chore-door/images/closed_door.svg";

let numClosedDoors = 3;
let openDoor1;
let openDoor2;
let openDoor3;

let currentlyPlaying = true;

let startButton = document.getElementById("start");

const isBot = door => {
    if (door.src === botDoorPath) {
      return true;
    } else {
      return false;
    }
}

const isClicked = (door) => {
    if (door.src === closedDoorPath) {
      return false;
    } else {
      return true;
    }
}

const playDoor = (door) => {
    numClosedDoors--;
    if (numClosedDoors === 0) {
      gameOver("win");
    } else if (isBot(door) === true) {
      gameOver()
    }
};


const randomChoreDoorGenerator = () => {
    choreDoor = Math.floor(Math.random() * numClosedDoors);
    if (choreDoor === 0) {
      openDoor1 = botDoorPath;
      openDoor2 = beachDoorPath;
      openDoor3 = spaceDoorPath;
    } else if (choreDoor === 1) {
      openDoor2 = botDoorPath;
      openDoor1 = beachDoorPath;
      openDoor3 = spaceDoorPath;
    } else if (choreDoor === 2) {
      openDoor3 = botDoorPath;
      openDoor1 = spaceDoorPath;
      openDoor2 = beachDoorPath;
    }
};

doorImage1.onclick = () => {
    if (!isClicked(doorImage1) && currentlyPlaying) {
      doorImage1.src = openDoor1;
      playDoor(doorImage1);
    }
}

doorImage2.onclick = () => {
    if (!isClicked(doorImage2) && currentlyPlaying) {
      doorImage2.src = openDoor2;
      playDoor(doorImage2);
    }
}
doorImage3.onclick = () => {
    if (!isClicked(doorImage3) && currentlyPlaying) {
      doorImage3.src = openDoor3;
      playDoor(doorImage3);
    }
}

startButton.onclick = () => {
    if (!currentlyPlaying) {
      startRound();
    }
}

const startRound = () => {
    numClosedDoors = 3;
    currentlyPlaying = true;
    startButton.innerHTML = "Good Luck!";
    doorImage1.src = closedDoorPath;
    doorImage2.src = closedDoorPath;
    doorImage3.src = closedDoorPath;
    randomChoreDoorGenerator();
}


const gameOver = (status) => {
    status;
    if (status === "win") {
      startButton.innerHTML = "You Win! Play again?";
    } else {
      startButton.innerHTML = "Game over! Play again?"
    }
    currentlyPlaying = false;
}

gameIsRunning = true;

const startGame = (time) => {
    let intro = document.getElementsByClassName("fading");
    let choredoor = document.getElementsByClassName("choredoor");
    setTimeout( () => {
        intro[0].style.display = "none";
        for (let i=0;i<choredoor.length;i++){
          choredoor[i].style.display = 'block';
        }
    }, time);
}

const makeVissible = () => {
  if (gameIsRunning === true) {
    startGame(5000)
  }
}


makeVissible()
startRound()