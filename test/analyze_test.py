import xml.etree.ElementTree as ET

def parse_and_print_xml(file_path):
    try:
        # 解析 XML 文件
        tree = ET.parse(file_path)
        root = tree.getroot()

        # 打印根元素信息
        print(f"Root Element: {root.tag}")
        print("-" * 50)

        # 递归打印 XML 节点
        def print_element(element, indent=0):
            spacing = " " * indent
            # 打印当前节点的标签和属性
            print(f"{spacing}Tag: {element.tag}, Attributes: {element.attrib}")
            # 打印当前节点的文本内容（如果有）
            if element.text and element.text.strip():
                print(f"{spacing}Text: {element.text.strip()}")
            # 递归处理子元素
            for child in element:
                print_element(child, indent + 4)

        print_element(root)

    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # 替换为你的 XML 文件路径
    file_path = "R5_base.xacro"
    parse_and_print_xml(file_path)
