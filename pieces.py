class piece:
  def __init__(self, type, color, pos):
    self.type = type
    self.color = color
    self.pos = pos

  def print_piece(self):
    if self.color == "black":
      print("\033[4m" + self.type + "\033[0m", end = " ")
    else:
      print(self.type, end = " ")
  
  def get_x(self):
    return self.pos[0]
  def get_y(self):
    return self.pos[1]
  def get_color(self):
    return self.color
  def get_type(self):
    return self.type
  
  def set_pos(self, x, y):
    self.pos = (x, y)

  def check_square(self, graph, x, y):
    return graph[x][y].color == "empty"

      

class empty(piece):
  def __init__(self, pos):
    piece.__init__(self, " ", "empty", pos)

class pawn(piece):
  def __init__(self, color, pos):
    piece.__init__(self, "p", color, pos)
  
  def check_valid_path(self, graph, dest_x, dest_y):
    direction = (self.color == "white") - (self.color == "black")
    if dest_x == self.pos[0]:
      if dest_y == self.pos[1] + direction:
        return True
      if dest_y == self.pos[1] + 2*direction:
        if dest_y != 3 + (self.color == "black"):
          return False
        return self.check_square(graph, dest_x, dest_y - direction)
      else:
        return False 
    if dest_y == self.pos[1] + direction:
      if dest_x == self.pos[0] - 1 or dest_x == self.pos[0] + 1:
        return graph[dest_x][dest_y].get_color() != self.color and graph[dest_x][dest_y].get_color() != "empty"
    return False


class rook(piece):
  def __init__(self, color, pos):
    piece.__init__(self, "r", color, pos)
    self.can_castle = True
  
  def toggle_castle_flag(self):
    self.can_castle = False

  def get_castle_flag(self):
    return self.can_castle

  def check_valid_path(self, graph, dest_x, dest_y):
    if dest_x == self.pos[0] and dest_y != self.pos[1]:
      direction = (self.pos[1] < dest_y) - (dest_y < self.pos[1])
      for y in range(self.pos[1] + direction, dest_y, direction):
        if not self.check_square(graph, dest_x, y):
          return False
      return True  

    if dest_y == self.pos[1] and dest_x != self.pos[0]:
      direction = (self.pos[0] < dest_x) - (dest_x < self.pos[0])
      for x in range(self.pos[0] + direction, dest_x, direction):
        if not self.check_square(graph, x, dest_y):
          return False
      return True  
    
    return False


class knight(piece):
  def __init__(self, color, pos):
    piece.__init__(self, "n", color, pos)

  def check_valid_path(self, graph, dest_x, dest_y):
    if abs(dest_x - self.pos[0]) == 2:
      if abs(dest_y - self.pos[1]) == 1:
        return True
    if abs(dest_y - self.pos[1]) == 2:
      if abs(dest_x - self.pos[0]) == 1:
        return True
    
    return False

class bishop(piece):
  def __init__(self, color, pos):
    piece.__init__(self, "b", color, pos)

  def check_valid_path(self, graph, dest_x, dest_y):
    if dest_x - self.pos[0] == dest_y - self.pos[1]:
      if dest_x - self.pos[0] > 0:
        for k in range(1, dest_x - self.pos[0]):
          if not self.check_square(graph, self.pos[0] + k, self.pos[1] + k):
            return False
        return True
      if dest_x - self.pos[0] < 0:
        for k in range(1, self.pos[0] - dest_x):
          if not self.check_square(graph, self.pos[0] - k, self.pos[1] - k):
            return False
        return True
      return False

    if dest_x - self.pos[0] == self.pos[1] - dest_y:
      if dest_x - self.pos[0] > 0:
        for k in range(1, dest_x - self.pos[0]):
          if not self.check_square(graph, self.pos[0] + k, self.pos[1] - k):
            return False
        return True
      if dest_x - self.pos[0] < 0:
        for k in range(1, self.pos[0] - dest_x):
          if not self.check_square(graph, self.pos[0] - k, self.pos[1] + k):
            return False
        return True

    return False


class queen(piece):
  def __init__(self, color, pos):
    piece.__init__(self, "Q", color, pos)

  def check_valid_path(self, graph, dest_x, dest_y):
    if dest_x == self.pos[0] and dest_y != self.pos[1]:
      direction = (self.pos[1] < dest_y) - (dest_y < self.pos[1])
      for y in range(self.pos[1] + direction, dest_y, direction):
        if not self.check_square(graph, dest_x, y):
          return False
      return True  

    if dest_y == self.pos[1] and dest_x != self.pos[0]:
      direction = (self.pos[0] < dest_x) - (dest_x < self.pos[0])
      for x in range(self.pos[0] + direction, dest_x, direction):
        if not self.check_square(graph, x, dest_y):
          return False
      return True  
  
    if dest_x - self.pos[0] == dest_y - self.pos[1]:
      if dest_x - self.pos[0] > 0:
        for k in range(1, dest_x - self.pos[0]):
          if not self.check_square(graph, self.pos[0] + k, self.pos[1] + k):
            return False
        return True
      if dest_x - self.pos[0] < 0:
        for k in range(1, self.pos[0] - dest_x):
          if not self.check_square(graph, self.pos[0] - k, self.pos[1] - k):
            return False
        return True
      return False

    if dest_x - self.pos[0] == self.pos[1] - dest_y:
      if dest_x - self.pos[0] > 0: 
        for k in range(1, dest_x - self.pos[0]):
          if not self.check_square(graph, self.pos[0] + k, self.pos[1] - k):
            return False
        return True
      if dest_x - self.pos[0] < 0:
        for k in range(1, self.pos[0] - dest_x):
          if not self.check_square(graph, self.pos[0] - k, self.pos[1] + k):
            return False
        return True

    return False


class king(piece):
  def __init__(self, color, pos):
    piece.__init__(self, "K", color, pos)
    self.can_castle = True

  def toggle_castle_flag(self):
    self.can_castle = False

  def check_valid_path(self, graph, dest_x, dest_y):
    if dest_x == self.pos[0] and dest_y == self.pos[1]:
      return False
    if abs(dest_x - self.pos[0]) <= 1:
      if abs(dest_y - self.pos[1]) <= 1:
        return True

    return False

  def check_castle(self, graph, rook_x):
    if not self.can_castle or not graph[rook_x][self.pos[1]].get_castle_flag():
      return "Cannot castle after moving King or rook"
    direction = (self.pos[0] > rook_x) - (rook_x > self.pos[0])
    for i in range(2):
      if self.check_check(graph, self.pos[0] + i*direction, self.pos[1]):
        return "Cannot castle through check"
    if rook_x == 0:
       if not self.check_square(graph, 1, self.pos[1]):
        return "Illegal move"     

  def check_check(self, graph, king_x = None, king_y = None):
    if not king_x:
      king_x = self.pos[0]
    if not king_y:
      king_y = self.pos[1]

    # check vertical up
    for y in range(king_y + 1, 8):
      if graph[king_x][y].get_color() != self.color and graph[king_x][y].get_type() in ["r", "Q"]:
        return True
      if graph[king_x][y].get_color() != "empty":
        break
    # check vertical down
    for y in range(king_y - 1, -1, -1):
      if graph[king_x][y].get_color() != self.color and graph[king_x][y].get_type() in ["r", "Q"]:
        return True    
      if graph[king_x][y].get_color() != "empty":
        break

    # check horizontal right
    for x in range(king_x + 1, 8):
      if graph[x][king_y].get_color() != self.color and graph[x][king_y].get_type() in ["r", "Q"]:
        return True
      if graph[x][king_y].get_color() != "empty":
        break
    # check horizontal left
    for x in range(king_x - 1, -1, -1):
      if graph[x][king_y].get_color() != self.color and graph[x][king_y].get_type() in ["r", "Q"]:
        return True
      if graph[x][king_y].get_color() != "empty":
        break

    # check diagonal upper right
    for k in range(1, min(8 - king_x, 8 - king_y)):
      if graph[king_x + k][king_y + k].get_color() != self.color and graph[king_x + k][king_y + k].get_type() in ["b", "Q"]:
        return True
      if graph[king_x + k][king_y + k].get_color() != self.color and graph[king_x + k][king_y + k].get_type() == "p" and self.color == "white":
        if k == 1:
          return True
      if graph[king_x + k][king_y + k].get_color() != "empty":
        break
    # check diagonal upper left
    for k in range(1, min(king_x, 8 - king_y)):
      if graph[king_x - k][king_y + k].get_color() != self.color and graph[king_x - k][king_y + k].get_type() in ["b", "Q"]:
        return True
      if graph[king_x - k][king_y + k].get_color() != self.color and graph[king_x - k][king_y + k].get_type() == "p" and self.color == "white":
        if k == 1:
          return True
      if graph[king_x - k][king_y + k].get_color() != "empty":
        break
    # check diagonal lower right
    for k in range(1, min(8 - king_x, king_y)):
      if graph[king_x + k][king_y - k].get_color() != self.color and graph[king_x + k][king_y - k].get_type() in ["b", "Q"]:
        return True
      if graph[king_x + k][king_y - k].get_color() != self.color and graph[king_x + k][king_y - k].get_type() == "p":
        if k == 1:
          return True
      if graph[king_x + k][king_y - k].get_color() != "empty":
        break
    # check diagonal lower left
    for k in range(1, min(king_x, king_y)):
      if graph[king_x - k][king_y - k].get_color() != self.color and graph[king_x - k][king_y - k].get_type() in ["b", "Q"]:
        return True
      if graph[king_x - k][king_y - k].get_color() != self.color and graph[king_x - k][king_y - k].get_type() == "p":
        if k == 1:
          return True
      if graph[king_x - k][king_y - k].get_color() != "empty":
        break
    
    # check for knights
    for p in [(2,1), (1,2), (-2,1), (-1,2), (2,-1), (1,-2), (-2,-1), (-1,-2)]:
      if king_x + p[0] in range(0,8) and king_y + p[1] in range(0,8):
        if graph[king_x + p[0]][king_y + p[1]].get_type() == "n":
          if graph[king_x + p[0]][king_y + p[1]].get_color() != self.color:
            return True

    return False
      
