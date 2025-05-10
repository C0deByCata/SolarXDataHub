"""Module for CRUD operations on the database."""

from typing import Optional

import pandas as pd

from solarxdatahub.config import Database
from solarxdatahub.database.connection import DataBaseConnection
from solarxdatahub.database.reading import (
    read_last_notification_timestamp,
    read_master_tb_device_status_mapping,
    read_master_tb_error_codes,
    read_master_tb_inverters,
    read_master_tb_request_options,
    read_openweather_last_request,
    read_weatherbit_last_request,
    read_weatherbit_requests_log,
)
from solarxdatahub.database.writting import (
    insert_openweather_air_pollution,
    insert_openweather_current,
    insert_openweather_requests_log,
    insert_tb_battery_data,
    insert_tb_energy_data,
    insert_tb_notification_log,
    insert_tb_phase_power_data,
    insert_weatherbit_current,
    insert_weatherbit_requests_log,
)


def get_master_tb_device_status_mapping():
    """Get the master_tb_device_status_mapping table."""
    return DataBaseConnection.read(
        host_name=Database.TARGET_HOST.name,
        query=read_master_tb_device_status_mapping,
        as_df=True,
    )


def get_master_tb_error_codes():
    """Get the master_tb_error_codes table."""
    return DataBaseConnection.read(
        host_name=Database.TARGET_HOST.name,
        query=read_master_tb_error_codes,
        as_df=True,
    )


def get_master_tb_inverters(inverter_sn: Optional[str] = None):
    """Get the master_tb_inverters table."""
    return DataBaseConnection.read(
        host_name=Database.TARGET_HOST.name,
        query=read_master_tb_inverters,
        params={"inverter_sn": inverter_sn},
        as_df=True,
    )


def get_weatherbit_requests_log():
    """Get the weatherbit_requests_log table."""
    return DataBaseConnection.read(
        host_name=Database.TARGET_HOST.name,
        query=read_weatherbit_requests_log,
        as_df=True,
    )


def get_openweather_requests_log():
    """Get the weatherbit_requests_log table."""
    return DataBaseConnection.read(
        host_name=Database.TARGET_HOST.name,
        query=read_weatherbit_requests_log,
        as_df=True,
    )


def get_master_tb_request_options():
    """Get the master_tb_request_options table."""
    return DataBaseConnection.read(
        host_name=Database.TARGET_HOST.name,
        query=read_master_tb_request_options,
        as_df=True,
    )


def insert_energy(df_energy: pd.DataFrame):
    """Insert data into the tb_energy_data table."""
    return DataBaseConnection.write(
        host_name=Database.TARGET_HOST.name,
        query=insert_tb_energy_data,
        data=df_energy,
        commit=True,
    )


def insert_phase_power(df_phase_power: pd.DataFrame):
    """Insert data into the tb_phase_power_data table."""
    return DataBaseConnection.write(
        host_name=Database.TARGET_HOST.name,
        query=insert_tb_phase_power_data,
        data=df_phase_power,
        commit=True,
    )


def insert_battery(df_battery: pd.DataFrame):
    """Insert data into the tb_battery_data table."""
    return DataBaseConnection.write(
        host_name=Database.TARGET_HOST.name,
        query=insert_tb_battery_data,
        data=df_battery,
        commit=True,
    )


def insert_weatherbit_requests_log_(df_weatherbit_requests_log: pd.DataFrame):
    """Insert data into the weatherbit_requests_log table."""
    return DataBaseConnection.write(
        host_name=Database.TARGET_HOST.name,
        query=insert_weatherbit_requests_log,
        data=df_weatherbit_requests_log,
        commit=True,
    )


def insert_weatherbit_current_(df_weatherbit_current: pd.DataFrame):
    """Insert data into the weatherbit_current table."""
    return DataBaseConnection.write(
        host_name=Database.TARGET_HOST.name,
        query=insert_weatherbit_current,
        data=df_weatherbit_current,
        commit=True,
    )


def insert_openweather_requests_log_(df_openweather_requests_log: pd.DataFrame):
    """Insert data into the openweather_requests_log table."""
    return DataBaseConnection.write(
        host_name=Database.TARGET_HOST.name,
        query=insert_openweather_requests_log,
        data=df_openweather_requests_log,
        commit=True,
    )


def insert_openweather_current_(df_openweather_current: pd.DataFrame):
    """Insert data into the openweather_current table."""
    return DataBaseConnection.write(
        host_name=Database.TARGET_HOST.name,
        query=insert_openweather_current,
        data=df_openweather_current,
        commit=True,
    )


def insert_openweather_air_pollution_(df_openweather_air_pollution: pd.DataFrame):
    """Insert data into the openweather_air_pollution table."""
    return DataBaseConnection.write(
        host_name=Database.TARGET_HOST.name,
        query=insert_openweather_air_pollution,
        data=df_openweather_air_pollution,
        commit=True,
    )


def get_last_notification_timestamp(inverter_id: int, notif_type: str) -> pd.DataFrame:
    """
    Devuelve el timestamp de la última notificación enviada para un inversor y tipo.
    """
    return DataBaseConnection.read(
        host_name=Database.TARGET_HOST.name,
        query=read_last_notification_timestamp,
        params={"inverter_id": inverter_id, "notification_type": notif_type},
        as_df=True,
    )


def insert_notification_log(df: pd.DataFrame):
    """
    Escribe un registro de notificación en la base de datos.
    """
    return DataBaseConnection.write(
        host_name=Database.TARGET_HOST.name,
        query=insert_tb_notification_log,
        data=df,
        commit=True,
    )


def get_weatherbit_last_request() -> pd.DataFrame:
    """Fetch the last request made to the Weatherbit API."""
    return DataBaseConnection.read(
        host_name=Database.TARGET_HOST.name,
        query=read_weatherbit_last_request,
        as_df=True,
    )


def get_openweather_last_request() -> pd.DataFrame:
    """Fetch the last request made to the OpenWeather API."""
    return DataBaseConnection.read(
        host_name=Database.TARGET_HOST.name,
        query=read_openweather_last_request,
        as_df=True,
    )
