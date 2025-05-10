"""Module to send notifications to the user by ntfy."""

from datetime import datetime, timedelta

import pandas as pd
import requests
from loguru import logger

from solarxdatahub.config import Ntfy
from solarxdatahub.database.crud import (
    get_last_notification_timestamp,
    insert_notification_log,
)


class NtfyNotification:
    """Class to store the ntfy notification configuration."""

    def __init__(self):
        self.topic = Ntfy.NTFY_TOPIC
        self.server = Ntfy.NTFY_SERVER
        self.user = Ntfy.NTFY_USER
        self.passwd = Ntfy.NTFY_PASS
        self.margin_time = int(Ntfy.NTFY_NOTIFY_REPEAT_MINUTES)
        self.excess_margin = int(Ntfy.NTFY_EXCESS_MARGIN)

    def send_ntfy_notification(self, title, message):
        """
        Envía una notificación a través de ntfy.

        title: Título de la notificación
        message: Mensaje de la notificación
        """
        try:
            response = requests.post(
                f"{self.server}/{self.topic}",
                data=message.encode("utf-8"),
                headers={"Title": title, "Priority": "urgent"},
                auth=(self.user, self.passwd),
                timeout=10,
            )
            response.raise_for_status()
            logger.info("Notificación enviada: {} - {}", title, message)
        except requests.RequestException as e:
            logger.error("Error al enviar la notificación: %s", e)
            raise
        except Exception as e:
            logger.error("Error desconocido al enviar la notificación: %s", e)
            raise

    def _should_notify(self, inverter_id: int, notif_type: str) -> bool:
        """Check if enough time has passed to re-notify."""
        df_last = get_last_notification_timestamp(
            inverter_id=inverter_id, notif_type=notif_type
        )
        if df_last.empty:
            return True
        last_time = pd.to_datetime(df_last.iloc[0]["sent_at"])
        return datetime.now() - last_time >= timedelta(minutes=self.margin_time)

    def _log_notification(self, inverter_id: int, notif_type: str):
        """Insert or update notification log."""
        df = pd.DataFrame(
            [
                {
                    "inverter_id": inverter_id,
                    "notification_type": notif_type,
                    "sent_at": datetime.now(),
                }
            ]
        )
        insert_notification_log(df)

    def check_energy(
        self, inverter_id: int, feedinpower: float, consumeenergy: float
    ) -> None:
        """Evaluates energy flow and sends a notification based on thresholds.

        Args:
            inverter_id (int): The ID of the inverter.
            feedinpower (float): The power fed into the grid.
            consumeenergy (float): The energy consumed by the load.
        """
        logger.info("Checking energy for inverter_id: {}", inverter_id)
        if feedinpower > (consumeenergy + self.excess_margin):
            notif_type = "energy_available"
            if self._should_notify(inverter_id, notif_type):
                self.send_ntfy_notification(
                    "Energia disponible",
                    "Puedes encender aparatos eléctricos para aprovechar tu propia energía.",
                )
                self._log_notification(inverter_id, notif_type)
        else:
            notif_type = "high_consumption"
            if self._should_notify(inverter_id, notif_type):
                self.send_ntfy_notification(
                    "Consumo elevado",
                    "Apaga aparatos porque estás gastando energía de la red.",
                )
                self._log_notification(inverter_id, notif_type)
