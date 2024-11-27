import os
import xml.etree.ElementTree as ET
def get_all_link(element):
            links = element.findall(".//link")  # 使用 XPath 表达式
            # 输出所有 link 元素
            print(f"Found {len(links)} link elements:")
            #for link in links:
            #    print(f"Tag: {link.tag}, Attributes: {link.attrib}, Text: {link.text.strip() if link.text else 'None'}")
            return links
        
def get_all_joint(element):
    joints = element.findall(".//joint")  # 使用 XPath 表达式
    # 输出所有 link 元素
    print(f"Found {len(joints)} link elements:")
    #for joint in joints:
    #    print(f"Tag: {joint.tag}, Attributes: {joint.attrib}, Text: {joint.text.strip() if joint.text else 'None'}")
    return joints

def fix_inertial(true_file_path,fix_file_path,base_link_name):
    try:
        print("开始修复")        
        tree = ET.parse(true_file_path)
        root = tree.getroot()

        links = get_all_link(root)
        joints = get_all_joint(root)
        
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
        
        
        def fix_link(target_link_name):
            #搜索joint树
            search_finish = False
            search_child_link_name = target_link_name
            search_joints = []

            while(search_finish == False):
                for joint in joints:
                    joint_name = joint.attrib.get("name")
                    #print(f"{joint_name}")
                    

                    child_link = joint.find("child")
                    parent_link = joint.find("parent")
                    child_link_name = child_link.attrib.get("link")
                    parent_link_name = parent_link.attrib.get("link")
                    
                    #print(f"{parent_link_name}")

                    #记录坐标叠加
                    if(child_link_name == search_child_link_name):
                        print("搜索到" + joint_name)
                        search_joints.append(joint)
                        search_child_link_name = parent_link_name
                        #如果搜索到base_link_name则结束搜索
                        if(parent_link_name == base_link_name):
                            search_finish = True
            
        
        target_link_name = "${prefix}_arm_link3"
        fix_link(target_link_name)

        #search_child_link = target_link
        # 用于存储 target_link joint树的列表
        #

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