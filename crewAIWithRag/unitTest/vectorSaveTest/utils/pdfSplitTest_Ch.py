# 功能说明：将PDF文件进行文本预处理,适用中文
# 准备工作：安装相关包
# pip install pdfminer.six

# 导入相关库
import logging
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
import re


# 设置日志模版
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 当处理中文文本时，按照标点进行断句
def sent_tokenize(input_string):
    sentences = re.split(r'(?<=[。！？；?!])', input_string)
    # 去掉空字符串
    return [sentence for sentence in sentences if sentence.strip()]


# PDF文档处理函数,从PDF文件中按指定页码提取文字
def extract_text_from_pdf(filename, page_numbers, min_line_length):
    # 申明变量
    paragraphs = []
    buffer = ''
    full_text = ''
    # 提取全部文本并按照一行一行进行截取，并在每一行后面加上换行符
    for i, page_layout in enumerate(extract_pages(filename)):
        # 如果指定了页码范围，跳过范围外的页
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                full_text += element.get_text() + '\n'
    # full_text：将文件按照一行一行进行截取，并在每一行后面加上换行符
    # logger.info(f"full_text: {full_text}")


    # 按空行分隔，将文本重新组织成段落
    # lines：将full_text按照换行符进行切割，此时空行则为空（‘’）
    lines = full_text.split('\n')
    # logger.info(f"lines: {lines}")

    # 将lines进行循环，取出每一个片段（text）进行处理合并成段落，处理逻辑为：
    # （1）首先判断text的最小行的长度是否大于min_line_length设置的值
    # （2）如果大于min_line_length，则将该text拼接在buffer后面，如果该text不是以连字符“-”结尾，则在行前加上一个空格；如果该text是以连字符“-”结尾，则去掉连字符）
    # （3）如果小于min_line_length且buffer中有内容，则将其添加到 paragraphs 列表中
    # （4）最后，处理剩余的缓冲区内容，在遍历结束后，如果 buffer 中仍有内容，则将其添加到 paragraphs 列表中
    for text in lines:
        if len(text) >= min_line_length:
            buffer += (' '+text) if not text.endswith('-') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)
    # logger.info(f"paragraphs: {paragraphs[:10]}")

    # 其返回值为划分段落的文本列表
    return paragraphs


# 将PDF文档处理函数得到的文本列表再按一定粒度，部分重叠式的切割文本，使上下文更完整
# chunk_size：每个文本块的目标大小（以字符为单位），默认为 800
# overlap_size：块之间的重叠大小（以字符为单位），默认为 200
def split_text(paragraphs, chunk_size=800, overlap_size=200):
    # 按指定 chunk_size 和 overlap_size 交叠割文本
    sentences = [s.strip() for p in paragraphs for s in sent_tokenize(p)]
    chunks = []
    i = 0
    while i < len(sentences):
        chunk = sentences[i]
        overlap = ''
        prev_len = 0
        prev = i - 1
        # 向前计算重叠部分
        while prev >= 0 and len(sentences[prev])+len(overlap) <= overlap_size:
            overlap = sentences[prev] + ' ' + overlap
            prev -= 1
        chunk = overlap+chunk
        next = i + 1
        # 向后计算当前chunk
        while next < len(sentences) and len(sentences[next])+len(chunk) <= chunk_size:
            chunk = chunk + ' ' + sentences[next]
            next += 1
        chunks.append(chunk)
        i = next
    # logger.info(f"chunks: {chunks[0:10]}")
    return chunks


def getParagraphs(filename, page_numbers, min_line_length):
    paragraphs = extract_text_from_pdf(filename, page_numbers, min_line_length)
    chunks = split_text(paragraphs, 800, 200)
    return chunks


if __name__ == "__main__":
    # 测试 PDF文档按一定条件处理成文本数据
    paragraphs = getParagraphs(
        "../input/健康档案.pdf",
        # page_numbers=[2, 3], # 指定页面
        page_numbers=None, # 加载全部页面
        min_line_length=1
    )
    # 测试前3条文本
    logger.info(f"只展示3段截取片段:")
    logger.info(f"截取的片段1: {paragraphs[0]}")
    logger.info(f"截取的片段2: {paragraphs[2]}")
    logger.info(f"截取的片段3: {paragraphs[3]}")



