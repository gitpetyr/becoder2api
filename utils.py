from ddddocr import DdddOcr
from ocr_stats import OCRStats

ocr1 = DdddOcr(show_ad=False, old=True)
ocr2 = DdddOcr(show_ad=False)
ocr3 = DdddOcr(show_ad=False, beta=True)

# 创建OCR统计管理器
ocr_stats = OCRStats()

def getcaptcha(img_bytes: bytes, success: bool | None = None) -> str:
    """
    智能验证码识别函数
    
    Args:
        img_bytes: 验证码图片的字节数据
        success: 上次识别是否成功的反馈（用于更新统计）
        
    Returns:
        str: 识别出的验证码文本
    """
    # 如果有上次识别的反馈，更新统计
    if hasattr(getcaptcha, 'last_ocr') and success is not None:
        ocr_stats.update_stats(getcaptcha.last_ocr, success)
    
    # 选择OCR
    chosen_ocr = ocr_stats.choose_ocr()
    getcaptcha.last_ocr = chosen_ocr
    
    # 使用选中的OCR进行识别
    if chosen_ocr == 'ocr1':
        return ocr1.classification(img_bytes)
    elif chosen_ocr == 'ocr2':
        return ocr2.classification(img_bytes)
    else:  # ocr3
        return ocr3.classification(img_bytes)