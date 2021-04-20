const length=8
var me=1
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
        stone.id='stone-'+i+'-'+j

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
    document.getElementById('stone-'+y+'-'+x).classList.add(stone_color[player])
}
tmp_func(length/2-1,length/2-1,1)
tmp_func(length/2,length/2,1)
tmp_func(length/2-1,length/2,0)
tmp_func(length/2,length/2-1,0)

Send('/ai', {'b':Board2Str(board)}, callback)


if (now_playing==1){
    Send('/ai', {'b':Board2Str(board)}, callback)
}

//put stone

hands_log=[]
function Put(x,y,player){
    x=Number(x)
    y=Number(y)
    
    if (now_playing!=player){
        Notify('AIが考えてます。ちょっと待ってね')
        return false
    }
    if (board[y][x][1-player] || board[y][x][player]){
        Notify('そこには置けません。')
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
                document.getElementById('stone-'+y+'-'+x).classList.add(stone_color[player])
                Reverse(x,y,nowx,nowy,dx,dy,player)
                is_valid_action=true
                break
            }
        }
    }
    if (is_valid_action){
        hands_log.push(x*8+y)
        if (now_playing==me){
            Notify('AI思考中...')
            f3()
            function f3(){//裏返している間は、boardが更新されきっていないので、更新されるまでしばらく待つ
                if(now_reversing){
                    setTimeout(()=>{
                        f3()
                    },200)
                }else{
                    Send('/ai', {'b':Board2Str(board)}, callback)
                }
            }
        }else{
            Notify('あなたの番です')
        }
        now_playing=1-now_playing
        return true
    }else{
        Notify('そこには置けません。\n（あなたは'+(player?'白':'黒')+'番です）')
        return false
    }
}

now_reversing=0
function Reverse(x1,y1,x2,y2,dx,dy,player){
    now_reversing++
    console.log({player,x1,y1,x2,y2,dx,dy})
    nowx=Number(x1)
    nowy=Number(y1)
    f(nowx,nowy)
    function f(nowx,nowy){
        nowx+=dx
        nowy+=dy
        if (nowx==x2 && nowy==y2){
            now_reversing--
            return
        }
        board[nowy][nowx][player]=1
        board[nowy][nowx][1-player]=0
        stone=document.getElementById('stone-'+nowy+'-'+nowx)
        stone.style.transform=stone.style.transform.includes('180')?'rotateX(0) rotateY(0)':'rotateX(180deg) rotateY(180deg)'
        f2(stone)

        setTimeout(()=>{
            f(nowx,nowy)
        },100)
    }

    function f2(stone){
        setTimeout(()=>{
            stone.classList.remove(stone_color[1-player])
            stone.classList.add(stone_color[player])
        },100)
    }
}

function Notify(str,mode){
    document.getElementById('notification_msg').innerText=str
}
Notify('注）研究用に、打った手のデータは保存されます')


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
        Notify('AIは何もできません。 \n あなたの番です。')
        now_playing=me
    }else if(dic['msg']=='done'){
        End()
    }else{
        console.warn('unexpected msg'+dic['msg'])
    }

    if(dic['userpass']){
        Notify('パスするしかなさそうです。\n AIの番になります。')
        now_playing=1-me
        setTimeout(()=>{
            Send('/ai', {'b':Board2Str(board)}, callback)
        },1000)
    }
}

function End(){
    user_stone=0
    cpu_stone=0
    for(i=0;i<8;i++){
        for(j=0;j<8;j++){
            if(board[i][j][me]){
                user_stone++
            }else if(board[i][j][1-me]){
                cpu_stone++
            }
        }
    }
    if (user_stone!=cpu_stone){
        Notify('試合終了！\n'+user_stone+':'+cpu_stone+'で、あなたの'+(user_stone>cpu_stone?'勝ち':'負け')+'です')
    }else{
        window.alert('試合終了！\n引き分けです')
    }
    Send('https://sdyzrnc9i1.execute-api.us-east-2.amazonaws.com/default/light-api',{'sid':'othello','method':'add','hand':hands_log.join('-'),'result':user_stone>cpu_stone?'win':user_stone<cpu_stone?'lose':'tie','user_stone':user_stone,'cpu_stone':cpu_stone,'board':Board2Str(board),'user_color':stone_color[me]},null)
}

/*
stones=document.getElementsByClassName('stone')
L=[]
console.log(stones.length)
for(i=0;i<stones.length;i++){
    stones[i].addEventListener('click',function(){
        id=this.id
        this.style.backgroundColor='red'
        y=Number(id.split('-')[1])
        x=Number(id.split('-')[2])
        L.push(y*8+x)
        console.log(L)
    })
}
*/