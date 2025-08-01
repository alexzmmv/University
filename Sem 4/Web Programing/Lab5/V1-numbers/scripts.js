var emptyCell = 9;

function isSolvable(puzzle) {
  let inversions = 0;
  for (let i = 0; i < puzzle.length; i++) {
    for (let j = i + 1; j < puzzle.length; j++) {
      if (puzzle[i] > puzzle[j] && puzzle[i] !== 9 && puzzle[j] !== 9) {
        inversions++;
      }
    }
  }
  return inversions % 2 === 0;
}

function loadPuzzle() {
  let puzzle;
  do {
    puzzle = [];
    for (let i = 1; i <= 9; i++) {
      puzzle.push(i);
    }
    puzzle.sort(() => Math.random() - 0.5);
  } while (!isSolvable(puzzle));

  emptyCell = puzzle.indexOf(9) + 1;

  for (let i = 1; i <= 9; i++) {
    const cell = document.getElementById(i);
    if (cell) {
      if (i !== emptyCell) {
        cell.textContent = puzzle[i - 1] !== 9 ? puzzle[i - 1] : "";
      } else {
        cell.textContent = "";
      }
    }
  }
}

function move(cellID, cell) {
  if (cellID == emptyCell) return;
  rest = cellID % 3;
  topPos = cellID > 3 ? cellID - 3 : -1;
  bottomPos = cellID < 7 ? cellID + 3 : -1;
  leftPos = rest != 1 ? cellID - 1 : -1;
  rightPos = rest > 0 ? cellID + 1 : -1;

  if (emptyCell != topPos && emptyCell != bottomPos && emptyCell != leftPos && emptyCell != rightPos)
    return;

  const emptyCellElement = document.getElementById(emptyCell);
  const temp = cell.textContent;
  cell.textContent = "";
  emptyCellElement.textContent = temp;
  emptyCell = cellID;
  checkWin();
}

function checkWin() {
  for (let i = 1; i <= 8; i++) {
    const cell = document.getElementById(i);
    if (cell.textContent != i.toString()) return;
  }
  const lastCell = document.getElementById(9);
  if (lastCell.textContent === "") {
    alert("Congratulations! You won!");
  }
}
