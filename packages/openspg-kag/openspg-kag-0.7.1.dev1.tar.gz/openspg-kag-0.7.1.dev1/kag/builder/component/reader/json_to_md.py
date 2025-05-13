import json
import os

def get_text(elements):
    """
    从元素列表（可能包含 text_run 和 equation）中取出文本，并拼接成字符串
    """
    parts = []
    for e in elements:
        if "text_run" in e:
            parts.append(e["text_run"].get("content", ""))
        elif "equation" in e:
            # 如果需要可以根据需要选择行内或块级公式，这里示例用行内公式格式
            eq_text = e["equation"].get("content", "")
            parts.append(f"\\({eq_text.strip()}\\)")
    return "".join(parts)

def block_to_markdown(block, block_map, level=0):
    """
    递归地将一个 block 转换为 Markdown 文本，level 用于控制列表或标题的缩进层级
    """
    md_lines = []
    indent = "  " * level  # 用于列表项或代码块格式的简单缩进
    block_type = block.get("block_type")
    
    # 根据不同类型转换内容
    if block_type == 1:
        # 容器块，通常包含 page 内容
        if "page" in block and "elements" in block["page"]:
            text = get_text(block["page"]["elements"])
            if text.strip():
                md_lines.append(indent + text.strip())
    elif block_type == 2:
        # 普通文本块
        if "text" in block and "elements" in block["text"]:
            text = get_text(block["text"]["elements"])
            if text.strip():
                md_lines.append(indent + text.strip())
    elif block_type == 3:
        # 标题：这里用 heading1 做示例
        if "heading1" in block and "elements" in block["heading1"]:
            text = get_text(block["heading1"]["elements"])
            if text.strip():
                # 根据层级生成 Markdown 标题（最多 6 级）
                header_prefix = "#" * (min(level + 1, 6))
                md_lines.append(f"{header_prefix} {text.strip()}")
    elif block_type == 12:
        # 无序列表项
        if "bullet" in block and "elements" in block["bullet"]:
            text = get_text(block["bullet"]["elements"])
            if text.strip():
                md_lines.append(indent + "- " + text.strip())
    elif block_type == 13:
        # 有序列表项
        if "ordered" in block and "elements" in block["ordered"]:
            text = get_text(block["ordered"]["elements"])
            if text.strip():
                md_lines.append(indent + "1. " + text.strip())
    elif block_type == 27:
        # 图片块
        if "image" in block:
            token = block["image"].get("token", "")
            # 这里使用 token 作为图片标识，实际可根据 token 得到真正的 URL
            md_lines.append(indent + f"![Image]({token})")
    else:
        # 其他未处理情况：尝试直接使用 text 字段
        if "text" in block and "elements" in block["text"]:
            text = get_text(block["text"]["elements"])
            if text.strip():
                md_lines.append(indent + text.strip())

    # 如果该 block 有子块，则递归处理
    children_ids = block.get("children", [])
    for child_id in children_ids:
        child_block = block_map.get(child_id)
        if child_block:
            child_md = block_to_markdown(child_block, block_map, level=level+1)
            if child_md:
                md_lines.extend(child_md)

    return md_lines

def main():
    # 加载 JSON 文件
    dir = os.path.dirname(__file__)
    with open(os.path.join(dir, "block_data.json"), "r", encoding="utf-8") as f:
        data = json.load(f)
    
    items = data.get("items", [])
    # 构造 block_id 到 block 的映射字典
    block_map = {block["block_id"]: block for block in items}

    # 找出所有根节点（parent_id 为空）
    root_blocks = [block for block in items if block.get("parent_id") == ""]

    md_lines = []
    for root in root_blocks:
        md_lines.extend(block_to_markdown(root, block_map, level=0))
        md_lines.append("")  # 各个根块之间空一行

    # 生成最终 Markdown 内容
    md_content = "\n".join(md_lines)
    
    # 输出到文件中
    with open(os.path.join(dir, "output.md"), "w", encoding="utf-8") as f:
        f.write(md_content)
    print("Markdown 文件已生成：output.md")

if __name__ == "__main__":
    main()