import os
import xml.etree.ElementTree as ET

def fix_inertial(true_file_path,fix_file_path,base_link_name):
    try:
        print("开始修复")
        
        tree = ET.parse(true_file_path)
        root = tree.getroot()
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
        
        def print_all_link(element):
            links = element.findall(".//link")  # 使用 XPath 表达式
            # 输出所有 link 元素
            print(f"Found {len(links)} link elements:")
            for link in links:
                print(f"Tag: {link.tag}, Attributes: {link.attrib}, Text: {link.text.strip() if link.text else 'None'}")

        print_all_link(root)

    except ET.ParseError as e:
        print(f"XML Parse Error: {e}")
    except FileNotFoundError:
        print(f"File not found: {true_file_path} or {fix_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    current_file_path = os.path.abspath(__file__)
    true_file_path = os.path.dirname(current_file_path) + "/urdf/R5a.urdf"
    fix_file_path = os.path.dirname(current_file_path) + "/urdf/R5_base.xacro"
    base_link_name = "${prefix}_arm_base_link"
    fix_inertial(true_file_path,fix_file_path,base_link_name)