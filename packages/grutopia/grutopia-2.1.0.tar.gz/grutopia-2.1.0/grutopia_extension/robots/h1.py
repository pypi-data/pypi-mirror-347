import os
from typing import List

import numpy as np
from omni.isaac.core.articulations import ArticulationSubset
from omni.isaac.core.prims import RigidPrim
from omni.isaac.core.robots.robot import Robot as IsaacRobot
from omni.isaac.core.scenes import Scene
from omni.isaac.core.utils.stage import add_reference_to_stage

from grutopia.core.config.robot import RobotCfg
from grutopia.core.robot.robot import BaseRobot
from grutopia.core.util import log


class H1(IsaacRobot):
    def __init__(
        self,
        prim_path: str,
        usd_path: str,
        name: str,
        position: np.ndarray = None,
        orientation: np.ndarray = None,
        scale: np.ndarray = None,
    ):
        add_reference_to_stage(prim_path=prim_path, usd_path=os.path.abspath(usd_path))
        super().__init__(prim_path=prim_path, name=name, position=position, orientation=orientation, scale=scale)

    def set_gains(self):
        """
        Set default stiffness (kps) and damping (kds) for joints.
        """
        joint_names = np.array(
            [
                'left_hip_yaw_joint',
                'right_hip_yaw_joint',
                'torso_joint',
                'left_hip_roll_joint',
                'right_hip_roll_joint',
                'left_shoulder_pitch_joint',
                'right_shoulder_pitch_joint',
                'left_hip_pitch_joint',
                'right_hip_pitch_joint',
                'left_shoulder_roll_joint',
                'right_shoulder_roll_joint',
                'left_knee_joint',
                'right_knee_joint',
                'left_shoulder_yaw_joint',
                'right_shoulder_yaw_joint',
                'left_ankle_joint',
                'right_ankle_joint',
                'left_elbow_joint',
                'right_elbow_joint',
            ]
        )

        joint_subset = ArticulationSubset(self, joint_names)

        kps = np.array(
            [
                200.0,
                200.0,
                300.0,
                200.0,
                200.0,
                100.0,
                100.0,
                200.0,
                200.0,
                100.0,
                100.0,
                300.0,
                300.0,
                100.0,
                100.0,
                40.0,
                40.0,
                100.0,
                100.0,
            ]
        )
        kds = np.array([5.0, 5.0, 6.0, 5.0, 5.0, 2.0, 2.0, 5.0, 5.0, 2.0, 2.0, 6.0, 6.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0])

        kps = self._articulation_view._backend_utils.expand_dims(kps, 0)
        kds = self._articulation_view._backend_utils.expand_dims(kds, 0)
        self._articulation_view.set_gains(kps=kps, kds=kds, save_to_usd=False, joint_indices=joint_subset.joint_indices)
        # VERY important!!! additional physics parameter
        self.set_solver_position_iteration_count(4)
        self.set_solver_velocity_iteration_count(0)


@BaseRobot.register('H1Robot')
class H1Robot(BaseRobot):
    def __init__(self, config: RobotCfg, scene: Scene):
        super().__init__(config, scene)
        self._sensor_config = config.sensors
        self._start_position = np.array(config.position) if config.position is not None else None
        self._start_orientation = np.array(config.orientation) if config.orientation is not None else None

        log.debug(f'h1 {config.name}: position    : ' + str(self._start_position))
        log.debug(f'h1 {config.name}: orientation : ' + str(self._start_orientation))

        usd_path = config.usd_path

        log.debug(f'h1 {config.name}: usd_path         : ' + str(usd_path))
        log.debug(f'h1 {config.name}: config.prim_path : ' + str(config.prim_path))
        self.isaac_robot = H1(
            prim_path=config.prim_path,
            name=config.name,
            position=self._start_position,
            orientation=self._start_orientation,
            usd_path=usd_path,
        )
        self.isaac_robot.set_enabled_self_collisions(True)

        self._robot_scale = np.array([1.0, 1.0, 1.0])
        if config.scale is not None:
            self._robot_scale = np.array(config.scale)
            self.isaac_robot.set_local_scale(self._robot_scale)

        self._robot_base = RigidPrim(prim_path=config.prim_path + '/pelvis', name=config.name + '_base')
        self._robot_right_ankle = RigidPrim(
            prim_path=config.prim_path + '/right_ankle_link', name=config.name + 'right_ankle'
        )
        self._robot_left_ankle = RigidPrim(
            prim_path=config.prim_path + '/left_ankle_link', name=config.name + 'left_ankle'
        )

        self._rigid_bodies = [self._robot_base, self._robot_right_ankle, self._robot_left_ankle]

    def get_rigid_bodies(self) -> List[RigidPrim]:
        return self._rigid_bodies

    def post_reset(self):
        super().post_reset()
        self.isaac_robot.set_gains()

    def get_ankle_height(self):
        return np.min([self._robot_right_ankle.get_world_pose()[0][2], self._robot_left_ankle.get_world_pose()[0][2]])

    def get_robot_scale(self):
        return self._robot_scale

    def get_robot_base(self) -> RigidPrim:
        return self._robot_base

    def get_world_pose(self):
        return self._robot_base.get_world_pose()

    def apply_action(self, action: dict):
        """
        Args:
            action (dict): inputs for controllers.
        """
        for controller_name, controller_action in action.items():
            if controller_name not in self.controllers:
                log.warning(f'unknown controller {controller_name} in action')
                continue
            controller = self.controllers[controller_name]
            control = controller.action_to_control(controller_action)
            self.isaac_robot.apply_action(control)

    def get_obs(self):
        position, orientation = self._robot_base.get_world_pose()

        # custom
        obs = {
            'position': position,
            'orientation': orientation,
            'controllers': {},
            'sensors': {},
        }

        # common
        for c_obs_name, controller_obs in self.controllers.items():
            obs['controllers'][c_obs_name] = controller_obs.get_obs()
        for sensor_name, sensor_obs in self.sensors.items():
            obs['sensors'][sensor_name] = sensor_obs.get_data()
        return obs
