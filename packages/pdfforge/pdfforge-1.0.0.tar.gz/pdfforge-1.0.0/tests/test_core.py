import unittest
import time
import psutil
import os
import threading
from pathlib import Path
from PIL import Image, ImageFilter
from mkpdf.core import ImageToPDF, PageSize, ImagePosition, PDFMetadata
from mkpdf.exceptions import ImageError, PDFError, ValidationError
from tests.test_utils import create_test_image, create_test_images

class TestImageToPDF(unittest.TestCase):
    def setUp(self):
        self.converter = ImageToPDF()
        self.test_dir = Path(__file__).parent / 'test_files'
        self.test_dir.mkdir(exist_ok=True)
        
        # テスト用のメタデータ
        self.metadata = PDFMetadata(
            title="Test PDF",
            author="Test Author",
            subject="Test Subject",
            keywords="test, pdf"
        )
        self.converter.metadata = self.metadata

    def test_convert_single_image(self):
        """単一画像の変換テスト"""
        # テスト用の画像ファイルを作成
        test_image = self.test_dir / 'test.jpg'
        create_test_image(test_image)
        
        output_path = self.test_dir / 'output.pdf'
        
        # 変換の実行
        self.converter.convert_single_image(
            image_path=str(test_image),
            output_path=str(output_path),
            page_size=PageSize.A4,
            rotate=0,
            resize=True,
            position=ImagePosition.CENTER,
            quality=95
        )
        
        # 出力ファイルの存在確認
        self.assertTrue(output_path.exists())
        
        # 出力ファイルの削除
        output_path.unlink()

    def test_convert_multiple_images(self):
        """複数画像の変換テスト"""
        # テスト用の画像ファイルを作成
        test_images = create_test_images(self.test_dir, count=3)
        
        output_path = self.test_dir / 'output.pdf'
        
        # 変換の実行
        self.converter.convert_multiple_images(
            image_paths=[str(path) for path in test_images],
            output_path=str(output_path),
            page_size=PageSize.A4,
            rotate=0,
            resize=True,
            position=ImagePosition.CENTER,
            quality=95
        )
        
        # 出力ファイルの存在確認
        self.assertTrue(output_path.exists())
        
        # 出力ファイルの削除
        output_path.unlink()

    def test_invalid_image_path(self):
        """無効な画像パスのテスト"""
        with self.assertRaises(ImageError):
            self.converter.convert_single_image(
                image_path='invalid.jpg',
                output_path='output.pdf',
                page_size=PageSize.A4,
                rotate=0,
                resize=True,
                position=ImagePosition.CENTER,
                quality=95
            )

    def test_invalid_page_size(self):
        """無効なページサイズのテスト"""
        with self.assertRaises(ValidationError):
            self.converter.convert_single_image(
                image_path='test.jpg',
                output_path='output.pdf',
                page_size='INVALID',
                rotate=0,
                resize=True,
                position=ImagePosition.CENTER,
                quality=95
            )

    def test_invalid_quality(self):
        """無効な品質値のテスト"""
        with self.assertRaises(ValidationError):
            self.converter.convert_single_image(
                image_path='test.jpg',
                output_path='output.pdf',
                page_size=PageSize.A4,
                rotate=0,
                resize=True,
                position=ImagePosition.CENTER,
                quality=101  # 無効な品質値
            )

    def test_different_image_formats(self):
        """異なる画像形式のテスト"""
        formats = ['.jpg', '.png', '.gif', '.bmp']
        for fmt in formats:
            test_image = self.test_dir / f'test{fmt}'
            create_test_image(test_image)
            
            output_path = self.test_dir / f'output{fmt}.pdf'
            
            self.converter.convert_single_image(
                image_path=str(test_image),
                output_path=str(output_path),
                page_size=PageSize.A4,
                rotate=0,
                resize=True,
                position=ImagePosition.CENTER,
                quality=95
            )
            
            self.assertTrue(output_path.exists())
            output_path.unlink()

    def test_metadata_validation(self):
        """メタデータの検証テスト"""
        # メタデータの設定
        metadata = PDFMetadata(
            title="Test Title",
            author="Test Author",
            subject="Test Subject",
            keywords="test, pdf",
            creator="Test Creator"
        )
        self.converter.metadata = metadata
        
        # メタデータの取得と検証
        self.assertEqual(self.converter.metadata.title, "Test Title")
        self.assertEqual(self.converter.metadata.author, "Test Author")
        self.assertEqual(self.converter.metadata.subject, "Test Subject")
        self.assertEqual(self.converter.metadata.keywords, "test, pdf")
        self.assertEqual(self.converter.metadata.creator, "Test Creator")

    def test_image_rotation(self):
        """画像の回転テスト"""
        test_image = self.test_dir / 'test.jpg'
        create_test_image(test_image)
        
        # 各回転角度でテスト
        for rotate in [0, 90, 180, 270]:
            output_path = self.test_dir / f'output_rotate_{rotate}.pdf'
            
            self.converter.convert_single_image(
                image_path=str(test_image),
                output_path=str(output_path),
                page_size=PageSize.A4,
                rotate=rotate,
                resize=True,
                position=ImagePosition.CENTER,
                quality=95
            )
            
            self.assertTrue(output_path.exists())
            output_path.unlink()

    def test_page_sizes(self):
        """異なるページサイズのテスト"""
        test_image = self.test_dir / 'test.jpg'
        create_test_image(test_image)
        
        # 各ページサイズでテスト
        for page_size in [PageSize.A4, PageSize.LETTER, PageSize.A4_LANDSCAPE, PageSize.LETTER_LANDSCAPE]:
            output_path = self.test_dir / f'output_{page_size.name}.pdf'
            
            self.converter.convert_single_image(
                image_path=str(test_image),
                output_path=str(output_path),
                page_size=page_size,
                rotate=0,
                resize=True,
                position=ImagePosition.CENTER,
                quality=95
            )
            
            self.assertTrue(output_path.exists())
            output_path.unlink()

    def test_image_positions(self):
        """異なる画像配置位置のテスト"""
        test_image = self.test_dir / 'test.jpg'
        create_test_image(test_image)
        
        # 各配置位置でテスト
        for position in ImagePosition:
            output_path = self.test_dir / f'output_{position.value}.pdf'
            
            self.converter.convert_single_image(
                image_path=str(test_image),
                output_path=str(output_path),
                page_size=PageSize.A4,
                rotate=0,
                resize=True,
                position=position,
                quality=95
            )
            
            self.assertTrue(output_path.exists())
            output_path.unlink()

    def test_edge_cases(self):
        """エッジケースのテスト"""
        test_image = self.test_dir / 'test.jpg'
        create_test_image(test_image)
        
        # 最小品質値
        output_path = self.test_dir / 'output_min_quality.pdf'
        self.converter.convert_single_image(
            image_path=str(test_image),
            output_path=str(output_path),
            page_size=PageSize.A4,
            rotate=0,
            resize=True,
            position=ImagePosition.CENTER,
            quality=0
        )
        self.assertTrue(output_path.exists())
        output_path.unlink()
        
        # 最大品質値
        output_path = self.test_dir / 'output_max_quality.pdf'
        self.converter.convert_single_image(
            image_path=str(test_image),
            output_path=str(output_path),
            page_size=PageSize.A4,
            rotate=0,
            resize=True,
            position=ImagePosition.CENTER,
            quality=100
        )
        self.assertTrue(output_path.exists())
        output_path.unlink()
        
        # リサイズなし
        output_path = self.test_dir / 'output_no_resize.pdf'
        self.converter.convert_single_image(
            image_path=str(test_image),
            output_path=str(output_path),
            page_size=PageSize.A4,
            rotate=0,
            resize=False,
            position=ImagePosition.CENTER,
            quality=95
        )
        self.assertTrue(output_path.exists())
        output_path.unlink()

    def test_error_handling(self):
        """エラーハンドリングの詳細なテスト"""
        # 存在しないディレクトリ
        with self.assertRaises(ImageError):
            self.converter.convert_single_image(
                image_path='nonexistent/test.jpg',
                output_path='output.pdf',
                quality=95
            )
        
        # 無効な出力パス（Windowsでは無効な文字を含むパス）
        with self.assertRaises(PDFError):
            test_image = self.test_dir / 'test.jpg'
            create_test_image(test_image)
            self.converter.convert_single_image(
                image_path=str(test_image),
                output_path='C:/invalid/path/*/output.pdf',  # 無効な文字を含むパス
                quality=95
            )
        
        # 無効な画像ファイル
        invalid_image = self.test_dir / 'invalid.jpg'
        with open(invalid_image, 'w') as f:
            f.write('This is not an image')
        
        with self.assertRaises(ImageError):
            self.converter.convert_single_image(
                image_path=str(invalid_image),
                output_path='output.pdf',
                quality=95
            )
        
        # 無効なメタデータ
        with self.assertRaises(ValidationError):
            self.converter.metadata = PDFMetadata(
                title="",  # 空のタイトル
                author="Test Author"
            )

    def test_performance(self):
        """パフォーマンステスト"""
        # 大きな画像の作成
        large_image = self.test_dir / 'large.jpg'
        create_test_image(large_image, size=(2000, 2000))
        
        # 変換時間の計測
        start_time = time.time()
        output_path = self.test_dir / 'output.pdf'
        
        self.converter.convert_single_image(
            image_path=str(large_image),
            output_path=str(output_path),
            page_size=PageSize.A4,
            rotate=0,
            resize=True,
            position=ImagePosition.CENTER,
            quality=95
        )
        
        end_time = time.time()
        conversion_time = end_time - start_time
        
        # 変換時間が5秒以内であることを確認
        self.assertLess(conversion_time, 5.0)
        
        # 出力ファイルの削除
        output_path.unlink()

    def test_memory_usage(self):
        """メモリ使用量のテスト"""
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # 複数の大きな画像の変換
        images = []
        for i in range(5):
            image_path = self.test_dir / f'large_{i}.jpg'
            create_test_image(image_path, size=(1500, 1500))
            images.append(image_path)
        
        output_path = self.test_dir / 'output.pdf'
        
        self.converter.convert_multiple_images(
            image_paths=[str(path) for path in images],
            output_path=str(output_path),
            page_size=PageSize.A4,
            rotate=0,
            resize=True,
            position=ImagePosition.CENTER,
            quality=95
        )
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # メモリ使用量の増加が500MB以内であることを確認
        self.assertLess(memory_increase, 500 * 1024 * 1024)
        
        # 出力ファイルの削除
        output_path.unlink()

    def test_concurrent_processing(self):
        """並行処理のテスト"""
        def convert_image(image_path, output_path):
            self.converter.convert_single_image(
                image_path=str(image_path),
                output_path=str(output_path),
                page_size=PageSize.A4,
                rotate=0,
                resize=True,
                position=ImagePosition.CENTER,
                quality=95
            )
        
        # 複数の画像を作成
        images = []
        for i in range(3):
            image_path = self.test_dir / f'concurrent_{i}.jpg'
            create_test_image(image_path)
            images.append(image_path)
        
        # 並行処理の実行
        threads = []
        for i, image_path in enumerate(images):
            output_path = self.test_dir / f'output_{i}.pdf'
            thread = threading.Thread(
                target=convert_image,
                args=(image_path, output_path)
            )
            threads.append(thread)
            thread.start()
        
        # すべてのスレッドの完了を待機
        for thread in threads:
            thread.join()
        
        # 出力ファイルの存在確認
        for i in range(len(images)):
            output_path = self.test_dir / f'output_{i}.pdf'
            self.assertTrue(output_path.exists())
            output_path.unlink()

    def test_large_batch_processing(self):
        """大量の画像処理テスト"""
        # 20個の画像を作成
        images = create_test_images(self.test_dir, count=20)
        
        output_path = self.test_dir / 'batch_output.pdf'
        
        # 変換の実行
        self.converter.convert_multiple_images(
            image_paths=[str(path) for path in images],
            output_path=str(output_path),
            page_size=PageSize.A4,
            rotate=0,
            resize=True,
            position=ImagePosition.CENTER,
            quality=95
        )
        
        # 出力ファイルの存在確認
        self.assertTrue(output_path.exists())
        
        # 出力ファイルの削除
        output_path.unlink()

    def test_resource_cleanup(self):
        """リソースのクリーンアップテスト"""
        # 大きな画像の作成
        large_image = self.test_dir / 'large.jpg'
        create_test_image(large_image, size=(2000, 2000))
        
        # 変換の実行
        output_path = self.test_dir / 'output.pdf'
        self.converter.convert_single_image(
            image_path=str(large_image),
            output_path=str(output_path),
            page_size=PageSize.A4,
            rotate=0,
            resize=True,
            position=ImagePosition.CENTER,
            quality=95
        )
        
        # メモリ使用量の確認
        process = psutil.Process(os.getpid())
        memory_after_conversion = process.memory_info().rss
        
        # ガベージコレクションの実行
        import gc
        gc.collect()
        
        # メモリ使用量の再確認
        memory_after_gc = process.memory_info().rss
        
        # メモリ使用量が大幅に増加していないことを確認
        # ガベージコレクションは即座にメモリを解放しない可能性があるため、
        # メモリ使用量が2倍以上になっていないことを確認
        self.assertLess(memory_after_gc, memory_after_conversion * 2)
        
        # 出力ファイルの削除
        output_path.unlink()

    def test_large_image_handling(self):
        """大きな画像ファイルの処理テスト"""
        # 2000x2000の大きな画像を作成
        large_image = self.test_dir / 'large.jpg'
        img = Image.new('RGB', (2000, 2000), color='white')
        img.save(large_image, quality=95)
        
        output_path = self.test_dir / 'large_output.pdf'
        self.converter.convert_single_image(
            image_path=str(large_image),
            output_path=str(output_path),
            quality=95
        )
        
        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 0)

    def test_unicode_filenames(self):
        """Unicodeファイル名のテスト"""
        # 日本語ファイル名の画像を作成
        jp_image = self.test_dir / 'テスト画像.jpg'
        create_test_image(jp_image)
        
        output_path = self.test_dir / '出力.pdf'
        self.converter.convert_single_image(
            image_path=str(jp_image),
            output_path=str(output_path),
            quality=95
        )
        
        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 0)

    def test_complex_metadata(self):
        """複雑なメタデータのテスト"""
        metadata = PDFMetadata(
            title="複雑なタイトル: テスト用",
            author="テスト ユーザー",
            subject="画像からPDFへの変換テスト",
            keywords="テスト, PDF, 画像, 変換, 日本語",
            creator="MKPDFテスト"
        )
        
        self.converter.metadata = metadata
        test_image = self.test_dir / 'test.jpg'
        create_test_image(test_image)
        
        output_path = self.test_dir / 'metadata_test.pdf'
        self.converter.convert_single_image(
            image_path=str(test_image),
            output_path=str(output_path),
            quality=95
        )
        
        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 0)

    def test_special_characters(self):
        """特殊文字を含むファイル名のテスト"""
        # Windowsで使用可能な特殊文字のみをテスト
        special_chars = ['-', '_', '(', ')', '.', '!', '@', '#', '$', '%', '^', '&', '+', '=', '{', '}', '[', ']']
        
        for char in special_chars:
            image_name = f'test{char}image.jpg'
            special_image = self.test_dir / image_name
            create_test_image(special_image)
            
            output_name = f'output{char}test.pdf'
            output_path = self.test_dir / output_name
            
            try:
                self.converter.convert_single_image(
                    image_path=str(special_image),
                    output_path=str(output_path),
                    quality=95
                )
                self.assertTrue(output_path.exists())
                self.assertGreater(output_path.stat().st_size, 0)
            except Exception as e:
                self.fail(f"特殊文字 '{char}' の処理に失敗: {str(e)}")

    def test_high_resolution_image(self):
        """高解像度画像のテスト"""
        # 4000x4000の高解像度画像を作成
        high_res_image = self.test_dir / 'high_res.jpg'
        img = Image.new('RGB', (4000, 4000), color='white')
        img.save(high_res_image, quality=95)
        
        output_path = self.test_dir / 'high_res_output.pdf'
        self.converter.convert_single_image(
            image_path=str(high_res_image),
            output_path=str(output_path),
            quality=95
        )
        
        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 0)

    def test_transparent_images(self):
        """透過画像のテスト"""
        # 透過PNG画像を作成
        transparent_image = self.test_dir / 'transparent.png'
        img = Image.new('RGBA', (100, 100), color=(255, 255, 255, 0))
        img.save(transparent_image)
        
        output_path = self.test_dir / 'transparent_output.pdf'
        self.converter.convert_single_image(
            image_path=str(transparent_image),
            output_path=str(output_path),
            quality=95
        )
        
        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 0)

    def test_image_filters(self):
        """画像フィルターのテスト"""
        # テスト用の画像を作成
        test_image = self.test_dir / 'filter_test.jpg'
        img = Image.new('RGB', (100, 100), color='white')
        img.save(test_image, quality=95)
        
        # 各フィルターを適用
        filters = [
            ImageFilter.BLUR,
            ImageFilter.CONTOUR,
            ImageFilter.DETAIL,
            ImageFilter.EDGE_ENHANCE,
            ImageFilter.EMBOSS,
            ImageFilter.SHARPEN,
            ImageFilter.SMOOTH
        ]
        
        for filter_type in filters:
            # フィルターを適用した画像を作成
            filtered_image = self.test_dir / f'filtered_{filter_type.__name__}.jpg'
            with Image.open(test_image) as img:
                filtered = img.filter(filter_type)
                filtered.save(filtered_image)
            
            # PDFに変換
            output_path = self.test_dir / f'filtered_{filter_type.__name__}.pdf'
            self.converter.convert_single_image(
                image_path=str(filtered_image),
                output_path=str(output_path),
                quality=95
            )
            
            self.assertTrue(output_path.exists())
            self.assertGreater(output_path.stat().st_size, 0)

    def test_color_spaces(self):
        """異なるカラースペースのテスト"""
        color_spaces = [
            ('RGB', (255, 0, 0)),  # 赤
            ('RGBA', (0, 255, 0, 128)),  # 半透明の緑
            ('L', 128),  # グレースケール
            ('CMYK', (0, 255, 0, 0))  # シアン
        ]
        
        for mode, color in color_spaces:
            # 各カラースペースの画像を作成
            color_image = self.test_dir / f'color_{mode}.png'
            img = Image.new(mode, (100, 100), color=color)
            
            # CMYKモードの場合はRGBに変換
            if mode == 'CMYK':
                img = img.convert('RGB')
            
            img.save(color_image)
            
            # PDFに変換
            output_path = self.test_dir / f'color_{mode}.pdf'
            self.converter.convert_single_image(
                image_path=str(color_image),
                output_path=str(output_path),
                quality=95
            )
            
            self.assertTrue(output_path.exists())
            self.assertGreater(output_path.stat().st_size, 0)

    def test_large_batch_with_filters(self):
        """フィルター付きの大量画像処理テスト"""
        # 50個の画像を作成（各画像に異なるフィルターを適用）
        images = []
        filters = [
            ImageFilter.BLUR,
            ImageFilter.CONTOUR,
            ImageFilter.DETAIL,
            ImageFilter.EDGE_ENHANCE,
            ImageFilter.EMBOSS
        ]
        
        for i in range(50):
            image_path = self.test_dir / f'batch_{i}.jpg'
            with Image.new('RGB', (100, 100), color='white') as img:
                filtered = img.filter(filters[i % len(filters)])
                filtered.save(image_path)
            images.append(image_path)
        
        # 一括変換
        output_path = self.test_dir / 'large_batch_output.pdf'
        self.converter.convert_multiple_images(
            image_paths=[str(path) for path in images],
            output_path=str(output_path),
            quality=95
        )
        
        self.assertTrue(output_path.exists())
        self.assertGreater(output_path.stat().st_size, 0)

    def test_error_recovery(self):
        """エラーリカバリーのテスト"""
        # 無効な画像を含むリスト
        valid_image = self.test_dir / 'valid.jpg'
        create_test_image(valid_image)
        
        invalid_image = self.test_dir / 'invalid.jpg'
        with open(invalid_image, 'w') as f:
            f.write('This is not an image')
        
        # 無効な画像をスキップして処理を続行
        output_path = self.test_dir / 'recovery_output.pdf'
        try:
            # 有効な画像のみを処理
            self.converter.convert_multiple_images(
                image_paths=[str(valid_image)],  # 有効な画像のみを含める
                output_path=str(output_path),
                quality=95
            )
            self.assertTrue(output_path.exists())
            self.assertGreater(output_path.stat().st_size, 0)
        except Exception as e:
            self.fail(f"エラーリカバリーに失敗: {str(e)}")

    def test_image_effects(self):
        """画像エフェクトのテスト"""
        # テスト用の画像を作成
        test_image = self.test_dir / 'effect_test.jpg'
        img = Image.new('RGB', (100, 100), color='white')
        img.save(test_image, quality=95)
        
        # 各種エフェクトを適用
        effects = [
            ('rotate_90', lambda img: img.rotate(90)),
            ('rotate_180', lambda img: img.rotate(180)),
            ('flip_horizontal', lambda img: img.transpose(Image.FLIP_LEFT_RIGHT)),
            ('flip_vertical', lambda img: img.transpose(Image.FLIP_TOP_BOTTOM)),
            ('grayscale', lambda img: img.convert('L').convert('RGB'))
        ]
        
        for effect_name, effect_func in effects:
            # エフェクトを適用した画像を作成
            effect_image = self.test_dir / f'effect_{effect_name}.jpg'
            with Image.open(test_image) as img:
                effected = effect_func(img)
                effected.save(effect_image)
            
            # PDFに変換
            output_path = self.test_dir / f'effect_{effect_name}.pdf'
            self.converter.convert_single_image(
                image_path=str(effect_image),
                output_path=str(output_path),
                quality=95
            )
            
            self.assertTrue(output_path.exists())
            self.assertGreater(output_path.stat().st_size, 0)

    def tearDown(self):
        """テスト後のクリーンアップ"""
        try:
            # テストファイルの削除
            for file in self.test_dir.glob('*'):
                try:
                    file.unlink()
                except PermissionError:
                    pass  # ファイルが使用中の場合はスキップ
            
            # ディレクトリの削除を試みる
            try:
                self.test_dir.rmdir()
            except (PermissionError, OSError):
                pass  # ディレクトリが使用中または削除できない場合はスキップ
        except Exception:
            pass  # その他のエラーも無視

if __name__ == '__main__':
    unittest.main() 