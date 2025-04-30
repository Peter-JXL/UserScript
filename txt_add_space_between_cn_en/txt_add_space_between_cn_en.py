import re
import argparse
import chardet

def detect_encoding(file_path):
    """检测文件编码"""
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']

def add_spaces_between_chars(text):
    """
    在中文、英文、数字之间添加空格
    规则：
    - 中文与英文/数字之间添加空格
    - 英文/数字与中文之间添加空格
    - 英文与数字之间添加空格
    - 数字与英文之间添加空格

    基础用法: python txt_processor.py input.txt

    自定义输出路径: python txt_processor.py input.txt -o output.txt
    """
    # 中文与字母/数字边界
    text = re.sub(r'([\u4e00-\u9fff])([a-zA-Z0-9])', r'\1 \2', text)
    text = re.sub(r'([a-zA-Z0-9])([\u4e00-\u9fff])', r'\1 \2', text)
    
    # 字母与数字边界
    text = re.sub(r'([a-zA-Z])(\d)', r'\1 \2', text)
    text = re.sub(r'(\d)([a-zA-Z])', r'\1 \2', text)
    
    return text

def process_txt(input_file, output_file, encoding):
    try:
        with open(input_file, 'r', encoding=encoding) as f:
            content = f.read()
        
        processed_content = add_spaces_between_chars(content)
        
        with open(output_file, 'w', encoding=encoding) as f:
            f.write(processed_content)
            
        print(f"处理完成！输出文件：{output_file}")
        
    except FileNotFoundError:
        print("错误：输入文件不存在")
    except Exception as e:
        print(f"处理失败：{str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="在中文、英文、数字之间添加空格")
    parser.add_argument("input", help="输入 TXT 文件路径")
    parser.add_argument("-o", "--output", help="输出文件路径（默认同输入文件名，后缀加 _processed）")
    parser.add_argument("--encoding", help="指定文件编码（如 gbk、utf-8 等）")
    
    args = parser.parse_args()
    
    input_path = args.input
    output_path = args.output
    
    # 自动生成输出路径
    if not output_path:
        base_name = os.path.splitext(input_path)[0]
        output_path = f"{base_name}_processed.txt"
    
    # 自动检测编码（如果未手动指定）
    encoding = args.encoding
    if not encoding:
        encoding = detect_encoding(input_path)
        print(f"自动检测到编码：{encoding}")
    
    process_txt(input_path, output_path, encoding)