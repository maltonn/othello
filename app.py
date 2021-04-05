import os
import numpy as np
from flask import *
app = Flask(__name__)

import othello
from agent_algo import Algo

@app.route('/start')
def just_call():
    return 'connected'

@app.route('/', methods=['GET'])
def Main():
    return render_template('index.html')

@app.route('/ai',methods=['GET'])
def ai():
    me=0 #先手・後手どちらでもこれで大丈夫
    board=np.zeros((8,8,2))
    board_str = request.args.get('b')

    for i in range(8):
        for j in range(8):
            s=board_str[i*8+j]
            if s=='u':#user
                board[i,j,1]=1
            elif s=='c':#cpu
                board[i,j,0]=1
            else:#s=0 : space
                pass
    
    valid,second_valid,valid_board=othello.CheckValid(board,me)
    if not second_valid:
        return jsonify({"msg": "done"})
    if not valid:
        return jsonify({"msg": "pass"})
    
    res=Algo(board,valid_board,me)
    print(res//8,res%8)

    next_board=othello.Put(res%8,res//8,board,me)

    valid,_,_=othello.CheckValid(next_board,1-me)
    
    return jsonify({"msg": "success","hand":str(res),"userpass":not valid})

if __name__ == '__main__':
    app.run()
    port = int(os.getenv('PORT', 5000))

