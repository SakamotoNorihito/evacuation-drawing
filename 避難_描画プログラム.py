from PIL import Image
from natsort import natsorted
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import pathlib
import os
import glob

# GIFアニメーション作成　参考サイト
# Pythonで複数画像からGIFを作る時に便利な処理まとめ
# https://watlab-blog.com/2021/01/31/python-gif/#%E5%8B%95%E7%94%BB%E3%81%8B%E3%82%89%E9%9D%99%E6%AD%A2%E7%94%BB%E3%82%92%E6%8A%BD%E5%87%BA%E3%81%99%E3%82%8B

# GIFアニメーション生成用関数
def create_gif(in_dir, out_filename):
    path_list = natsorted(glob.glob(os.path.join(*[path_dir, '*'])))    # ファイルパスをソートしてリストする
    imgs = []                                                           # 画像をappendするための空配列を定義
 
    # ファイルのフルパスからファイル名と拡張子を抽出
    for i in range(len(path_list)):
        img = Image.open(path_list[i])                          # 画像ファイルを1つずつ開く
        imgs.append(img)                                        # 画像をappendで配列に格納していく
 
    # appendした画像配列をGIFにする。durationで持続時間(単位：ms)、loopでループ数を指定可能。
    imgs[0].save(out_filename,save_all=True, append_images=imgs[1:], optimize=False, duration=100, loop=0)

#CSVファイルの読み込み
CSV_DATA = "C:\\Users\\mashiko234\\Documents\\研究室\\修士論文関係\\取得データ\\視界・誘導半径と避難効率の関係（誘導者の初期配置：先行研究）\\Rind=5\\Rvis=2\\simulation(basic)6.csv"
#CSV_DATA = "C:\\Users\\mashiko234\\source\\repos\\SFM(basic)\\SFM(basic)\\simulation(basic)0.csv"
col_names = ['c{0:02d}'.format(i) for i in range(10000)]
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
R_vis = float(df_simulationCondition.iat[1,5])
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

#描画したい要素の選択
draw_e = True       #希望方向
draw_v = False      #速度
draw_t = 131        #描画したい秒数

#e_x, e_y（希望方向）の抽出
df_e_x = df_coordinate.filter(like='e_x',axis='columns')
df_e_y = df_coordinate.filter(like='e_y',axis='columns')
# print(df_e_x)
# print(df_e_y)

#抽出したe_x, e_y（希望方向）を誘導者, 避難者のものに振り分け
df_e_x_g = df_e_x.filter(regex='^誘',axis='columns')
df_e_y_g = df_e_y.filter(regex='^誘',axis='columns')
df_e_x_e = df_e_x.filter(regex='^避',axis='columns')
df_e_y_e = df_e_y.filter(regex='^避',axis='columns')
# print(df_e_x_g)
# print(df_e_y_g)
# print(df_e_x_e)
# print(df_e_y_e)

#v_x, v_y（速度）の抽出
df_v_x = df_coordinate.filter(like='のv_x',axis='columns')
df_v_y = df_coordinate.filter(like='のv_y',axis='columns')
# print(df_v_x)
# print(df_v_y)

#抽出したv_x, v_y（速度）を誘導者, 避難者のものに振り分け
df_v_x_g = df_v_x.filter(regex='^誘',axis='columns')
df_v_y_g = df_v_y.filter(regex='^誘',axis='columns')
df_v_x_e = df_v_x.filter(regex='^避',axis='columns')
df_v_y_e = df_v_y.filter(regex='^避',axis='columns')
# print(df_v_x_g)
# print(df_v_y_g)
# print(df_v_x_e)
# print(df_v_y_e)

#画像保存先フォルダのパスを取得
path_dir = pathlib.Path('C:\\Users\\mashiko234\\Documents\\プログラム（Python）\\避難の様子')

#１秒毎のスナップショットを取得
for i in range(len(df_x_coord)):
    #指定時間になったら描画を停止する
    if i == draw_t:
        break

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

    #出口視認可能領域の描画
    circle_exit_can_be_seen = patches.Circle(xy=(room_size_x,0),radius=R_vis,ec='k',fill=False,linestyle='dashed')
    ax.add_patch(circle_exit_can_be_seen)
    #出口視認可能領域の描画（後で消す）
    circle_exit_can_be_seen_test = patches.Circle(xy=(room_size_x,0),radius=R_vis - 0,ec='k',fill=False,linestyle='dashed')
    ax.add_patch(circle_exit_can_be_seen_test)
    #出口視認可能領域の描画（後で消す）
    circle_exit_can_be_seen_test = patches.Circle(xy=(room_size_x,0),radius=R_vis + 0,ec='k',fill=False,linestyle='dashed')
    ax.add_patch(circle_exit_can_be_seen_test)

    #誘導者の描画
    for j in range(len(df_x_coord_g.columns)):
        #誘導者のx, y座標の抽出
        guide_x = float(df_x_coord_g.iat[i,j])
        guide_y = float(df_y_coord_g.iat[i,j])
        #誘導者の希望方向の抽出
        guide_e_x = float(df_e_x_g.iat[i,j])
        guide_e_y = float(df_e_y_g.iat[i,j])
        #誘導者の速度の抽出
        guide_v_x = float(df_v_x_g.iat[i,j])
        guide_v_y = float(df_v_y_g.iat[i,j])
        #誘導者と誘導半径の描画
        guide = patches.Circle(xy=(guide_x,guide_y),radius=R_agent,fc='r',ec='r')
        circle_ind = patches.Circle(xy=(guide_x,guide_y),radius=R_ind,ec='r',fill=False,linestyle='dashed')
        circle_vis = patches.Circle(xy=(guide_x,guide_y),radius=R_vis,ec='k',fill=False,linestyle='dashed')
        ax.add_patch(guide)
        ax.add_patch(circle_ind)
        ax.add_patch(circle_vis)        
        #誘導者の希望方向の描画（赤色）
        if draw_e == True:
            ax.arrow(x=guide_x,y=guide_y,dx=guide_e_x,dy=guide_e_y,head_width=0.2,head_length=0.1,fc='r',ec='r')
        #誘導者の速度の描画（黒色）
        elif draw_v == True:
            ax.arrow(x=guide_x,y=guide_y,dx=guide_v_x,dy=guide_v_y,head_width=0.2,head_length=0.1)

    #避難者の描画
    for j in range(len(df_x_coord_e.columns)):
        #避難者のx, y座標の抽出
        evacuee_x = float(df_x_coord_e.iat[i,j])
        evacuee_y = float(df_y_coord_e.iat[i,j])
        #避難者の希望方向の抽出
        evacuee_e_x = float(df_e_x_e.iat[i,j])
        evacuee_e_y = float(df_e_y_e.iat[i,j])
        #避難者の速度の抽出
        evacuee_v_x = float(df_v_x_e.iat[i,j])
        evacuee_v_y = float(df_v_y_e.iat[i,j])
        #避難者の描画        
        evacuee = patches.Circle(xy=(evacuee_x,evacuee_y),radius=R_agent,fc='b',ec='b')        
        ax.add_patch(evacuee)
        #避難者の希望方向の描画（赤色）
        if draw_e == True:
            ax.arrow(x=evacuee_x,y=evacuee_y,dx=evacuee_e_x,dy=evacuee_e_y,head_width=0.2,head_length=0.1,fc='r',ec='r')        
        #避難者の速度の描画（黒色）
        elif draw_v == True:
            ax.arrow(x=evacuee_x,y=evacuee_y,dx=evacuee_v_x,dy=evacuee_v_y,head_width=0.2,head_length=0.1)        
    
    #画像を保存先フォルダに保存
    path_img = path_dir.joinpath(f'{i}秒.png')
    fig.savefig(path_img)

#gifを保存先フォルダに保存
path_img = path_dir.joinpath('animation.gif')
create_gif(in_dir=path_dir,out_filename=path_img)

#plt.show()