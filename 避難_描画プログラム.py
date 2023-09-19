from PIL import Image
from natsort import natsorted
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pathlib
import os
import glob

# GIFアニメーション生成用関数
def create_gif(in_dir, out_filename):
    path_list = natsorted(glob.glob(os.path.join(*[path_dir, '*'])))    # ファイルパスをソートしてリストする
    imgs = []                                                           # 画像をappendするための空配列を定義
 
    # ファイルのフルパスからファイル名と拡張子を抽出
    for i in range(len(path_list)):
        img = Image.open(path_list[i])                          # 画像ファイルを1つずつ開く
        imgs.append(img)                                        # 画像をappendで配列に格納していく
 
    # appendした画像配列をGIFにする。durationで持続時間、loopでループ数を指定可能。
    imgs[0].save(out_filename,save_all=True, append_images=imgs[1:], optimize=False, duration=100, loop=0)


#CSVファイルの読み込み
CSV_DATA = "C:\\Users\\mashiko234\\source\\repos\\SFM(basic)\\SFM(basic)\\simulation(basic)2.csv"
col_names = ['c{0:02d}'.format(i) for i in range(209)]
df = pd.read_csv(CSV_DATA, header=None, encoding="Shift-JIS",names=col_names)
# print(df)
# df.info()

#シミュレーション条件（部屋の大きさ等）格納用データフレーム
df_simulationCondition = df.iloc[[0,1],:]
room_size_x = float(df_simulationCondition.iat[1,0])
room_size_y = float(df_simulationCondition.iat[1,1])
width_exit = float(df_simulationCondition.iat[1,2])
R_agent = float(df_simulationCondition.iat[1,3])
R_ind = float(df_simulationCondition.iat[1,4])
# print(room_size_x)
# print(room_size_y)
# print(width_exit)
# print(R_agent)
# print(R_ind)

#座標データ格納用データフレーム
headerList = list(df.iloc[2,2:])
df_coordinate = df.iloc[3:,2:]
df_coordinate.columns = headerList
# print(headerList)
# print(df_coordinate)

#x, y座標の抽出
df_x_coord = df_coordinate.filter(like='x座標',axis='columns')
df_y_coord = df_coordinate.filter(like='y座標',axis='columns')
# print(df_x_coord)
# print(df_y_coord)

#抽出したx, y座標を誘導者, 避難者のものに振り分け
df_x_coord_g = df_x_coord.filter(regex='^誘',axis='columns')
df_y_coord_g = df_y_coord.filter(regex='^誘',axis='columns')
df_x_coord_e = df_x_coord.filter(regex='^避',axis='columns')
df_y_coord_e = df_y_coord.filter(regex='^避',axis='columns')
# print(df_x_coord_g)
# print(df_y_coord_g)
# print(df_x_coord_e)
# print(df_y_coord_e)

#画像保存先フォルダのパスを取得
path_dir = pathlib.Path('C:\\Users\\mashiko234\\Documents\\プログラム（Python）\\避難の様子')

#１秒毎のスナップショットを取得
for i in range(len(df_x_coord)):
    #描画領域の準備
    fig = plt.figure()
    ax = plt.axes()

    #部屋の壁の描画
    ax.vlines(x=[0,room_size_x],ymin=-room_size_y/2,ymax=room_size_y/2,colors="k")
    ax.hlines(y=[-room_size_y/2,room_size_y/2],xmin=0,xmax=room_size_x,colors="k")
    #出口の描画
    ax.vlines(room_size_x,-width_exit/2,width_exit/2,colors="w")

    #描画領域のアスペクト比の設定
    plt.axis('scaled')
    ax.set_aspect('equal')

    #軸目盛りを非表示にする
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    #枠線を非表示にする
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)

    #誘導者の描画
    for j in range(len(df_x_coord_g.columns)):
        guide_x = float(df_x_coord_g.iat[i,j])
        guide_y = float(df_y_coord_g.iat[i,j])
        guide = patches.Circle(xy=(guide_x,guide_y),radius=R_agent,fc='r',ec='r')
        circle_ind = patches.Circle(xy=(guide_x,guide_y),radius=R_ind,ec='k',fill=False,linestyle='dashed')
        ax.add_patch(guide)
        ax.add_patch(circle_ind)

    #避難者の描画
    for j in range(len(df_x_coord_e.columns)):
        evacuee_x = float(df_x_coord_e.iat[i,j])
        evacuee_y = float(df_y_coord_e.iat[i,j])
        evacuee = patches.Circle(xy=(evacuee_x,evacuee_y),radius=R_agent,fc='b',ec='b')        
        ax.add_patch(evacuee)
    
    #画像を保存先フォルダに保存
    path_img = path_dir.joinpath(f'{i}秒.png')
    fig.savefig(path_img)

#gifを保存先フォルダに保存
path_img = path_dir.joinpath('animation.gif')
create_gif(in_dir=path_dir,out_filename=path_img)

#plt.show()