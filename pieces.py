def print_moves(valid_squares):
    print("Moves: ", end="")
    for s in valid_squares:
        print(chr(s[0] + 97) + str(s[1] + 1), end = ", ")
    print("")


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

    def check_straights(self, graph):
        valid_squares = set()
        # check vertical up
        for y in range(self.pos[1] + 1, 8):
            valid_squares.add((self.pos[0], y))
            if graph[self.pos[0]][y].get_color() != "empty":
                break
        # check vertical down
        for y in range(self.pos[1] - 1, -1, -1):
            valid_squares.add((self.pos[0], y))
            if graph[self.pos[0]][y].get_color() != "empty":
                break
        # check horizontal right
        for x in range(self.pos[0] + 1, 8):
            valid_squares.add((x, self.pos[1]))
            if graph[x][self.pos[1]].get_color() != "empty":
                break
        # check horizontal left
        for x in range(self.pos[0] - 1, -1, -1):
            valid_squares.add((x, self.pos[1]))
            if graph[x][self.pos[1]].get_color() != "empty":
                break

        return valid_squares

    def check_diagonals(self, graph):
        valid_squares = set()
        # check diagonal upper right
        for k in range(1, 1 + min(7 - self.pos[0], 7 - self.pos[1])):
            valid_squares.add((self.pos[0] + k, self.pos[1] + k))
            if graph[self.pos[0] + k][self.pos[1] + k].get_color() != "empty":
                break
        # check diagonal upper left
        for k in range(1, 1 + min(self.pos[0], 7 - self.pos[1])):
            valid_squares.add((self.pos[0] - k, self.pos[1] + k))
            if graph[self.pos[0] - k][self.pos[1] + k].get_color() != "empty":
                break
        # check diagonal lower right
        for k in range(1, 1 + min(7 - self.pos[0], self.pos[1])):
            valid_squares.add((self.pos[0] + k, self.pos[1] - k))
            if graph[self.pos[0] + k][self.pos[1] - k].get_color() != "empty":
                break
        # check diagonal lower left
        for k in range(1, 1 + min(self.pos[0], self.pos[1])):
            valid_squares.add((self.pos[0] - k, self.pos[1] - k))
            if graph[self.pos[0] - k][self.pos[1] - k].get_color() != "empty":
                break

        return valid_squares

    def check_knights(self, graph):
        valid_squares = set()
        for p in [(2,1), (1,2), (-2,1), (-1,2), (2,-1), (1,-2), (-2,-1), (-1,-2)]:
            if self.pos[0] + p[0] in range(8) and self.pos[1] + p[1] in range(8):
                valid_squares.add((self.pos[0] + p[0], self.pos[1] + p[1]))

        return valid_squares

    def check_kings(self, graph):
        valid_squares = set()
        for p in [(-1,-1), (0,-1), (1,-1), (1,0), (1,1), (0,1), (-1,1), (-1,0)]:
            if self.pos[0] + p[0] in range(8) and self.pos[1] + p[1] in range(8):
                valid_squares.add((self.pos[0] + p[0], self.pos[1] + p[1]))

        return valid_squares

    def check_pawns(self, graph):
        valid_squares = set()
        direction = (self.color == "white") - (self.color == "black")
        # check double move
        if self.pos[1] == 1 + (self.color == "black")*5:
            if self.check_square(graph, self.pos[0], self.pos[1] + 2*direction):
                valid_squares.add((self.pos[0], self.pos[1] + 2*direction))
        # check double straight
        if self.check_square(graph, self.pos[0], self.pos[1] + direction):
            valid_squares.add((self.pos[0], self.pos[1] + direction))
        # check attack
        for k in [-1,1]:
            if self.pos[0] + k in range(8):
                if graph[self.pos[0] + k][self.pos[1] + direction].get_color() not in [self.color, "empty"]:
                    valid_squares.add((self.pos[0] + k, self.pos[1] + direction))

        return valid_squares

    def check_attackers(self, graph):
        attackers = {s for s in self.check_diagonals(graph) if graph[s[0]][s[1]].get_color() != self.color and graph[s[0]][s[1]].get_type() in ["b", "Q"]}
        if len(attackers) > 0:
            return True
        attackers = {s for s in self.check_straights(graph) if graph[s[0]][s[1]].get_color() != self.color and graph[s[0]][s[1]].get_type() in ["r", "Q"]}
        if len(attackers) > 0:
            return True
        attackers = {s for s in self.check_knights(graph) if graph[s[0]][s[1]].get_color() != self.color and graph[s[0]][s[1]].get_type() in ["n"]}
        if len(attackers) > 0:
            return True
        attackers = {s for s in self.check_pawns(graph) if graph[s[0]][s[1]].get_color() != self.color and graph[s[0]][s[1]].get_type() in ["p"]}
        if len(attackers) > 0:
            return True
        attackers = {s for s in self.check_kings(graph) if graph[s[0]][s[1]].get_color() != self.color and graph[s[0]][s[1]].get_type() in ["K"]}
        if len(attackers) > 0:
            return True

        return False


class empty(piece):
    def __init__(self, pos):
        piece.__init__(self, " ", "empty", pos)

class pawn(piece):
    def __init__(self, color, pos):
        piece.__init__(self, "p", color, pos)

    def get_valid_squares(self, graph):
        return {s for s in self.check_pawns(graph) if graph[s[0]][s[1]].get_color() != self.color}

class rook(piece):
    def __init__(self, color, pos):
        piece.__init__(self, "r", color, pos)
        self.can_castle = True

    def toggle_castle_flag(self):
        self.can_castle = False

    def get_castle_flag(self):
        return self.can_castle

    def get_valid_squares(self, graph):
        return {s for s in self.check_straights(graph) if graph[s[0]][s[1]].get_color() != self.color}

class knight(piece):
    def __init__(self, color, pos):
        piece.__init__(self, "n", color, pos)

    def get_valid_squares(self, graph):
        return {s for s in self.check_knights(graph) if graph[s[0]][s[1]].get_color() != self.color}

class bishop(piece):
    def __init__(self, color, pos):
        piece.__init__(self, "b", color, pos)

    def get_valid_squares(self, graph):
        return {s for s in self.check_diagonals(graph) if graph[s[0]][s[1]].get_color() != self.color}

class queen(piece):
    def __init__(self, color, pos):
        piece.__init__(self, "Q", color, pos)

    def get_valid_squares(self, graph):
        return {s for s in self.check_straights(graph).union(self.check_diagonals(graph)) if graph[s[0]][s[1]].get_color() != self.color}

class king(piece):
    def __init__(self, color, pos):
        piece.__init__(self, "K", color, pos)
        self.can_castle = True

    def toggle_castle_flag(self):
        self.can_castle = False

    def get_valid_squares(self, graph):
        return {s for s in self.check_kings(graph) if graph[s[0]][s[1]].get_color() != self.color}

    def check_castle(self, graph, rook_x):
        if not self.can_castle or not graph[rook_x][self.pos[1]].get_castle_flag():
            return "Cannot castle after moving King or rook"
        direction = (self.pos[0] > rook_x) - (rook_x > self.pos[0])
        for i in range(2):
            if graph[self.pos[0] + i*direction][self.pos[1]].check_attackers(graph):
                return "Cannot castle through check"
        if rook_x == 0:
             if not self.check_square(graph, 1, self.pos[1]):
                return "Illegal move"
