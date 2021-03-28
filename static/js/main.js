const length=8
var me=0
const stone_color=['black','white']

//set grid
board_grid=document.getElementById('board_grid')
for (i=0;i<length;i++){
    row=document.createElement('div')
    row.classList.add('row')
    for(j=0;j<length;j++){
        cell=document.createElement('div')
        cell.classList.add('cell')
        
        stone=document.createElement('div')
        stone.classList.add('stone')
        stone.id='cell-'+i+'-'+j

        cell.appendChild(stone)
        cell.addEventListener('click',function(){
            tmp=this.childNodes[0].id.split('-')
            x=tmp[2]
            y=tmp[1]
            Put(x,y,me)
        })

        row.appendChild(cell)
    }
    board_grid.appendChild(row)
}


//initialize
var board=[]
var valid_board=[]
var now_playing=0

for(i=0;i<length;i++){
    tmp=[]
    for(j=0;j<length;j++){
        tmp.push([0,0])
    }
    board.push(tmp)
}

tmp_func=(x,y,player)=>{
    board[y][x][player]=1
    document.getElementById('cell-'+y+'-'+x).classList.add(stone_color[player])
}
tmp_func(length/2-1,length/2-1,1)
tmp_func(length/2,length/2,1)
tmp_func(length/2-1,length/2,0)
tmp_func(length/2,length/2-1,0)


//put stone
function Put(x,y,player){
    x=Number(x)
    y=Number(y)

    if (now_playing!=player){
        return false
    }
    if (board[y][x][1-player]){
        return false
    }

    is_valid_action=false
    
    dxy=[
            [-1,-1],[0,-1],[1,-1],
            [-1, 0],       [1, 0],
            [-1, 1],[0, 1],[1, 1],
        ]
    for(i=0;i<dxy.length;i++){
        dx=dxy[i][0]
        dy=dxy[i][1]
        nowx=x
        nowy=y
        while(true){
            nowx+=dx
            nowy+=dy
            if(nowx==-1 || nowx==length || nowy==-1 || nowy==length){
                break        
            }
            if(board[nowy][nowx][player]==0 && board[nowy][nowx][1-player]==0){
                break
            }
            if(board[nowy][nowx][player]){
                if(Math.max(Math.abs(nowx-x),Math.abs(nowy-y))==1){//同じ色が2連続
                    break
                }

                board[y][x][player]=1
                document.getElementById('cell-'+y+'-'+x).classList.add(stone_color[player])
                Reverse(x,y,nowx,nowy,dx,dy,player)
                is_valid_action=true
                break
            }
        }
    }
    if (is_valid_action){
        if (now_playing==me){
            Notify('AI思考中...')
            Send('/ai', {'b':Board2Str(board)}, callback)
        }else{
            Notify('あなたの番です')
        }
        now_playing=1-now_playing
        return true
    }else{
        return false
    }
}
function Reverse(x1,y1,x2,y2,dx,dy,player){
    nowx=x1
    nowy=y1
    while(true){
        nowx+=dx
        nowy+=dy
        if (nowx==x2 && nowy==y2){
            return
        }
        board[nowy][nowx][player]=1
        board[nowy][nowx][1-player]=0
        document.getElementById('cell-'+nowy+'-'+nowx).classList.remove(stone_color[1-player])
        document.getElementById('cell-'+nowy+'-'+nowx).classList.add(stone_color[player])
    }
}

function Notify(str,mode){
    document.getElementById('notification_msg').innerText=str
}
Notify('あなたの番です')


function Board2Str(board){
    s=''
    for(i=0;i<8;i++){
        for(j=0;j<8;j++){
            if(board[i][j][me]){
                s+='u'
            }
            else if(board[i][j][1-me]){
                s+='c'
            }else{
                s+='0'
            }
        }
    }
    return s
}

function callback(dic){
    if(dic['msg']=='success'){
        tmp=Number(dic['hand'])
        x=tmp%8
        y=(tmp-x)/8
        Put(x,y,1-me)
    }else if(dic['msg']=='pass'){
        Notify('Pass - あなたの番です。')
    }else if(dic['msg']=='done'){
        End()
    }else{
        console.warn('unexpected msg'+dic['msg'])
    }
}

function End(){
    //終了処理
}


//TODO : ユーザー側で手がなくなった場合。
//         アニメーション