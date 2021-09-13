df = {
    'index' : [0,1,2],
    'cols' : [
        { 
            'name' : 'growth',
            'data' : [.5, .7, 1.2]
        },
        { 
            'name' : 'Name',
            'data' : ['Paul', 'George', 'Ringo']
        },
    ]
}

def get_row(df, idx):
    results = []
    value_idx = df['index'].index(idx)
    for col in df['cols']:
        results.append(col['data'][value_idx])
    print results

def get_col(df, name):
    for col in df['cols']:
        if col['name'] == name:
            print col['data']


get_row(df, 0)