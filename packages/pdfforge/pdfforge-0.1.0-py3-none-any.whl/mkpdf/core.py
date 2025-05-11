from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter, landscape
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
from typing import Union, List, Tuple, Optional, Dict
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from .exceptions import ImageError, PDFError, ValidationError

class PageSize(Enum):
    A4 = A4
    LETTER = letter
    A4_LANDSCAPE = landscape(A4)
    LETTER_LANDSCAPE = landscape(letter)

class ImagePosition(Enum):
    CENTER = "center"
    TOP_LEFT = "top_left"
    TOP_RIGHT = "top_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_RIGHT = "bottom_right"

@dataclass
class PDFMetadata:
    title: str = ""
    author: str = ""
    subject: str = ""
    keywords: str = ""
    creator: str = "MKPDF"

    def __post_init__(self):
        """メタデータのバリデーション"""
        if not self.title:
            raise ValidationError("タイトルは空にできません")
        if not self.author:
            raise ValidationError("著者は空にできません")
        if not self.creator:
            raise ValidationError("作成者は空にできません")

class ImageToPDF:
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif']
        self._quality = 95
        self._metadata = PDFMetadata(
            title="Untitled Document",
            author="MKPDF",
            subject="Image to PDF Conversion",
            keywords="PDF, Image, Conversion",
            creator="MKPDF"
        )
    
    @property
    def quality(self) -> int:
        return self._quality
    
    @quality.setter
    def quality(self, value: int):
        if not 0 <= value <= 100:
            raise ValidationError(f"無効な品質値です: {value}")
        self._quality = value
    
    @property
    def metadata(self) -> PDFMetadata:
        return self._metadata
    
    @metadata.setter
    def metadata(self, value: PDFMetadata):
        self._metadata = value

    def _validate_image(self, image_path: str) -> bool:
        """画像ファイルの検証を行う"""
        if not os.path.exists(image_path):
            raise ImageError(f"ファイルが見つかりません: {image_path}")
        
        try:
            with Image.open(image_path) as img:
                img.verify()
        except Exception as e:
            raise ImageError(f"無効な画像ファイルです: {image_path}") from e
        
        return True

    def _get_image_size(self, image: Image.Image, max_size: Tuple[int, int]) -> Tuple[int, int]:
        """画像サイズを計算する"""
        width, height = image.size
        max_width, max_height = max_size
        
        # アスペクト比を維持しながらリサイズ
        ratio = min(max_width/width, max_height/height)
        return int(width * ratio), int(height * ratio)

    def _calculate_position(
        self,
        image_size: Tuple[int, int],
        page_size: Tuple[int, int],
        position: ImagePosition
    ) -> Tuple[float, float]:
        """画像の配置位置を計算する"""
        width, height = image_size
        page_width, page_height = page_size
        
        if position == ImagePosition.CENTER:
            return (page_width - width) / 2, (page_height - height) / 2
        elif position == ImagePosition.TOP_LEFT:
            return 0, page_height - height
        elif position == ImagePosition.TOP_RIGHT:
            return page_width - width, page_height - height
        elif position == ImagePosition.BOTTOM_LEFT:
            return 0, 0
        elif position == ImagePosition.BOTTOM_RIGHT:
            return page_width - width, 0
        else:
            return (page_width - width) / 2, (page_height - height) / 2

    def convert_single_image(
        self,
        image_path: str,
        output_path: str,
        page_size: Union[PageSize, Tuple[int, int]] = PageSize.A4,
        rotate: int = 0,
        resize: bool = True,
        position: ImagePosition = ImagePosition.CENTER,
        quality: Optional[int] = None
    ) -> None:
        """
        単一の画像をPDFに変換する
        
        Args:
            image_path: 入力画像のパス
            output_path: 出力PDFのパス
            page_size: PDFのページサイズ
            rotate: 回転角度（0, 90, 180, 270）
            resize: 画像をページサイズに合わせてリサイズするかどうか
            position: 画像の配置位置
            quality: 画像の品質（0-100）
        """
        if not isinstance(page_size, PageSize):
            raise ValidationError(f"無効なページサイズです: {page_size}")
        if rotate not in [0, 90, 180, 270]:
            raise ValidationError(f"無効な回転角度です: {rotate}")
        if not isinstance(position, ImagePosition):
            raise ValidationError(f"無効な配置位置です: {position}")
        if quality is not None and not 0 <= quality <= 100:
            raise ValidationError(f"無効な品質値です: {quality}")

        try:
            # 出力ディレクトリの存在確認と作成
            output_dir = os.path.dirname(output_path)
            if output_dir and not os.path.exists(output_dir):
                try:
                    os.makedirs(output_dir)
                except (OSError, IOError) as e:
                    raise PDFError(f"出力ディレクトリの作成に失敗しました: {e}")

            # 画像の読み込み
            try:
                img = Image.open(image_path)
            except (IOError, OSError) as e:
                raise ImageError(f"画像の読み込みに失敗しました: {e}")

            # 画像の回転
            if rotate != 0:
                img = img.rotate(rotate, expand=True)

            # ページサイズの取得
            if isinstance(page_size, PageSize):
                page_width, page_height = page_size.value
            else:
                page_width, page_height = page_size

            # 画像のリサイズ
            if resize:
                img_width, img_height = img.size
                scale = min(page_width / img_width, page_height / img_height)
                new_width = int(img_width * scale)
                new_height = int(img_height * scale)
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # PDFの作成
            try:
                c = canvas.Canvas(output_path, pagesize=(page_width, page_height))
            except Exception as e:
                raise PDFError(f"PDFの作成に失敗しました: {e}")

            # メタデータの設定
            if self.metadata:
                c.setTitle(self.metadata.title)
                c.setAuthor(self.metadata.author)
                c.setSubject(self.metadata.subject)
                c.setKeywords(self.metadata.keywords)
                if self.metadata.creator:
                    c.setCreator(self.metadata.creator)

            # 画像の配置位置の計算
            img_width, img_height = img.size
            if position == ImagePosition.CENTER:
                x = (page_width - img_width) / 2
                y = (page_height - img_height) / 2
            elif position == ImagePosition.TOP_LEFT:
                x = 0
                y = page_height - img_height
            elif position == ImagePosition.TOP_RIGHT:
                x = page_width - img_width
                y = page_height - img_height
            elif position == ImagePosition.BOTTOM_LEFT:
                x = 0
                y = 0
            elif position == ImagePosition.BOTTOM_RIGHT:
                x = page_width - img_width
                y = 0

            # 画像の配置
            try:
                c.drawImage(image_path, x, y, width=img_width, height=img_height)
            except Exception as e:
                raise PDFError(f"画像の配置に失敗しました: {e}")

            # PDFの保存
            try:
                c.save()
            except Exception as e:
                raise PDFError(f"PDFの保存に失敗しました: {e}")

        except (ImageError, PDFError, ValidationError):
            raise
        except Exception as e:
            raise PDFError(f"予期せぬエラーが発生しました: {e}")

    def convert_multiple_images(
        self,
        image_paths: List[str],
        output_path: str,
        page_size: Union[PageSize, Tuple[int, int]] = PageSize.A4,
        rotate: int = 0,
        resize: bool = True,
        position: ImagePosition = ImagePosition.CENTER,
        quality: Optional[int] = None
    ) -> None:
        """
        複数の画像を1つのPDFに変換する
        
        Args:
            image_paths: 入力画像のパスのリスト
            output_path: 出力PDFのパス
            page_size: PDFのページサイズ
            rotate: 回転角度（0, 90, 180, 270）
            resize: 画像をページサイズに合わせてリサイズするかどうか
            position: 画像の配置位置
            quality: 画像の品質（0-100）
        """
        if not isinstance(page_size, PageSize):
            raise ValidationError(f"無効なページサイズです: {page_size}")
        if rotate not in [0, 90, 180, 270]:
            raise ValidationError(f"無効な回転角度です: {rotate}")
        if not isinstance(position, ImagePosition):
            raise ValidationError(f"無効な配置位置です: {position}")
        if not 0 <= quality <= 100:
            raise ValidationError(f"無効な品質値です: {quality}")
        
        if isinstance(page_size, PageSize):
            page_size = page_size.value
            
        # PDFの作成
        c = canvas.Canvas(output_path, pagesize=page_size)
        
        # メタデータの設定
        c.setTitle(self.metadata.title)
        c.setAuthor(self.metadata.author)
        c.setSubject(self.metadata.subject)
        c.setKeywords(self.metadata.keywords)
        c.setCreator(self.metadata.creator)
        
        for image_path in image_paths:
            self._validate_image(image_path)
            
            # 画像を開く
            image = Image.open(image_path)
            
            # 回転
            if rotate in [90, 180, 270]:
                image = image.rotate(rotate, expand=True)
            
            # 画像サイズの計算
            if resize:
                width, height = self._get_image_size(image, page_size)
            else:
                width, height = image.size
            
            # 画像の配置位置を計算
            x, y = self._calculate_position((width, height), page_size, position)
            
            # 画像の品質設定
            if quality is not None:
                self.quality = quality
            
            # 画像をPDFに追加
            c.drawImage(
                ImageReader(image),
                x, y,
                width=width,
                height=height,
                preserveAspectRatio=True,
                mask='auto'
            )
            c.showPage()
        
        c.save() 