# Image to PDF Converter (pdfforge)

様々な形式の画像を高品質なPDFに変換するPythonライブラリです。バッチ変換やメタデータ付与、コマンドライン操作、設定ファイルによるカスタマイズなど、実用的な機能を多数搭載しています。

## 特徴

- 複数の画像を1つのPDFに結合
- 様々な画像形式に対応（PNG, JPEG, BMP, GIF, TIFF, WebP, HEIC）
- 画像の前処理機能
  - リサイズ
  - 回転
  - フィルター適用（ぼかし、シャープ化、エッジ検出など）
  - 色空間変換
- 進捗表示
- エラーハンドリング
- 設定ファイルによるカスタマイズ
- コマンドラインインターフェース

## インストール

```bash
pip install pdfforge
```

## 基本的な使い方

### コマンドラインから

```bash
# 基本的な使用方法
pdfforge input/*.jpg output.pdf

# 画像のリサイズを指定
pdfforge input/*.jpg output.pdf --width 800 --height 600

# 画像の回転を指定
pdfforge input/*.jpg output.pdf --rotate 90

# フィルターを適用
pdfforge input/*.jpg output.pdf --filter blur

# 複数のオプションを組み合わせ
pdfforge input/*.jpg output.pdf --width 800 --rotate 90 --filter sharpen
```

### Pythonコードから

```python
from pdfforge import ImageToPDF

# 基本的な使用方法
converter = ImageToPDF()
converter.convert("input/*.jpg", "output.pdf")

# 画像のリサイズを指定
converter = ImageToPDF(width=800, height=600)
converter.convert("input/*.jpg", "output.pdf")

# 画像の回転を指定
converter = ImageToPDF(rotate=90)
converter.convert("input/*.jpg", "output.pdf")

# フィルターを適用
from PIL import ImageFilter
converter = ImageToPDF(filter=ImageFilter.BLUR)
converter.convert("input/*.jpg", "output.pdf")

# 複数のオプションを組み合わせ
converter = ImageToPDF(
    width=800,
    height=600,
    rotate=90,
    filter=ImageFilter.SHARPEN
)
converter.convert("input/*.jpg", "output.pdf")
```

## 高度な使い方

### 設定ファイルの使用

`~/.pdfforge/config.json`に設定ファイルを作成することで、デフォルトの設定をカスタマイズできます：

```json
{
    "width": 800,
    "height": 600,
    "rotate": 0,
    "filter": "none",
    "output_format": "PDF",
    "compression_quality": 85
}
```

### エラーハンドリング

```python
from pdfforge import ImageToPDF, ConversionError

try:
    converter = ImageToPDF()
    converter.convert("input/*.jpg", "output.pdf")
except ConversionError as e:
    print(f"変換エラー: {e}")
```

### 進捗表示のカスタマイズ

```python
from pdfforge import ImageToPDF
from tqdm import tqdm

converter = ImageToPDF(progress_bar=tqdm)
converter.convert("input/*.jpg", "output.pdf")
```

## サポートされている画像形式

- PNG
- JPEG
- BMP
- GIF
- TIFF
- WebP
- HEIC

## サポートされているフィルター

- ぼかし（Blur）
- シャープ化（Sharpen）
- エッジ検出（Edge Detection）
- 輪郭検出（Contour）
- エンボス（Emboss）
- スムージング（Smooth）

## ライセンス

MITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 貢献

1. このリポジトリをフォーク
2. 新しいブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 作者

- tikisan - 初期開発者

## 謝辞

- [Pillow](https://python-pillow.org/) - 画像処理ライブラリ
- [ReportLab](https://www.reportlab.com/) - PDF生成ライブラリ
- [tqdm](https://github.com/tqdm/tqdm) - プログレスバーライブラリ

## 注意事項

- 大量の画像を処理する場合は、メモリ使用量に注意してください
- HEIC形式の画像を処理するには、追加のライブラリが必要な場合があります
- 一部の画像形式は、Pillowのインストール時に追加の依存関係が必要な場合があります

## トラブルシューティング

### 一般的な問題

1. **メモリエラー**
   - 画像のサイズを小さくする
   - バッチ処理を使用する
   - システムのメモリを増やす

2. **画像形式のサポート**
   - Pillowが正しくインストールされているか確認
   - 必要な追加ライブラリをインストール

3. **パフォーマンスの問題**
   - 画像の前処理を最適化
   - マルチスレッド処理を検討
   - バッチサイズを調整

### よくある質問

1. **Q: 大量の画像を処理するには？**
   A: バッチ処理を使用し、適切なバッチサイズを設定してください。

2. **Q: 特定の画像形式がサポートされていない場合は？**
   A: Pillowのドキュメントを確認し、必要な追加ライブラリをインストールしてください。

3. **Q: メモリ使用量を最適化するには？**
   A: 画像のサイズを小さくし、バッチ処理を使用してください。

## 開発者向け情報

### テスト

```bash
# すべてのテストを実行
pytest

# 特定のテストを実行
pytest tests/test_core.py

# カバレッジレポートを生成
pytest --cov=pdfforge tests/
```

### コードスタイル

このプロジェクトは[PEP 8](https://www.python.org/dev/peps/pep-0008/)に従っています。

### ドキュメント

```bash
# ドキュメントを生成
cd docs
make html
```

## 更新履歴

### 0.1.0 (2024-03-XX)
- 初期リリース
- 基本的な画像からPDFへの変換機能
- 画像の前処理機能
- コマンドラインインターフェース
- 設定ファイルサポート

## ロードマップ

- [ ] マルチスレッド処理のサポート
- [ ] より多くの画像形式のサポート
- [ ] PDFの暗号化機能
- [ ] 画像の自動最適化
- [ ] バッチ処理の改善
- [ ] より詳細な進捗表示
- [ ] エラーログの強化
- [ ] ユニットテストの追加
- [ ] ドキュメントの拡充
- [ ] パフォーマンスの最適化 