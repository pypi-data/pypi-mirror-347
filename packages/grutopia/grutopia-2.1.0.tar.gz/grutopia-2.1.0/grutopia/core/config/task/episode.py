from typing import Any, List, Optional, Tuple

from pydantic import BaseModel

from grutopia.core.config.robot import RobotCfg
from grutopia.core.config.scene import ObjectCfg as Object


class EpisodeCfg(BaseModel, extra='allow'):
    """
    Represents the configuration details for an episode in a simulation or robotics application.

    This class defines the structure of an episode's settings, including the scene's assets, scaling, positioning, orientation,
    as well as the robots and objects involved. It is designed to be flexible and extensible, allowing for customization of various aspects of the simulation environment.

    Attributes:
        scene_asset_path (Optional[str]): The file path to the scene asset. Defaults to None.
        scene_scale (Optional[Tuple[float, float, float]]): Scaling factors applied to the scene along the x, y, and z axes. Defaults to (1.0, 1.0, 1.0).
        scene_position (Optional[Tuple[float, float, float]]): The position of the scene's origin in world coordinates. Defaults to (0, 0, 0).
        scene_orientation (Optional[Tuple[float, float, float, float]]): The quaternion representing the scene's orientation. Defaults to (1.0, 0, 0, 0).
        robots (Optional[List[RobotModel]]): A list of configurations for robots participating in the episode. Defaults to an empty list.
        objects (Optional[List[Object]]): A list of objects present in the scene. Defaults to an empty list.
        extra (Optional[Dict[str, Any]]): Additional configuration options not covered by the predefined attributes. Defaults to an empty dictionary.

    Note:
        The class inherits from `BaseModel` and specifies `extra='allow'` to permit additional keys in the configuration without raising an error.
    """

    scene_asset_path: Optional[str] = None
    scene_scale: Optional[Tuple[float, float, float]] = (1.0, 1.0, 1.0)
    scene_position: Optional[Tuple[float, float, float]] = (0, 0, 0)
    scene_orientation: Optional[Tuple[float, float, float, float]] = (1.0, 0, 0, 0)
    robots: Optional[List[RobotCfg]] = []
    objects: Optional[List[Object]] = []
    extra: Optional[Any] = None


class EpisodeConfigFile(BaseModel, extra='allow'):
    """
    Episode config file model.
    """

    episodes: List[EpisodeCfg]
