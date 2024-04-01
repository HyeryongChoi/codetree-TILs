import sys
from collections import deque

input = sys.stdin.readline

# L체스판크기, N기사수, Q명령수
L, N, Q = map(int, input().split())

# LxL 체스판, 0빈칸, 1함정, 2벽
# 테두리를 벽으로 둘러 처리하기
board = [[2]*(L+2)] + [[2]+list(map(int, input().split()))+[2] for _ in range(L)] + [[2]*(L+2)]

# 기사정보 (r,c,h,w,k) -> 좌측 상단(r,c) ~ 세로h, 가로w, 초기체력k
knights = dict()
hps = [0]*(N+1) # 기사들 초기 체력 정보 저장
for i in range(1,N+1):
    knights[i] = list(map(int, input().split()))
    hps[i] = knights[i][4]

# 왕의 명령 (i, d) -> i번 기사 방향 d로 한 칸 이동 (1<=i<=N)
commands = [list(map(int, input().split())) for _ in range(Q)]

# u, r, d, l
dy = [-1, 0, 1, 0]
dx = [0, 1, 0, -1]


def push(k_start, k_direction):
    q = deque([k_start]) # push할 기사 번호 목록 탐색 시 사용하는 큐
    pushed = set([k_start]) # 실제로 push할 기사 번호 목록
    dmg = [0]*(N+1) # 기사별 데미지 누적

    while q:
        k_idx = q.popleft()
        
        (r,c,h,w,k) = knights[k_idx]

        nr, nc = r+dy[k_direction], c+dx[k_direction]
        # 현재 기사 이동 시 벽에 부딪히는지 탐색
        for y in range(nr, nr+h):
            for x in range(nc, nc+w):
                if isWall(y,x): return # 벽에 부딪히는 경우 모두 취소
                if isTrap(y,x): dmg[k_idx] += 1 # 명령 받은 기사 포함 움직이는 기사 모두 일단 데미지 처리
        
        # 다른 기사와 겹치는지 탐색
        for idx in knights:
            if idx in pushed: continue

            (tr,tc,th,tw,_) = knights[idx]

            if nr > tr+th-1: continue
            if nr+h-1 < tr: continue
            if nc > tc+tw-1: continue
            if nc+w-1 < tc: continue

            q.append(idx) # 기사[idx]에 겹치는 다른 기사를 다시 찾기 위함
            pushed.add(idx)
    
    # 명령을 받은 기사가 입은 데미지 초기화
    dmg[k_start] = 0

    # push할 기사 이동
    for idx in pushed:
        (r,c,h,w,k) = knights[idx]

        # 현재 체력 이상의 데미지를 받는 경우 기사 삭제
        if dmg[idx] >= k: del knights[idx]
        else: # 살아있는 기사 이동
            nr, nc = r+dy[k_direction], c+dx[k_direction]
            knights[idx] = (nr, nc, h, w, k-dmg[idx])


def isWall(y, x):
    return board[y][x] == 2

def isTrap(y,x):
    return board[y][x] == 1

def solution():
    for k_idx, k_direction in commands:
        # 체스판에서 사라진 기사인 경우 다음 명령으로 넘어감
        if k_idx not in knights: continue

        # [1] 기사 이동
        push(k_idx, k_direction)

    # 생존한 기사들이 총 받은 데미지의 합?
    answer = 0
    for idx in knights:
        answer += hps[idx] - knights[idx][4]

    print(answer)
    

solution()