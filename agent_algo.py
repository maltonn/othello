import numpy as np

import othello

pos_rewards={
        3:[0, 7, 63, 56],#角
        1:[18, 21, 45, 42]+[2, 5, 23, 47, 61, 58, 40, 16]+[13, 22, 46, 53, 50, 41, 17, 10]+[59, 60, 39, 31, 4, 3, 24, 32],
        0:[11, 12, 25, 33, 30, 38, 51, 52]+[19, 20, 29, 37, 44, 43, 34, 26],
        -1:[55, 62, 57, 48, 8, 1, 6, 15],
        -3:[49, 54, 14, 9],
}
prs=[0]*64
for key,lst in pos_rewards.items():
    for val in lst:
        prs[val]=key

def argmax(L):
    idx=-1
    mx=-10**9-1
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
        results=[]
        hand=-1

        for i in range(64):
            y=i//8
            x=i%8
            if not valid_board[y,x]:
                continue
                
            next_board=othello.Put(x,y,board,player)
            
            result=dfs(depth+1,next_board,None,1-player,me)
            results.append(result)
            hand=i

        if depth==0:
            return hand,max(results)
        else:            
            if player==me:
                return max(results)
            else:
                return min(results)+0.01*mean(results) #相手が最適に打つと全部-1になる場合、うっかりミスする確率が高いやつを選ぶ

def dfs2(depth,max_depth,board,valid_board,player,me):
    if depth==max_depth:
        reward=0
        for i in range(64):
            x=i%8
            y=i//8
            if board[y,x,me]:
                reward+=prs[i]
            elif board[y,x,1-me]:
                reward-=prs[i]

        #確定石の計算
        certain_board=np.zeros_like(board)
        for rot_num in range(4):
            board_rot=np.rot90(board,rot_num)
            certain_board_rot=np.rot90(certain_board,rot_num)
            for h in range(8):
                for t in range(h+1):
                    for p in (me,1-me):
                        if not board_rot[h-t,t,p]:
                            continue
                        if (h-t-1<0 or certain_board_rot[h-t-1,t,p]) and (t-1<0 or certain_board_rot[h-t,t-1,p]) and (h-t-1<0 or t-1<0 or certain_board_rot[h-t-1,t-1,p]):
                            certain_board_rot[h-t,t,p]=1
        
        for i in range(64):
            x=i%8
            y=i//8
            if certain_board[y,x,me]:
                reward+=5
            elif certain_board[y,x,1-me]:
                reward-=5
        
        return reward

    if depth!=0:#valid_boardが存在するのは初めの１回だけ
        valid,sv,valid_board=othello.CheckValid(board,player)
    else:
        valid=True
        sv=True

    if not sv:#終わり
        my_stone=np.sum(board[:,:,me])
        oppose_stone=np.sum(board[:,:,1-me])
        if my_stone>oppose_stone:
            return 10**9
        elif my_stone<oppose_stone:
            return -10**9
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

        if np.sum(valid_board)>=16:
            max_depth=3

        for i in range(64):
            y=i//8
            x=i%8
            if not valid_board[y,x]:
                continue

            next_board=othello.Put(x,y,board,player)
            reward=dfs2(depth+1,max_depth,next_board,None,1-player,me)

            if depth==0:
                hands.append(i)
            
            rewards.append(reward)
    
    if depth==0:#-> player==me
        return hands[argmax(rewards)],max(rewards)

    if player==me:
        return max(rewards)
    else:
        return min(rewards) #0.8*min(rewards)+0.2*mean(rewards)

def Algo(board,valid_board,player):
    stone_count=np.sum(board)
    if stone_count>=57:
        hand,result=dfs(0,board,valid_board,player,player)
    else:
        hand,reward=dfs2(0,3,board,valid_board,player,player)
        #othello.Show(board)
        #print('reward:',reward)


    return hand #int


