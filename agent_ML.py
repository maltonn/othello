import random
import tensorflow as tf
gpu_devices = tf.config.experimental.list_physical_devices('GPU')
for device in gpu_devices:
    tf.config.experimental.set_memory_growth(device, True)
from tensorflow.keras.models import load_model


def RandomDecide(valid_board):
    while True:
        r=random.randint(0,8**2-1)
        y,x=r//8,r%8
        if valid_board[y,x]:
            return r

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
        return RandomDecide(valid_board)