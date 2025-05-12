from typing import Optional, Tuple

from grutopia.core.config.scene import ObjectCfg


class DynamicCubeCfg(ObjectCfg):
    type: Optional[str] = 'DynamicCube'
    color: Optional[Tuple[float, float, float]] = None
    mass: Optional[float] = None
    density: Optional[float] = None
    collider: Optional[bool] = True


class VisualCubeCfg(ObjectCfg):
    type: Optional[str] = 'VisualCube'
    color: Optional[Tuple[float, float, float]] = None


class UsdObjCfg(ObjectCfg):
    type: Optional[str] = 'UsdObject'
    usd_path: str
    collider: Optional[bool] = True
