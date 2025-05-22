#  Docune（ドキュン）	

##  目的

**Docune（ドキュン）** は、研究論文や技術文献の PDF を
**管理・閲覧・メモ・検索** できるようにすることを目的とした文献管理アプリです。

市販の文献管理ソフトは

* 有料で手が出しにくかったり
* 操作感が合わなかったり

と、なかなか「これだ！」と思えるものに出会えませんでした。

そこで、文献管理ツールを目指してこのアプリを開発しました。

##  主な機能

詳細な使い方は[こちら](/use/document/use.md)で確認できます。


###  基本機能
- 文献（タイトル・著者・出版年・カテゴリ・タグ）の登録・編集・削除
- PDFファイルのアップロードと表示

- メモ記述・保存（Markdown対応）

- 進捗状況（未読／途中／読了）の管理

###  AI機能
**AIによる類似文献検索**（SentenceTransformer + Cosine Similarity）ができます。

- PDF本文をベクトル化し、他の文献と類似度を比較
- 類似文献はボタン1つで検索＆表示

###  UI/UX
- Tailwind CSS で統一されたレスポンシブデザイン
- Alpine.js による表示切替

##  利用ライブラリ

| 分類     | 使用技術                  |
|----------|---------------------------|
| バックエンド | Django 5.x     |
| フロントエンド | Tailwind CSS, Alpine.js     |
| PDF処理  | `pdfminer.six` |
| 類似検索 | `sentence-transformers` (MiniLM) |
| メモ形式 | Markdown（`markdown` パッケージ） |

---

## 💡 起動方法

### 起動方法1(batファイル)
batファイルを使って動かす場合は、PYTHON_EXEでPythonのパスを指定してください。

### 起動方法2

すでに、pythonの環境がある場合は次のようにライブラリをインストールして実行することができます。

```bash
# 環境構築
pip install -r requirements.txt

# マイグレーション
python manage.py migrate

# 開発サーバー起動
python manage.py runserver
```

