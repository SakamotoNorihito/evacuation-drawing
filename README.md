# はじめに
本プログラムは、[SFM-basic-リポジトリの避難誘導用ブランチのプログラム](https://github.com/SakamotoNorihito/evacuation-drawing.git)を実行した際に出力されるCSVデータを用いて、避難の様子を描画することを目的に作成されました。コードはPythonで記述されています。

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
プログラムを実行すると、各時刻ごとの避難の様子を描画したpngファイルとそれらを連結したgifファイルが保存先フォルダに生成されます。

# 作成者
坂本矩仁
