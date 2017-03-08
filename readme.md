Library Paste
----

###導入方法

1. PackageControlを入れてない場合は入れる（[PackageControle](https://packagecontrol.io/installation#st2)）
2. コマンドパレットを開いて（macなら⌘+shift+P、windowsはctrl+shift+P）「Add Repository」
3. 「 https://github.com/snuke/LibraryPaste 」と入力してEnter
4. コマンドパレットを開いて「Install Packages」
5. 「LibraryPaste」と入力してEnter
6. コマンドパレットを開いて「Browse Packages」
7. 6で開いたPackagesフォルダからLibraryPasteフォルダを探して開く
8. 「root.txt」を開いて、自分のライブラリがあるフォルダへのパスを書く
9. 「Default (使っているOS名).sublime-keymap」を開いて、「"keys": ["なんちゃら"]」となってるところを好きなキーバインドに書き換える（僕はMacで"super+r"と"super+k"にしてます）

###使い方

以下のルールでコードを書き、"command+r"。（違うキーバインドにした場合はそれ）

|記法|説明|
|---|---|
|[*foo*]|"*foo*.cpp" の中身を貼り付ける（行頭に書いたときのみ）|
|空のファイル|"template.cpp" の中身を貼り付ける|
|scn *a*,*b:l*|scanf("%d%lld",&*a*,&*b*); みたいに置換される（詳細は下に）|
|df *a*,*b:l*|int a; ll b;scanf("%d%lld",&*a*,&*b*); みたいに置換される（詳細は下に）|
|print,dl,*a*,*b*|printf("%d %lld",*a*,*b*); みたいに置換される（詳細は下に）|
|cout,*a*,*b*;|cout<<*a*<<" "<<*b*<<endl; みたいに置換される(cin,cerrも同様)|
|[}/[rand]|６桁の乱数（100000~999999）に置換される|

コードを参考にして自分流に改造するのがおすすめです。

また、"command+k"で下になにかが出てくるので貼りたいライブラリの名前を入れると、最初に現れる空行にライブラリが貼られる。（詳細は下に）

###scn/df について

scn foo,bar... などと書くと scanf に変換してくれる。foo(bar)の部分は、

- *a* と書くと "%d",&*a* にな
- *a*:◯ と書くと "%◯",&*a* になる
- *a*:c の場合は " %c",&*a* になる
- *a*:s の場合は "%s",*a* になる
- *a*:l の場合は "%lld",&*a* になる

df の場合はさらに変数宣言までよしなに追加してくれる。

#####例

```c
scn a,b:c,c:s,d:l;
scn a,b
while (scn a);
if (scn a,b==scn c,d) { scn e; scn f,g;}
df a,b:c,c:s,d:l,e:f
```
↓

```c
scanf("%d %c%s%lld",&a,&b,c,&d);
scanf("%d%d",&a,&b);
while (scanf("%d",&a));
if (scanf("%d%d",&a,&b)==scanf("%d%d",&c,&d)) { scanf("%d",&e); scanf("%d%d",&f,&g);}
int a;
char b;
ll d;
double e;
scanf("%d %c%s%lld%lf",&a,&b,c,&d,&e);
```

2 行目の例の通り行末のセミコロンは省略できる。
3,4 行目の例の通り記号で区切れたりする。（cin/cout/cerr/printとは仕様が違う）

### print について

print,dd,a,b などと書くと printf に変換してくれる。

ddの部分はフォーマット指定子をよしなにいれると良い。
lにした場合は %lld になる。
fにした場合は %.10f になる。

#####例

```c
print,dd,a,b;
print,dlfs,a,b,c,d.c_str()
```

↓

```c
printf("%d %d\n",a,b);
printf("%d %lld %.10f %s\n",a,b,c,d.c_str());
```

###macroペーストモードについて
"command+k"で下になにかが出てくるので貼りたいライブラリの名前を入れると、最初に現れる空行にライブラリが貼られる。
これは本来macroペースト用で、*root*/macro/hoge.cpp のような場所にマクロ（とかtypedefとか）を入れておくといい感じに貼られる。
ただ、普通のライブラリを貼るときにも使えて、*root*/hoge.cpp のような場所に置いてあるライブラリを先頭に空行を付けて張ってくれる。
また、普通のライブラリを貼るとき、`hoge;`のようにセミコロンを末尾につけるとインラインで展開される。


