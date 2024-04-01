import sys
from collections import deque

input = sys.stdin.readline

# L 벨트길이, Q 명령 개수
L, Q = map(int, input().split())
raw_commands = [input().split() for _ in range(Q)]
commands = []

# 명령어 정규화
for c in raw_commands:
    if c[0] == '100':
        op_code, t, x, name = int(c[0]), int(c[1]), int(c[2]), c[3]
        commands.append((op_code, t, x, name))
    elif c[0] == '200':
        op_code, t, x, name, n = int(c[0]), int(c[1]), int(c[2]), c[3], int(c[4])
        commands.append((op_code, t, x, name, n))
    else:
        op_code, t = map(int, c)
        commands.append((op_code, t))

# 명령 종류
# 초밥 만들기 100 t, x, name - t시각 x위치에 name초밥 1개 올리기
# 손님 입장 200 t, x, name, n - name인 사람이 t시각 x위치에 n개의 초밥을 먹을 때까지 대기
# 사진 촬영 300 t - t시각에 사람 수, 초밥 수 출력

def pprint(dict_board):
    for key, value in dict_board.items():
        print(f'{key}: {value}')
    print()


def rotate(belt):
    new_belt = dict()
    # belt = {key: value[:] for key, value in belt.items()}

    for x in belt:
        new_belt[(x+1)%L] = belt[x]
    
    return new_belt


def eat(x, waited, belt):
    name, n = waited[x]

    while n > 0 and x in belt and name in belt[x]:
        belt[x].remove(name)
        n-= 1

    if n > 0: waited[x] = [name, n]
    else: waited[x] = []


def eatAll(waited, belt):
    for x in belt:
        if x in waited and len(waited[x]) > 0:
            eat(x, waited, belt)




def solution():
    #belt = deque([[] for _ in range(L)])
    #waited = [[] for _ in range(L)]
    belt = dict()
    waited = dict()

    # 각 초밥에 사람 이름을 적어서 회전하는 벨트 위에 올려 놓음
    # 원형 형태의 초밥 벨트, L개의 의자
    # 의자는 x = 0 ~ L-1
    # 의자:초밥 = 1:n
    # 처음엔 벨트 위에 초밥 없음, 의자에도 사람 없음

    prev_time = commands[0][1]
    for command in commands:
        op_code, time = command[0], command[1]
 
        # 초밥 벨트는 1초에 1칸씩 시계방향으로 회전
        for t in range(time-prev_time):
            belt = rotate(belt)
            eatAll(waited, belt)

        # [1] 초밥 만들기
        if op_code == 100:
            x, name = command[2], command[3]

            # t시각에 x 위치 앞에 name을 부착한 초밥 하나 올려놓음
            # 같은 위치에 여러 회전 초밥 가능, 같은 이름이 부착된 초밥 같은 위치 가능
            if x not in belt: belt[x] = []
            belt[x].append(name)
   

            # t시각에 x위치에서 초밥을 기다리는 손님이 있다면 초밥 먹기
            if x in waited and len(waited[x]) > 0:
                eat(x, waited, belt)

        
        # [2] 손님 입장
        elif op_code == 200:
            x, name, n = command[2], command[3], command[4]

            # x앞으로 오는 초밥들 중 자신의 이름이 적혀있는 초밥을 n개 먹고 자리를 뜸
            # 만약 t시각, x위치에 name초밥이 놓여 있다면 착석 즉시 먹게 되며, 동시에 여러 개 먹기 가능
            while n > 0 and x in belt and name in belt[x]:
                belt[x].remove(name)
                n -= 1
            
            # 이름이 name인 사람이 t시각에 x 의자에 앉음
            # 해당 위치에 사람이 없음을 가정해도 좋음
            if n > 0:
                waited[x] = [name, n]
        
        # [3] 사진 촬영
        else:
            # t시각에 오마카세 집 모습 촬영
            # (1) 초밥 회전 후 (2) 손님이 초밥 먹은 후 (3) 사진 촬영 진행
            # 남아있는 사람 수와 남아있는 초밥 수 출력
            p_count = 0
            c_count = 0

            for x in waited:
                if len(waited[x]) > 0: p_count += 1

            for x in belt:
                c_count += len(belt[x])
            
            print(p_count, c_count)
        
        prev_time = time

solution()