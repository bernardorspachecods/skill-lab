import unittest

from context_lab_core.errors import PermissionDenied
from context_lab_core.models import Membership, Project, Workspace
from context_lab_core.services import TaskService
from context_lab_storage.memory import InMemoryStores


class TaskServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.stores = InMemoryStores()
        self.stores.workspaces.save(Workspace(id="ws-1", name="Acme"))
        self.stores.memberships.save(
            Membership(workspace_id="ws-1", user_id="user-1", role="member")
        )
        self.stores.memberships.save(
            Membership(workspace_id="ws-1", user_id="user-2", role="member")
        )
        self.stores.projects.save(
            Project(id="project-1", workspace_id="ws-1", name="Launch")
        )
        self.service = TaskService(
            workspaces=self.stores.workspaces,
            memberships=self.stores.memberships,
            projects=self.stores.projects,
            tasks=self.stores.tasks,
            notifications=self.stores.notifications,
        )

    def test_member_can_create_task_in_workspace_project(self) -> None:
        task = self.service.create_task(
            actor_id="user-1",
            project_id="project-1",
            title="Prepare release notes",
        )

        self.assertEqual(task.title, "Prepare release notes")
        self.assertEqual(task.status, "todo")
        self.assertEqual(self.stores.tasks.get(task.id), task)

    def test_non_member_cannot_create_task(self) -> None:
        with self.assertRaises(PermissionDenied):
            self.service.create_task(
                actor_id="outsider",
                project_id="project-1",
                title="Attempted access",
            )

    def test_assigned_task_creates_notification_for_member(self) -> None:
        task = self.service.create_task(
            actor_id="user-1",
            project_id="project-1",
            title="Review implementation",
            assignee_id="user-2",
        )

        self.assertEqual(len(self.stores.notifications.items), 1)
        self.assertEqual(self.stores.notifications.items[0].user_id, "user-2")
        self.assertEqual(self.stores.notifications.items[0].task_id, task.id)

    def test_task_cannot_be_assigned_to_non_member(self) -> None:
        with self.assertRaises(PermissionDenied):
            self.service.create_task(
                actor_id="user-1",
                project_id="project-1",
                title="Review implementation",
                assignee_id="outsider",
            )


if __name__ == "__main__":
    unittest.main()
