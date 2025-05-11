import logging
import sys
from pathlib import Path

def setup_logger(name: str = "mkpdf", level: int = logging.INFO) -> logging.Logger:
    """
    ロガーの設定を行う
    
    Args:
        name: ロガー名
        level: ログレベル
    
    Returns:
        logging.Logger: 設定済みのロガー
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # コンソール出力用のハンドラ
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # ログフォーマットの設定
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(formatter)
    
    # ハンドラの追加
    logger.addHandler(console_handler)
    
    return logger

# デフォルトのロガー
logger = setup_logger() 