import pydeck as pdk
import pandas as pd
import streamlit as st
import io
import sys
import numpy as np

# y = np.arange(5, 10)
# for i in y:
#   print(f"{i}")
#   print("{x}".format(x=i))


# number = st.number_input('数値を入力してください', min_value=0.01, max_value=1.0, value=0.1)
r = st.slider("radius", 1, 100, 10) # スライダー

data = pd.DataFrame(None)
uploaded_file = st.file_uploader("Upload CSV file ", type='csv') # ファイルアップロード
if uploaded_file is not None:
  data = pd.read_csv(uploaded_file)
# else:
#   sys.exit()

data = pd.read_csv("./data/data_small.csv")

cell_size = 0.1
data["longitude"] = (data["pickup_longitude"] // cell_size + 0.5) * cell_size
data["latitude"] = (data["pickup_latitude"] // cell_size + 0.5) * cell_size

# data = pd.read_csv("./data/data_small.csv")
# print(data["tip_amount"].sum())

# st.write(data)
lat = st.selectbox("latitude", data.columns, index=6) # セレクトボックス
lon = st.selectbox("longitude", data.columns, index=5) # セレクトボックス
height = st.selectbox("height", data.columns, index=3) # セレクトボックス

sum_height = "sum_"+str(height)
# for tooltip
# elevation_item_str = "<b>{item}</b>: {{{item}}}, {{{lon}}}, {{{lat}}}".format(item=str(ave_height), lon=str(lon), lat=str(lat))
# elevation_item_str = "<b>{item}</b>: {{{item}}}".format(item=str(sum_height))
elevation_item_str = "<b>{item}</b>: {{{item}}}".format(item="sum_"+height)

# each query
q_type = st.selectbox("query type", ["sum", "average", "max", "min", "count"])

min_lat = int(data[lat].min() * r) # error if pandas is from dp_pandas
max_lat = int(data[lat].max() * r) # error if pandas is from dp_pandas
min_lon = int(data[lon].min() * r) # error if pandas is from dp_pandas
max_lon = int(data[lon].max() * r)  # error if pandas is from dp_pandas
col_num = max_lat - min_lat + 10
row_num = max_lon - min_lon + 10

coord = []
for i in range(row_num):
  tmp = []
  for j in range(col_num):
    tmp.append(pd.DataFrame(None)) # ここでNoneを入れるとdp_numpyを使ってくれない
  coord.append(tmp)

for ind, row in data.iterrows():
  row_lat = int(row[lat]*r) - min_lat
  row_lon = int(row[lon]*r) - min_lon
  coord[row_lon][row_lat] = pd.concat([coord[row_lon][row_lat], row.to_frame().T], join='outer', axis=0) # 同じ区画のデータを連結
  # print("row=", row.to_frame().T)

df = pd.DataFrame(None)
for i in range(row_num):
  for j in range(col_num):
    longitude = (i + min_lon + 0.5) / r # 中心に据えるため0.5を足す
    latitude = (j + min_lat + 0.5) / r
    if (q_type == "sum"):
      if (coord[i][j].empty):
        continue
      sum = coord[i][j]['passenger_count'].agg('sum')
      add_df = pd.DataFrame([[longitude, latitude, sum]], columns=[lon, lat, 'sum_'+height])
      df = pd.concat([df, add_df])
# print(df)
# print(height)

st.pydeck_chart(pdk.Deck(
  map_style=None,
  initial_view_state=pdk.ViewState(
      map_provider="mapbox",
      # for NY
      latitude=40.71,
      longitude=-74.0,
      zoom=12,
      pitch=50,
    ),
    layers=[
      pdk.Layer(
        "ColumnLayer",
        data=df,
        # data = data,
        get_position=[lon, lat],
        get_elevation='sum_'+height,
        # get_elevation="tip_amount",
        elevation_scale=50,
        get_fill_color=[64, 64, 255, 100],
        radius=4200/r*10,
        pickable=True,
        auto_highlight=True,
      )
    ],
    tooltip={
      'html': elevation_item_str,
      'style': {
        'color': 'white'
      }
    }
))
