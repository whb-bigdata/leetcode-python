import glob
import logging
import os
import sys
from pypdf import PdfReader, PdfWriter

# 屏蔽 pypdf 的底层警告日志
logging.getLogger("pypdf").setLevel(logging.ERROR)


# ==========================================
# 模块 1：获取与处理文件名
# ==========================================
def get_target_filepaths(work_dir="."):
    """获取当前目录下两个待合并的 PDF 文件名及自动生成的输出文件名。

    规则：
    1. file1 为名字较短的 PDF，file2 为名字较长的 PDF。
    2. 输出文件名固定为 file1 的名称 + '_T.pdf'。

    Returns:
        tuple: (file1, file2, output_file) 或在文件不足时返回 None
    """
    # 查找所有 pdf 文件（排除已经是合并结果的 *_T.pdf）
    search_pattern = os.path.join(work_dir, "*.pdf")
    pdf_files = [
        f for f in glob.glob(search_pattern)
    ]

    if len(pdf_files) < 2:
        print(
            f"❌ 错误：在 '{work_dir}' 目录下至少需要 2 个 PDF 文件！当前仅找到 {len(pdf_files)} 个。"
        )
        return None

    if len(pdf_files) > 2:
        print(f"⚠️ 提示：找到 {len(pdf_files)} 个 PDF 文件，默认使用前 2 个。")
        pdf_files = pdf_files[:2]

    # 按文件名长度升序排序（短的在前，长的在后）
    pdf_files.sort(key=lambda f: len(os.path.basename(f)))

    file1 = pdf_files[0]
    file2 = pdf_files[1]

    # 生成输出文件名：file1 名字 + _T.pdf
    file1_base, _ = os.path.splitext(file1)
    output_file = f"{file1_base}_T.pdf"

    return file1, file2, output_file


# ==========================================
# 模块 2：PDF 交叉合并
# ==========================================
def merge_pdfs_interleaved(file1, file2, output_file):
    """将两个 PDF 文件按页交替合并，并保存为新的文件。

    Args:
        file1 (str): 较短文件名的 PDF 路径
        file2 (str): 较长文件名的 PDF 路径
        output_file (str): 输出文件路径

    Returns:
        bool: 执行成功返回 True，失败返回 False
    """
    try:
        reader1 = PdfReader(file1)
        reader2 = PdfReader(file2)
        writer = PdfWriter()

        len1 = len(reader1.pages)
        len2 = len(reader2.pages)
        max_len = max(len1, len2)

        # 交叉插入页面
        for i in range(max_len):
            if i < len1:
                writer.add_page(reader1.pages[i])
            if i < len2:
                writer.add_page(reader2.pages[i])

        # 写入新文件
        with open(output_file, "wb") as f_out:
            writer.write(f_out)

        # 显式关闭 reader 解除对源文件的读取占用（防止 Windows 下删除失败）
        reader1.close()
        reader2.close()

        print(f"✅ 合并成功！新文件已输出至: {output_file}")
        return True

    except Exception as e:
        print(f"❌ PDF 合并过程中发生错误: {e}")
        return False


# ==========================================
# 模块 3：清理源文件
# ==========================================
def cleanup_files(*file_paths):
    """安全删除指定的源文件。

    Args:
        *file_paths: 需要删除的文件路径列表
    """
    for file_path in file_paths:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"🗑️ 已成功删除源文件: {file_path}")
        except Exception as e:
            print(f"⚠️ 删除文件 '{file_path}' 失败: {e}")


# ==========================================
# 主控制流程
# ==========================================
def main():
    # 1. 调用模块 1：获取文件名
    paths = get_target_filepaths()
    if not paths:
        return

    file1, file2, output_file = paths
    print(f"🔍 识别到 File 1 (较短): {file1}")
    print(f"🔍 识别到 File 2 (较长): {file2}")
    print(f"📄 目标输出文件: {output_file}")

    # 2. 调用模块 2：进行合并
    success = merge_pdfs_interleaved(file1, file2, output_file)

    # 3. 调用模块 3：合并成功后清理源文件
    if success:
        cleanup_files(file1, file2)


if __name__ == "__main__":
    main()