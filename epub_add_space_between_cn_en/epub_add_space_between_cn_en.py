import zipfile
import os
import re
import tempfile
from bs4 import BeautifulSoup, NavigableString, Comment

# 该脚本处理 EPUB 文件：在中文和英文/数字之间添加空格以改善阅读体验；
# 英文与数字之间不加空格（如 AK47、iPhone12 保持原样）；
# 百分号（半角 % / 全角 ％）与汉字之间也加空格。


def process_text(text):
    if not text:
        return text
    # 1. 中文 + 字母/数字：中文AK47 → 中文 AK47
    text = re.sub(r'([\u4e00-\u9fff])([a-zA-Z0-9]+)', r'\1 \2', text)
    # 2. 字母/数字 + 中文：AK47中文 → AK47 中文
    text = re.sub(r'([a-zA-Z0-9]+)([\u4e00-\u9fff])', r'\1 \2', text)
    # 3. 百分号（半角 % 或全角 ％）+ 中文：50%中文 → 50% 中文
    text = re.sub(r'([%％])([\u4e00-\u9fff])', r'\1 \2', text)
    return text


def process_html(content):
    """处理 HTML 内容，同时优化正文和 <title> 标签"""
    soup = BeautifulSoup(content, 'html.parser')

    # ==================== 处理 <title> 标签 ====================
    if soup.title:
        title_text = soup.title.get_text()
        if title_text:
            soup.title.clear()
            soup.title.append(process_text(title_text))

    # ==================== 处理正文部分 ====================
    body = soup.find('body')
    target = body if body else soup

    for element in target.find_all(string=True):
        if isinstance(element, NavigableString) and element.strip() \
                and not isinstance(element, Comment):
            new_text = process_text(str(element))
            element.replace_with(new_text)

    return str(soup)


def process_toc_ncx(content):
    """处理 toc.ncx 目录文件中的文本，添加空格"""
    try:
        soup = BeautifulSoup(content, 'xml')
    except Exception:
        soup = BeautifulSoup(content, 'html.parser')

    for text_tag in soup.find_all('text'):
        if text_tag.string:
            new_text = process_text(str(text_tag.string))
            text_tag.string.replace_with(new_text)

    return str(soup)


def process_epub(input_file, output_file):
    """处理 EPUB 文件"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # 解压 EPUB 文件
        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)

        # 处理所有 HTML/XHTML 与 toc.ncx 文件
        for root, _, files in os.walk(tmp_dir):
            for file in files:
                file_path = os.path.join(root, file)

                if file.lower().endswith(('.html', '.xhtml')):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    modified_content = process_html(content)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)

                elif file.lower() == 'toc.ncx':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    modified_content = process_toc_ncx(content)
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)

        # 重新打包 EPUB：mimetype 必须在最前且不压缩
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_out:
            mimetype_path = os.path.join(tmp_dir, 'mimetype')
            if os.path.exists(mimetype_path):
                zip_out.write(mimetype_path, 'mimetype',
                              compress_type=zipfile.ZIP_STORED)

            for root, _, files in os.walk(tmp_dir):
                for file in files:
                    if file == 'mimetype':
                        continue
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, tmp_dir)
                    zip_out.write(file_path, arcname)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        description='在 EPUB 文件中添加空格（包括 <title> 标签、百分号与汉字之间）'
    )
    parser.add_argument('input', help='输入 EPUB 文件路径')
    parser.add_argument('output', help='输出 EPUB 文件路径')

    args = parser.parse_args()

    process_epub(args.input, args.output)
    print(f"处理完成！输出文件：{args.output}")