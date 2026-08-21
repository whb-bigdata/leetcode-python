import os
import shutil
from pathlib import Path


def organize_files():
    # 获取当前 Python 脚本所在的目录，并指向子文件夹 xhsdownloads
    current_dir = Path(__file__).resolve().parent
    target_dir = current_dir / "xhsdownloads"

    # 检查 xhsdownloads 文件夹是否存在
    if not target_dir.exists():
        print(f"错误: 找不到文件夹 '{target_dir}'")
        return

    # 支持常见的图片格式扩展名
    valid_extensions = {".jpg", ".jpeg", ".png", ".webp", ".heic"}

    # 计数器
    moved_count = 0

    # 遍历 xhsdownloads 目录下的所有内容
    for file_path in target_dir.iterdir():
        # 仅处理文件且匹配图片后缀，跳过已创建的子文件夹
        if file_path.is_file() and file_path.suffix.lower() in valid_extensions:
            file_name = file_path.name

            # 按下划线 '_' 拆分文件名
            parts = file_name.split("_")

            # 确保文件名包含下划线分隔的标题部分
            if len(parts) >= 2:
                # 获取标题前缀（例如："澳洲授课硕转Mphil研究硕攻略（一）"）
                folder_name = parts[0].strip()

                # 新文件夹路径：./xhsdownloads/主题文件夹名/
                destination_folder = target_dir / folder_name

                # 如果文件夹不存在，自动在 xhsdownloads 内部创建
                destination_folder.mkdir(parents=True, exist_ok=True)

                # 移动文件到目标文件夹
                target_file_path = destination_folder / file_name
                shutil.move(str(file_path), str(target_file_path))

                print(f"移动成功: {file_name} ➔ {folder_name}/")
                moved_count += 1

    print(f"\n整理完成！共处理了 {moved_count} 张图片。")


if __name__ == "__main__":
    organize_files()