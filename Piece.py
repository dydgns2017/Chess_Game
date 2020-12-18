class Piece:
    def __init__(self,position,team):
        self.position = position
        self.team = team
        self.moved_once = False
        self.direction = -1 if team == "black" else 1
        # black == -1 || white == 1

    def move_forward(self,num):
        return [self.position[0], self.position[1] + self.direction*num]

    def move_backward(self,num):
        return [self.position[0], self.position[1] - self.direction*num]


    def move_queenside(self,num):
        return [self.position[0] - abs(self.direction*num), self.position[1]]    

    def move_kingside(self,num):
        return [self.position[0] + abs(self.direction*num), self.position[1]]



    def move_forward_queenside(self,num):
        return [self.position[0] - abs(self.direction*num), self.position[1] + self.direction*num]  

    def move_forward_kingside(self,num):
        return [self.position[0] + abs(self.direction*num), self.position[1] + self.direction*num]
    

    def move_backward_queenside(self,num):
        return [self.position[0] - abs(self.direction*num), self.position[1] - self.direction*num]  

    def move_backward_kingside(self,num):
        return [self.position[0] + abs(self.direction*num), self.position[1] - self.direction*num]
    
    def move_knight_circle(self,num):
        circle = [[2,1],[2,-1], [-2,1],[-2,-1], [1,2],[-1,2], [1,-2],[-1,-2]]
        return [self.position[0] + circle[num][0], self.position[1] + circle[num][1]]

    def change_position(self,new_position):
        self.position = new_position
        self.moved_once = True

        




class Pawn(Piece):
    def __init__(self, position, team):
        super().__init__(position, team)
        self.name = 'Pawn'
        self.symbol = '♟︎' if team=="black" else "♙"
        self.move_ability = [1,0,0,0,1,1,0,0]

class Knight(Piece):
    def __init__(self,position, team):
        super().__init__(position, team)
        self.name = 'Knight'
        self.symbol = '♞' if team=="black" else "♘"
        self.move_ability = [0,0,0,0,0,0,0,0]

class Rook(Piece):
    def __init__(self, position, team):
        super().__init__(position, team)
        self.name = "Rook"
        self.symbol = '♜' if team=="black" else "♖"
        self.move_ability = [8,8,8,8,0,0,0,0]

class Bishop(Piece):
    def __init__(self, position, team):
        super().__init__(position, team)
        self.name = "Bishop"
        self.symbol = '♝' if team=="black" else "♗"
        self.move_ability = [0,0,0,0,8,8,8,8]

class Queen(Piece):
    def __init__(self, position, team):
        super().__init__(position, team)
        self.name = "Queen"
        self.symbol = '♛' if team=="black" else "♕"
        self.move_ability = [8,8,8,8,8,8,8,8]

class King(Piece):
    def __init__(self, position, team):
        super().__init__(position, team)
        self.name = 'King'
        self.symbol = '♚' if team=="black" else "♔"
        self.move_ability = [1,1,1,1,1,1,1,1]