var emptyCell = [16, 15];

function isSolvable(puzzle) {
  let inversions = 0;
  for (let i = 0; i < puzzle.length; i++) {
    for (let j = i + 1; j < puzzle.length; j++) {
      if (puzzle[i] > puzzle[j] && puzzle[i] !== 16 && puzzle[i] !== 15 && puzzle[j] !== 16 && puzzle[j] !== 15) {
        inversions++;
      }
    }
  }
  return inversions % 2 === 0;
}

function showoriginal() {
  emptyCell = [16, 15];
  
  for (let i = 1; i <= 16; i++) {
    const cell = document.getElementById(i);
    if (cell) {
      if (emptyCell.indexOf(i) === -1) {
        cell.style.backgroundImage = `url('../output_parts/${i}.png')`;
      } else {
        cell.style.backgroundImage = "";
      }
    }
  }
  
}

function loadPuzzle() {
  let puzzle;
  do {
    puzzle = [];
    for (let i = 1; i <= 16; i++) {
      puzzle.push(i);
    }
    puzzle.sort(() => Math.random() - 0.5);
  } while (!isSolvable(puzzle));

  emptyCell = [puzzle.indexOf(16) + 1, puzzle.indexOf(15) + 1];

  for (let i = 1; i <= 16; i++) {
    const cell = document.getElementById(i);
    if (cell) {
      if (puzzle[i - 1] !== 16 && puzzle[i - 1] !== 15) {
        cell.style.backgroundImage = `url('../output_parts/${puzzle[i - 1]}.png')`;
      } else {
        cell.style.backgroundImage = "";
      }
    }
  }
}

function move(cellID, cell) {
  if (emptyCell.includes(cellID)) return;
  
  const row = Math.ceil(cellID / 4);
  const col = cellID % 4 === 0 ? 4 : cellID % 4;
  
  let adjacentEmptyCell = null;
  
  for (let i = 0; i < emptyCell.length; i++) {
    const emptyID = emptyCell[i];
    const emptyRow = Math.ceil(emptyID / 4);
    const emptyCol = emptyID % 4 === 0 ? 4 : emptyID % 4;
    
    if ((Math.abs(row - emptyRow) === 1 && col === emptyCol) || (Math.abs(col - emptyCol) === 1 && row === emptyRow)) {
      adjacentEmptyCell = emptyID;
      break;
    }
  }
  
  if (adjacentEmptyCell) {
    const emptyCellElement = document.getElementById(adjacentEmptyCell);
    const temp = cell.style.backgroundImage;
    cell.style.backgroundImage = "";
    emptyCellElement.style.backgroundImage = temp;
    
    const index = emptyCell.indexOf(adjacentEmptyCell);
    if (index !== -1) {
      emptyCell[index] = cellID;
    }
    
  }
  checkWin();
}

function checkWin() {
  for (let i = 1; i <= 14; i++) {
    const cell = document.getElementById(i);
    const expectedImage = `url("../output_parts/${i}.png")`;
    if (cell.style.backgroundImage !== expectedImage) return;
  }
  
  const cell15 = document.getElementById(15);
  const cell16 = document.getElementById(16);
  
  if (cell15.style.backgroundImage === "" && cell16.style.backgroundImage === "") {
    alert("Congratulations! You won!");
  }
}
