# -*- coding: utf-8 -*-
from fpdf import FPDF


def pdfSaveTool(text: str, filename: str = "task_output.pdf") -> str:
    """
    使用这个工具来保存任务输出为PDF文件，支持中文。
    :param text: 要保存的文本内容
    :param filename: 保存的PDF文件名
    :return: 保存状态消息
    """
    # 初始化PDF
    pdf = FPDF()
    pdf.add_page()
    # 添加和设置字体，使用支持中文的字体文件（如 simhei.ttf）
    pdf.add_font('SimHei', '', 'simhei.ttf', uni=True)
    pdf.set_font('SimHei', '', 16)
    # 添加标题
    pdf.cell(200, 10, '任务输出', ln=True, align='C')

    # 写入文本内容（支持中文）
    pdf.set_font('SimHei', '', 12)
    pdf.multi_cell(0, 10, text)

    # 保存PDF文件
    pdf.output(filename)

    return f"Task output saved as {filename}"


# 调用工具函数保存中文PDF
pdfSaveTool("你好，欢迎使用PDF保存工具", "task_output.pdf")
