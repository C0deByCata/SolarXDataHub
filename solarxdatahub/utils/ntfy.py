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
        # 1) Leer el último log (cualquiera)
        df_last_all = get_last_notification_timestamp(
            inverter_id, notification_type=None
        )
        if not df_last_all.empty:
            last_type = df_last_all.iloc[0]["notification_type"]
            if last_type == notif_type:
                # Mismo estado que antes, no notificamos
                return False

        # 2) Ahora comprobar el margen de tiempo para este tipo
        df_last_same = get_last_notification_timestamp(
            inverter_id, notification_type=notif_type
        )
        if df_last_same.empty:
            return True  # nunca se envió este tipo
        last_time = pd.to_datetime(df_last_same.iloc[0]["sent_at"])
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

    def check_energy(self, inverter_id: int, feedinpower: float) -> None:
        """Evaluates energy flow and sends a notification based on thresholds.

        Args:
            inverter_id (int): The ID of the inverter.
            feedinpower (float): The power fed into the grid.
        """
        logger.info("Checking energy for inverter_id: {}", inverter_id)
        # load_power = acpower - feedinpower  # consumo instantáneo en W
        # surplus_power = acpower - load_power  # W disponibles sobre el margen

        if feedinpower > self.excess_margin:
            notif_type = "energy_available"
            title = "Energia disponible"
            message = (
                f"Tienes {feedinpower:.0f} W de excedente (umbral {self.excess_margin:.0f} W). "
                "Puedes encender aparatos para aprovechar tu propia energía."
            )
            logger.info(message)
        elif feedinpower < -self.excess_margin:
            notif_type = "high_consumption"
            title = "Consumo elevado"
            message = (
                f"Estás consumiendo {abs(feedinpower):.0f} W por encima de tu producción "
                f"(umbral {self.excess_margin:.0f} W). Apaga aparatos para ahorrar."
            )
            logger.info(message)
        else:
            return  # Ni excedente ni consumo suficientemente grande

        if self._should_notify(inverter_id, notif_type):
            self.send_ntfy_notification(title, message)
            self._log_notification(inverter_id, notif_type)
