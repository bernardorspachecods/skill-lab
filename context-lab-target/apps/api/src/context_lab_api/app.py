from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

from context_lab_core.errors import NotFound, PermissionDenied
from context_lab_core.models import Membership, Project, Workspace
from context_lab_core.services import TaskService
from context_lab_storage.memory import InMemoryStores


class CreateTaskRequest(BaseModel):
    title: str
    assignee_id: str | None = None


class TaskResponse(BaseModel):
    id: str
    project_id: str
    title: str
    status: str
    assignee_id: str | None = None


def _default_service() -> TaskService:
    stores = InMemoryStores()
    stores.workspaces.save(Workspace(id="demo-workspace", name="Demo"))
    stores.memberships.save(
        Membership(
            workspace_id="demo-workspace",
            user_id="demo-user",
            role="owner",
        )
    )
    stores.projects.save(
        Project(
            id="demo-project",
            workspace_id="demo-workspace",
            name="Demo project",
        )
    )
    return TaskService(
        workspaces=stores.workspaces,
        memberships=stores.memberships,
        projects=stores.projects,
        tasks=stores.tasks,
        notifications=stores.notifications,
    )


def create_app(*, task_service: TaskService | None = None) -> FastAPI:
    service = task_service or _default_service()
    app = FastAPI(title="Context Lab")

    @app.post(
        "/projects/{project_id}/tasks",
        response_model=TaskResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def create_task(
        project_id: str,
        payload: CreateTaskRequest,
        x_user_id: str | None = Header(default=None),
    ) -> TaskResponse:
        if x_user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="X-User-Id header is required",
            )

        try:
            task = service.create_task(
                actor_id=x_user_id,
                project_id=project_id,
                title=payload.title,
                assignee_id=payload.assignee_id,
            )
        except PermissionDenied as exc:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=str(exc),
            ) from exc
        except NotFound as exc:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(exc),
            ) from exc
        except ValueError as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=str(exc),
            ) from exc

        return TaskResponse(
            id=task.id,
            project_id=task.project_id,
            title=task.title,
            status=task.status,
            assignee_id=task.assignee_id,
        )

    return app


app = create_app()
