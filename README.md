- pandas
- openpyxl
- pytest

## 実行方法
1. 必要なライブラリをインストールします。

   python -m pip install pandas openpyxl pytest

2. sample.csvを用意します。
3. main.pyを実行します。

   python main.py

4. 売上集計.xlsxが出力されます。

## 自動テスト
次のコマンドでテストを実行できます。

   python -m pytest -v

売上計算、重複検出、入力不備の検出をテストします。