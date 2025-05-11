import click
import glob
from pathlib import Path
from typing import List
from .core import ImageToPDF, PageSize, ImagePosition, PDFMetadata
from .config import Config, load_config, get_default_config_path

@click.group()
def cli():
    """画像をPDFに変換するコマンドラインツール"""
    pass

@cli.group()
def config():
    """設定ファイルの管理"""
    pass

@config.command()
@click.option('--page-size', type=click.Choice(['A4', 'LETTER', 'A4_LANDSCAPE', 'LETTER_LANDSCAPE']))
@click.option('--quality', type=click.IntRange(0, 100))
@click.option('--position', type=click.Choice(['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right']))
@click.option('--resize/--no-resize')
@click.option('--rotate', type=click.IntRange(0, 270, 90))
@click.option('--title', help='デフォルトのPDFタイトル')
@click.option('--author', help='デフォルトの作成者')
@click.option('--subject', help='デフォルトのサブジェクト')
@click.option('--keywords', help='デフォルトのキーワード（カンマ区切り）')
def set(page_size, quality, position, resize, rotate, title, author, subject, keywords):
    """設定を更新する"""
    config = load_config()
    
    if page_size:
        config.default_page_size = page_size
    if quality is not None:
        config.default_quality = quality
    if position:
        config.default_position = position
    if resize is not None:
        config.default_resize = resize
    if rotate is not None:
        config.default_rotate = rotate
    
    if any([title, author, subject, keywords]):
        if title:
            config.default_metadata['title'] = title
        if author:
            config.default_metadata['author'] = author
        if subject:
            config.default_metadata['subject'] = subject
        if keywords:
            config.default_metadata['keywords'] = keywords
    
    config.save(get_default_config_path())
    click.echo("設定を更新しました")

@config.command()
def show():
    """現在の設定を表示する"""
    config = load_config()
    click.echo("現在の設定:")
    click.echo(f"ページサイズ: {config.default_page_size}")
    click.echo(f"品質: {config.default_quality}")
    click.echo(f"配置位置: {config.default_position}")
    click.echo(f"リサイズ: {config.default_resize}")
    click.echo(f"回転角度: {config.default_rotate}")
    click.echo("\nメタデータ:")
    for key, value in config.default_metadata.items():
        click.echo(f"  {key}: {value}")

@config.command()
def reset():
    """設定をデフォルト値に戻す"""
    config = Config()
    config.save(get_default_config_path())
    click.echo("設定をデフォルト値に戻しました")

@cli.command()
@click.argument('image_path', type=click.Path(exists=True))
@click.argument('output_path', type=click.Path())
@click.option('--page-size', type=click.Choice(['A4', 'LETTER', 'A4_LANDSCAPE', 'LETTER_LANDSCAPE']), default='A4')
@click.option('--rotate', type=click.IntRange(0, 270, 90), default=0)
@click.option('--resize/--no-resize', default=True)
@click.option('--position', type=click.Choice(['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right']), default='center')
@click.option('--quality', type=click.IntRange(0, 100), default=95)
@click.option('--title', help='PDFのタイトル')
@click.option('--author', help='PDFの作成者')
@click.option('--subject', help='PDFのサブジェクト')
@click.option('--keywords', help='PDFのキーワード（カンマ区切り）')
def single(image_path: str, output_path: str, page_size: str, rotate: int, resize: bool,
           position: str, quality: int, title: str, author: str, subject: str, keywords: str):
    """単一の画像をPDFに変換する"""
    converter = ImageToPDF()
    
    # メタデータの設定
    metadata = PDFMetadata(
        title=title or "",
        author=author or "",
        subject=subject or "",
        keywords=keywords or ""
    )
    converter.metadata = metadata
    
    # 変換の実行
    converter.convert_single_image(
        image_path=image_path,
        output_path=output_path,
        page_size=getattr(PageSize, page_size),
        rotate=rotate,
        resize=resize,
        position=getattr(ImagePosition, position.upper()),
        quality=quality
    )
    
    click.echo(f"PDFファイルを作成しました: {output_path}")

@cli.command()
@click.argument('input_pattern', type=str)
@click.argument('output_path', type=click.Path())
@click.option('--page-size', type=click.Choice(['A4', 'LETTER', 'A4_LANDSCAPE', 'LETTER_LANDSCAPE']), default='A4')
@click.option('--rotate', type=click.IntRange(0, 270, 90), default=0)
@click.option('--resize/--no-resize', default=True)
@click.option('--position', type=click.Choice(['center', 'top_left', 'top_right', 'bottom_left', 'bottom_right']), default='center')
@click.option('--quality', type=click.IntRange(0, 100), default=95)
@click.option('--title', help='PDFのタイトル')
@click.option('--author', help='PDFの作成者')
@click.option('--subject', help='PDFのサブジェクト')
@click.option('--keywords', help='PDFのキーワード（カンマ区切り）')
def multiple(input_pattern: str, output_path: str, page_size: str, rotate: int, resize: bool,
            position: str, quality: int, title: str, author: str, subject: str, keywords: str):
    """複数の画像を1つのPDFに変換する"""
    converter = ImageToPDF()
    
    # メタデータの設定
    metadata = PDFMetadata(
        title=title or "",
        author=author or "",
        subject=subject or "",
        keywords=keywords or ""
    )
    converter.metadata = metadata
    
    # 画像ファイルの検索
    image_paths = sorted(glob.glob(input_pattern))
    if not image_paths:
        click.echo(f"エラー: パターン '{input_pattern}' に一致する画像ファイルが見つかりません")
        return
    
    # 変換の実行
    converter.convert_multiple_images(
        image_paths=image_paths,
        output_path=output_path,
        page_size=getattr(PageSize, page_size),
        rotate=rotate,
        resize=resize,
        position=getattr(ImagePosition, position.upper()),
        quality=quality
    )
    
    click.echo(f"PDFファイルを作成しました: {output_path}")
    click.echo(f"変換した画像ファイル数: {len(image_paths)}")

def main():
    cli() 