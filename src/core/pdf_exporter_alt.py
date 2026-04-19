"""
替代 PDF 导出模块 - 使用 reportlab (不需要 weasyprint 和 libpango)
当 weasyprint 不可用时使用此模块
使用 Platypus 框架实现更好的格式化
"""

from pathlib import Path
from io import BytesIO
import logging
import re
from html.parser import HTMLParser

logger = logging.getLogger(__name__)

# Matches runs of CJK (Chinese/Japanese/Korean) and related Unicode characters
_CJK_RE = re.compile(
    r'[\u2E80-\u2EFF\u2F00-\u2FDF\u3000-\u303F\u3040-\u309F\u30A0-\u30FF'
    r'\u3100-\u312F\u3200-\u33FF\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF'
    r'\uFE10-\uFE4F\uFF00-\uFFEF]+'
)


class HTMLToReportlabParser(HTMLParser):
    """將 HTML 解析為 reportlab 可用的元素"""

    def __init__(self, mono_font='Courier', cjk_font=None):
        super().__init__()
        self.elements = []
        self.current_text = []
        self.in_code = False
        self.in_pre = False
        self.in_h1 = False
        self.in_h2 = False
        self.in_h3 = False
        self.in_strong = False
        self.in_em = False
        self.list_items = []
        self.in_list = False
        self.mono_font = mono_font
        self.cjk_font = cjk_font

    @staticmethod
    def _escape_xml(text):
        """轉義 XML 特殊字符"""
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        return text

    def _apply_fonts(self, text):
        """轉義 XML 並將 CJK 字符包裝在 CJK 字體標籤中，其餘保持預設字體"""
        text = self._escape_xml(text)
        if not self.cjk_font:
            return text
        result = []
        last = 0
        for m in _CJK_RE.finditer(text):
            if m.start() > last:
                result.append(text[last:m.start()])
            result.append(f'<font name="{self.cjk_font}">{m.group()}</font>')
            last = m.end()
        if last < len(text):
            result.append(text[last:])
        return ''.join(result)

    def handle_starttag(self, tag, attrs):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self._flush_text()
            setattr(self, f'in_{tag}', True)
        elif tag == 'p':
            self._flush_text()
        elif tag == 'strong' or tag == 'b':
            self.in_strong = True
        elif tag == 'em' or tag == 'i':
            self.in_em = True
        elif tag == 'code':
            self.in_code = True
        elif tag == 'pre':
            self.in_pre = True
            self._flush_text()
        elif tag in ['ul', 'ol']:
            self._flush_text()
            self.in_list = True
            self.list_items = []
        elif tag == 'li':
            if self.current_text:
                self.list_items.append(''.join(self.current_text).strip())
                self.current_text = []
        elif tag == 'br':
            self.current_text.append('\n')

    def handle_endtag(self, tag):
        if tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            self._flush_text(tag)
            setattr(self, f'in_{tag}', False)
        elif tag == 'p':
            self._flush_text()
        elif tag == 'strong' or tag == 'b':
            self.in_strong = False
        elif tag == 'em' or tag == 'i':
            self.in_em = False
        elif tag == 'code':
            self.in_code = False
        elif tag == 'pre':
            self._flush_text('pre')
            self.in_pre = False
        elif tag in ['ul', 'ol']:
            if self.current_text:
                self.list_items.append(''.join(self.current_text).strip())
                self.current_text = []
            if self.list_items:
                self.elements.append(('list', self.list_items[:]))
            self.list_items = []
            self.in_list = False
        elif tag == 'li':
            if self.current_text:
                self.list_items.append(''.join(self.current_text).strip())
                self.current_text = []

    def handle_data(self, data):
        # 跳過空白
        if not data.strip() and not self.in_pre:
            if self.current_text:
                self.current_text.append(' ')
            return

        # 處理特殊格式
        if self.in_strong:
            data = f'<b>{self._apply_fonts(data)}</b>'
        elif self.in_em:
            data = f'<i>{self._apply_fonts(data)}</i>'
        elif self.in_code:
            data = f'<font name="{self.mono_font}" color="darkred">{self._escape_xml(data)}</font>'
        elif not self.in_pre:
            data = self._apply_fonts(data)

        self.current_text.append(data)

    def _flush_text(self, tag=None):
        """將累積的文本轉換為元素"""
        if not self.current_text:
            return

        text = ''.join(self.current_text).strip()
        if not text:
            self.current_text = []
            return

        if tag and tag.startswith('h'):
            self.elements.append((tag, text))
        elif tag == 'pre':
            self.elements.append(('pre', text))
        elif not self.in_list:
            self.elements.append(('p', text))

        self.current_text = []

    def get_elements(self):
        """獲取所有解析的元素"""
        self._flush_text()
        return self.elements


class PDFExporterAlt:
    """使用 reportlab 的 PDF 导出器 - 无需系统库"""

    DEFAULT_SETTINGS = {
        "page_size": "A4",
        "margin_top": "20mm",
        "margin_right": "20mm",
        "margin_bottom": "20mm",
        "margin_left": "20mm",
        "font_size": 12,  # 基礎字體大小,與MDViewer一致
    }

    def __init__(self, settings: dict = None):
        """初始化 PDF 导出器"""
        self.settings = {**self.DEFAULT_SETTINGS, **(settings or {})}
        self._check_reportlab()

    def _check_reportlab(self):
        """检查 reportlab 是否可用"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate
            self.reportlab_available = True
        except ImportError:
            logger.warning("reportlab 未安装，无法使用 PDF 导出")
            self.reportlab_available = False

    def export_to_file(self, html_content: str, output_path: str) -> tuple[bool, str]:
        """导出 HTML 为 PDF 文件

        Returns:
            tuple[bool, str]: (成功與否, 錯誤訊息)
        """
        if not self.reportlab_available:
            error_msg = "reportlab 未安裝"
            logger.error(error_msg)
            return False, error_msg

        try:
            from reportlab.lib.pagesizes import A4, LETTER, A3, LEGAL
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import mm
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
            from reportlab.lib.enums import TA_LEFT, TA_CENTER
            from reportlab.pdfbase import pdfmetrics
            from reportlab.pdfbase.ttfonts import TTFont
            import os

            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # 页面大小映射
            page_sizes = {
                "A4": A4,
                "Letter": LETTER,
                "A3": A3,
                "Legal": LEGAL,
            }

            page_size = page_sizes.get(self.settings.get("page_size", "A4"), A4)

            # 解析边距
            margin_top = self._parse_size(self.settings.get("margin_top", "20mm"))
            margin_bottom = self._parse_size(self.settings.get("margin_bottom", "20mm"))
            margin_left = self._parse_size(self.settings.get("margin_left", "20mm"))
            margin_right = self._parse_size(self.settings.get("margin_right", "20mm"))

            # 创建 PDF 文档
            doc = SimpleDocTemplate(
                str(output_path),
                pagesize=page_size,
                topMargin=margin_top,
                bottomMargin=margin_bottom,
                leftMargin=margin_left,
                rightMargin=margin_right
            )

            # 搜尋可用的 CJK（中文）字體
            CJK_FONT_CANDIDATES = [
                '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
                '/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc',
                '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc',
                '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
                '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            ]
            cjk_font_name = None
            for candidate in CJK_FONT_CANDIDATES:
                if os.path.exists(candidate):
                    try:
                        kwargs = {'subfontIndex': 0} if candidate.endswith('.ttc') else {}
                        pdfmetrics.registerFont(TTFont('CJKFont', candidate, **kwargs))
                        cjk_font_name = 'CJKFont'
                        logger.info(f"已註冊 CJK 字體: {candidate}")
                        break
                    except Exception as e:
                        logger.warning(f"無法註冊 {candidate}: {e}")

            if cjk_font_name is None:
                logger.warning("未找到 CJK 字體，中文可能無法顯示")

            # 主體字體使用 DejaVu Sans（Latin），CJK 字符透過 inline font tag 切換
            body_font = 'Helvetica'
            try:
                dejavu_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
                if os.path.exists(dejavu_path):
                    pdfmetrics.registerFont(TTFont('DejaVuSans', dejavu_path))
                    body_font = 'DejaVuSans'
            except Exception as e:
                logger.warning(f"無法註冊 DejaVu Sans: {e}")

            # 等寬字體（代碼塊）
            mono_font_name = 'Courier'
            try:
                dejavu_path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
                if os.path.exists(dejavu_path):
                    pdfmetrics.registerFont(TTFont('DejaVuSansMono', dejavu_path))
                    mono_font_name = 'DejaVuSansMono'
            except Exception as e:
                logger.warning(f"無法註冊 DejaVu Sans Mono: {e}")

            # 獲取樣式
            styles = getSampleStyleSheet()

            # 獲取基礎字體大小
            base_font_size = self.settings.get("font_size", 12)

            # 自定義樣式 - 與MDViewer的CSS樣式一致（無邊框線）
            # h1: 2em (移除 border-bottom)
            styles.add(ParagraphStyle(
                name='CustomH1',
                parent=styles['Heading1'],
                fontName=body_font,
                fontSize=base_font_size * 2,
                spaceAfter=16,
                spaceBefore=24,
                textColor='#000000'
            ))

            # h2: 1.5em
            styles.add(ParagraphStyle(
                name='CustomH2',
                parent=styles['Heading2'],
                fontName=body_font,
                fontSize=base_font_size * 1.5,
                spaceAfter=16,
                spaceBefore=24,
                textColor='#000000'
            ))

            # h3: 1.25em
            styles.add(ParagraphStyle(
                name='CustomH3',
                parent=styles['Heading3'],
                fontName=body_font,
                fontSize=base_font_size * 1.25,
                spaceAfter=16,
                spaceBefore=24,
                textColor='#000000'
            ))

            # h4: 1em
            styles.add(ParagraphStyle(
                name='CustomH4',
                parent=styles['Heading4'],
                fontName=body_font,
                fontSize=base_font_size,
                spaceAfter=16,
                spaceBefore=24,
                textColor='#000000'
            ))

            # 代碼塊樣式 - 使用支持 Unicode 的等寬字體
            # 使用更明顯的背景色 (#e8e8e8) 以便在 PDF 中清楚顯示
            styles.add(ParagraphStyle(
                name='CodeBlock',
                parent=styles['Code'],
                fontSize=base_font_size * 0.85,  # 85% of base
                fontName=mono_font_name,  # 使用註冊的等寬字體
                leftIndent=16,
                rightIndent=16,
                spaceBefore=16,
                spaceAfter=16,
                backColor='#e8e8e8',  # 更明顯的灰色背景（原為 #f6f8fa）
                wordWrap='CJK'  # 支持中文字符換行
            ))

            # 正常段落樣式 - 增加行距以匹配MDViewer
            styles['Normal'].fontName = body_font
            styles['Normal'].fontSize = base_font_size
            styles['Normal'].leading = base_font_size * 1.6  # line-height: 1.6
            styles['Normal'].spaceAfter = 6
            styles['Normal'].wordWrap = 'CJK'

            # 解析 HTML 並構建文檔
            story = []
            parser = HTMLToReportlabParser(mono_font=mono_font_name, cjk_font=cjk_font_name)

            # 清理 HTML
            clean_html = self._clean_html(html_content)
            parser.feed(clean_html)

            elements = parser.get_elements()

            for elem_type, content in elements:
                if elem_type == 'h1':
                    story.append(Paragraph(content, styles['CustomH1']))
                elif elem_type == 'h2':
                    story.append(Paragraph(content, styles['CustomH2']))
                elif elem_type == 'h3':
                    story.append(Paragraph(content, styles['CustomH3']))
                elif elem_type == 'h4':
                    story.append(Paragraph(content, styles['CustomH4']))
                elif elem_type in ['h5', 'h6']:
                    story.append(Paragraph(content, styles['Heading4']))
                elif elem_type == 'pre':
                    # 代碼塊 - 與MDViewer樣式一致
                    story.append(Preformatted(content, styles['CodeBlock']))
                elif elem_type == 'list':
                    # 列表項
                    for item in content:
                        if item:
                            story.append(Paragraph(f"• {item}", styles['Normal']))
                elif elem_type == 'p':
                    # 普通段落
                    if content:
                        story.append(Paragraph(content, styles['Normal']))

            # 構建 PDF
            doc.build(story)
            logger.info(f"PDF 导出成功: {output_path}")
            return True, ""

        except Exception as e:
            error_msg = f"PDF 導出失敗: {str(e)}"
            logger.error(error_msg, exc_info=True)
            return False, error_msg

    def _clean_html(self, html_content: str) -> str:
        """清理 HTML，移除不需要的標籤"""
        # 移除 <head> 和其內容
        html_content = re.sub(r'<head>.*?</head>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

        # 移除 <style> 標籤
        html_content = re.sub(r'<style[^>]*>.*?</style>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

        # 移除 <script> 標籤
        html_content = re.sub(r'<script[^>]*>.*?</script>', '', html_content, flags=re.DOTALL | re.IGNORECASE)

        # 只保留 <body> 內容
        body_match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL | re.IGNORECASE)
        if body_match:
            html_content = body_match.group(1)

        return html_content

    def export_to_bytes(self, html_content: str) -> bytes:
        """导出为 PDF 字节"""
        try:
            from reportlab.lib.pagesizes import A4
            from reportlab.platypus import SimpleDocTemplate
            from io import BytesIO

            buffer = BytesIO()
            # 使用相同的導出邏輯
            # ... (實現類似 export_to_file)

            return buffer.getvalue()

        except Exception as e:
            logger.error(f"PDF 生成失败: {str(e)}")
            return b""

    @staticmethod
    def _parse_size(size_str: str) -> float:
        """解析大小字符串 (例如 '20mm')"""
        from reportlab.lib.units import mm, cm, inch

        if size_str.endswith('mm'):
            return float(size_str[:-2]) * mm
        elif size_str.endswith('cm'):
            return float(size_str[:-2]) * cm
        elif size_str.endswith('in'):
            return float(size_str[:-2]) * inch
        else:
            return float(size_str)

    def update_settings(self, **kwargs):
        """更新设置"""
        self.settings.update(kwargs)
