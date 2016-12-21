var rock = "rock"
var paper = "paper"
var scissors = "scissors"

var moves = [rock, paper, scissors]

var winMoves = {
    rock: scissors,
    paper: rock,
    scissors: paper,
}

var playerWins = "<span class=\"player-win\">You win!</span>"
var opponentWins = "<span class=\"opponent-win\">You lose :(</span>"
var tie = "<span class=\"tie\">It's a tie!</span>"
var error = "Unknown move"

var numberOfWins = 0
var numberOfLoses = 0
var numberOfTies = 0
var numberOfPlays = 0

var opponentMoveClasses = document.getElementById("opponent-move").className + " "

function play(move) {
    var iaMove = chooseRandomElement(moves)
    var result = getResult(move, iaMove)

    document.getElementById("opponent-move").className = opponentMoveClasses + iaMove
    document.getElementById("result-message").innerHTML = result
    document.getElementById("share-score").innerHTML = "Share score: " + numberOfWins
    document.getElementById("result").style["display"] = "block"

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

// POST SCORE

var POST_SCORE_INTERVAL_MILLIS = 5000
var lastPostedScore = numberOfWins

function post_score() {
    if (lastPostedScore != numberOfWins) {
        submit_score(numberOfWins)
        lastPostedScore = numberOfWins
    }
}

window.setInterval(post_score, POST_SCORE_INTERVAL_MILLIS)
