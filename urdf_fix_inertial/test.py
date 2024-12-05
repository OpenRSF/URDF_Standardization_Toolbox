import os
import xml.etree.ElementTree as ET
import numpy as np

import urdf_analyze_base as urdf_tool
        
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

        # 搜索目标link到base_link经过的joint
def fix_link(target_link_name,joints):
    translation = np.array([0.0, 0.0, 0.0])
    rotation_matrix = np.array([
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0],
        [0.0, 0.0, 1.0]
    ])

    pose = urdf_tool.Pose.from_translation_and_rotation(translation, rotation_matrix)


    # 搜索joint树
    search_finish = False
    search_child_link_name = target_link_name
    search_joints = []

    while search_finish == False:
        for joint in joints:
            joint_name = joint.attrib.get("name")
            # print(f"{joint_name}")

            child_link = joint.find("child")
            parent_link = joint.find("parent")
            child_link_name = child_link.attrib.get("link")
            parent_link_name = parent_link.attrib.get("link")

            # print(f"{parent_link_name}")

            # 记录坐标叠加
            if child_link_name == search_child_link_name:
                xyzrpy = urdf_tool.origin_analyze(joint.find("origin"))
                print(xyzrpy)
                print(urdf_tool.rpy_to_rotation_matrix(xyzrpy[3:6]))
                
                search_joints.append(joint)
                search_child_link_name = parent_link_name
                # 如果搜索到base_link_name则结束搜索
                if parent_link_name == base_link_name:
                    search_finish = True

def fix_inertial(true_file_path, fix_file_path, base_link_name):
    try:
        print("开始修复")
        true_tree = ET.parse(true_file_path)
        fix_tree = ET.parse(fix_file_path)

        true_root = true_tree.getroot()
        fix_root = fix_tree.getroot()

        #links = urdf_tool.get_all_link(root)
        true_joints = urdf_tool.get_all_joint(true_root)
        fix_joints = urdf_tool.get_all_joint(fix_root)
        

        fix_link("${prefix}_arm_link3",true_joints)
        fix_link("${prefix}_arm_link3",fix_joints)

        # search_child_link = target_link
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
    fix_inertial(true_file_path, fix_file_path, base_link_name)
