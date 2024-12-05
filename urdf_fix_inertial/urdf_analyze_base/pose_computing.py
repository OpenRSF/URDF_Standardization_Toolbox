import numpy as np
from scipy.spatial.transform import Rotation

def rpy_to_rotation_matrix(rpy):
    # 定义 Roll, Pitch, Yaw 角度 (弧度)
    roll = rpy[0]  # 例如 30 度
    pitch = rpy[1]  # 例如 45 度
    yaw = rpy[2]   # 例如 60 度

    # 计算旋转矩阵
    cos_roll, sin_roll = np.cos(roll), np.sin(roll)
    cos_pitch, sin_pitch = np.cos(pitch), np.sin(pitch)
    cos_yaw, sin_yaw = np.cos(yaw), np.sin(yaw)

    rotation_matrix = np.array([
        [cos_yaw * cos_pitch, cos_yaw * sin_pitch * sin_roll - sin_yaw * cos_roll, cos_yaw * sin_pitch * cos_roll + sin_yaw * sin_roll],
        [sin_yaw * cos_pitch, sin_yaw * sin_pitch * sin_roll + cos_yaw * cos_roll, sin_yaw * sin_pitch * cos_roll - cos_yaw * sin_roll],
        [-sin_pitch, cos_pitch * sin_roll, cos_pitch * cos_roll]
    ])

    return rotation_matrix

class Pose:
    def __init__(self, translation, rotation_matrix):
        self.translation = np.array(translation)
        self.rotation_matrix = np.array(rotation_matrix)

    @classmethod
    def from_translation_and_rotation(cls, translation, rotation_matrix):
        return cls(translation, rotation_matrix)

    @classmethod
    def from_translation_and_quaternion(cls, translation, quaternion):
        rotation = Rotation.from_quat(quaternion)
        rotation_matrix = rotation.as_dcm()
        return cls(translation, rotation_matrix)

    def get_pose_matrix(self):
        pose_matrix = np.eye(4)
        pose_matrix[:3, :3] = self.rotation_matrix
        pose_matrix[:3, 3] = self.translation
        return pose_matrix

## 示例使用
#translation = np.array([1.0, 2.0, 3.0])
#rotation_matrix = np.array([
#    [0.98480775, 0.17364818, -0.0],
#    [-0.17364818, 0.98480775, -0.0],
#    [0.0, 0.0, 1.0]
#])
#
#pose = Pose.from_translation_and_rotation(translation, rotation_matrix)
#
#print("Position:", pose.translation)
#print("Rotation Matrix:\n", pose.rotation_matrix)
#print("Pose Matrix:\n", pose.get_pose_matrix())
#print("Roll, Pitch, Yaw (rad):", pose.get_roll_pitch_yaw())
#
## 从四元数创建位姿
#quaternion = np.array([1.0, 0.0, 0.0, 0.0])  # 单位四元数表示没有旋转
#pose_from_quaternion = Pose.from_translation_and_quaternion(translation, quaternion)
#
#print("Position (from quaternion):", pose_from_quaternion.translation)
#print("Rotation Matrix (from quaternion):\n", pose_from_quaternion.rotation_matrix)
#print("Pose Matrix (from quaternion):\n", pose_from_quaternion.get_pose_matrix())
#print("Roll, Pitch, Yaw (rad) (from quaternion):", pose_from_quaternion.get_roll_pitch_yaw())
