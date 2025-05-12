from typing import Any, Dict

from grutopia.core.datahub import DataHub
from grutopia.core.runtime.task_runtime import TaskRuntime
from grutopia.core.util import log
from grutopia_extension.agents.core.agent import BaseAgent

# Load NPC from NPC repo
from grutopia_extension.agents.npc_agent import NPC
from grutopia_extension.agents.npc_agent.config import NPCUserConfig


@BaseAgent.register('NPCAgent')
class NPCAgentClient(BaseAgent):
    """
    NPC Agent.

    This agent won't be terminated.
    """

    def __init__(
        self, task_name: str, robot_name: str | None, agent_config: Dict, sync_mode: str, task_runtime: TaskRuntime
    ):
        super().__init__(task_name, robot_name, agent_config, sync_mode, task_runtime)
        log.debug(f'=============== agent_config: {agent_config} ===============')
        try:
            cfg = NPCUserConfig(**agent_config)
        except Exception as e:
            log.error('agent_config of this agent(NPC) is not valid (By grutopia.core.runtime.npc.NPCUserConfig)')
            raise e
        self.npc = NPC(cfg, task_runtime.extra)

    # TODO: Figure out a better way to implement this method.
    def decision_making(self, obs: Any) -> Any:
        """
        This agent won't be terminated.
        """
        obs = DataHub.get_obs_by_task_name(self.task_name)
        response_list = self.npc.feed(self.robot_name, obs, self.chat.get_message())
        for response in response_list:
            self.chat.send_message(**response.model_dump())
        return {}
