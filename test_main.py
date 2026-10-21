
import os
import subprocess
import sys
from pathlib import Path

MAIN_PY = Path(__file__).with_name("main.py")


def run_program(tmp_path, csv_data):
    # テスト用のCSVを作成する
    (tmp_path / "sample.csv").write_text(
        csv_data,
        encoding="utf-8-sig"
    )

    # 本体プログラムを実行する
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    return subprocess.run(
        [sys.executable, str(MAIN_PY)],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env
    )


def test_sales_calculation_and_excel(tmp_path):
    csv_data = (
        "商品,個数,価格\n"
        "キーボード,2,3000\n"
        "マウス,3,1500\n"
        "モニター,1,20000\n"
    )

    result = run_program(tmp_path, csv_data)

    assert result.returncode == 0
    assert "合計売上: 30500 円" in result.stdout
    assert (tmp_path / "売上集計.xlsx").exists()


def test_duplicate_detection(tmp_path):
    csv_data = (
        "商品,個数,価格\n"
        "マウス,3,1500\n"
        "マウス,3,1500\n"
    )

    result = run_program(tmp_path, csv_data)

    assert result.returncode == 0
    assert "重複している可能性があるデータ" in result.stdout


def test_invalid_data_stops_processing(tmp_path):
    csv_data = (
        "商品,個数,価格\n"
        "マウス,,1500\n"
    )

    result = run_program(tmp_path, csv_data)

    assert result.returncode != 0
    assert "数値以外の値があります" in result.stdout
    assert not (tmp_path / "売上集計.xlsx").exists()
