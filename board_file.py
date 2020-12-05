import pieces

class board:

  def __init__(self):
    all_pieces = {pieces.empty((x-1, y-1)) for x in range(1, 9) for y in range(3, 7)}

    for x in range(1, 9):
      all_pieces.add(pieces.pawn("white", (x-1, 2-1)))
      all_pieces.add(pieces.pawn("black", (x-1, 7-1)))
    for y in [1, 8]:
      for r in [1, 8]:
        all_pieces.add(pieces.rook("white"*(y==1) + "black"*(y==8), (r-1, y-1)))
      for n in [2, 7]:
        all_pieces.add(pieces.knight("white"*(y==1) + "black"*(y==8), (n-1, y-1)))
      for b in [3, 6]:
        all_pieces.add(pieces.bishop("white"*(y==1) + "black"*(y==8), (b-1, y-1)))
      all_pieces.add(pieces.king("white"*(y==1) + "black"*(y==8), (5-1, y-1)))
      all_pieces.add(pieces.queen("white"*(y==1) + "black"*(y==8), (4-1, y-1)))

    self.all_pieces = all_pieces


  def get_graph(self):
    graph = [[None for i in range(8)] for i in range(8)]
    for p in self.all_pieces:
      graph[p.get_x()][p.get_y()] = p

    return graph


  def print_board(self):
    graph = self.get_graph()

    print("\t", end="")
    for x in range(8):
      print(chr(x+97), end = " ")
    print("\n")
    for y in range(8, 0, -1):
      print(y, end = "\t")
      for x in range(1, 9):
        graph[x-1][y-1].print_piece()
      print("")
    print("")

      
  def move(self, color, type, start, dest):
    if type not in ["p", "r", "n", "b", "Q", "K"]:
      return type + " is not a valid piece"
    if len(start) != 2 or ord(start[0]) not in range(97, 105) or int(start[1]) not in range(1, 9):
      return start + " not on chess board" 
    if len(dest) != 2 or ord(dest[0]) not in range(97, 105) or int(dest[1]) not in range(1, 9):
      return dest + " not on chess board" 


    start_x = ord(start[0]) - 97
    start_y = int(start[1]) - 1

    active_piece = None
    for p in self.all_pieces:
      if p.get_type() == type and p.get_color() == color and p.get_x() == start_x and p.get_y() == start_y:
        active_piece = p
    if active_piece == None:
      return "No " + str(color) + " " + str(type) + " at " + str(start) 

    dest_x = ord(dest[0]) - 97
    dest_y = int(dest[1]) - 1

    target_piece = None
    for p in self.all_pieces:
      if p.get_x() == dest_x and p.get_y() == dest_y:
        target_piece = p
    if target_piece != None and target_piece.get_color() == color:
      return target_piece.get_type() + " is already on " + dest

    if active_piece.get_type() == "p" and target_piece.get_type() != " " and dest_x == active_piece.get_x():
      return "Illegal move"

    if not active_piece.check_valid_path(self.get_graph(), dest_x, dest_y):
      return "Illegal move"

    self.all_pieces.remove(target_piece)
    self.all_pieces.remove(active_piece)
    active_piece.set_pos(dest_x, dest_y)
    self.all_pieces.add(active_piece)
    empty_piece = pieces.empty((start_x, start_y))
    self.all_pieces.add(empty_piece)


    this_king = None
    opponent_king = None  
    for p in self.all_pieces:
      if p.get_type() == "K" and p.get_color() == color:
        this_king = p
      if p.get_type() == "K" and p.get_color() != color:
        opponent_king = p

    if this_king.check_check(self.get_graph()):
      self.all_pieces.remove(empty_piece)
      self.all_pieces.remove(active_piece)
      active_piece.set_pos(start_x, start_y)
      self.all_pieces.add(active_piece)
      self.all_pieces.add(target_piece)
      return "This move leads to check"

    # check for promotion
    if active_piece.get_type() == "p" and (dest_y == 7 or dest_y == 0):
      while True:
        type = input("What would you like to promote to (Q, r, n, or b)?")
        if type in ["r", "n", "b", "Q"]:
          break
      self.all_pieces.remove(active_piece)
      promoted = None
      if type == "Q":
        promoted = pieces.queen(active_piece.get_color(), (dest_x, dest_y))
      if type == "r":
        promoted = pieces.rook(active_piece.get_color(), (dest_x, dest_y))
      if type == "n":
        promoted = pieces.knight(active_piece.get_color(), (dest_x, dest_y))
      if type == "b":
        promoted = pieces.bishop(active_piece.get_color(), (dest_x, dest_y))
      self.all_pieces.add(promoted)

    # check castle flag
    if active_piece.get_type() in ["r", "K"]:
      active_piece.toggle_castle_flag()
    


    if opponent_king.check_check(self.get_graph()):
      return "Check"


  def castle(self, color, file):
    king = None
    rook = None
    for p in self.all_pieces:
      if p.get_type() == "K" and p.get_color() == color:
        king = p  
      if p.get_type() == "r" and p.get_color() == color and p.get_x() == file:
        rook = p  

    direction = (file > king.get_x()) - (king.get_x() > file) 

    empty1 = None
    empty2 = None
    for p in self.all_pieces:
      if p.get_type() == " " and p.get_x() == king.get_x() + direction and p.get_y() == king.get_y():
        empty1 = p  
      if p.get_type() == " " and p.get_x() == king.get_x() + 2*direction and p.get_y() == king.get_y():
        empty2 = p  
    if empty1 == None or empty2 == None:
      return "Illegal castle"

    err = king.check_castle(self.get_graph(), file)
    if err != None:
      return err

    self.all_pieces.remove(king)
    self.all_pieces.remove(rook)
    self.all_pieces.remove(empty1)
    self.all_pieces.remove(empty2)
    
    
    king.set_pos(king.get_x() + 2*direction, king.get_y())
    rook.set_pos(king.get_x() - direction, king.get_y())
    empty1.set_pos(king.get_x() - 2*direction, king.get_y())
    empty2.set_pos(file, king.get_y())

    self.all_pieces.add(king)
    self.all_pieces.add(rook)
    self.all_pieces.add(empty1)
    self.all_pieces.add(empty2)

    king.toggle_castle_flag()
    


  def can_escape_check(self, color):
    # for type in ["K", "Q", "b", "n", "r", "p"]:
    #   for x1 in [chr(i) for i in range(97,105)]:
    #     for y1 in range(1, 9):
    #       for x2 in [chr(i) for i in range(97,105)]:
    #         for y2 in range(1, 9):
    #           err = self.move(color, type, str(x1) + str(y1), str(x2) + str(y2))
    #           f.write(color + "\t" + type + "\t" + str(x1) + str(y1) + "\t" + str(x2) + str(y2) + "\tERR: " + str(err) + "\n")
    #           if err == None or err == "Check":
    #             return True


    # f = open("file.txt", "w")
    for p in {piece for piece in self.all_pieces if piece.get_color() == color}:
      start = chr(p.get_x()+ 97) + str(p.get_y() + 1)
      type = p.get_type()
      for x in [chr(i) for i in range(97,105)]:
        for y in range(1, 9):
          err = self.move(color, type, start, str(x) + str(y))
          # f.write(color + "\t" + type + "\t" + start + "\t" + str(x) + str(y) + "\tERR: " + str(err) + "\n")
          if err == None or err == "Check":
            return True  

    return False  
    
