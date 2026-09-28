from dataclasses import dataclass
from typing import Literal


TaskStatus = Literal["todo", "in_progress", "done", "archived"]
MembershipRole = Literal["owner", "member"]


@dataclass(frozen=True)
class Workspace:
    id: str
    name: str


@dataclass(frozen=True)
class Membership:
    workspace_id: str
    user_id: str
    role: MembershipRole


@dataclass(frozen=True)
class Project:
    id: str
    workspace_id: str
    name: str


@dataclass(frozen=True)
class Task:
    id: str
    project_id: str
    title: str
    status: TaskStatus
    assignee_id: str | None = None


@dataclass(frozen=True)
class Notification:
    id: str
    user_id: str
    kind: str
    task_id: str
    delivered: bool = False
