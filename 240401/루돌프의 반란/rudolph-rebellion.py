import sys

input = sys.stdin.readline

# c루돌프힘, d산타힘
n,m,p,c,d = map(int, input().split())
rudolf = [pos-1 for pos in list(map(int, input().split()))]
santas = [[santa[0], santa[1]-1, santa[2]-1] for santa in [list(map(int, input().split())) for _ in range(p)]]

board = [[0]*n for _ in range(n)]

RUDOLF = 31

board[rudolf[0]][rudolf[1]] = RUDOLF
for index, y, x in santas:
    board[y][x] = index

# 8방향 상우하좌, 대각선
dy = [-1,0,1,0,-1,-1,1,1]
dx = [0,1,0,-1,-1,1,-1,1]

def pprint(board):
    for row in board:
        print(*row)
    print('-------------')

# 상호작용
def santaSanta(num1, num2, pos, direction):
    santa1 = 0 
    santa2 = 0

    for order in range(len(santas)):
        if santas[order][0] == num1:
            santa1 = order
        if santas[order][0] == num2:
            santa2 = order

    # santas, board 업데이트
    santas[santa1] = [num1, pos[0], pos[1]]
    board[pos[0]][pos[1]] = num1

    ny = santas[santa2][1] + dy[direction]
    nx = santas[santa2][2] + dx[direction]

    # 밀려난 위치가 게임판 밖이라면 해당 산타는 게임에서 탈락
    if ny < 0 or ny >= n or nx < 0 or nx >= n:
        santas.pop(santa2)
        return

    # 다른 산타가 있다면 다른 산타는 1칸 밀림
    if 1 <= board[ny][nx] <= 30:
        num3 = board[ny][nx]
        santaSanta(num2, num3, (ny,nx), direction)
    else:
        santas[santa2] = [num2, ny, nx]
        board[ny][nx] = num2

def pushSanta(target, direction, size):
    global santas

    for order in range(len(santas)):
        if santas[order][0] == target:
            y, x = santas[order][1], santas[order][2]

            board[y][x] = RUDOLF

            ny = y + dy[direction]*size
            nx = x + dx[direction]*size

            # 밀려난 위치가 게임판 밖이라면 산타는 게임에서 탈락
            if ny < 0 or ny >= n or nx < 0 or nx >= n:
                santas.pop(order)
                return
            
            # 밀려난 위치에 다른 산타가 있다면 그 산타는 1칸 해당 방향으로 밀려남
            if 1 <= board[ny][nx] <= 30:
                num2 = board[ny][nx]
                santaSanta(target, num2, (ny,nx), direction)
            else:
                santas[order] = [target, ny, nx]
                board[ny][nx] = target

            return
            


# def deleteSanta(target):
#     global santas

#     santas = [santa for santa in santas if santa[0] != target]
        

def getRudolfNextPos(rudolf, santa):
    y, x = rudolf
    min_dist = 1e9
    next_pos = (y,x)
    direction = -1

    for dir in range(8):
        ny = y + dy[dir]
        nx = x + dx[dir]

        if ny < 0 or ny >= n or nx < 0 or nx >= n: continue

        dist = getDist((ny,nx),santa)
        if dist < min_dist:
            min_dist = dist
            next_pos = (ny, nx)
            direction = dir
    
    return next_pos, direction

def getSantaNextPos(santa, rudolf):
    y, x = santa
    min_dist = getDist(santa, rudolf)
    next_pos = (y,x)
    direction = -1

    for dir in range(4):
        ny = y + dy[dir]
        nx = x + dx[dir]

        if ny < 0 or ny >= n or nx < 0 or nx >= n: continue
        if 1 <= board[ny][nx] <= 30: continue
        # 루돌프는 고려하지 않고 일단 움직임

        dist = getDist((ny,nx),rudolf)
        if dist < min_dist:
            min_dist = dist
            next_pos = (ny, nx)
            direction = dir

    # 움직일 수 있는 칸이 없다면 움직이지 않음
    # 움직일 수 있는 칸이 있더라도 루돌프로부터 가까워질 수 없다면 움직이지 않음
    return next_pos, direction
            
def getDist(pos1,pos2):
    r1, c1 = pos1
    r2, c2 = pos2

    return (r1-r2)**2 + (c1-c2)**2

def solution():
    global rudolf

    # 각 산타의 점수
    scores = [0]*(p+1)

    # 해당 값보다 크거나 같은 턴일 때만 움직일 수 있음
    canMoves = [-1]*(p+1)

    #pprint(board)
    for turn in range(m):
        #print(f'{turn+1}번째 턴 결과')
        # 산타가 모두 게임에서 탈락하게 된다면 즉시 게임 종료
        if len(santas) == 0: break

        # 루돌프와의 거리 기준 오름차순, r, c 기준 내림차순 정렬
        santas.sort(key = lambda santa: (getDist(rudolf, santa[1:]), -santa[1], -santa[2]))

        # 루돌프 한 번 움직이기
        board[rudolf[0]][rudolf[1]] = 0
        rudolf, r_direction = getRudolfNextPos(rudolf, (santas[0][1], santas[0][2]))

        # 루돌프가 움직여서 산타와 충돌한 경우
        if 1 <= board[rudolf[0]][rudolf[1]] <= 30:
            target_santa = board[rudolf[0]][rudolf[1]]
            scores[target_santa] += c
            board[rudolf[0]][rudolf[1]] = RUDOLF

            # 산타는 루돌프가 이동해온 방향으로 C칸 만큼 밀려남
            pushSanta(target_santa, r_direction, c)

            # 루돌프와 충돌한 산타는 turn+1번째 턴까지 기절
            canMoves[target_santa] = turn + 2

        # 게임판에 루돌프 위치시키기
        board[rudolf[0]][rudolf[1]] = RUDOLF
        
        #print(f'{turn+1}턴: 루돌프가 움직인 후')
        #pprint(board)
        #print('기절상태', canMoves)

        # 1~p번 산타 순서대로 한 번씩 움직이기
        for i in range(1,p+1):
            # i번 산타가 기절한 경우 움직일 수 없음
            if turn < canMoves[i]: continue

            cur_order = -1
            for order in range(len(santas)):
                if santas[order][0] == i:
                    cur_order = order
                    break

            # i번 산타가 탈락한 경우 움직일 수 없음
            if cur_order < 0: continue

            s_pos = (santas[cur_order][1], santas[cur_order][2])

            board[s_pos[0]][s_pos[1]] = 0

            s_pos, s_direction = getSantaNextPos(s_pos,rudolf)

            # 산타가 움직이지 않은 경우 다음 산타로 넘어감
            if s_direction < 0: continue

            # 산타 움직임
            santas[cur_order] = [i, s_pos[0], s_pos[1]]
            board[s_pos[0]][s_pos[1]] = i

            # 산타가 움직여서 루돌프와 충돌한 경우
            if s_pos == rudolf:
                scores[i] += d

                # 산타는 자신이 이동해온 반대방향으로 d칸 만큼 밀려남
                pushSanta(i, (s_direction+2)%4, d)

                # 루돌프와 충돌한 산타는 turn+1번째 턴까지 기절
                canMoves[i] = turn + 2

        #print(f'{turn+1}턴: 산타들이 움직인 후')
        #pprint(board)
        #print('기절상태', canMoves)

        # 매 턴 이후 아직 탈락하지 않은 산타들에게는 1점씩 부여
        for i in range(len(santas)):
            scores[santas[i][0]] += 1
    
    # 게임종료 후 각 산타가 얻은 최종 점수
    print(*scores[1:])

solution()

# 아니 이거 기절한 산타랑 부딪히면 어떻게 되는거지?