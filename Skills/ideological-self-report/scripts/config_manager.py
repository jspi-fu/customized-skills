"""
配置管理脚本 - 统一管理写作风格配置和模板路径
"""
import os
import sys
import json
import argparse
import hashlib
from datetime import datetime
from pathlib import Path

# 设置路径
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")
REQUIREMENTS_FILE = os.path.join(BASE_DIR, "references", "requirements.md")


def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return get_default_config()


def save_config(config):
    """保存配置文件"""
    config['last_updated'] = datetime.now().isoformat()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)
    return {"success": True, "message": "配置已保存"}


def get_default_config():
    """获取默认配置"""
    return {
        "template_path": "",
        "file_index": [],
        "writing_style": {
            "word_count": {
                "total": "1700-1900字",
                "ideological": "600-700字",
                "study": "250-350字",
                "work": "250-350字",
                "life": "100-150字",
                "self_criticism": "150-200字"
            },
            "historical_weaknesses": [],
            "opening_patterns": [],
            "user_info": {
                "name": "",
                "identity": "",
                "positions": []
            }
        },
        "last_updated": ""
    }


def scan_template_path(template_path):
    """扫描模板路径下的所有文件"""
    if not template_path or not os.path.exists(template_path):
        return []

    files = []
    for root, _, filenames in os.walk(template_path):
        for filename in filenames:
            if filename.endswith('.txt') or filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, template_path)
                # 计算文件哈希用于变更检测
                with open(filepath, 'rb') as f:
                    file_hash = hashlib.md5(f.read()).hexdigest()
                files.append({
                    "path": rel_path,
                    "hash": file_hash,
                    "analyzed": False
                })
    return files


def check_new_files(config):
    """检查是否有新增或变更的文件"""
    template_path = config.get('template_path', '')
    if not template_path:
        return {"has_new": False, "message": "未配置模板路径"}

    # 转换为绝对路径
    if not os.path.isabs(template_path):
        template_path = os.path.join(BASE_DIR, template_path)

    if not os.path.exists(template_path):
        return {"has_new": False, "message": f"模板路径不存在: {template_path}"}

    current_files = scan_template_path(template_path)
    existing_index = {f['path']: f for f in config.get('file_index', [])}

    new_files = []
    changed_files = []

    for file_info in current_files:
        path = file_info['path']
        if path not in existing_index:
            new_files.append(file_info)
        elif existing_index[path]['hash'] != file_info['hash']:
            changed_files.append(file_info)

    return {
        "has_new": len(new_files) > 0 or len(changed_files) > 0,
        "new_files": [f['path'] for f in new_files],
        "changed_files": [f['path'] for f in changed_files],
        "all_files": current_files
    }


def update_file_index(config, files):
    """更新文件索引，标记已分析"""
    existing = {f['path']: f for f in config.get('file_index', [])}

    for file_info in files:
        file_info['analyzed'] = True
        existing[file_info['path']] = file_info

    config['file_index'] = list(existing.values())
    return config


def get_unanalyzed_files(config):
    """获取尚未分析的文件列表"""
    template_path = config.get('template_path', '')
    if not template_path:
        return []

    # 转换为绝对路径
    if not os.path.isabs(template_path):
        template_path = os.path.join(BASE_DIR, template_path)

    file_index = config.get('file_index', [])
    unanalyzed = []

    for f in file_index:
        if not f.get('analyzed', False):
            full_path = os.path.join(template_path, f['path'])
            if os.path.exists(full_path):
                unanalyzed.append(full_path)

    return unanalyzed


def read_file_content(filepath):
    """读取文件内容"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: {str(e)}"


def reset_config():
    """重置配置为默认状态"""
    default_config = get_default_config()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, ensure_ascii=False, indent=2)
    return {"success": True, "message": "配置已重置为默认状态"}


def setup_user_info(config, name, identity, positions):
    """设置用户基本信息
    
    Args:
        config: 当前配置
        name: 用户姓名
        identity: 用户身份（如学生、护士等）
        positions: 职务列表，格式为 "开始日期:职务名称,开始日期:职务名称"
              例如: "2025-03-27:科爱社部长,2024-01:班级宣传委员"
    
    Returns:
        更新后的配置
    """
    # 解析职务信息
    position_list = []
    if positions:
        for pos in positions.split(','):
            if ':' in pos:
                start_date, title = pos.split(':', 1)
                position_list.append({
                    "title": title.strip(),
                    "start_date": start_date.strip(),
                    "end_date": None
                })
    
    # 更新用户信息
    if 'writing_style' not in config:
        config['writing_style'] = get_default_config()['writing_style']
    
    config['writing_style']['user_info'] = {
        "name": name,
        "identity": identity,
        "positions": position_list
    }
    
    return config


def save_analysis_result(config, user_info=None, word_count=None, 
                        opening_patterns=None, historical_weaknesses=None):
    """保存模型分析历史思想汇报的结果到配置
    
    由模型调用，将分析历史文件后提取的信息保存到 config.json
    
    Args:
        config: 当前配置
        user_info: 用户基本信息字典，包含 name, identity, positions
        word_count: 字数要求字典，包含各章节的字数限制
        opening_patterns: 开篇句式列表
        historical_weaknesses: 历史缺点列表，每项包含 theme, description, date
    
    Returns:
        更新后的配置
    """
    if 'writing_style' not in config:
        config['writing_style'] = get_default_config()['writing_style']
    
    # 更新用户信息
    if user_info:
        config['writing_style']['user_info'] = user_info
    
    # 更新字数要求
    if word_count:
        config['writing_style']['word_count'] = word_count
    
    # 更新开篇句式
    if opening_patterns:
        # 合并新的开篇句式，避免重复
        existing = set(config['writing_style'].get('opening_patterns', []))
        existing.update(opening_patterns)
        config['writing_style']['opening_patterns'] = list(existing)
    
    # 更新历史缺点
    if historical_weaknesses:
        existing = config['writing_style'].get('historical_weaknesses', [])
        # 根据 theme 去重，保留最新的
        existing_themes = {w['theme'] for w in existing}
        for weakness in historical_weaknesses:
            if weakness['theme'] not in existing_themes:
                existing.append(weakness)
        config['writing_style']['historical_weaknesses'] = existing
    
    return config


def main():
    parser = argparse.ArgumentParser(description="配置管理工具")
    parser.add_argument("action", choices=[
        "check", "status", "reset", "get-unanalyzed", "mark-analyzed", "setup", "save-analysis"
    ], help="执行的操作")
    parser.add_argument("--template-path", help="设置模板路径（绝对或相对路径）")
    parser.add_argument("--files", help="要标记为已分析的文件路径，逗号分隔")
    parser.add_argument("--name", help="用户姓名（setup命令使用）")
    parser.add_argument("--identity", help="用户身份（setup命令使用）")
    parser.add_argument("--positions", help="职务信息，格式：开始日期:职务名称,开始日期:职务名称（setup命令使用）")
    parser.add_argument("--analysis-data", help="分析结果JSON字符串（save-analysis命令使用）")

    args = parser.parse_args()

    if args.action == "check":
        # 检查配置状态和新文件
        config = load_config()
        result = check_new_files(config)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.action == "status":
        # 显示当前配置状态
        config = load_config()
        status = {
            "template_path": config.get('template_path', '未设置'),
            "file_count": len(config.get('file_index', [])),
            "unanalyzed_count": len([f for f in config.get('file_index', []) if not f.get('analyzed', False)]),
            "user_info": config.get('writing_style', {}).get('user_info', {}),
            "last_updated": config.get('last_updated', '从未更新')
        }
        print(json.dumps(status, ensure_ascii=False, indent=2))

    elif args.action == "reset":
        # 重置配置
        result = reset_config()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.action == "get-unanalyzed":
        # 获取未分析的文件
        config = load_config()
        files = get_unanalyzed_files(config)
        print(json.dumps({"files": files}, ensure_ascii=False, indent=2))

    elif args.action == "mark-analyzed":
        # 标记文件为已分析
        if not args.files:
            print(json.dumps({"error": "需要提供 --files 参数"}, ensure_ascii=False))
            sys.exit(1)

        config = load_config()
        file_list = args.files.split(',')

        for filepath in file_list:
            for f in config.get('file_index', []):
                if f['path'] == filepath or os.path.join(config.get('template_path', ''), f['path']) == filepath:
                    f['analyzed'] = True

        save_config(config)
        print(json.dumps({"success": True, "message": f"已标记 {len(file_list)} 个文件为已分析"}, ensure_ascii=False))

    elif args.action == "setup":
        # 设置用户基本信息
        if not args.name or not args.identity:
            print(json.dumps({
                "error": "setup命令需要提供 --name 和 --identity 参数",
                "usage": "python config_manager.py setup --name \"姓名\" --identity \"身份\" --positions \"开始日期:职务,开始日期:职务\""
            }, ensure_ascii=False))
            sys.exit(1)

        config = load_config()
        config = setup_user_info(config, args.name, args.identity, args.positions)
        save_config(config)
        
        result = {
            "success": True,
            "message": "用户基本信息已保存",
            "user_info": config['writing_style']['user_info']
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.action == "save-analysis":
        # 保存模型分析结果
        if not args.analysis_data:
            print(json.dumps({
                "error": "save-analysis命令需要提供 --analysis-data 参数",
                "usage": "python config_manager.py save-analysis --analysis-data '{JSON字符串}'"
            }, ensure_ascii=False))
            sys.exit(1)

        try:
            analysis_data = json.loads(args.analysis_data)
            config = load_config()
            
            config = save_analysis_result(
                config,
                user_info=analysis_data.get('user_info'),
                word_count=analysis_data.get('word_count'),
                opening_patterns=analysis_data.get('opening_patterns'),
                historical_weaknesses=analysis_data.get('historical_weaknesses')
            )
            save_config(config)
            
            result = {
                "success": True,
                "message": "分析结果已保存",
                "saved_data": {
                    "user_info": analysis_data.get('user_info'),
                    "word_count": analysis_data.get('word_count'),
                    "opening_patterns_count": len(analysis_data.get('opening_patterns', [])),
                    "historical_weaknesses_count": len(analysis_data.get('historical_weaknesses', []))
                }
            }
            print(json.dumps(result, ensure_ascii=False, indent=2))
        except json.JSONDecodeError as e:
            print(json.dumps({
                "error": f"JSON解析错误: {str(e)}",
                "hint": "请确保 --analysis-data 参数是有效的JSON字符串"
            }, ensure_ascii=False))
            sys.exit(1)


if __name__ == "__main__":
    main()
