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


    if not valid:
        if second_time:
            return False,False,valid_board
        else:
            CheckValid(board,now_player,second_time=True)

    return valid,True,valid_board

import random
def RandomDecide(valid_board):
    while True:
        r=random.randint(0,8**2-1)
        y,x=r//8,r%8
        if valid_board[y,x]:
            return r


import tensorflow as tf
gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)
from tensorflow.keras.models import load_model
def ModelDecide(board,valid_board):
    model = load_model('model.h5')
    output_data = model.predict(board.reshape(1,8,8,2))
    res = np.argmax(output_data[0])
    y,x=res//8,res%8
    if valid_board[y,x]:
        return res
    else:
        return RandomDecide(valid_board)

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
