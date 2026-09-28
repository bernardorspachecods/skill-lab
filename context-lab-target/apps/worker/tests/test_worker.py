import unittest

from context_lab_core.models import Notification
from context_lab_storage.memory import NotificationMemoryStore
from context_lab_worker.worker import NotificationWorker


class RecordingDelivery:
    def __init__(self) -> None:
        self.notifications: list[Notification] = []

    def send(self, notification: Notification) -> None:
        self.notifications.append(notification)


class FailingDelivery:
    def send(self, notification: Notification) -> None:
        raise RuntimeError(f"delivery failed: {notification.id}")


class NotificationWorkerTests(unittest.TestCase):
    def test_run_once_delivers_pending_notifications_and_marks_them(self) -> None:
        store = NotificationMemoryStore()
        notification = Notification(
            id="notification-1",
            user_id="user-1",
            kind="task_assigned",
            task_id="task-1",
        )
        store.save(notification)
        delivery = RecordingDelivery()
        worker = NotificationWorker(notifications=store, delivery=delivery)

        processed = worker.run_once()

        self.assertEqual(processed, 1)
        self.assertEqual(delivery.notifications, [notification])
        self.assertEqual(store.pending(), [])

    def test_failed_delivery_stays_pending_and_stops_current_cycle(self) -> None:
        store = NotificationMemoryStore()
        notification = Notification(
            id="notification-1",
            user_id="user-1",
            kind="task_assigned",
            task_id="task-1",
        )
        store.save(notification)
        worker = NotificationWorker(
            notifications=store,
            delivery=FailingDelivery(),
        )

        with self.assertRaisesRegex(RuntimeError, "delivery failed"):
            worker.run_once()

        self.assertEqual(store.pending(), [notification])


if __name__ == "__main__":
    unittest.main()
