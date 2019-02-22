package main

import (
	"fmt"
	"strings"
)

// Question: Sudoku Solver
//
// 		Write a program to solve a Sudoku puzzle by filling the empty cells.
// 		A sudoku solution must satisfy all of the following rules:
// 			1. Each of the digits 1-9 must occur exactly once in each row.
//			2. Each of the digits 1-9 must occur exactly once in each column.
//			3. Each of the the digits 1-9 must occur exactly once in each of the 9 3x3 sub-boxes of the grid.
//		Empty cells are indicated by the character '.'.
//
// Input:
//
//		Sudoku board
//
// Output:
//
// 		Filled board
//
// Sample:
//
// 		input:
// 		[
// 			["5","3",".",  ".","7",".",  ".",".","."],
// 			["6",".",".",  "1","9","5",  ".",".","."],
// 			[".","9","8",  ".",".",".",  ".","6","."],
//
// 			["8",".",".",  ".","6",".",  ".",".","3"],
// 			["4",".",".",  "8",".","3",  ".",".","1"],
// 			["7",".",".",  ".","2",".",  ".",".","6"],
//
// 			[".","6",".",  ".",".",".",  "2","8","."],
// 			[".",".",".",  "4","1","9",  ".",".","5"],
// 			[".",".",".",  ".","8",".",  ".","7","9"]
// 		]
// 		output:
//		[
//			["5","3","4",  "6","7","8",  "9","1","2"],
//			["6","7","2",  "1","9","5",  "3","4","8"],
//			["1","9","8",  "3","4","2",  "5","6","7"],
//
//			["8","5","9",  "7","6","1",  "4","2","3"],
//			["4","2","6",  "8","5","3",  "7","9","1"],
//			["7","1","3",  "9","2","4",  "8","5","6"],
//
//			["9","6","1",  "5","3","7",  "2","8","4"],
//			["2","8","7",  "4","1","9",  "6","3","5"],
//			["3","4","5",  "2","8","6",  "1","7","9"]
//		]
//
// AC: 100%
//
// URL: https://leetcode.com/problems/sudoku-solver/

// Game ...
type Game struct {
	board [][]byte			// game board
	cands [][]map[byte]byte	// cells possible candidates
	filled map[[2]int]int	// filled cells
	frontier []Cell			// frontier to explore
}

// Cell ...
type Cell struct {
	row int		// cell row index
	col int		// cell col index
	num byte	// cell value
}

// fork a new game based on provide one
func forkGame(game *Game) *Game {

	// fork game.board
	newBorad := [][]byte{}
	for _, row := range game.board {
		newRow := []byte{}
		for _, col := range row {
			newRow = append(newRow, col)
		}
		newBorad = append(newBorad, newRow)
	}

	// fork game.cands
	newCands := [][]map[byte]byte{}
	for _, row := range game.cands {
		newRow := []map[byte]byte{}
		for _, col := range row {
			newCell := map[byte]byte{}
			for _, val := range col {
				newCell[val] = val
			}
			newRow = append(newRow, newCell)
		}
		newCands = append(newCands, newRow)
	}

	// fork game.filled
	newFilled := map[[2]int]int{}
	for key, val := range game.filled {
		newFilled[key] = val
	}

	// fork game.frontier
	newFrontier := []Cell{}
	for _, item := range game.frontier {
		newFrontier = append(newFrontier, item)
	}

	newGame := Game{newBorad, newCands, newFilled, newFrontier}
	return &newGame
}

// fork game.board
func copyBoard(target, board [][]byte) {

	// fork board
	for i, row := range target {
		for j, col := range row {
			board[i][j] = col
		}
	}
}

// get game board initial frontier
func initFrontier(board [][]byte) []Cell {
    frontier := []Cell{}

    // get initial filled cells as frontier
    for i := 0; i < 9; i++ {
        for j := 0; j < 9; j++ {
            if board[i][j] != '.' {
                frontier = append(frontier, Cell{i, j, board[i][j]})
            }
        }
    }
    return frontier
}

// get game initial cells possible candidates
func initCands() [][]map[byte]byte {
    cands := [][]map[byte]byte{}

    // get initial candidates
    for i := 0; i < 9; i++ {
        row := []map[byte]byte{}
        for j := 0; j < 9; j++ {
            cell := map[byte]byte{'1':'1', '2':'2', '3':'3',
            	'4':'4', '5':'5', '6':'6', '7':'7', '8':'8', '9':'9'}
            row = append(row, cell)
        }
        cands = append(cands, row)
    }
    
    return cands
}

// kick out impossible candidates
func kickCands(game *Game, cand Cell) bool {
	row, col, num := cand.row, cand.col, cand.num
    
    if game.filled[[2]int{row, col}] == 1 {
        return true
    }
    
    // clear row
    for j := 0; j < 9; j++ {
        if j == col {
            continue
        }

		delete(game.cands[row][j], num)
		// empty candidate list means conflict
		if len(game.cands[row][j]) == 0 {
			return false
		}

        // final candidate and the cell has not been filled
        if len(game.cands[row][j]) == 1 && game.filled[[2]int{row, j}] == 0 {
			for _, rest := range game.cands[row][j] {
				game.frontier = append(game.frontier, Cell{row, j, rest})
			}
        }
    }
    
    // clear col
    for i := 0; i < 9; i++ {
        if i == row {
            continue
        }

		delete(game.cands[i][col], num)
		// empty candidate list means conflict
		if len(game.cands[i][col]) == 0 {
			return false
		}

		// final candidate and the cell has not been filled
		if len(game.cands[i][col]) == 1 && game.filled[[2]int{i, col}] == 0 {
			for _, rest := range game.cands[i][col] {
				game.frontier = append(game.frontier, Cell{i, col, rest})
			}
        }
    }
    
    // clear small map
	mapRow, mapCol := row/3, col/3
	mapRow, mapCol  = mapRow*3, mapCol*3
    for i := mapRow; i < mapRow+3; i++ {
        for j := mapCol; j < mapCol+3; j++ {
            if i == row && j == col {
                continue
            }

			delete(game.cands[i][j], num)
			// empty candidate list means conflict
			if len(game.cands[i][j]) == 0 {
				return false
			}

			// final candidate and the cell has not been filled
			if len(game.cands[i][j]) == 1 && game.filled[[2]int{i, j}] == 0 {
				for _, rest := range game.cands[i][j] {
					game.frontier = append(game.frontier, Cell{i, j, rest})
				}
            }
        }
    }
    
    // fill cands
	game.cands[row][col] = map[byte]byte{num:num}

    return true
}

// search try candidate
func getTryCand(game *Game) [2]int {
	for i, row := range game.cands {
		for j, cands := range row {
			if len(cands) > 1 {
				return [2]int{i, j}
			}
		}
	}
	return [2]int{}
}

// solve step
func solveStep(game *Game) bool {

	// loop all frontiers
	for len(game.frontier) > 0 {

		// pop out frontier
		curr := game.frontier[0]
        row, col, num := curr.row, curr.col, curr.num
		game.frontier = game.frontier[1:]
        if game.filled[[2]int{row, col}] == 1 {
            continue
        }

		// kick out impossible candidates
		status := kickCands(game, curr)
		if status == false {
			return status
		}

		// fill frontier into board
		game.filled[[2]int{row, col}] = 1
		game.board[row][col] = num
	}

	return true
}

// solve game
func solveSudoku(board [][]byte)  {

	// initial game
    cands := initCands()
	filled := map[[2]int]int{}
	frontier := initFrontier(board)
	initGame := &Game{board, cands, filled, frontier}
	games := []*Game{initGame}

	for {

		// pop out game to solve
		toSolveGame := games[len(games)-1]
		tmpGame := forkGame(toSolveGame)
		games = games[:len(games)-1]

		// solve the game
		status := solveStep(tmpGame)
		printSudoku(tmpGame.board)

		if status == true {
			// no conflict

			if len(tmpGame.filled) == 81 {
				// all cells have been filled
				// refresh final result
				games = append(games, tmpGame)
				break

			} else {
				// game not solved
				// need to fork try game
				tryGame := forkGame(tmpGame)
				tryCand := getTryCand(tmpGame)
				tryRow, tryCol := tryCand[0], tryCand[1]

				// select try value
				for key, _ := range tmpGame.cands[tryRow][tryCol] {
					fmt.Println("try", tryRow, tryCol, string(key))

					// refresh curr game
					delete(tmpGame.cands[tryRow][tryCol], key)
					if len(tmpGame.cands[tryRow][tryCol]) == 1 {
						for key, _ := range tmpGame.cands[tryRow][tryCol] {
							tmpGame.frontier = append(tmpGame.frontier, Cell{tryRow, tryCol, key})
						}
					}
					games = append(games, tmpGame)

					// try game
					tryGame.frontier = append(tryGame.frontier, Cell{tryRow, tryCol, key})
					games = append(games, tryGame)

					break
				}
			}
		} else {
			// conflict
			// drop out current game
			fmt.Println("rollback")
		}
	}

	// solved game
	copyBoard(games[len(games)-1].board, board)
}

// print game board
func printSudoku(board [][]byte) {
	fmt.Println("=====================")
	for i, row := range board {
		rawStr := []string{}
		if i == 3 || i == 6 {
			fmt.Println("---------------------")
		}
		for j, item := range row {
			if j == 3 || j == 6 {
				rawStr = append(rawStr, "|")
			}
			rawStr = append(rawStr, string(item))
		}
		fmt.Println(strings.Join(rawStr, " "))
	}
	fmt.Println("=====================")
	fmt.Println("")
}

// get sudoku game
func getSudoku() [][]byte {

	//rawBoard := [][]string{{"5","3",".",".","7",".",".",".","."},{"6",".",".","1","9","5",".",".","."},{".","9","8",".",".",".",".","6","."},{"8",".",".",".","6",".",".",".","3"},{"4",".",".","8",".","3",".",".","1"},{"7",".",".",".","2",".",".",".","6"},{".","6",".",".",".",".","2","8","."},{".",".",".","4","1","9",".",".","5"},{".",".",".",".","8",".",".","7","9"}}
	rawBoard := [][]string{{".",".","9","7","4","8",".",".","."},{"7",".",".",".",".",".",".",".","."},{".","2",".","1",".","9",".",".","."},{".",".","7",".",".",".","2","4","."},{".","6","4",".","1",".","5","9","."},{".","9","8",".",".",".","3",".","."},{".",".",".","8",".","3",".","2","."},{".",".",".",".",".",".",".",".","6"},{".",".",".","2","7","5","9",".","."}}
	//rawBoard := [][]string{{".",".",".",".",".",".",".",".","."},{".",".",".",".",".",".",".",".","."},{".",".",".",".",".",".",".",".","."},{".",".",".",".",".",".",".",".","."},{".",".",".",".",".",".",".",".","."},{".",".",".",".",".",".",".",".","."},{".",".",".",".",".",".",".",".","."},{".",".",".",".",".",".",".",".","."},{".",".",".",".",".",".",".",".","."}}

	board := [][]byte{}
	for _, rawRow := range rawBoard {
		row := []byte{}
		for _, rawCol := range rawRow {
			row = append(row, []byte(rawCol)...)
		}
		board = append(board, row)
	}

	return board
}

func main() {

	board := getSudoku()
	solveSudoku(board)
	printSudoku(board)
}