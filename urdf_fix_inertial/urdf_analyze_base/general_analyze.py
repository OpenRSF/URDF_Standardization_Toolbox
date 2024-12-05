import os
import xml.etree.ElementTree as ET

def get_all_link(element):
    links = element.findall(".//link")  # 使用 XPath 表达式
    # 输出所有 link 元素
    print(f"Found {len(links)} link elements:")
    # for link in links:
    #    print(f"Tag: {link.tag}, Attributes: {link.attrib}, Text: {link.text.strip() if link.text else 'None'}")
    return links


def get_all_joint(element):
    joints = element.findall(".//joint")  # 使用 XPath 表达式
    # 输出所有 link 元素
    print(f"Found {len(joints)} link elements:")
    # for joint in joints:
    #    print(f"Tag: {joint.tag}, Attributes: {joint.attrib}, Text: {joint.text.strip() if joint.text else 'None'}")
    return joints

def origin_string_analyze(input_string):
    # 使用 split() 方法将字符串分割成列表
    parts = input_string.split()
    # 将每个部分转换为浮点数
    float_numbers = [float(part) for part in parts]
    return float_numbers

def origin_analyze(origin):
    origin_xyz = origin.attrib.get("xyz")
    origin_rpy = origin.attrib.get("rpy")

    #print("搜索到" + joint_name + "的origin:" + origin_xyz)
    output = origin_string_analyze(origin_xyz) + origin_string_analyze(origin_rpy)

    return output