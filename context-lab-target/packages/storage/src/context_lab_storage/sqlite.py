import sqlite3

from context_lab_core.models import (
    Membership,
    Notification,
    Project,
    Task,
    Workspace,
)


class SQLiteWorkspaceStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def get(self, workspace_id: str) -> Workspace | None:
        row = self._connection.execute(
            "SELECT id, name FROM workspaces WHERE id = ?",
            (workspace_id,),
        ).fetchone()
        return None if row is None else Workspace(id=row["id"], name=row["name"])

    def save(self, workspace: Workspace) -> None:
        self._connection.execute(
            """
            INSERT INTO workspaces (id, name) VALUES (?, ?)
            ON CONFLICT(id) DO UPDATE SET name = excluded.name
            """,
            (workspace.id, workspace.name),
        )
        self._connection.commit()


class SQLiteMembershipStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def get(self, workspace_id: str, user_id: str) -> Membership | None:
        row = self._connection.execute(
            """
            SELECT workspace_id, user_id, role
            FROM memberships
            WHERE workspace_id = ? AND user_id = ?
            """,
            (workspace_id, user_id),
        ).fetchone()
        return (
            None
            if row is None
            else Membership(
                workspace_id=row["workspace_id"],
                user_id=row["user_id"],
                role=row["role"],
            )
        )

    def save(self, membership: Membership) -> None:
        self._connection.execute(
            """
            INSERT INTO memberships (workspace_id, user_id, role)
            VALUES (?, ?, ?)
            ON CONFLICT(workspace_id, user_id)
            DO UPDATE SET role = excluded.role
            """,
            (membership.workspace_id, membership.user_id, membership.role),
        )
        self._connection.commit()


class SQLiteProjectStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def get(self, project_id: str) -> Project | None:
        row = self._connection.execute(
            "SELECT id, workspace_id, name FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        return (
            None
            if row is None
            else Project(
                id=row["id"],
                workspace_id=row["workspace_id"],
                name=row["name"],
            )
        )

    def save(self, project: Project) -> None:
        self._connection.execute(
            """
            INSERT INTO projects (id, workspace_id, name) VALUES (?, ?, ?)
            ON CONFLICT(id)
            DO UPDATE SET workspace_id = excluded.workspace_id,
                          name = excluded.name
            """,
            (project.id, project.workspace_id, project.name),
        )
        self._connection.commit()


class SQLiteTaskStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def get(self, task_id: str) -> Task | None:
        row = self._connection.execute(
            """
            SELECT id, project_id, title, status, assignee_id
            FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        ).fetchone()
        return (
            None
            if row is None
            else Task(
                id=row["id"],
                project_id=row["project_id"],
                title=row["title"],
                status=row["status"],
                assignee_id=row["assignee_id"],
            )
        )

    def save(self, task: Task) -> None:
        self._connection.execute(
            """
            INSERT INTO tasks (id, project_id, title, status, assignee_id)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id)
            DO UPDATE SET project_id = excluded.project_id,
                          title = excluded.title,
                          status = excluded.status,
                          assignee_id = excluded.assignee_id
            """,
            (task.id, task.project_id, task.title, task.status, task.assignee_id),
        )
        self._connection.commit()


class SQLiteNotificationStore:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def save(self, notification: Notification) -> None:
        self._connection.execute(
            """
            INSERT INTO notifications (id, user_id, kind, task_id, delivered)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(id)
            DO UPDATE SET user_id = excluded.user_id,
                          kind = excluded.kind,
                          task_id = excluded.task_id,
                          delivered = excluded.delivered
            """,
            (
                notification.id,
                notification.user_id,
                notification.kind,
                notification.task_id,
                int(notification.delivered),
            ),
        )
        self._connection.commit()

    def pending(self) -> list[Notification]:
        rows = self._connection.execute(
            """
            SELECT id, user_id, kind, task_id, delivered
            FROM notifications
            WHERE delivered = 0
            ORDER BY rowid
            """
        ).fetchall()
        return [self._to_model(row) for row in rows]

    def mark_delivered(self, notification_id: str) -> None:
        self._connection.execute(
            "UPDATE notifications SET delivered = 1 WHERE id = ?",
            (notification_id,),
        )
        self._connection.commit()

    @staticmethod
    def _to_model(row: sqlite3.Row) -> Notification:
        return Notification(
            id=row["id"],
            user_id=row["user_id"],
            kind=row["kind"],
            task_id=row["task_id"],
            delivered=bool(row["delivered"]),
        )


class SQLiteStores:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection
        self._connection.row_factory = sqlite3.Row
        self._initialize_schema()
        self.workspaces = SQLiteWorkspaceStore(connection)
        self.memberships = SQLiteMembershipStore(connection)
        self.projects = SQLiteProjectStore(connection)
        self.tasks = SQLiteTaskStore(connection)
        self.notifications = SQLiteNotificationStore(connection)

    @classmethod
    def in_memory(cls) -> "SQLiteStores":
        return cls(sqlite3.connect(":memory:"))

    def close(self) -> None:
        self._connection.close()

    def _initialize_schema(self) -> None:
        self._connection.executescript(
            """
            PRAGMA foreign_keys = ON;

            CREATE TABLE IF NOT EXISTS workspaces (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS memberships (
                workspace_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                role TEXT NOT NULL,
                PRIMARY KEY (workspace_id, user_id),
                FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
            );

            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                workspace_id TEXT NOT NULL,
                name TEXT NOT NULL,
                FOREIGN KEY (workspace_id) REFERENCES workspaces(id)
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                project_id TEXT NOT NULL,
                title TEXT NOT NULL,
                status TEXT NOT NULL,
                assignee_id TEXT,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            );

            CREATE TABLE IF NOT EXISTS notifications (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                kind TEXT NOT NULL,
                task_id TEXT NOT NULL,
                delivered INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            );
            """
        )
        self._connection.commit()
