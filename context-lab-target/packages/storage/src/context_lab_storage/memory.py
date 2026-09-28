from dataclasses import dataclass, field

from context_lab_core.models import (
    Membership,
    Notification,
    Project,
    Task,
    Workspace,
)


@dataclass
class WorkspaceMemoryStore:
    items: dict[str, Workspace] = field(default_factory=dict)

    def get(self, workspace_id: str) -> Workspace | None:
        return self.items.get(workspace_id)

    def save(self, workspace: Workspace) -> None:
        self.items[workspace.id] = workspace


@dataclass
class MembershipMemoryStore:
    items: dict[tuple[str, str], Membership] = field(default_factory=dict)

    def get(self, workspace_id: str, user_id: str) -> Membership | None:
        return self.items.get((workspace_id, user_id))

    def save(self, membership: Membership) -> None:
        self.items[(membership.workspace_id, membership.user_id)] = membership


@dataclass
class ProjectMemoryStore:
    items: dict[str, Project] = field(default_factory=dict)

    def get(self, project_id: str) -> Project | None:
        return self.items.get(project_id)

    def save(self, project: Project) -> None:
        self.items[project.id] = project


@dataclass
class TaskMemoryStore:
    items: dict[str, Task] = field(default_factory=dict)

    def get(self, task_id: str) -> Task | None:
        return self.items.get(task_id)

    def save(self, task: Task) -> None:
        self.items[task.id] = task


@dataclass
class NotificationMemoryStore:
    items: list[Notification] = field(default_factory=list)

    def save(self, notification: Notification) -> None:
        self.items.append(notification)

    def pending(self) -> list[Notification]:
        return [notification for notification in self.items if not notification.delivered]

    def mark_delivered(self, notification_id: str) -> None:
        self.items = [
            Notification(
                id=notification.id,
                user_id=notification.user_id,
                kind=notification.kind,
                task_id=notification.task_id,
                delivered=True,
            )
            if notification.id == notification_id
            else notification
            for notification in self.items
        ]


@dataclass
class InMemoryStores:
    workspaces: WorkspaceMemoryStore = field(default_factory=WorkspaceMemoryStore)
    memberships: MembershipMemoryStore = field(default_factory=MembershipMemoryStore)
    projects: ProjectMemoryStore = field(default_factory=ProjectMemoryStore)
    tasks: TaskMemoryStore = field(default_factory=TaskMemoryStore)
    notifications: NotificationMemoryStore = field(
        default_factory=NotificationMemoryStore
    )
