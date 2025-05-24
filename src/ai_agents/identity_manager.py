
class AgentIdentityManager:

    class Triage:
        task_name   : str = 'triage'
        triage_agent: str = 'triage_agent'


    @classmethod
    def get_task_agents(cls, task: str) -> list[str]:
        """
        Returns a list of task agents.
        """

        task_map = {
            cls.Triage.task_name: [
                cls.Triage.triage_agent,
            ],
        }

        return task_map.get(task.lower(), [])