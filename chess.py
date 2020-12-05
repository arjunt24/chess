from board_file import board
from copy import deepcopy

b = board()
b.print_board()

white_move = 1
while True:
  prompt = "Enter move for " + "White: "*white_move + "Black: "*(~white_move)

  move = input(prompt).strip()
  if move == "quit":
    break

  color = "white"*white_move + "black"*(~white_move) 

  err = None
  if len(move.split(" ")) != 3:
    if "O-O-O" in move:
      err = b.castle(color, 0)
    elif "O-O" in move:
      err = b.castle(color, 7)
    else:
      print("Illegal input")
      continue 
  else: 
    type = move.split(" ")[0]
    start = move.split(" ")[1]
    dest = move.split(" ")[2]
    
    err = b.move(color, type, start, dest)

  if err != None and err != "Check":
    print(err)
    continue
    
  b.print_board()
  if err == "Check":
    copy_board = deepcopy(b)
    if not copy_board.can_escape_check("white"*(~white_move) + "black"*white_move):
      print("Checkmate! " + "White"*white_move + "Black"*(~white_move) + " wins!")
      break
    print("Check!")

  
  white_move = ~white_move
  
