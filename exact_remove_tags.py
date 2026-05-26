import os
import re

# 目标技术文档目录
TARGET_DIR = os.path.join('content', 'docs')

def remove_tech_tags():
    # 精确匹配行首的 tech_tags: ["xxx", "xxx"] 格式，并连带匹配最后的换行符 \n
    # ^ 确保只从行首开始匹配，\[.*?\] 干净地吃掉方括号及里面的所有标签
    pattern = re.compile(r'^tech_tags\s*:\s*\[.*?\]\s*\n', re.MULTILINE)
    
    count = 0
    print(f"正在精准扫描目录: {TARGET_DIR} ...")

    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 执行精准替换，直接把这一整行抽掉
                    new_content = pattern.sub('', content)

                    if new_content != content:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"[已精准删除 tech_tags 行] {file_path}")
                        count += 1
                except Exception as e:
                    print(f"[错误] 无法处理文件 {file_path}: {e}")

    print(f"\n清理完毕！共精准删除了 {count} 个技术文档中的 tech_tags 字段。")

if __name__ == "__main__":
    # 执行前建议先用 git commit 留个快照，方便随时回滚
    remove_tech_tags()