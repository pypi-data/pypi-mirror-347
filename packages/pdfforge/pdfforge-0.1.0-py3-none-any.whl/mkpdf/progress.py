from typing import Optional, Callable
import sys
from tqdm import tqdm

class ProgressBar:
    """プログレスバーの管理クラス"""
    
    def __init__(self, total: int, desc: str = "処理中"):
        """
        プログレスバーの初期化
        
        Args:
            total: 全体の処理数
            desc: プログレスバーの説明
        """
        self.pbar = tqdm(
            total=total,
            desc=desc,
            unit="ファイル",
            ncols=80,
            file=sys.stdout
        )
    
    def update(self, n: int = 1) -> None:
        """
        プログレスバーを更新
        
        Args:
            n: 進捗量
        """
        self.pbar.update(n)
    
    def close(self) -> None:
        """プログレスバーを閉じる"""
        self.pbar.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

def create_progress_bar(total: int, desc: str = "処理中") -> ProgressBar:
    """
    プログレスバーを作成する
    
    Args:
        total: 全体の処理数
        desc: プログレスバーの説明
    
    Returns:
        ProgressBar: プログレスバーオブジェクト
    """
    return ProgressBar(total, desc) 