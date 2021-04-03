import numpy as np

import othello

def argmax(L):
    idx=-1
    mx=-1000
    for i,v in enumerate(L):
        if v>mx:
            mx=v
            idx=i
    return idx

def mean(L):
    return sum(L)/len(L)

def dfs(depth,board,valid_board,player,me):
    if depth!=0:#valid_boardが存在するのは初めの１回だけ
        valid,sv,valid_board=othello.CheckValid(board,1-player)
    else:
        valid=True
        sv=True

    if not sv:#終わり
        my_stone=np.sum(board[:,:,me])
        oppose_stone=np.sum(board[:,:,1-me])
        if my_stone>oppose_stone:
            return 1
        elif my_stone<oppose_stone:
            return -1
        else:
            return 0
        
    elif not valid:#pass
        result=dfs(depth+1,board,None,1-player,me) #ここでcheckvalidを1回分無駄に実行することになるので、どうにかしたい
        return result
        #depth=0の時は常にvalid=True（関数の外で判定済み）
    
    else:
        result_mx=-2
        result_mn=2
        hand=-1

        for i in range(64):
            y=i//8
            x=i%8
            if not valid_board[y,x]:
                continue
                
            next_board=othello.Put(x,y,board,player)
            
            result=dfs(depth+1,next_board,None,1-player,me)

            if player==me:#お互いに最善手を尽くすと仮定
                result_mx=max(result,result_mx)
                hand=i
            else:
                result_mn=min(result,result_mn)
                # player!=me → depth!=0 → handの情報が必要になることはない
                        
        if depth==0:
            return hand,result_mx
        else:            
            if player==me:
                return result_mx
            else:
                return result_mn

def dfs2(depth,max_depth,board,valid_board,player,me):
    if depth!=0:#valid_boardが存在するのは初めの１回だけ
        valid,sv,valid_board=othello.CheckValid(board,1-player)
    else:
        valid=True
        sv=True

    if not sv:#終わり
        my_stone=np.sum(board[:,:,me])
        oppose_stone=np.sum(board[:,:,1-me])
        if my_stone>oppose_stone:
            return 100
        elif my_stone<oppose_stone:
            return -100
        else:
            return 0
        
    elif not valid:#pass
        score=dfs2(depth+1,max_depth,board,None,1-player,me) #ここでcheckvalidを1回分無駄に実行することになるので、どうにかしたい
        return score
        #depth=0の時は常にvalid=True（関数の外で判定済み）
    else:
        if depth==0:
            hands=[]
        
        rewards=[]
        
        if player==me:
            v=1
        else:
            v=-1

        if np.sum(valid_board)>=16:
            max_depth=3

        for i in range(64):
            y=i//8
            x=i%8
            if not valid_board[y,x]:
                continue
            
            if depth<max_depth:
                next_board=othello.Put(x,y,board,player)
                reward=0.5*dfs2(depth+1,max_depth,next_board,None,1-player,me)+prs[i]*v
            else:
                reward=prs[i]*v

            if depth==0:
                hands.append(i)
            
            rewards.append(reward)
    
    if depth==0:#-> player==me
        return hands[argmax(rewards)],max(rewards)+0.3*len(rewards)

    c=len(rewards)
    if player==me:
        return max(rewards) + ((3*c-9)/(2*c+2)) if depth>=max_depth-1 else 0
    else:
        return 0.9*min(rewards)+0.1*mean(rewards) - ((3*c-9)/(4*c+4)) if depth>=max_depth-1 else 0 #「最適解を選んだ時の報酬」と「適当に選んだ時の期待値」の平均 #相手の打てる手が少ないほうが良い(?)

pos_rewards={
            3:[0, 7, 63, 56],#角
            1:[18, 21, 45, 42]+[2, 5, 23, 47, 61, 58, 40, 16]+[13, 22, 46, 53, 50, 41, 17, 10]+[59, 60, 39, 31, 4, 3, 24, 32],
            0:[11, 12, 25, 33, 30, 38, 51, 52]+[19, 20, 29, 37, 44, 43, 34, 26],
            -1:[49, 54, 14, 9]+[55, 62, 57, 48, 8, 1, 6, 15],
}

prs=[0]*64
for key,lst in pos_rewards.items():
    for val in lst:
        prs[val]=key


def Algo(board,valid_board,player):
    stone_count=np.sum(board)
    if stone_count>=57:
        hand,result=dfs(0,board,valid_board,player,player)
    else:
        hand,reward=dfs2(0,3,board,valid_board,player,player)
        #othello.Show(board)
        #print('reward:',reward)


    return hand #int

import random
def RandomDecide(_,valid_board,__):
    while True:
        r=random.randint(0,8**2-1)
        y,x=r//8,r%8
        if valid_board[y,x]:
            return r



"""
import tensorflow as tf
gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)
from tensorflow.keras.models import load_model
def ModelDecide(board,valid_board,player):
    if player!=0:
        raise Exception('player mus be 0')
    
    model = load_model('model.h5')
    output_data = model.predict(board.reshape(1,8,8,2))
    res = np.argmax(output_data[0])
    y,x=res//8,res%8
    if valid_board[y,x]:
        return res
    else:
        return RandomDecide(board,valid_board,player)
"""