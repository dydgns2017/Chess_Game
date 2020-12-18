from Game import *

game = Game()

#초기상태 설정(시작 턴, 말 위치...)
game.init_normal_game()

print(game)

# print(game.status)

#게임 루프 시작
while game.status != "stop":

    #checkmate면 게임 끝
    if game.is_checkmate() == True:
        print("게임 끝")
        if game.turn == "black":
            win = "white가"
        elif game.turn == "white":
            win = "black이"    
        print(f"{win} 이겼습니다.")
        break

    #좌표 선택
    selected_piece = list(map(int,input("좌표 위의 말을 선택하세요: ").split()))

    selected_piece = game.piece_on(selected_piece)

    # 좌표의 팀 체크
    if game.turn_check(selected_piece) == False:
      continue
    else:
      pass

    #갈 수 있는 좌표 표시
    if selected_piece:
        print(f"{selected_piece.name}은 해당 좌표들로 움직일 수 있습니다: {game.legal_moves(selected_piece)}")

    #새 좌표 선택
    new_position = list(map(int,input("움직일 좌표를 선택하세요: ").split()))

    #새 좌표로 이동: 체크라면 자동으로 확인
    game.move_piece_to(selected_piece, new_position)
    # 이동 할 수 없는 좌표인 경우 좌표 다시 선택

    #다음 턴으로 바꿈
    game.next_turn()

    print(game)
    #print("-------------------------------------------------")
