
# SVMを使用した自然言語の極性分析

## 1. 自然言語の極性分析とは

自然言語の極性分析では、文章内の感情を検出することを目的としたものが多いです。今回ご紹介する自然言語の極性分析では、任意の文章が  
「ネガティブな文章」なのか、あるいは「ポジティブな文章」なのかを判別します。
  
<br />
## 2. 使用するアルゴリズム：SVM（Support Vector Machine）

今回の自然言語の極性分析に使用する機械学習のアルゴリズムはSVM(Support Vector Machine)と呼ばれるものです。  
SVMは機械学習のなかの「教師あり学習」に用いられる高性能のパターン認識モデルです。

SVMは、基本的には何らかのデータの集合を２クラスに分類する問題に適用されます。今回の極性分析で言えば、自然言語を「ネガティブ」  
「ポジティブ」の２クラスに分類している、ということになります。

◆図：データを２クラスに分類する  

![2class](https://bytebucket.org/snippets/moekoasano/a46A78/raw/7cdc533246478dcad09a2da25fc122714be6624b/2class.PNG)

また、今回は２つの極性「ネガティブ」「ポジティブ」が値を持たないため、「ネガティブ＝0」「ポジティブ＝1」として値を付与することによって、  
ロジスティック回帰を適用します。この値を数学的に表現するのであれば、「自然言語がポジティブである確率」と捉えることができます。  
教師データはあらかじめポジティブかネガティブかが明らかであるため「0」か「1」を付与しますが、未知の自然言語に対してはSVMで判別した結果  
0.5より大きい場合はラベル「1」、0.5以下の場合はラベル「0」を付与します。

このロジスティック回帰を適用する方法を使用することで、２クラス分類問題から多クラス分類問題へ拡張することも可能です。

<br />
## 3. 学習に使用するツール：LIBLINEAR

LIBLINEARはオープンソースの機械学習ライブラリで、線形SVMとロジスティック回帰をサポートしています。  
「train」ファイル、「predict」ファイルの２つを実行するだけで、学習と予測ができます。

### 3-1. インストール

インストールには、以下２種類の方法があります。

① パッケージ管理用のコマンドを使用する  
② LIBLINEARのgit hubリポジトリをクローンする  
<br />
①の場合は、以下のコマンドを実行します。（※環境は、Ubuntu 16.04）
```
$ sudo apt install liblinear-tools
```

②の場合は、以下のコマンドを実行します。
```
$ git clone https://github.com/cjlin1/liblinear.git
```

### 3-2. 学習

学習する際に使用する教師データは、以下の形式で記載する必要があります。
```
【ラベル】 1:【変数1の値】 2:【変数2の値】・・・
```

教師データが格納されているディレクトリに「train」ファイルをコピーし、以下のコマンドを実行します。
```
$ ./train 【教師データファイル名】  
 
※aptコマンドでインストールした場合は、以下のコマンドでも学習可能  
$ liblinear-train 【教師データファイル名】  
```
実行後には、「【教師データファイル名】.model」という名前のモデルファイルが作成されます。

### 3-3. 予測

予測の精度測定用のテストデータについても、「3-2.学習」と同様のフォーマットで作成します。  
「predict」ファイルと3-2で作成されたモデルファイルを使用して、テストデータに対して予測を行い、モデルの精度（正答率）を確認します。  
また、予測の場合は予測結果を出力するファイルも指定する必要があります。  
```
$ ./predict 【テストデータファイル名】 【モデルファイル名】 【結果出力ファイル名】  

※aptコマンドでインストールした場合は、以下のコマンドでも学習可能  
$ liblinear-predict 【テストデータファイル名】 【モデルファイル名】 【結果出力ファイル名】
```

## 4. 手順

今回は、以下の手順で自然言語の極性分析を行いました。

① 自然言語データの入手  
② 自然言語データの加工  
③ LIBLINEARでの学習  
④ LIBLINEARで作成した学習モデルの精度確認  
⑤ 学習モデルから見る自然言語の極性の傾向を出力  


### 4-1. 自然言語データの入手

今回は、SNS「twitter」の「2017年8月3日」に投稿されたツイートを使用しました。  

ツイート（とツイートに関する付加情報）は、json形式で取得できます。取得したjsonファイルから、ツイートの部分のみを取得し、時間×ユーザーごとにテキストファイルに格納しました。  
このとき、泣いている絵文字「😢」が入っているツイートには、ファイル名に「\_n」を、笑っている絵文字「😃」が入っているツイートには、「\_p」を付加しました。  
```
【例】 テキストファイル名  
FujiyamaBeauty_2017_Jul_24_21:53:00_p.txt   
```

### 4-2. 自然言語データの加工

入手したツイートを以下のようにラベルを付与することで教師データを作成しました。
```
０：ネガティブなツイート（泣いている絵文字「😢」が入っているツイート）  
１：ポジティブなツイート（笑っている絵文字「😃」が入っているツイート）
```

#### ★教師データ作成までのデータ加工の流れ

まず、4-1で入手したツイートのjsonファイルの「わかち書き」を行います。  
わかち書きとは、自然言語を単語ごとに分解する処理のことで、今回は形態素ごとに分解しました。  
また、わかち書きの処理は「MeCab」という形態素解析エンジンを使用しました。   
```
$ python3 wakatiAndEmoji.py
```
```
【例】形態素ごとにわかち書き  
けもの　🐯　は　い　て　も　のけもの　🙅　は　いない　😃🌈✨
```  

また、絵文字についてはラベルの振り分け対象となる「😃」と「😢」は取り除き、それ以外は１文字ずつに分解して全て後ろに結合します。  
```  
【例】絵文字の処理  
けもの　は　い　て　も　のけもの　は　いない　🐯　🙅　🌈　✨
```

その後、「😃」が含まれていたツイートには、ファイル名に「\_p\_」を、「😢」が含まれていたツイートにはファイル名に「\_n\_」を加え、  
ポジティブかネガティブかを識別できるようにします。
  
```  
【例】ファイル名の例  
masa1234h123456_2017_Jul_28_11:30:33_p_wakati.txt（ポジティブの場合）  
masa8823sachi_2017_Jun_29_04:16:04_n_wakati.txt（ネガティブの場合）  
```

わかち書きにした形態素にIDを付与します。pickle形式で出力します。  
```
$ python3 giveId.py
```
pickle形式なので中身を見ることはできませんが、出力ファイルのイメージは以下です。  
```  
【例】形態素とIDの対応ファイルイメージ  
けもの:1　は:2　い:3　て:4　も:5　のけもの:6　は:7　いない:8
```  

わかち書きにした形態素と全ツイート（2017年8月3日の全てのツイート）内の出現回数の対応表を作成します。  
出力イメージは上の例と同様で、こちらもpickle形式で出力します。この出力ファイルは基本的には使用せず、ある形態素の出現回数が非常に多く、  
分析に影響をきたす場合のみ使用します。  
```
$ python3 giveFreq.py
```

<br />
最後に、先ほど作成した形態素とIDの対応表を使って、LIBLINEARに入力する形式（ここではSVMファイルと呼びます）へツイートを加工します。  
```
$ python3 makeSvm.py
```
「3-2. 学習」に記載したフォーマットに従うと、SVMファイルのイメージは以下のようになります。  
```
【例】LIBLINEAR入力ファイル  
1 1:1 2:2 3:1 4:1 5:1 6:1 7:1 8:1
```

一番左の「1」はツイートのラベルです。その後は「形態素のID：出現回数」が並びます。ここで使用される出現回数は、「一つのツイート内での出現回数」です。また、今回は出現回数nを「log(n + 1)」としました。

SVMファイルが出力されたら、LIBLINEARで機械学習にかけていきます。


### 4-3. LIBLINEARでの学習

学習を行うにあたって、先ほど出力したSVMファイル内のデータを、「教師データ」と「テストデータ」に分割します。  
データ数は、教師：テスト＝８：２程度としています。

データ分割後は、「3-2.学習」に記載した手順に従って学習を行います。

今回は線形回帰ではなく、ロジスティック回帰を適用したため、コマンドにオプション「-s 0」が入ります。
```
$ ./train  __-s  0__  【教師データファイル名】   
もしくは、  
$ liblinear-train __-s 0__  【教師データファイル名】
```

### 4-4. LIBLINEARで作成した学習モデルの精度確認

4-3で作成されたモデルの精度を確認します。「3-3.予測」に記載した手順に従って予測の精度確認を行います。

今回は線形回帰ではなく、ロジスティック回帰を適用したため、コマンドにオプション「-b 0」が入ります。
```
$ ./predict  __-b  0__  【テストデータファイル名】   
もしくは、  
$ liblinear-predict __-b 0__  【テストデータファイル名】
```

予測精度は以下になりました。上々です！（※括弧内は正解数/テスト回数）
```
Accuracy = 84.5568% (6992/8269)
```

自然言語処理に関する予測精度は、一般的に80〜90％あたりが良いとされています。低い精度はモデルとして問題がありますが、  
高すぎる場合は「Leakage」と呼ばれる別の問題が発生している可能性が高いため、工程の見直しが必要です。  
<br />

### 参考：Leakageとは  
教師データが意図しない付加情報を持つことによって学習モデルや機械学習アルゴリズムに本来以上の性能をもたらす状態。

### 参考サイト  
[Leakage | Kaggle](https://www.kaggle.com/wiki/Leakage)


### 4-5. 学習モデルから見る自然言語の極性の傾向を出力

4-3で作成されたモデルの精度に問題ないことが確認できたため、モデルから「ポジティブな文章に発生しやすい言葉」と「ネガティブな文章に発生しやすい言葉」を
上位10ワードずつ出力します。
```
$ python3 outTop10.py
```
<br />
結果は以下のようになりました。
```
__ポジティブなワード  TOP１０__　※順位：ワード（係数）    
👑1位：おはよう（4.823900374658731）  
  2位：こんにちは（4.399281365006475）  
  3位：👋 （3.161750770218674）  
  4位：こんばんは（3.140766234643241）  
  5位：🌃 （2.843907374046311）  
  6位：✌（2.721985515610678）  
  7位：⤴（2.598121029638836）  
  8位：鳥（2.242509869878366）  
  9位：上手（2.04881634056313）  
 10位：ワクワク（2.021030977814608）  　　
```
➡️　挨拶の後にはポジティブな内容が続きやすい？  
➡️ 「鳥」はちょっと意外・・・！？🕊✨  


<br />
```
__ネガティブなワード  TOP１０__　※順位：ワード（係数）   
👑1位：悲しい（-3.492035374990581）  
  2位：寂しい（-3.416340450429398）  
  3位：感動（-2.988588503853097）  
  4位：たかっ（-2.610280917969484）  
  5位：泣ける（-2.556913512403219）  
  6位：泣い（-2.507611175022146）  
  7位：涙（-2.34718730692362）  
  8位：残念（-2.317099767545713）  
  9位：切ない（-2.185512324493972）    
 10位：泣き（-2.184524742193111）  
```
➡️ 「たかっ」という叶わなかった願望らしき形態素が４位に。。。  
➡️ その他はだいたい泣いています（TДT）  
