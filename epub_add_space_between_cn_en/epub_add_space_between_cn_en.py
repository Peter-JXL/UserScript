import zipfile
import os
import re
import tempfile
import shutil
from bs4 import BeautifulSoup, NavigableString

# 该脚本处理 EPUB 文件：在中文和英文、数字之间添加个空格，以改善阅读体验。

def process_text(text):

    # 处理中文与字母/数字之间的边界
    text = re.sub(r'([\u4e00-\u9fff])([a-zA-Z0-9]+)', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z0-9]+)([\u4e00-\u9fff])', r'\1 \2', text)
    
    # 处理字母与数字之间的边界
    text = re.sub(r'([a-zA-Z]+)(\d+)', r'\1 \2', text)
    text = re.sub(r'(\d+)([a-zA-Z]+)', r'\1 \2', text)
    
    return text

def process_html(content):
    """处理 HTML 内容"""
    soup = BeautifulSoup(content, 'html.parser')
    
    for element in soup.find_all(string=True):
        if isinstance(element, NavigableString) and element.strip():
            new_text = process_text(element)
            element.replace_with(new_text)
    
    return str(soup)

def process_epub(input_file, output_file):
    """处理 EPUB 文件"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        # 解压EPUB文件
        with zipfile.ZipFile(input_file, 'r') as zip_ref:
            zip_ref.extractall(tmp_dir)
        
        # 处理所有HTML/XHTML文件
        for root, _, files in os.walk(tmp_dir):
            for file in files:
                if file.lower().endswith(('.html', '.xhtml')):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    modified_content = process_html(content)
                    
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(modified_content)
        
        # 重新打包EPUB
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zip_out:
            for root, _, files in os.walk(tmp_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, tmp_dir)
                    zip_out.write(file_path, arcname)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='在 EPUB 文件中添加空格')
    parser.add_argument('input', help='输入 EPUB 文件路径')
    parser.add_argument('output', help='输出 EPUB 文件路径')
    
    args = parser.parse_args()
    
    process_epub(args.input, args.output)
    print(f"处理完成！输出文件：{args.output}")