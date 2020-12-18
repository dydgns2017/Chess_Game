from Piece import *

class Game:
    def __init__(self):
        self.turn = "black"
        self.turn_count = 0
        self.status = "playing"
        self.board = [] # piece 객체가 들어있다
        self.positions = []
        self.size = [8,8]

    def __str__(self):
        output = ""
        for v in range(self.size[1]-1, -1, -1):
            for h in range(0,self.size[0]):
                piece_exist = self.piece_on([h,v])
                if piece_exist:
                    output += piece_exist.symbol
                else:
                    output += "."
                if h < self.size[0]:
                    output += " "
            output += f"{v}\n"
        return output + "0 1 2 3 4 5 6 7"

    def init_normal_game(self):
        self.board = []
        self.turn = "black"
        self.status = "playing"
        # black is top side
        for i in range(8):
            self.board.append(Pawn([i,1],"white"))
        
        self.board.append(Rook([0,0],"white"))
        self.board.append(Knight([1,0],"white"))
        self.board.append(Bishop([2,0],"white"))
        self.board.append(Queen([3,0],"white"))

        self.board.append(King([4,0],"white"))
        self.board.append(Bishop([5,0],"white"))
        self.board.append(Knight([6,0],"white"))
        self.board.append(Rook([7,0],"white"))
        
        for i in range(8):
            self.board.append(Pawn([i,6],"black"))
        self.board.append(Rook([0,7],"black"))
        self.board.append(Knight([1,7],"black"))
        self.board.append(Bishop([2,7],"black"))
        self.board.append(Queen([3,7],"black"))

        self.board.append(King([4,7],"black"))
        self.board.append(Bishop([5,7],"black"))
        self.board.append(Knight([6,7],"black"))
        self.board.append(Rook([7,7],"black"))
    
    def init_test_game(self):
        self.board = []
        self.board.append(Rook([0,0],"white"))
        self.board.append(King([5,0],"black"))
        self.board.append(Pawn([4,1],"black"))

    # 특정 좌표에 있는 말 객체를 반환한다
    def piece_on(self, position):
        for piece in self.board:
            if piece.position == position:
                return piece
        # print("이 자리는 비어있습니다") # for debugging
        return 0
    
    # 매개변수로 주어진 좌표가 보드 위에 있는지 확인한다
    def on_board(self, pos):
        return 0 <= pos[0] < self.size[0]  and  0 <= pos[1] < self.size[1]
    
    # 매개변수로 주어진 말이 이동할 수 있는 좌표들을 찾아서 반환한다 -- 아군 왕을 체크로 만드는 경우는 확인하지 않는다



    def can_move_to(self, piece): 
        if not piece:
            return 0
        abilities = [piece.move_forward, piece.move_backward, piece.move_queenside, piece.move_kingside, piece.move_forward_queenside, piece.move_forward_kingside, piece.move_backward_queenside, piece.move_backward_kingside]

        positions = []

        # 비숍, 룩, 퀸, 킹의 가능한 움직임들
        if piece.name not in ["Pawn","Knight"]:
            for i in range(8):
                for num in range(1, piece.move_ability[i]+1):
                    new_position = abilities[i](num)
                    # 이동한 새 좌표가 board 밖이면
                    if not self.on_board(new_position):
                        break
                    # 이동한 좌표에 말이 있는지 확인
                    overlapping = self.piece_on(new_position)
                    # overlappiing에 값이 있다면
                    if overlapping:
                        # 적군이면
                        if piece.team != overlapping.team:
                            positions.append(new_position)
                            break
                        # 아군이면
                        else:
                            break
        
                    # 조건을 모두 통과하면
                    positions.append(new_position)
        
        elif piece.name == "Pawn":
            help = [0,4,5]

            for i in range(len(help)):
                for num in range(1, piece.move_ability[help[i]]+1):
                    new_position = abilities[help[i]](num)
                    # 이동한 새 좌표가 board 밖이면
                    if not self.on_board(new_position):
                        break

                    # 이동한 좌표에 말이 있는지 확인
                    overlapping = self.piece_on(new_position)

                    # 대각선일 경우 >> help[ 4 >= x and 5 <= x]
                    if(help[i] == 4 or help[i] == 5):
                        #이동한 좌표에 말이 있으면
                        if overlapping:
                            # 적군이면
                            if piece.team != overlapping.team:
                                # print(f"{piece.team} 발견 {overlapping.team}!! at", new_position)
                                positions.append(new_position)
                                break
                            # 아군이면
                            else:
                                break

                    # 대각선이 아닌 경우 >> help[1]        
                    elif(help[i] == 0):
                        if not overlapping:
                            #폰을 한번도 움직이지 않았다면 -- 2칸 전진 가능
                            if piece.moved_once == False:
                                positions.append(new_position)
                                positions.append(piece.move_forward(2))
                            #폰을 한번이라도 움직였다면 -- 1칸만 전진 가능
                            else:
                                positions.append(new_position)
                        else:
                            break

        elif piece.name == "Knight":
            for num in range(8):
                new_position = piece.move_knight_circle(num)
                # 이동한 새 좌표가 board 밖이면
                if not self.on_board(new_position):
                    continue
                # 이동한 좌표에 말이 있는지 확인
                overlapping = self.piece_on(new_position)
                # overlappiing에 값이 있다면
                if overlapping:
                    # 적군이면
                    if piece.team != overlapping.team:
                        positions.append(new_position)
                        continue
                    # 아군이면
                    else:
                        continue
                # 조건을 모두 통과하면
                positions.append(new_position)
                     
        return positions

    # 일단 같은 가로줄에 있을 때만 2 말 사이에 있는 값을 구하는 함수이다 
    def horizontal_between_ab(self, piece_a, piece_b):
        h_diff, v_diff = piece_a.position[0] - piece_b.position[0], piece_a.position[1] - piece_b.position[1]
        if v_diff == 0:
            positions = []
            for i in range(1, abs(h_diff)):
                positions.append([piece_a.position[0] - i * (h_diff/abs(h_diff)), piece_a.position[1]])
            return positions
        else:
            return 0

    def is_position_vulnerable(self, pos, team):
        for piece in self.board:
            if piece.team != team:
                if pos in self.can_move_to(piece):
                    return True
        return False

    # # 말을 움직일때 
    # # 현재 차례인 팀의 왕이 체크인지 확인
    # def board_is_check(self):
    #     for piece in self.board:
    #         # 적군 말들의 가능한 모든 경로들을 파악하고 아군 왕의 위치와 중복되는지 확인한다
    #         # 적일 때
    #         if piece.team != self.turn:
    #             # 체크를 확인할 때는 임시로 움직인 말들도 있다
    #             # 그래서 임시로 먹힌 말이면 건너뛰도록 설정해줘야 한다
    #             skip = False
    #             for temp_piece in self.board:
    #                 #
    #                 if temp_piece != piece and temp_piece.position == piece.position:
    #                     print(temp_piece, piece)
    #                     skip = True
    #                     break
    #             can_move_to = self.can_move_to(piece)
    #             if skip:
    #                 can_move_to += temp_piece.position
    #             if self.king_position(self.turn) in can_move_to:
    #                 return True
    #     return False

    def board_is_check(self):

        for i, piece in enumerate(self.board):
            if piece.team != self.turn:

                temp_dead = 0
                # 만약 아군 말이 적군 위치와 곂치는 경우
                for same_team in self.board:
                    if same_team.team == self.turn:
                        if same_team.position == piece.position:
                            temp_dead = self.board.pop(i)
                            break
                
                
                if self.king_position(self.turn) in self.can_move_to(piece):
                    # print("왕을 잡을 수 있습니다")
                    if temp_dead:
                        # print("dkdk")
                        self.board.append(temp_dead)
                    return True
                
                if temp_dead:
                    self.board.append(temp_dead)
        return False


    def is_checkmate(self):
            
        #모든 보드에 있는 말 == piece
        count = 0   # 체크가 안되는 경우 확인
        for piece in self.board:
            #아군말일때
            # print(f"{piece.team}과 {self.turn}은 같습니다!!")
            if piece.team == self.turn:
                #아군말의 이동가능한 좌표
                for place in self.legal_moves(piece):
                    origin_position = piece.position
                    self.move_piece_to_for_checkmate(piece, place)

                    # 여기가 문제!!!!!!!!!!!!!!!!!!!
                    if self.board_is_check() == False:
                        # print(f"체크가 아닌 경우: \n{self.__str__()}")
                        # print(self.king_position(self.turn))
                        count += 1
                    self.move_piece_to_for_checkmate(piece, origin_position) 
        if(count == 0):
            
            # print(count)  
            return True  

    def team_can_go_to(self, pos, team):
        for piece in self.board:
            if piece.team == team:
                #그 좌표가 아군 piece의 이동가능한 모든 좌표에 있는지
                if pos in self.can_move_to(piece):
                    return True
        return False

    # 매개변수로 주어진 말이 이동할 수 있는 좌표들을 찾아서 반환한다 -- 아군 왕을 체크로 만드는 경우 제외시킨다
    def legal_moves(self, piece):
        illegal_moves = []
        all_moves = self.can_move_to(piece)
        if not all_moves:
            return []
        for place in all_moves:
            # 임시로 말의 위치를 변경한다 -- Piece 클래스가 보유하고 있는 메소드를 사용하지 않는다
            origin = piece.position

            piece.position = place
            if self.board_is_check():
                illegal_moves.append(place)
            # 말의 위치를 원래 위치로 되돌린다
            piece.position = origin
        
        # all_moves illegal_moves를 제거한다
        for i in illegal_moves:
            all_moves.remove(i)
        
        # check for castling
        if piece.name == "King":
            # print("---will check for castling")
            # 위험하지 않다면
            if not self.is_position_vulnerable(piece.position, piece.team):
                # print("---king is safe")
                #킹을 한번도 안움직였다면
                if piece.moved_once == False:
                    # print("---king never moved")
                    for piece2 in self.board:
                        #룩인 경우 & 룩을 한번도 안움직였다면
                        if piece2.name == "Rook" and piece2.team == piece.team and piece2.moved_once == False:
                            # print("---there is same team rook that never moved at", piece2.position)
                            #킹과 룩 사이가 비어있다면
                            empty = True
                            for pos in self.horizontal_between_ab(piece, piece2):
                                # print(pos)
                                if self.piece_on(pos):
                                    empty = False
                            if not empty:
                                continue
                            
                            # print("---king between rook is empty")
                            # 킹이 이동하는 칸을 적이 공격 가능하면 안된다 
                            safe = True
                            count = 2   # 왕은 캐슬링 때 2칸만 이동한다
                            for pos in self.horizontal_between_ab(piece, piece2):
                                if not count:
                                    break
                                if self.is_position_vulnerable(pos, piece.team):
                                    safe = False
                                    break
                                count -= 1
                            
                            if safe:
                                # print("castling is possible")
                                # print(piece.position)
                                # print(piece2.position)
                                # print(f"{piece.position[0]} > {piece2.position[0]}")
                                if piece.position[0] > piece2.position[0]:
                                    # print("kingside")
                                    all_moves.append(piece.move_queenside(2))
                                    # all_moves.append(piece.move_kingside(2))
                                else:
                                    # all_moves.append(piece.move_queenside(2))
                                    # print(piece.move_kingside(2))
                                    all_moves.append(piece.move_kingside(2))

        return all_moves
            
    # 특정 팀의 왕 말의 위치를 반환한다 v
    def king_position(self, team):
        for piece in self.board:
            if piece.name == "King" and piece.team == team:
                return piece.position
        # print(f"Alert: {team} team's King not found")  # for debugging
        return 0

    # 특정 말을 특정 위치로 이동시킨다 -- 적군 말이 있을 경우 적군 말을 제거한다
    def move_piece_to(self, piece, new_position):
        legal_moves = self.legal_moves(piece)
        if not legal_moves:
            return 0
        if new_position in legal_moves:
            # 움직이려고 하는 위치에 적군 말이 있으면 없애준다
            overlapping = self.piece_on(new_position)
            if overlapping:
                # 적군이면
                if overlapping.team != piece.team:
                    # print("its overlapping and enemy")
                    self.board.remove(overlapping)
                # 아군이면 -- 에러!
                else:
                    # print("***ERROR*** 뭔가 문제가 생겼습니다")
                    return 0
            # 캐슬링인지 확인해서 룩도 옮겨주어야 한다
            if piece.name == "King" and abs(piece.position[0] - new_position[0]) > 1:
                # find Rook on same team
                rook_piece = [0,0] # [queenside, kingside]
                for piece2 in self.board:
                    if piece2.name == "Rook" and piece2.team == piece.team:
                        if piece2.position[0] == 0:
                            rook_piece[0] = piece2
                        else:
                            rook_piece[1] = piece2
                # kingside castling
                if piece.position[0] - new_position[0] < 0:
                    rook_piece[1].change_position([new_position[0]-1, new_position[1]])
                else:
                    rook_piece[0].change_position([new_position[0]+1, new_position[1]])
            piece.change_position(new_position)

        else:
            # print(f"{new_position} 위치로 이동할 수 없습니다")
            return 0

    def move_piece_to_for_checkmate(self, piece, new_position):
        piece.position = new_position

    # 다음 턴/차례로 바꾼다
    def next_turn(self):
        if(self.turn == "black"):
            self.turn = "white"

        elif(self.turn == "white"):
            self.turn = "black"
        
        else:
            pass
            #print("팀 변경 오류 --> def next_turn(self): ...")   # for debugging

    def turn_check(self,piece):
        if not piece:
            return False
        if(piece.team != self.turn):
            return False
        else:
            return True

'''
6 0
5 2
6 1
6 3
5 0
7 2
4 0
6 0

6 7
7 5
6 6
6 4
5 7
6 6
4 7

1 0
2 2
1 1
1 3
2 0
0 2
3 0
1 0
1 0
1 1


checkmate
0 6
0 5
4 1
4 3
4 6
4 4
3 0
5 2
0 5
0 4
5 0
2 3
0 4
0 3
5 2
5 6

'''