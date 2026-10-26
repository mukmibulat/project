import pandas as pd
from fastapi import FastAPI, HTTPException
from segment_tree import SegmentTreeIndex
from hash_map import build_hash_index
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

df_hash = pd.read_csv('data/amazon.csv')
keys = df_hash['OrderID'].astype(str)
hash_index = build_hash_index(keys)

df_segment = pd.read_csv('data/amazon.csv')
df_segment = df_segment.sort_values('OrderDate').reset_index(drop=True)

segment_index = SegmentTreeIndex(df_segment)

app.mount(
    '/static',
    StaticFiles(directory='static'),
    name='static'
)


@app.get('/')
def home():
    return FileResponse('static/index.html')

@app.get('/api/hash-map/{order_id}')
def get_order_by_id(order_id: str):
    row_id = hash_index.get(order_id)

    if row_id is None:
        raise HTTPException(
            status_code=404,
            detail='order не найден'
        )

    return df_hash.iloc[row_id].to_dict()


@app.get('/api/segment-tree/sum')
def get_quantity_sum(left: int, right: int):
    if left < 0 or right >= len(segment_index.values) or left > right:
        raise HTTPException(
            status_code=400,
            detail='Invalid range'
        )

    total = segment_index.range_query(left, right)

    return {
        'left': left,
        'right': right,
        'quantity_sum': total
    }


@app.put('/api/segment-tree/update')
def update_quantity(pos: int, value: int):
    if pos < 0 or pos >= len(segment_index.values):
        raise HTTPException(
            status_code=400,
            detail='Invalid position'
        )

    segment_index.update(pos, value)

    return {
        'position': pos,
        'new_value': value,
        'message': 'quantity обновлено'
    }


