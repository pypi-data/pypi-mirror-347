from grutopia.core.config import Config, SimConfig
from grutopia.core.gym_env import Env
from grutopia.core.runtime import SimulatorRuntime
from grutopia.core.util import has_display
from grutopia.macros import gm
from grutopia_extension import import_extensions
from grutopia_extension.configs.robots.jetbot import (
    JetbotRobotCfg,
    move_along_path_cfg,
    move_to_point_cfg,
)
from grutopia_extension.configs.tasks import (
    SingleInferenceEpisodeCfg,
    SingleInferenceTaskCfg,
)

headless = False

if not has_display():
    headless = True


config = Config(
    simulator=SimConfig(physics_dt=1 / 240, rendering_dt=1 / 240, use_fabric=False),
    task_config=SingleInferenceTaskCfg(
        episodes=[
            SingleInferenceEpisodeCfg(
                scene_asset_path=gm.ASSET_PATH + '/scenes/empty.usd',
                robots=[
                    JetbotRobotCfg(
                        position=(0.0, 0.0, 0.0),
                        controllers=[move_to_point_cfg, move_along_path_cfg],
                        scale=(5.0, 5.0, 5.0),
                    )
                ],
            ),
        ],
    ),
)

sim_runtime = SimulatorRuntime(config_class=config, headless=headless, native=headless)

path = [(3.0, 3.0, 0.0), (1.0, 0.0, 0.0), (0.0, -1.0, 0.0), (-1.0, 0.5, 0.0)]

import_extensions()
# import custom extensions here.
import numpy as np

env = Env(sim_runtime)
obs, _ = env.reset()

i = 0

env_action = {
    move_along_path_cfg.name: [path],
}

print(f'actions: {env_action}')

while env.simulation_app.is_running():
    i += 1
    obs, _, terminated, _, _ = env.step(action=env_action)

    if i % 1000 == 0:
        print(i)
        current_point = obs['controllers'][move_along_path_cfg.name]['current_point']
        error = np.linalg.norm(obs['position'][:2] - current_point[:2])
        print(f'position: {obs["position"]}, error: {error}')

env.simulation_app.close()
