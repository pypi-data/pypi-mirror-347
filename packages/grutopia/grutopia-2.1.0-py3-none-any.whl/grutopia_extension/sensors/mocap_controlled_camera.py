import math
from typing import Dict

import numpy as np
import omni.isaac.core.utils.numpy.rotations as rot_utils
from omni.isaac.sensor import Camera as i_Camera
from scipy.spatial.transform import Rotation as R

from grutopia.core.robot.robot import BaseRobot, Scene
from grutopia.core.robot.sensor import BaseSensor
from grutopia.core.util import log
from grutopia_extension.configs.sensors import MocapControlledCameraCfg

DISPLACEMENT_THRESHOLD = 0.05
NUM_SPECIFIC_POSE_FRAMES = 60


@BaseSensor.register('MocapControlledCamera')
class MocapControlledCamera(BaseSensor):
    """
    wrap of isaac sim's Camera class
    """

    def __init__(self, config: MocapControlledCameraCfg, robot: BaseRobot, name: str = None, scene: Scene = None):
        super().__init__(config, robot, scene)
        self.name = name
        self.config = config

        self.camera_mover = CameraMover([0, 0, 0])

    def create_camera(self) -> i_Camera:
        """Create an isaac-sim camera object.

        Initializes the camera's resolution and prim path based on configuration.

        Returns:
            i_Camera: The initialized camera object.
        """
        # Initialize the params for the camera
        resolution = self.config.resolution if self.config.resolution else (320, 240)
        translation = self.config.translation if self.config.translation else None
        orientation = self.config.orientation if self.config.translation else None

        prim_path = self._robot.config.prim_path + '/' + self.config.prim_path
        log.debug('camera_prim_path: ' + prim_path)
        log.debug('name            : ' + self.config.name)
        log.debug(f'resolution      : {resolution}')
        return i_Camera(prim_path=prim_path, resolution=resolution, translation=translation, orientation=orientation)

    def post_reset(self):
        if self.config.enable:
            self._camera = self.create_camera()
            self._camera.initialize()
            # self._camera.add_pointcloud_to_frame()
            # self._camera.add_distance_to_image_plane_to_frame()
            # self._camera.add_semantic_segmentation_to_frame()
            # self._camera.add_instance_segmentation_to_frame()
            # self._camera.add_instance_id_segmentation_to_frame()
            self._camera.add_bounding_box_2d_tight_to_frame()

    def get_data(self) -> Dict:
        if self.config.enable:
            rgba = self._camera.get_rgba()
            frame = self._camera.get_current_frame()
            return {'rgba': rgba, 'frame': frame}
        return {}

    @property
    def camera(self):
        return self._camera


class CameraMover(object):
    def __init__(self, target_point, rate=[3, 5, 5]):
        self.qualified_count = 0
        self.is_move = False

        self.l_hand_0_start_point = None
        self.camera_start_point = None
        self.target_point = self.set_target_position(target_point)

        self.rate = rate

    def __call__(self, camera_position, camera_orientation, results):
        self.condition_judgment(results)

        # maintain current position if condition not met
        if not self.is_move:
            self.l_hand_0_start_point = None
            self.camera_start_point = None
            self.qualified_count = 0
            return camera_position, camera_orientation

        if self.qualified_count < NUM_SPECIFIC_POSE_FRAMES:
            self.qualified_count += 1
            return camera_position, camera_orientation

        # set the starting point
        lh_bones_kps_cam = results.get('lh_bones_kps_cam', None)
        if self.l_hand_0_start_point is None:
            self.l_hand_0_start_point = lh_bones_kps_cam[0]
            self.camera_start_point = camera_position

        # calculate the left-hand coordinate difference in the world coordinate system
        l_hand_0_gap = np.round([a - b for a, b in zip(lh_bones_kps_cam[0], self.l_hand_0_start_point)], 3)
        l_hand_0_gap = [-1 * l_hand_0_gap[2], l_hand_0_gap[0], -1 * l_hand_0_gap[1]]
        l_hand_0_gap = [l_hand_0_gap[i] * self.rate[i] for i in range(3)]

        rot_matrices = rot_utils.quats_to_rot_matrices(camera_orientation)
        l_hand_0_gap = np.dot(rot_matrices, l_hand_0_gap)

        # superimpose the difference and calculate the orientation
        new_camera_position = self.camera_start_point + l_hand_0_gap
        euler_angles = CameraMover.compute_orientation(new_camera_position, self.target_point)
        new_camera_orientation = rot_utils.euler_angles_to_quats(euler_angles, degrees=True)

        return new_camera_position, new_camera_orientation

    def set_target_position(self, target_point):
        self.target_point = np.array(target_point)

    def condition_judgment(self, results):
        lh_bones_kps = results.get('lh_bones_kps', None)
        if lh_bones_kps is None:
            self.is_move = False
            return

        thumb_finger = lh_bones_kps[4]
        index_finger = lh_bones_kps[8]
        distance = math.sqrt(
            (index_finger[0] - thumb_finger[0]) ** 2
            + (index_finger[1] - thumb_finger[1]) ** 2
            + (index_finger[2] - thumb_finger[2]) ** 2
        )

        if distance < DISPLACEMENT_THRESHOLD:
            self.is_move = True
        else:
            self.is_move = False

    @staticmethod
    def compute_orientation(P1, P2):
        vector = np.array(P2) - np.array(P1)
        unit_vector = vector / np.linalg.norm(vector)

        origin_vector = np.array([1, 0, 0])
        axis = np.cross(origin_vector, unit_vector)
        axis = axis / np.linalg.norm(axis)
        angle = np.arccos(np.dot(origin_vector, unit_vector))

        r = R.from_rotvec(axis * angle)
        euler_angles = r.as_euler('xyz', degrees=True)

        return euler_angles
