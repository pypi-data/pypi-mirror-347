import json
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict

@dataclass
class Config:
    """MKPDFの設定"""
    default_page_size: str = "A4"
    default_quality: int = 95
    default_position: str = "center"
    default_resize: bool = True
    default_rotate: int = 0
    default_metadata: Dict[str, str] = None
    
    def __post_init__(self):
        if self.default_metadata is None:
            self.default_metadata = {
                "title": "",
                "author": "",
                "subject": "",
                "keywords": "",
                "creator": "MKPDF"
            }
    
    @classmethod
    def from_file(cls, path: str) -> 'Config':
        """
        設定ファイルから設定を読み込む
        
        Args:
            path: 設定ファイルのパス
        
        Returns:
            Config: 設定オブジェクト
        """
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls(**data)
    
    def save(self, path: str) -> None:
        """
        設定をファイルに保存する
        
        Args:
            path: 保存先のパス
        """
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(asdict(self), f, indent=4, ensure_ascii=False)

def get_default_config_path() -> Path:
    """
    デフォルトの設定ファイルパスを取得する
    
    Returns:
        Path: 設定ファイルのパス
    """
    config_dir = Path.home() / '.mkpdf'
    config_dir.mkdir(exist_ok=True)
    return config_dir / 'config.json'

def load_config(config_path: Optional[str] = None) -> Config:
    """
    設定を読み込む
    
    Args:
        config_path: 設定ファイルのパス（Noneの場合はデフォルトパスを使用）
    
    Returns:
        Config: 設定オブジェクト
    """
    if config_path is None:
        config_path = get_default_config_path()
    
    if Path(config_path).exists():
        return Config.from_file(config_path)
    else:
        config = Config()
        config.save(config_path)
        return config 