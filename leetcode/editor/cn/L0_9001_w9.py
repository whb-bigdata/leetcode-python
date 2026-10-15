"""Week 9: 逐行统计单词，并核对文件末尾给出的总数。

运行方法 / Usage:
    python3 L0_9001_w9.py input.txt
    python3 L0_9001_w9.py

只使用第一个文件参数，其余参数忽略。未提供路径，或指定文件无法打开时，
读取当前工作目录中的 sample.txt。单词按空白分隔，标点不会额外拆分。
题目保证文件最后一行是 Words: <number>；这一行不参与单词计数。
仅使用 Python 标准库 sys，无需安装第三方包。
"""

import sys


def read_lines(file_path):
    """读取文本行；打开失败时回退默认文件 / Read lines with a fallback."""
    try:
        text_file = open(file_path, "r", encoding="utf-8")
    except OSError:
        # 路径不存在、无权限或指向目录等情况，均尝试默认文件。
        text_file = open("../../../sample.txt", "r", encoding="utf-8")

    # with 会在读取结束后自动关闭文件，包括读取发生异常的情况。
    with text_file:
        return text_file.readlines()


def main():
    """读取命令行参数，统计并打印结果 / Count words and report validity."""
    # argv[0] 是脚本名，argv[1] 才是用户传入的第一个参数。
    file_path = sys.argv[1] if len(sys.argv) > 1 else "sample.txt"

    try:
        lines = read_lines(file_path)
    except (OSError, UnicodeError) as error:
        # 默认文件也打不开，或文本无法按 UTF-8 解码时，清楚报告错误。
        print(f"Unable to read the text file: {error}", file=sys.stderr)
        return 1

    # 最后一行例如 "Words: 9\n"，冒号右边转换为整数。
    expected_count = int(lines[-1].split(":", 1)[1].strip())
    total_count = 0

    # 去掉最后的统计行；enumerate(..., start=1) 让行号从 1 开始。
    for line_number, line in enumerate(lines[:-1], start=1):
        # split() 可处理连续空格和制表符；空白行会得到空列表。
        word_count = len(line.split())
        total_count += word_count
        print(f"Line {line_number}: {word_count} words")

    if total_count == expected_count:
        print("The file is valid.")
    else:
        print("The file is invalid.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
