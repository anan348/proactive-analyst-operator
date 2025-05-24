
class AgentIdentityManager:

    class Triage:
        triage_agent: str = 'triage_agent'


    @classmethod
    def get_task_agents(cls, task: str) -> list[str]:
        """
        Returns a list of task agents.
        """

        task_map = {
            'triage': [
                cls.Triage.triage_agent,
            ],
        }

        return task_map.get(task.lower(), [])