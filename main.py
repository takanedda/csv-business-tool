
import pandas as pd

# CSVファイルを読み込む
try:
    df = pd.read_csv("sample.csv", encoding="utf-8-sig")
except FileNotFoundError:
    print("エラー：sample.csv が見つかりません。")
    raise SystemExit(1)

# 必要な列があるか確認する
required_columns = ["商品", "個数", "価格"]
missing_columns = [
    col for col in required_columns if col not in df.columns
]

if missing_columns:
    print("必要な列がありません:", missing_columns)
    raise SystemExit(1)

# 商品名の空欄を確認する
errors_found = False

empty_product = (
    df["商品"].isna()
    | df["商品"].astype("string").str.strip().eq("").fillna(True)
)

if empty_product.any():
    rows = (df.index[empty_product] + 2).tolist()
    print("商品名が空欄です。CSVの行番号:", rows)
    errors_found = True

# 個数と価格が数値か確認する
for col in ["個数", "価格"]:
    original = df[col].copy()
    converted = pd.to_numeric(original, errors="coerce")
    invalid = converted.isna()

    if invalid.any():
        rows = (df.index[invalid] + 2).tolist()
        print(f"{col}に空欄または数値以外の値があります。行番号:", rows)
        errors_found = True

    df[col] = converted

    # 重複データを検出する
duplicates = df.duplicated(
    subset=["商品", "個数", "価格"],
    keep=False
)

if duplicates.any():
    print("重複している可能性があるデータ:")
    print(df.loc[duplicates, ["商品", "個数", "価格"]])
else:
    print("重複データはありません。")


# 不備があれば、計算と出力を中止する
if errors_found:
    print("データを修正してから、もう一度実行してください。")
    raise SystemExit(1)

# 売上金額を計算する
df["売上金額"] = df["個数"] * df["価格"]

# 合計売上を計算する
total_sales = df["売上金額"].sum()

# Excelファイルに保存する
df.to_excel("売上集計.xlsx", index=False)

print(df)
print("合計売上:", total_sales, "円")
print("Excelファイルを出力しました！")
