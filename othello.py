import numpy as np

def CheckValid(board,now_player,second_time=False): #今のplayerがどこに石を置けるか？
    valid=False#一つでも石を置く場所があるか？
    valid_board=np.zeros((8,8)).astype('bool')

    for i in range(8**2):
        x,y=i%8,i//8
        player=now_player
        flag=False
        if board[y,x,player] or board[y,x,1-player]:
            continue#置いた場所にすでに石がある

        for dx,dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            nowx=x+dx
            nowy=y+dy
            if nowx==-1 or nowx==8 or nowy==-1 or nowy==8 or not board[nowy,nowx,1-player]:
                continue #置いた場所＋dに相手の駒がない or そこが場外

            while True:
                nowx+=dx
                nowy+=dy
                if nowx==-1 or nowx==8 or nowy==-1 or nowy==8:
                    break #場外

                if board[nowy,nowx,player]==0 and board[nowy,nowx,1-player]==0:
                    break #空マス

                if board[nowy,nowx,player]:
                    flag=True
                    break

            if flag:
                break

        if flag:#ある位置に置ける
            valid=True
            valid_board[y,x]=1


    if second_time:
        return valid
    else:
        if valid:
            return True,True,valid_board
        else:
            second_valid=CheckValid(board,1-now_player,second_time=True)
            return False,second_valid,valid_board


def Show(board):
    for i in range(8):
        s=''
        for j in range(8):
            if board[i,j,0] and board[i,j,1]:
                raise Exception

            if board[i,j,0]:
                s+='●'
            elif board[i,j,1]:
                s+='〇'
            else:
                s+='__'
        print(s)

    print()


def Reverse(c1,c2,board,player):#boardが書き変わる
    #c1からc2まで裏返す
    x1,y1=c1
    x2,y2=c2

    dx=x2-x1
    dy=y2-y1

    if dx:#0/1へ変換
        dx//=abs(dx)
    if dy:
        dy//=abs(dy)

    nowx=x1
    nowy=y1
    while True:
        nowx+=dx
        nowy+=dy
        if nowx==x2 and nowy==y2:
            return 

        board[nowy,nowx,player]=1
        board[nowy,nowx,1-player]=0


def Put(x,y,board,player):
    board=board.copy()
    board[y,x,player]=1
    for dx,dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
        nowx=x+dx
        nowy=y+dy
        if nowx==-1 or nowx==8 or nowy==-1 or nowy==8:
            continue

        if not board[nowy,nowx,1-player]:
            continue

        while True:
            nowx+=dx
            nowy+=dy
            if nowx==-1 or nowx==8 or nowy==-1 or nowy==8:
                break 

            if board[nowy,nowx,player]==0 and board[nowy,nowx,1-player]==0:
                break 

            if board[nowy,nowx,player]:
                Reverse((x,y),(nowx,nowy),board,player) #boardが書き変わる
                break

    return board