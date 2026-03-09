#!/usr/bin/env python3
"""
格式化 Markdown 内容，遵循 mkdocs-shadcn 规范
"""
import re
import sys
from pathlib import Path


def is_list_item(line: str) -> bool:
    """检查是否是列表项"""
    trimmed = line.strip()
    # 匹配: - item, * item, + item, 1. item, - [ ] item, - [x] item
    return bool(re.match(r'^[-*+]\s', trimmed)) or bool(re.match(r'^\d+\.\s', trimmed))


def find_last_non_empty_index(lines: list, start_index: int) -> int:
    """从 start_index 向前查找最后一个非空行的索引，如果没有返回 -1"""
    for i in range(start_index, -1, -1):
        if lines[i].strip() != '':
            return i
    return -1


def fix_list_spacing(content: str) -> str:
    """
    修复 Markdown 列表间距
    规则：
    1. 一组列表的第一个列表项前：有且只有一个空行
    2. 同一组列表的列表项之间：没有空行
    3. 不同组列表之间：有且只有一个空行
    4. 列表项与后续非列表内容之间：有且只有一个空行
    """
    lines = content.split('\n')
    result = []

    for i, line in enumerate(lines):
        current_is_list = is_list_item(line)

        if current_is_list and result:
            # 检查前一行
            prev_line = result[-1]
            prev_is_list = is_list_item(prev_line)

            if prev_is_list:
                # 前一行也是列表项：同一组，直接添加，不做处理
                pass
            elif prev_line.strip() == '':
                # 前一行是空行，需要判断是否是同一组列表
                # 向前查找最后一个非空行
                last_non_empty_idx = find_last_non_empty_index(result, len(result) - 2)

                if last_non_empty_idx >= 0 and is_list_item(result[last_non_empty_idx]):
                    # 空行之前是列表项：属于同一组列表，删除所有连续空行
                    while result and result[-1].strip() == '':
                        result.pop()
                else:
                    # 空行之前不是列表项：这是新一组列表的开始
                    # 确保只有一个空行（只处理当前列表项前的连续空行）
                    # 从后向前查找连续的空行
                    consecutive_empty = 0
                    for j in range(len(result) - 1, -1, -1):
                        if result[j].strip() == '':
                            consecutive_empty += 1
                        else:
                            break
                    # 删除多余的连续空行，只保留一个
                    while consecutive_empty > 1:
                        result.pop()
                        consecutive_empty -= 1
                    # 正好一个空行，不做处理
            else:
                # 前一行有实际内容但不是列表项：新的一组列表开始，需要添加空行
                result.append('')

        result.append(line)

    return '\n'.join(result)


def format_markdown(content: str) -> str:
    """
    格式化 Markdown 内容，遵循 mkdocs-shadcn 规范

    功能包括：
    1. 分离 YAML frontmatter
    2. 清理所有现有的独立分隔符
    3. 按规范添加标题分割线
    4. 统一图片格式为居中 HTML 格式
    5. 修复列表间距
    """
    # 1. 分离 YAML frontmatter
    frontmatter = ""
    main_content = content
    yaml_match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---\r?\n', content)
    if yaml_match:
        frontmatter = yaml_match.group(0)
        main_content = content[yaml_match.end():]

    # 2. [核心要求] 彻底清空所有现有的、独立成行的分隔符
    lines = re.split(r'\r?\n', main_content)
    clean_lines = []
    for line in lines:
        trimmed = line.strip()
        # 匹配 ---, ***, ___ 等，且不能是表格的一部分
        if not re.match(r'^(?:[-*_]\s*){3,}$', trimmed):
            clean_lines.append(line)

    # 3. 构建结果
    result_lines = []
    in_h2_section = False
    h3_count_in_section = 0

    for i, line in enumerate(clean_lines):
        trimmed = line.strip()

        if trimmed.startswith('## '):
            # H2 规则：上方加空行，下方紧跟分隔符
            if result_lines and result_lines[-1] != '':
                result_lines.append('')
            result_lines.append(line)
            result_lines.append('---')
            in_h2_section = True
            h3_count_in_section = 0
        elif trimmed.startswith('### '):
            # H3 规则：
            h3_count_in_section += 1
            if in_h2_section and h3_count_in_section == 1:
                # H2 后的第一个 H3，不加分隔符，仅确保上方有空行
                while result_lines and result_lines[-1] == '':
                    result_lines.pop()
                result_lines.append('')
                result_lines.append(line)
            else:
                # 后续 H3，上方加分隔符
                while result_lines and result_lines[-1] == '':
                    result_lines.pop()
                if result_lines:
                    result_lines.append('')
                    result_lines.append('---')
                    result_lines.append('')
                result_lines.append(line)
        elif trimmed.startswith('# '):
            # H1 重置状态
            in_h2_section = False
            result_lines.append(line)
        else:
            # 其他内容
            result_lines.append(line)

    # 4. 图片居中与清理 (最后处理，避免正则冲突)
    processed = frontmatter + '\n'.join(result_lines)

    # 清理可能已经存在的居中包装（避免重复）
    # 匹配 Markdown 图片语法的居中包装
    processed = re.sub(
        r'<p align="center">\s*(!\[.*?\]\(.*?\))\s*</p>',
        r'\1',
        processed,
        flags=re.IGNORECASE
    )
    # 匹配 HTML img 的居中包装
    processed = re.sub(
        r'<p align="center">\s*(<img[\s\S]*?>)\s*</p>',
        r'\1',
        processed,
        flags=re.IGNORECASE
    )

    def normalize_asset_path(src: str) -> str:
        """
        规范化资源路径：
        - 跳过网络链接 (http:// 或 https://)
        - 本地路径中包含 assets/ 且不以 /assets 开头的，转换为 /assets 绝对路径
        """
        # 跳过网络链接
        if src.startswith(('http://', 'https://')):
            return src
        # 本地路径中包含 assets/ 且不是以 /assets 开头的绝对路径
        if 'assets/' in src and not src.startswith('/assets/'):
            idx = src.find('assets/')
            return '/' + src[idx:]
        return src

    # 统一添加居中包装
    # 将 Markdown 图片语法转换为纯 HTML 格式
    def replace_markdown_image(match):
        alt = match.group(1) or ''
        src = match.group(2)
        # 处理 src 路径
        src = normalize_asset_path(src)
        return f'<p align="center">\n  <img src="{src}" alt="{alt}">\n</p>'

    processed = re.sub(
        r'!\[([^\]]*)\]\(([^)]+)\)',
        replace_markdown_image,
        processed,
        flags=re.IGNORECASE
    )

    # 处理 img 标签
    def process_img_tags(text):
        """处理所有 img 标签，确保都被正确包装"""
        pattern = r'<img([\s\S]*?)>'
        matches = list(re.finditer(pattern, text, re.IGNORECASE))

        # 从后往前替换，避免位置偏移
        for match in reversed(matches):
            start, end = match.span()
            # 检查是否已经在 <p align="center"> 中
            before = text[:start]
            # 查找前面是否有 <p align="center"> 且后面没有对应的 </p>
            last_p_start = before.rfind('<p align="center">')
            last_p_end = before.rfind('</p>')

            attrs = match.group(1)

            # 提取并处理 src 路径
            src_match = re.search(r'src="([^"]+)"', attrs, re.IGNORECASE)
            if src_match:
                src = src_match.group(1)
                new_src = normalize_asset_path(src)
                if new_src != src:
                    attrs = attrs.replace(f'src="{src}"', f'src="{new_src}"')

            if last_p_start > last_p_end:
                # 已经在居中段落中，只更新路径
                text = text[:start] + f'<img{attrs}>' + text[end:]
            else:
                # 不在居中段落中，需要包装并清理 alt/title
                attrs = re.sub(r'\s+alt=".*?"', ' alt=""', attrs, flags=re.IGNORECASE)
                attrs = re.sub(r'\s+title=".*?"', '', attrs, flags=re.IGNORECASE)
                replacement = f'<p align="center">\n  <img{attrs}>\n</p>'
                text = text[:start] + replacement + text[end:]

        return text

    processed = process_img_tags(processed)

    # 5. 修复列表间距
    processed = fix_list_spacing(processed)

    # 6. 收尾清理
    processed = re.sub(r'\n{3,}', '\n\n', processed)
    processed = re.sub(r'(## .*\n)---\n\n', r'\1---\n', processed)

    return processed


def process_file(file_path: Path) -> bool:
    """处理单个文件，返回是否成功"""
    try:
        content = file_path.read_text(encoding='utf-8')
        formatted = format_markdown(content)
        file_path.write_text(formatted, encoding='utf-8')
        print(f"[OK] {file_path}")
        return True
    except Exception as e:
        print(f"[ERROR] {file_path}: {e}")
        return False


def walk_directory(dir_path: Path) -> tuple[int, int]:
    """
    递归遍历目录处理所有 .md 文件
    返回: (处理的文件数, 成功处理的文件数)
    """
    total_files = 0
    success_files = 0

    for item in dir_path.iterdir():
        if item.is_dir():
            if item.name == 'assets':
                continue
            sub_total, sub_success = walk_directory(item)
            total_files += sub_total
            success_files += sub_success
        elif item.suffix == '.md':
            total_files += 1
            if process_file(item):
                success_files += 1

    return total_files, success_files


def main():
    if len(sys.argv) < 2:
        print("Usage: python format.py <file_path_or_directory>")
        print("  - 如果是文件路径：格式化单个 Markdown 文件")
        print("  - 如果是目录路径：递归格式化该目录下所有 Markdown 文件")
        sys.exit(1)

    target_path = Path(sys.argv[1])

    if not target_path.exists():
        print(f"Path not found: {target_path}")
        sys.exit(1)

    if target_path.is_file():
        # 处理单个文件
        if target_path.suffix != '.md':
            print(f"Error: Not a Markdown file: {target_path}")
            sys.exit(1)

        print(f"Formatting: {target_path}")
        if process_file(target_path):
            print(f"Successfully formatted: {target_path}")
        else:
            print(f"Failed to format: {target_path}")
            sys.exit(1)

    elif target_path.is_dir():
        # 递归处理目录
        print(f"Scanning directory: {target_path}\n")

        total, success = walk_directory(target_path)

        print("\n" + "=" * 40)
        print("Completed!")
        print(f"Files scanned: {total}")
        print(f"Files formatted successfully: {success}")

        if success < total:
            sys.exit(1)


if __name__ == "__main__":
    main()
