from fastapi.testclient import TestClient

from context_lab_core.models import Membership, Project, Workspace
from context_lab_core.services import TaskService
from context_lab_api.app import create_app
from context_lab_storage.memory import InMemoryStores


def build_client() -> TestClient:
    stores = InMemoryStores()
    stores.workspaces.save(Workspace(id="ws-1", name="Acme"))
    stores.memberships.save(
        Membership(workspace_id="ws-1", user_id="user-1", role="member")
    )
    stores.projects.save(Project(id="project-1", workspace_id="ws-1", name="Launch"))
    service = TaskService(
        workspaces=stores.workspaces,
        memberships=stores.memberships,
        projects=stores.projects,
        tasks=stores.tasks,
        notifications=stores.notifications,
    )
    return TestClient(create_app(task_service=service))


def test_api_creates_task_for_authenticated_workspace_member() -> None:
    client = build_client()

    response = client.post(
        "/projects/project-1/tasks",
        headers={"X-User-Id": "user-1"},
        json={"title": "Prepare release notes"},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Prepare release notes"
    assert response.json()["status"] == "todo"


def test_api_rejects_task_creation_without_membership() -> None:
    client = build_client()

    response = client.post(
        "/projects/project-1/tasks",
        headers={"X-User-Id": "outsider"},
        json={"title": "Attempted access"},
    )

    assert response.status_code == 403


def test_api_passes_assignee_through_creation_and_creates_notification() -> None:
    client = build_client()

    response = client.post(
        "/projects/project-1/tasks",
        headers={"X-User-Id": "user-1"},
        json={"title": "Review implementation", "assignee_id": "user-1"},
    )

    assert response.status_code == 201
    assert response.json()["assignee_id"] == "user-1"
