#!/usr/bin/env python3
"""
检查并补充 mkdocs.yml 配置
确保项目符合 mkdocs-shadcn 主题规范
"""
import sys
import yaml
from pathlib import Path
from typing import Any


# shadcn 主题必需的插件
REQUIRED_PLUGINS = [
    'search',
]

# shadcn 主题推荐的 Markdown 扩展
RECOMMENDED_EXTENSIONS = [
    'admonition',
    'codehilite',
    'fenced_code',
    'footnotes',
    'pymdownx.blocks.details',
    'pymdownx.blocks.tab',
    'pymdownx.progressbar',
    'pymdownx.tabbed',
    'attr_list',
]

# shadcn 主题必需的 theme 配置
REQUIRED_THEME_CONFIG = [
    'name',
]


def load_yaml(file_path: Path) -> dict | None:
    """加载 YAML 文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    except Exception as e:
        print(f"[ERROR] 无法加载 {file_path}: {e}")
        return None


def check_theme(config: dict) -> tuple[bool, list[str]]:
    """检查主题配置"""
    issues = []
    theme = config.get('theme', {})

    # 检查主题名称
    if theme.get('name') != 'shadcn':
        issues.append("主题应设置为 'shadcn'")

    # 检查必要的 theme 配置
    if 'show_title' not in theme:
        issues.append("建议设置 theme.show_title")

    return len(issues) == 0, issues


def check_plugins(config: dict) -> tuple[bool, list[str]]:
    """检查插件配置"""
    issues = []
    plugins = config.get('plugins', [])

    # 转换为列表（可能是列表或包含配置的字典）
    if isinstance(plugins, dict):
        plugin_names = list(plugins.keys())
    elif isinstance(plugins, list):
        plugin_names = []
        for p in plugins:
            if isinstance(p, str):
                plugin_names.append(p)
            elif isinstance(p, dict):
                plugin_names.extend(p.keys())
    else:
        plugin_names = []

    # 检查必需插件
    for req_plugin in REQUIRED_PLUGINS:
        if req_plugin not in plugin_names:
            issues.append(f"缺少必需插件: {req_plugin}")

    return len(issues) == 0, issues


def check_markdown_extensions(config: dict) -> tuple[bool, list[str]]:
    """检查 Markdown 扩展配置"""
    issues = []
    extensions = config.get('markdown_extensions', [])

    # 转换为列表
    if isinstance(extensions, list):
        ext_names = []
        for e in extensions:
            if isinstance(e, str):
                ext_names.append(e)
            elif isinstance(e, dict):
                ext_names.extend(e.keys())
    else:
        ext_names = []

    # 检查推荐的扩展
    missing = []
    for req_ext in RECOMMENDED_EXTENSIONS:
        if req_ext not in ext_names:
            missing.append(req_ext)

    if missing:
        issues.append(f"缺少推荐的 Markdown 扩展: {', '.join(missing)}")

    return len(issues) == 0, issues


def check_navigation(config: dict) -> tuple[bool, list[str]]:
    """检查导航配置"""
    issues = []

    if 'nav' not in config:
        issues.append("缺少导航配置 'nav'")

    return len(issues) == 0, issues


def check_site_metadata(config: dict) -> tuple[bool, list[str]]:
    """检查站点元数据配置"""
    issues = []

    if 'site_name' not in config:
        issues.append("缺少站点名称 'site_name'")

    return len(issues) == 0, issues


def generate_supplement(config: dict) -> dict:
    """生成补充配置"""
    supplement = {}

    # 补充主题配置
    if 'theme' not in config:
        supplement['theme'] = {'name': 'shadcn'}
    elif config.get('theme', {}).get('name') != 'shadcn':
        supplement['theme'] = {'name': 'shadcn'}

    theme = supplement.get('theme', {})
    original_theme = config.get('theme', {})

    # 添加推荐的 theme 配置
    if 'show_title' not in original_theme:
        theme['show_title'] = True
    if 'show_stargazers' not in original_theme:
        theme['show_stargazers'] = True
    if 'topbar_sections' not in original_theme:
        theme['topbar_sections'] = False
    if 'show_datetime' not in original_theme:
        theme['show_datetime'] = False

    if theme:
        supplement['theme'] = theme

    # 补充插件
    if 'plugins' not in config:
        supplement['plugins'] = ['search']
    else:
        plugins = config.get('plugins', [])
        if isinstance(plugins, dict):
            plugin_names = list(plugins.keys())
        elif isinstance(plugins, list):
            plugin_names = []
            for p in plugins:
                if isinstance(p, str):
                    plugin_names.append(p)
                elif isinstance(p, dict):
                    plugin_names.extend(p.keys())
        else:
            plugin_names = []

        # 添加缺失的必需插件
        new_plugins = []
        for req in REQUIRED_PLUGINS:
            if req not in plugin_names:
                new_plugins.append(req)

        if new_plugins:
            if isinstance(plugins, list):
                supplement['plugins'] = plugins + new_plugins
            else:
                supplement['plugins'] = new_plugins

    # 补充 Markdown 扩展
    if 'markdown_extensions' not in config:
        supplement['markdown_extensions'] = RECOMMENDED_EXTENSIONS
    else:
        extensions = config.get('markdown_extensions', [])
        if isinstance(extensions, list):
            ext_names = []
            for e in extensions:
                if isinstance(e, str):
                    ext_names.append(e)
                elif isinstance(e, dict):
                    ext_names.extend(e.keys())
        else:
            ext_names = []

        missing_exts = [e for e in RECOMMENDED_EXTENSIONS if e not in ext_names]
        if missing_exts:
            if isinstance(extensions, list):
                supplement['markdown_extensions'] = extensions + missing_exts
            else:
                supplement['markdown_extensions'] = missing_exts

    return supplement


def apply_supplement(config: dict, supplement: dict) -> dict:
    """将补充配置应用到原配置"""
    result = config.copy()

    # 合并主题配置
    if 'theme' in supplement:
        if 'theme' not in result:
            result['theme'] = supplement['theme']
        else:
            result['theme'] = {**result['theme'], **supplement['theme']}

    # 合并插件
    if 'plugins' in supplement:
        original_plugins = result.get('plugins', [])
        new_plugins = supplement['plugins']

        # 合并列表
        if isinstance(original_plugins, list) and isinstance(new_plugins, list):
            # 去重合并
            seen = set()
            merged = []
            for p in original_plugins + new_plugins:
                p_name = p if isinstance(p, str) else list(p.keys())[0]
                if p_name not in seen:
                    seen.add(p_name)
                    merged.append(p)
            result['plugins'] = merged

    # 合并 Markdown 扩展
    if 'markdown_extensions' in supplement:
        original_exts = result.get('markdown_extensions', [])
        new_exts = supplement['markdown_extensions']

        if isinstance(original_exts, list) and isinstance(new_exts, list):
            seen = set()
            merged = []
            for e in original_exts + new_exts:
                e_name = e if isinstance(e, str) else list(e.keys())[0]
                if e_name not in seen:
                    seen.add(e_name)
                    merged.append(e)
            result['markdown_extensions'] = merged

    return result


def check_project(project_path: Path) -> dict:
    """检查项目配置"""
    mkdocs_path = project_path / 'mkdocs.yml'

    if not mkdocs_path.exists():
        return {
            'found': False,
            'path': str(mkdocs_path),
            'issues': ['未找到 mkdocs.yml 文件'],
            'supplement': None
        }

    config = load_yaml(mkdocs_path)
    if config is None:
        return {
            'found': False,
            'path': str(mkdocs_path),
            'issues': ['无法解析 mkdocs.yml 文件'],
            'supplement': None
        }

    all_issues = []

    # 执行各项检查
    checks = [
        ('theme', check_theme),
        ('plugins', check_plugins),
        ('markdown_extensions', check_markdown_extensions),
        ('navigation', check_navigation),
        ('site_metadata', check_site_metadata),
    ]

    for name, check_func in checks:
        passed, issues = check_func(config)
        for issue in issues:
            all_issues.append(f"[{name}] {issue}")

    # 生成补充配置
    supplement = generate_supplement(config)

    return {
        'found': True,
        'path': str(mkdocs_path),
        'issues': all_issues,
        'supplement': supplement,
        'config': config
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python check_config.py <project_directory>")
        print("  检查并补充 mkdocs.yml 配置")
        sys.exit(1)

    project_path = Path(sys.argv[1])

    if not project_path.exists():
        print(f"[ERROR] 路径不存在: {project_path}")
        sys.exit(1)

    if not project_path.is_dir():
        print(f"[ERROR] 路径不是目录: {project_path}")
        sys.exit(1)

    print(f"检查项目: {project_path}")
    print("=" * 50)

    result = check_project(project_path)

    if not result['found']:
        print(f"[ERROR] {result['issues'][0]}")
        sys.exit(1)

    print(f"\n[配置检查] {result['path']}")

    if result['issues']:
        print("\n[发现问题]")
        for issue in result['issues']:
            print(f"  - {issue}")
    else:
        print("\n[✓] 配置检查通过")

    if result['supplement']:
        print("\n[建议补充的配置]")
        print(yaml.dump(result['supplement'], allow_unicode=True, default_flow_style=False))

    # 检查是否需要自动应用
    if len(sys.argv) > 2 and sys.argv[2] == '--apply':
        mkdocs_path = project_path / 'mkdocs.yml'
        new_config = apply_supplement(result['config'], result['supplement'])

        with open(mkdocs_path, 'w', encoding='utf-8') as f:
            yaml.dump(new_config, f, allow_unicode=True, default_flow_style=False)

        print(f"\n[✓] 已自动应用补充配置到 {mkdocs_path}")

    print("\n" + "=" * 50)
    print("检查完成")


if __name__ == "__main__":
    main()