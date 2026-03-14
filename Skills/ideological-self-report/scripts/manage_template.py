import os
import sys
import argparse

# 设置工作目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REFERENCES_DIR = os.path.join(BASE_DIR, "references")
CUSTOM_FILE = os.path.join(REFERENCES_DIR, "custom-format.md")
DEFAULT_FILE = os.path.join(REFERENCES_DIR, "default-format.md")

def check_status():
    """检查自定义模板是否存在并返回当前应使用的文件路径"""
    if os.path.exists(CUSTOM_FILE):
        return {"exists": True, "active_file": CUSTOM_FILE}
    return {"exists": False, "active_file": DEFAULT_FILE}

def reset_to_default():
    """删除自定义模板文件以恢复默认状态"""
    if os.path.exists(CUSTOM_FILE):
        try:
            os.remove(CUSTOM_FILE)
            return {"success": True, "message": "已成功恢复默认配置"}
        except Exception as e:
            return {"success": False, "message": f"恢复默认配置失败: {str(e)}"}
    return {"success": True, "message": "当前已是默认配置"}

def update_custom(content):
    """保存学习到的语言风格和结构特点"""
    try:
        with open(CUSTOM_FILE, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"success": True, "message": f"分析结果已保存至 {CUSTOM_FILE}"}
    except Exception as e:
        return {"success": False, "message": f"保存分析结果失败: {str(e)}"}

def main():
    parser = argparse.ArgumentParser(description="管理思想汇报模板配置文件")
    parser.add_argument("action", choices=["status", "reset", "update"], help="执行的操作")
    parser.add_argument("--content", help="当 action 为 update 时，需要写入的文件内容（直接字符串）")
    parser.add_argument("--file", help="当 action 为 update 时，从指定文件读取内容")

    args = parser.parse_args()

    if args.action == "status":
        result = check_status()
        print(f"Status: {'Exists' if result['exists'] else 'Not Found'}")
        print(f"Active File: {result['active_file']}")
    elif args.action == "reset":
        result = reset_to_default()
        print(f"Result: {'Success' if result['success'] else 'Failure'}")
        print(f"Message: {result['message']}")
    elif args.action == "update":
        content = None
        # 优先从文件读取
        if args.file:
            try:
                with open(args.file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"Error: 读取文件失败: {str(e)}")
                sys.exit(1)
        # 其次使用命令行传入的内容
        elif args.content:
            content = args.content
        else:
            print("Error: 更新操作需要 --content 或 --file 参数")
            sys.exit(1)
        result = update_custom(content)
        print(f"Result: {'Success' if result['success'] else 'Failure'}")
        print(f"Message: {result['message']}")

if __name__ == "__main__":
    main()
