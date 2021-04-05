import joblib

from agent_algo import Algo
import numpy as np

class Board:
    def __init__(self,length,save_history=True):
        self.now_player= 0 # 0,1
        self.done=False 
        
        self.length=length
        if length%2:
            raise Exception('length mus be even number')
        
        self.board=np.zeros((length,length,2)).astype('bool')
        
        self.board[length//2,length//2,0]=1
        self.board[length//2-1,length//2-1,0]=1
        self.board[length//2-1,length//2,1]=1
        self.board[length//2,length//2-1,1]=1

        self.save_history=save_history
        self.stone_count=4

        if save_history:
            self.board_history=[]
            self.valid_board_history=[]
            self.action_history=[]

        self.CheckValid()

    def Reverse(self,c1,c2):#c1,c2:tuple(x,y)
        player=self.now_player
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

            self.board[nowy,nowx,player]=1
            self.board[nowy,nowx,1-player]=0
            

    def Put(self,x,y,):
        #(x,y)にコマを置く。
        player=self.now_player
        if not self.valid_board[y,x]:
            raise Exception('action in out of rule')
        if self.save_history:
            self.board_history.append(self.board.copy())
            self.valid_board_history.append(self.valid_board.copy().flatten())
            self.action_history.append((x,y,player)) #このboardで次に誰がどこに置くか

        for dx,dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
            nowx=x+dx
            nowy=y+dy
            if nowx==-1 or nowx==self.length or nowy==-1 or nowy==self.length:
                continue

            if not self.board[nowy,nowx,1-player]:
                continue

            while True:
                nowx+=dx
                nowy+=dy
                if nowx==-1 or nowx==self.length or nowy==-1 or nowy==self.length:
                    break 

                if self.board[nowy,nowx,player]==0 and self.board[nowy,nowx,1-player]==0:
                    break 

                if self.board[nowy,nowx,player]:
                    self.Reverse((x,y),(nowx,nowy))            
                    break
        

        self.stone_count+=1
        #print('turn',self.stone_count-4)
        self.board[y,x,player]=1
        self.now_player=1-self.now_player
        self.CheckValid()


    def CheckValid(self,second_time=False): #今のplayerがどこに石を置けるか？
        valid=False#一つでも石を置く場所があるか？
        valid_board=np.zeros((self.length,self.length)).astype('bool')

        for i in range(self.length**2):
            x,y=i%self.length,i//self.length
            player=self.now_player
            flag=False
            if self.board[y,x,player] or self.board[y,x,1-player]:
                continue#置いた場所にすでに石がある

            for dx,dy in [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]:
                nowx=x+dx
                nowy=y+dy
                if nowx==-1 or nowx==self.length or nowy==-1 or nowy==self.length or not self.board[nowy,nowx,1-player]:
                    continue #置いた場所＋dに相手の駒がない or そこが場外

                while True:
                    nowx+=dx
                    nowy+=dy
                    if nowx==-1 or nowx==self.length or nowy==-1 or nowy==self.length:
                        break #場外

                    if self.board[nowy,nowx,player]==0 and self.board[nowy,nowx,1-player]==0:
                        break #空マス

                    if self.board[nowy,nowx,player]:
                        flag=True
                        break

                if flag:
                    break
    
            if flag:#ある位置に置ける
                valid=True
                valid_board[y,x]=1

        self.valid=valid
        self.valid_board=valid_board

        if not valid:
            if second_time:
                self.done=True
            else:
                self.now_player=1-self.now_player
                self.CheckValid(second_time=True)

        return valid,valid_board

    def Show(self):
        for i in range(self.length):
            s=''
            for j in range(self.length):
                if self.board[i,j,0] and self.board[i,j,1]:
                    raise Exception

                if self.board[i,j,0]:
                    s+='●'
                elif self.board[i,j,1]:
                    s+='〇'
                else:
                    s+='__'
            print(s)

        print()
        
import random
def RandomDecide(valid_board):
    while True:
        r=random.randint(0,8**2-1)
        y,x=r//8,r%8
        if valid_board[y,x]:
            return y*8+x

def play(game_no):
    me=0
    B=Board(8)
    while not B.done:
        if game_no==-1:print('player:',B.now_player)
        
        if B.now_player==me:
            res=Algo(B.board,B.valid_board,me)
        else:
            res=RandomDecide(B.valid_board)
        B.Put(res%8,res//8)
        
        if game_no==-1:
            B.Show()
            print('---------------------\n\n\n')

        #print('\r','game{} : {}'.format(game_no,'|'+'#'*(B.stone_count)+' '*(64-B.stone_count))+'|',end="") #ゲージの初期値が4/60だが気にしない

    my_stone=np.sum(B.board[:,:,me])
    opp_stone=np.sum(B.board[:,:,1-me])

    #print('\r game{} : me:{} opp:{} {}'.format(game_no,my_stone,opp_stone,'win' if my_stone>opp_stone else 'lose' if my_stone<opp_stone else 'tie'),end="")

    return my_stone>opp_stone


if __name__ == '__main__':
    #play(-1)
    n=500
    result = joblib.Parallel(n_jobs=-3,verbose=10)(joblib.delayed(play)(i) for i in range(n))
    print('勝率{:.2f}%'.format(sum(result)/n*100))