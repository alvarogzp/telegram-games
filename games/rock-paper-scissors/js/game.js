var rock = "rock"
var paper = "paper"
var scissors = "scissors"

var moves = [rock, paper, scissors]

var winMoves = {
    rock: scissors,
    paper: rock,
    scissors: paper,
}

var playerWins = "You win!"
var opponentWins = "You lose :("
var tie = "It's a tie!"
var error = "Unknown move"

var numberOfWins = 0
var numberOfLoses = 0
var numberOfTies = 0
var numberOfPlays = 0

function play(move) {
    var iaMove = chooseRandomElement(moves)
    var result = getResult(move, iaMove)

    document.getElementById("your-move").innerHTML = move
    document.getElementById("your-move-message").style["display"] = "block"
    document.getElementById("opponent-move").innerHTML = iaMove
    document.getElementById("opponent-move-message").style["display"] = "block"
    document.getElementById("result-message").innerHTML = result
    document.getElementById("number-wins").innerHTML = numberOfWins
    document.getElementById("number-loses").innerHTML = numberOfLoses
    document.getElementById("number-ties").innerHTML = numberOfTies
    document.getElementById("number-plays").innerHTML = numberOfPlays
}

function getResult(playerMove, opponentMove) {
    numberOfPlays++
    if (winMoves[playerMove] == opponentMove) {
        numberOfWins++
        return playerWins
    } else if (playerMove == winMoves[opponentMove]) {
        numberOfLoses++
        return opponentWins
    } else if (playerMove == opponentMove) {
        numberOfTies++
        return tie
    } else {
        return error
    }
}

function chooseRandomElement(array) {
    return array[Math.floor(Math.random() * array.length)]
}
