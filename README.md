# はじめに
本プログラムは、[SFM-basic-リポジトリのguideブランチのプログラム](https://github.com/SakamotoNorihito/SFM-basic-.git)を実行した際に出力されるCSVデータを用いて、避難の様子を描画することを目的に作成されました。コードはPythonで記述されています。

# 動作環境
OS:Microsoft Windows 11  
実行環境:VisualStudioCode  

## 実行に必要なパッケージ
・Pillow  
・natsort  
・pandas  
・matplotlib

# 使用方法
## CSVファイルの読み込み
CSVファイル読み込みのために、ファイルの絶対パスを取得します。
```
#CSVファイルの読み込み
CSV_DATA = "C:\\Users\\mashiko234\\Documents\\研究室\\出力結果　まとめ\\通常の避難\\simulation(basic)25.csv"
```

同様に、画像を保存するためのフォルダについてのパスも取得します。
```
#画像保存先フォルダのパスを取得
path_dir = pathlib.Path('C:\\Users\\mashiko234\\Documents\\プログラム（Python）\\避難の様子')
```

## プログラムの実行
プログラムを実行すると、各時刻ごとの避難の様子を描画したスナップショットとそれらを連結したアニメーションが保存先フォルダに生成されます。  

下記の例は
```
R_ind = 3;			//誘導者の誘導半径(m)
R_vis = 2;			//エージェントの視界半径(m)
```
の時の避難の様子です。

### スナップショット
![0秒 (1)](https://github.com/SakamotoNorihito/evacuation-drawing/assets/137757680/6c835bc2-1a6f-4d7c-8fbd-a2c438f2221a)

### アニメーション
![animation](https://github.com/SakamotoNorihito/evacuation-drawing/assets/137757680/9588d9a0-cdfe-44ac-86ae-943c37fe0abe)

# 作成者
坂本矩仁
