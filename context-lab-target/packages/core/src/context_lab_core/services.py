from uuid import uuid4

from .errors import NotFound, PermissionDenied
from .models import Notification, Task
from .ports import (
    MembershipStore,
    NotificationStore,
    ProjectStore,
    TaskStore,
    WorkspaceStore,
)


class TaskService:
    """Expose task use cases while keeping storage details behind ports."""

    def __init__(
        self,
        *,
        workspaces: WorkspaceStore,
        memberships: MembershipStore,
        projects: ProjectStore,
        tasks: TaskStore,
        notifications: NotificationStore,
    ) -> None:
        self._workspaces = workspaces
        self._memberships = memberships
        self._projects = projects
        self._tasks = tasks
        self._notifications = notifications

    def create_task(
        self,
        *,
        actor_id: str,
        project_id: str,
        title: str,
        assignee_id: str | None = None,
    ) -> Task:
        normalized_title = title.strip()
        if not normalized_title:
            raise ValueError("Task title cannot be empty")

        project = self._projects.get(project_id)
        if project is None:
            raise NotFound(f"Project not found: {project_id}")

        if self._workspaces.get(project.workspace_id) is None:
            raise NotFound(f"Workspace not found: {project.workspace_id}")

        if self._memberships.get(project.workspace_id, actor_id) is None:
            raise PermissionDenied("Workspace membership is required")

        if (
            assignee_id is not None
            and self._memberships.get(project.workspace_id, assignee_id) is None
        ):
            raise PermissionDenied("Assignee must belong to the workspace")

        task = Task(
            id=str(uuid4()),
            project_id=project.id,
            title=normalized_title,
            status="todo",
            assignee_id=assignee_id,
        )
        self._tasks.save(task)

        if assignee_id is not None:
            self._notifications.save(
                Notification(
                    id=str(uuid4()),
                    user_id=assignee_id,
                    kind="task_assigned",
                    task_id=task.id,
                )
            )

        return task
