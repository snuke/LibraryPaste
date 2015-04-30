Library Paste
----

###導入方法

1. PackageControlを入れてない場合は入れる（[PackageControle](https://packagecontrol.io/installation#st2)）
2. コマンドパレットを開いて（macなら⌘+shift+P、windowsはctrl+shift+P）「add rep」と入力してEnter
3. 「 https://github.com/snuke/LibraryPaste.git 」と入力してEnter
4. コマンドパレットを開いて「install」と入力してEnter
5. 「LibraryPaste」と入力してEnter
6. メニューから「Sublime Text 2」→「Preferences」→「Browse Packages...」で開く
7. 「LibraryPaste.py」を開いて、4行目にある「root = ""」のところに自分のライブラリがあるフォルダへのパスを書く
8. 「Default (使っているOS名).sublime-keymap」を開いて、「"keys": ["なんちゃら"]」となってるところを好きなキーバインドに書き換える（僕はMacで"super+r"にしてます）

###使い方

以下のルールでコードを書き、"ctrl+r" を押す。（違うキーバインドにした場合はそれを押す）

|記法|説明|
|---|---|
|[*foo*]|"*foo*.cpp" の中身を貼り付ける（行頭に書いたときのみ動作します）|
|空のファイル|"template.cpp" の中身を貼り付ける|
|scn *a*,*b*|scanf("%d%d",&*a*,&*b*) に置換される（詳細は下に書きます）|
|[rand]|６桁の乱数（100000~999999）に置換される（行頭でなくても動作します）|
|cout,*a*,*b*;|cout<<a<<" "<<b<<endl; みたいに置換される|

###scn について

scn foo,bar... と書くと scanf に変換してくれます。foo(bar)の部分は、

- *a* と書くと "%d",&*a* になります
- *a*-◯ と書くと "%◯",&*a* になります
- *a*-c の場合は " %c",&*a* になります
- *a*-s の場合は "%s",*a* になります
- *a*-l の場合は "%lld",&*a* になります


#####例

```c
scn a,b-c,c-s,d-l;
scn a,b
while (scn a);
if (scn a,b==scn c,d) { scn e; scn f,g;}
```
↓

```c
scanf("%d %c%s%lld",&a,&b,c,&d);
scanf("%d%d",&a,&b);
while (scanf("%d",&a));
if (scanf("%d%d",&a,&b)==scanf("%d%d",&c,&d)) { scanf("%d",&e); scanf("%d%d",&f,&g);}
```

2 行目の例の通り、行末のセミコロンは省略できます。
