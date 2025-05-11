from pathlib import Path
from PIL import Image

def create_test_image(path: Path, size: tuple = (100, 100), color: str = 'red') -> None:
    """
    テスト用の画像ファイルを作成する
    
    Args:
        path: 画像ファイルのパス
        size: 画像サイズ (width, height)
        color: 画像の色
    """
    img = Image.new('RGB', size, color=color)
    img.save(path)

def create_test_images(directory: Path, count: int = 3) -> list[Path]:
    """
    複数のテスト用画像ファイルを作成する
    
    Args:
        directory: 画像ファイルを保存するディレクトリ
        count: 作成する画像ファイルの数
    
    Returns:
        list[Path]: 作成した画像ファイルのパスのリスト
    """
    directory.mkdir(exist_ok=True)
    image_paths = []
    
    for i in range(count):
        path = directory / f'test_{i}.jpg'
        create_test_image(path)
        image_paths.append(path)
    
    return image_paths