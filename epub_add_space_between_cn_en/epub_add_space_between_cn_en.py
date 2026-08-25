import zipfile
import os
import re
import tempfile
import shutil
from bs4 import BeautifulSoup, NavigableString, Comment

# 该脚本处理 EPUB 文件：在中文和英文/数字之间添加空格以改善阅读体验；英文与数字之间不加空格（如 AK47、iPhone12 保持原样）。

def process_text(text):
    """处理中文与字母、数字之间的空格（英文与数字之间不加空格，如 AK47 保持不拆）"""
    # 处理中文与字母/数字之间的边界
    text = re.sub(r'([\u4e00-\u9fff])([a-zA-Z0-9]+)', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z0-9]+)([\u4e00-\u9fff])', r'\1 \2', text)
    return text


def process_html(content):
    """处理 HTML 内容，同时优化正文和 <title> 标签"""
    soup = BeautifulSoup(content, 'html.parser')

    # ==================== 处理 <title> 标签（新增需求） ====================
    # 小说正文中 <title> 内的内容也需要加空格
    if soup.title:
        if soup.title.string:
            new_title = process_text(soup.title.string)
            soup.title.string.replace_with(new_title)

    # ==================== 处理正文部分 ====================
    body = soup.find('body')

    if body:
        for element in body.find_all(string=True):
            if isinstance(element, NavigableString) and element.strip() and not isinstance(element, Comment):
                new_text = process_text(element)
                element.replace_with(new_text)
    else:
        # 如果没有 <body> 标签，直接处理整个文档
        for element in soup.find_all(string=True):
            if isinstance(element, NavigableString) and element.strip() and not isinstance(element, Comment):
                new_text = process_text(element)
                element.replace_with(new_text)

    return str(soup)


def process_toc_ncx(content):
    """处理 toc.ncx 目录文件中的文本，添加空格"""
    soup = BeautifulSoup(content, 'xml')
    
    for text_tag in soup.find_all('text'):
        if text_tag.string:
            new_text = process_text(text_tag.string)
            text_tag.string.replace_with(new_text)
    
    return str(soup)


def process_epub(input_file, output_file):
    """处理 EPUB 文件"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # 解压 EPUB 文件
        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)
        
        # 处理所有 HTML/XHTML 文件
        for root, _, files in os.walk(tmp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                
                # 处理 HTML 和 XHTML 文件
                if file.lower().endswith(('.html', '.xhtml')):
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    modified_content = process_html(content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
                
                # 处理 toc.ncx 文件
                elif file.lower() == 'toc.ncx':
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    modified_content = process_toc_ncx(content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
        
        # 重新打包 EPUB
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_out:
            for root, _, files in os.walk(tmp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, tmp_dir)
                    zip_out.write(file_path, arcname)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='在 EPUB 文件中添加空格（包括 <title> 标签）')
    parser.add_argument('input', help='输入 EPUB 文件路径')
    parser.add_argument('output', help='输出 EPUB 文件路径')
    
    args = parser.parse_args()
    
    process_epub(args.input, args.output)
    print(f"处理完成！输出文件：{args.output}")
