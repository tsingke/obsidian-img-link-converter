#!/usr/bin/env python3
import os
import re
import sys
import shutil

#-------------手动设置图片路径-------------------------
# 📁 图片集中目录（根据你的设置）
ATTACH_DIR = "附件/图片"
#---------------------------------------------------

# 支持的图片扩展名
IMG_EXTS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp', 'tiff']
IMG_EXTS_PATTERN = '|'.join(IMG_EXTS)

# 匹配 ![[图片名.xxx]] 的 Obsidian 图片 wiki 链接
wiki_img_pattern = re.compile(r'!\[\[([^\[\]]+?\.(?:' + IMG_EXTS_PATTERN + r'))\]\]')

# 记录图片重命名映射
rename_map = {}

def rename_images(vault_root):
    """重命名含空格图片文件为中划线版本"""
    attach_dir_abs = os.path.join(vault_root, ATTACH_DIR)
    print(f"📁 扫描图片目录：{attach_dir_abs}")
    if not os.path.isdir(attach_dir_abs):
        print(f"❌ 错误：图片目录不存在：{attach_dir_abs}")
        return

    for filename in os.listdir(attach_dir_abs):
        if ' ' in filename and any(filename.lower().endswith(ext) for ext in IMG_EXTS):
            new_filename = filename.replace(' ', '-')
            src = os.path.join(attach_dir_abs, filename)
            dst = os.path.join(attach_dir_abs, new_filename)

            # 避免重名
            count = 1
            while os.path.exists(dst):
                name, ext = os.path.splitext(new_filename)
                dst = os.path.join(attach_dir_abs, f"{name}-{count}{ext}")
                count += 1

            os.rename(src, dst)
            rename_map[filename] = os.path.basename(dst)
            print(f"📝 重命名: {filename} → {os.path.basename(dst)}")
        else:
            rename_map[filename] = filename

def process_file(file_path, vault_root, dry_run=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    if not wiki_img_pattern.search(content):
        print(f"ℹ️ 无图片 Wiki 链接，跳过: {file_path}")
        return

    print(f"✅ 处理文件: {file_path}")

    def replacer(match):
        original_image_name = match.group(1)
        new_image_name = rename_map.get(original_image_name, original_image_name)
        final_path = os.path.join(ATTACH_DIR, new_image_name).replace("\\", "/")
        print(f"🔹 转换: {match.group(0)} → ![]({final_path})")
        return f"![]({final_path})"

    new_content = wiki_img_pattern.sub(replacer, content)

    if dry_run:
        print(f"👀 预览模式，未写入文件: {file_path}")
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"💾 写入完成: {file_path}")

def process_directory(root_dir, dry_run=True):
    rename_images(root_dir)

    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.md'):
                file_path = os.path.join(dirpath, filename)
                process_file(file_path, root_dir, dry_run=dry_run)

if __name__ == "__main__":
    vault_root = os.getcwd()
    print(f"🔎 开始处理 Vault 目录: {vault_root}")
    print("---------------------------------------------")
    process_directory(vault_root, dry_run=False)
    print("✅ 所有处理完成！")
