""" "Queries for reading data from the database."""


def read_master_tb_device_status_mapping() -> str:
    """Read the master_tb_device_status_mapping table."""
    return """SELECT code, status, description
            FROM master_tb_device_status_mapping;"""


def read_master_tb_inverters(inverter_sn: str = None) -> str:
    """Read the master_tb_inverters table."""
    if inverter_sn:
        return f"""SELECT id FROM master_tb_inverters WHERE inverterSN = '{inverter_sn}';"""
    else:
        return """SELECT id, inverterSN, sn, inverterType, site_name, description
                FROM master_tb_inverters;"""


def read_master_tb_error_codes() -> str:
    """Read the master_tb_error_codes table."""
    return """SELECT code, message
            FROM master_tb_error_codes;"""


def read_weatherbit_hourly_data() -> str:
    """Fetch the most recent calculation datetime from weatherbit hourly data."""
    return """SELECT MAX(calculation_datetime) AS last_dt
                FROM weatherbit.tb_hourly_data
                WHERE DATE(calculation_datetime) = CURDATE();"""


def read_weatherbit_requests_log() -> str:
    """Fetch the total requests made to the Weatherbit API today."""

    return """SELECT COUNT(*) AS total_requests
            FROM weatherbit.tb_requests_log
            WHERE DATE(request_datetime) = CURDATE();"""


def read_openweather_requests_log() -> str:
    """Fetch the total requests made to the OpenWeather API today."""

    return """SELECT COUNT(*) AS total_requests
            FROM openweather.tb_requests_log
            WHERE DATE(request_datetime) = CURDATE();"""


def read_master_tb_request_options() -> str:
    """Read the master_tb_request_options table."""
    return """SELECT id, request_type
            FROM openweather.master_tb_request_options;"""


def read_last_notification_timestamp(
    inverter_id: int, notification_type: str = None
) -> str:
    """
    Devuelve el timestamp de la última notificación enviada para un inversor y tipo.
    """
    var = f"""SELECT sent_at FROM solaxcloud.tb_notification_log
            WHERE inverter_id = {inverter_id} AND notification_type = '{notification_type}';"""
    return var


def read_weatherbit_last_request() -> str:
    """Fetch the last request made to the Weatherbit API."""
    return """SELECT MAX(request_datetime) AS last_request
            FROM weatherbit.tb_requests_log;"""


def read_openweather_last_request() -> str:
    """Fetch the last request made to the OpenWeather API."""
    return """SELECT MAX(request_datetime) AS last_request
            FROM openweather.tb_requests_log;"""
