from context_lab_core.models import Membership, Project, Workspace
from context_lab_core.services import TaskService
from context_lab_storage.sqlite import SQLiteStores


def test_task_service_round_trips_through_sqlite() -> None:
    stores = SQLiteStores.in_memory()
    try:
        stores.workspaces.save(Workspace(id="ws-1", name="Acme"))
        stores.memberships.save(
            Membership(workspace_id="ws-1", user_id="user-1", role="member")
        )
        stores.projects.save(
            Project(id="project-1", workspace_id="ws-1", name="Launch")
        )
        service = TaskService(
            workspaces=stores.workspaces,
            memberships=stores.memberships,
            projects=stores.projects,
            tasks=stores.tasks,
            notifications=stores.notifications,
        )

        task = service.create_task(
            actor_id="user-1",
            project_id="project-1",
            title="Persist release notes",
        )

        assert stores.tasks.get(task.id) == task
    finally:
        stores.close()
