import pandas as pd
import sys
from pathlib import Path


def parse_percent(series):
    """Remove trailing percent sign and convert to float."""
    return series.astype(str).str.rstrip('%').astype(float)


def analyze_retention(file_path, output_prefix=None):
    df = pd.read_csv(file_path)

    # Normalize percent columns
    df['影片位置 (%)'] = parse_percent(df['影片位置 (%)'])
    df['訂閱者續看率 (%)'] = parse_percent(df['訂閱者續看率 (%)'])
    df['非訂閱者續看率 (%)'] = parse_percent(df['非訂閱者續看率 (%)'])

    df['觀看差距 (%)'] = df['訂閱者續看率 (%)'] - df['非訂閱者續看率 (%)']
    large_gap = df[df['觀看差距 (%)'] > 10]

    if output_prefix is None:
        output_prefix = Path(file_path).stem

    output_csv = f"{output_prefix}_with_gap.csv"
    df.to_csv(output_csv, index=False)

    analysis_lines = []
    if not large_gap.empty:
        max_row = large_gap.loc[large_gap['觀看差距 (%)'].idxmax()]
        analysis_lines.append(
            f"\u5dee\u503c\u6700\u5927\u7684\u4f4d\u7f6e\u5728 {max_row['影片位置 (%)']}\uFF0C\u5dee\u503c {max_row['觀看差距 (%)']:.2f}%\u3002"
        )
        positions = large_gap['影片位置 (%)'].tolist()
        analysis_lines.append(
            f"\u5171\u5075\u6e2c\u5230 {len(large_gap)} \u500b\u4f4d\u7f6e\u5dee\u503c\u8d85\u904e 10%\u3002\u4f4d\u7f6e\u7bc4\u570d\u7d04\u5728 {positions[0]} \u81f3 {positions[-1]}%\u3002"
        )

        if df.iloc[0]['觀看差距 (%)'] > 10:
            analysis_lines.append(
                "\u5f71\u7247\u958b\u982d\u5c31\u51fa\u73fe\u5927\u91cf\u975e\u8a02\u95b1\u8005\u8df3\u51fa\uFF0C\u53ef\u8003\u616e\u52a0\u5f37\u5f71\u7247\u958b\u5834\u3002"
            )

        range_30_40 = df[(df['影片位置 (%)'] >= 30) & (df['影片位置 (%)'] <= 40)]
        if not range_30_40.empty and (range_30_40['觀看差距 (%)'] > 10).any():
            analysis_lines.append(
                "30%\uFF5E40% \u4f4d\u7f6e\u9644\u8fd1\u89c0\u5bdf\u5230\u660e\u986f\u65b7\u5d16\uFF0C\u53ef\u6aa2\u67e5\u6b64\u6bb5\u5167\u5bb9\u6216\u8f49\u5831\u662f\u5426\u9069\u7576\u3002"
            )
    else:
        analysis_lines.append("\u672a\u89c0\u5bdf\u5230\u5dee\u503c\u8d85\u904e 10% \u7684\u4f4d\u7f6e\u3002")

    analysis_lines.append("\u5efa\u8b70\uff1a\u958b\u5834\u82e5\u6389\u592a\u591a\uFF0C\u53ef\u52a0\u5f37\u5438\u5f15\u529b\uFF1B\u8f49\u5831\u6216\u4e3b\u984c\u5207\u63db\u4fdd\u6301\u7bc0\u594f\u3002")

    analysis_txt = f"{output_prefix}_analysis.txt"
    with open(analysis_txt, 'w', encoding='utf-8') as f:
        for line in analysis_lines:
            f.write(line + "\n")

    print("\u5206\u6790\u5b8c\u6210\u3002\u7d50\u679c\u8f38\u51fa\u81f3:", output_csv, analysis_txt)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("\u7528\u6cd5: python analyze_retention.py retention.csv [output_prefix]")
        sys.exit(1)
    file_path = sys.argv[1]
    prefix = sys.argv[2] if len(sys.argv) > 2 else None
    analyze_retention(file_path, prefix)
