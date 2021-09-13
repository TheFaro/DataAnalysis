ser = {
    'index' : [0,1,2,3],
    'data' : [145, 142, 38, 13],
    'name' : 'songs'
}

def get(ser, idx):
    value_idx = ser['index'].index(idx)
    print ser['data'][value_idx]

get(ser, 1)

songs = {
    'index' : ['Paul', 'John', 'George', 'Ringo'],
    'data' : [145,142,38,13],
    'name' : 'counts'
}

get(songs, 'John')