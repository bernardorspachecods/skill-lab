from typing import Protocol

from context_lab_core.models import Notification
from context_lab_core.ports import NotificationStore


class NotificationDelivery(Protocol):
    def send(self, notification: Notification) -> None: ...


class NotificationWorker:
    """Deliver pending notifications and leave failed deliveries retryable."""

    def __init__(
        self,
        *,
        notifications: NotificationStore,
        delivery: NotificationDelivery,
    ) -> None:
        self._notifications = notifications
        self._delivery = delivery

    def run_once(self) -> int:
        pending = self._notifications.pending()
        for notification in pending:
            self._delivery.send(notification)
            self._notifications.mark_delivered(notification.id)
        return len(pending)
