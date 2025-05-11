class MKPDFError(Exception):
    """MKPDFの基本例外クラス"""
    pass

class ImageError(MKPDFError):
    """画像関連のエラー"""
    pass

class PDFError(MKPDFError):
    """PDF生成関連のエラー"""
    pass

class ValidationError(MKPDFError):
    """入力値の検証エラー"""
    pass 