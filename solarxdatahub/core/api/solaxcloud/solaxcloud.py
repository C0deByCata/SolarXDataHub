"""Module for interacting with the Solax Cloud API."""

from datetime import datetime

import pandas as pd
import requests
from loguru import logger

from solarxdatahub.config import SolaxCloud
from solarxdatahub.database.crud import (
    get_master_tb_inverters,
    insert_battery,
    insert_energy,
    insert_phase_power,
)
from solarxdatahub.models.model_solaxcloud import SolaxCloudResponse, SolaxCloudResult
from solarxdatahub.utils.ntfy import NtfyNotification


class SolaxCloudAPI:
    """Class for interacting with the Solax Cloud API."""

    def __init__(self):
        self.api_url = SolaxCloud.API_URL
        self.token_id = SolaxCloud.TOKEN_ID
        self.wifi_sn = SolaxCloud.WIFI_SN
        self.headers = {"Content-Type": "application/json", "tokenId": self.token_id}
        self.payload = {"wifiSn": self.wifi_sn}
        self.ntfy = NtfyNotification()

    def get_real_time_data(self) -> None:
        """Get the real-time data from the Solax Cloud API."""
        try:
            response = requests.post(
                self.api_url, headers=self.headers, json=self.payload, timeout=10
            )
            response.raise_for_status()
            data = response.json()
            solax_response = SolaxCloudResponse(**data)
            if not solax_response.success or solax_response.result is None:
                logger.error(
                    "API SolaXCloud returned an error: {}", solax_response.exception
                )
                return None
            return solax_response
        except requests.exceptions.Timeout:
            logger.error("The request to the Solax Cloud API timed out.")
            return None
        except requests.exceptions.ConnectionError:
            logger.error(
                "A connection error occurred while accessing the Solax Cloud API."
            )
            return None
        except requests.exceptions.HTTPError as e:
            logger.error("HTTP error occurred: {}", e)
            return None
        except requests.exceptions.RequestException as e:
            logger.error(
                "An unexpected error occurred while accessing the Solax Cloud API: {}",
                e,
            )
            return None

    def process_solaxcloud_response(self, response: SolaxCloudResponse) -> None:
        """
        Process the response from the Solax Cloud API.

        This method divides the information contained in the response into several
        pandas DataFrames, each corresponding to a database table. Later these DataFrames
        can be used to insert data into the database.

        Args:
            response (SolaxCloudResponse): The validated response from the API.
        """
        result: SolaxCloudResult = response.result

        common_columns = self.common_columns(result)
        inverter_df = get_master_tb_inverters()
        if inverter_df.empty:
            logger.error(
                "Inverter ID not found for SN: {}. Response uploadTime: {}",
                result.inverterSN,
                result.uploadTime,
            )
            return
        inverter_id = int(inverter_df.iloc[0]["id"])
        logger.info(
            "Processing data for inverter ID: {} (SN: {}, uploadTime: {})",
            inverter_id,
            result.inverterSN,
            result.uploadTime,
        )
        self.process_tb_energy_data(result, common_columns, inverter_id)
        self.process_tb_phase_power_data(result, common_columns, inverter_id)
        self.process_tb_battery_data(result, common_columns, inverter_id)
        logger.info(
            "Data from SolaxCloud processed successfully for inverter ID: {}",
            inverter_id,
        )
        self.ntfy.check_energy(
            inverter_id,
            feedinpower=result.feedinpower or 0,
        )

    def process_tb_energy_data(
        self, result: SolaxCloudResponse, common_columns: dict, inverter_id: int
    ) -> None:
        """
        Prepare the response from the Solax Cloud API for the tb_energy_data table.

        Args:
            result (SolaxCloudResponse): The validated response from the API.
            common_columns (dict): Common columns for the DataFrames.
            inverter_id (int): The inverter ID.
        """
        df_energy = pd.DataFrame(
            [
                {
                    "fecha": common_columns["fecha"],
                    "periodo": common_columns["periodo"],
                    "min": common_columns["minute"],
                    "inverter_id": inverter_id,
                    "acpower": result.acpower,
                    "yieldtoday": result.yieldtoday,
                    "yieldtotal": result.yieldtotal,
                    "feedinpower": result.feedinpower,
                    "feedinenergy": result.feedinenergy,
                    "consumeenergy": result.consumeenergy,
                    "uploadTime": result.uploadTime,
                }
            ]
        )
        insert_energy(df_energy)
        logger.info(
            "Energy data inserted into tb_energy_data for inverter ID: {} with uploadTime: {}",
            inverter_id,
            result.uploadTime,
        )

    def process_tb_phase_power_data(
        self, result: SolaxCloudResponse, common_columns: dict, inverter_id: int
    ) -> None:
        """Prepare the response from the Solax Cloud API for the tb_phase_power_data table.

        Args:
            result (SolaxCloudResponse): The validated response from the API.
            common_columns (dict): Common columns for the DataFrames.
            inverter_id (int): The inverter ID.
        """
        df_phase_power = pd.DataFrame(
            [
                {
                    "fecha": common_columns["fecha"],
                    "periodo": common_columns["periodo"],
                    "min": common_columns["minute"],
                    "inverter_id": inverter_id,
                    "peps1": result.peps1,
                    "peps2": result.peps2,
                    "peps3": result.peps3,
                    "powerdc1": result.powerdc1,
                    "powerdc2": result.powerdc2,
                    "powerdc3": result.powerdc3,
                    "powerdc4": result.powerdc4,
                    "uploadTime": result.uploadTime,
                }
            ]
        )
        insert_phase_power(df_phase_power)
        logger.info(
            "Phase data inserted into tb_phase_power_data for inverter ID: {} with uploadTime: {}",
            inverter_id,
            result.uploadTime,
        )

    def process_tb_battery_data(
        self, result: SolaxCloudResponse, common_columns: dict, inverter_id: int
    ) -> None:
        """Prepare the response from the Solax Cloud API for the tb_battery_data table.

        Args:
            result (SolaxCloudResponse): The validated response from the API.
            common_columns (dict): Common columns for the DataFrames.
            inverter_id (int): The inverter ID.
        """
        df_battery = pd.DataFrame(
            [
                {
                    "fecha": common_columns["fecha"],
                    "periodo": common_columns["periodo"],
                    "min": common_columns["minute"],
                    "inverter_id": inverter_id,
                    "batPower": result.batPower,
                    "soc": result.soc,
                    "batStatus": result.batStatus,
                    "uploadTime": result.uploadTime,
                }
            ]
        )
        insert_battery(df_battery)
        logger.info(
            "Battery data inserted into tb_battery_data for inverter ID: {} with uploadTime: {}",
            inverter_id,
            result.uploadTime,
        )

    def common_columns(self, result: SolaxCloudResponse) -> dict:
        """Return the common columns for the DataFrames.

        Args:
            result (SolaxCloudResponse): The validated response from the API.

        Returns:
            dict: A dictionary with the common columns for the DataFrames.

        Note:
            'uploadTime': '2025-02-15 19:38:40' format
        """
        try:
            upload_time = result.uploadTime
            datetime.strptime(upload_time, "%Y-%m-%d %H:%M:%S")
            fecha = upload_time.split(" ")[0]
            hora = upload_time.split(" ")[1]
            periodo = hora.split(":")[0]
            minute = hora.split(":")[1]
            return {
                "fecha": fecha,
                "periodo": periodo,
                "minute": minute,
            }
        except ValueError as e:
            logger.error("Invalid uploadTime format: {}", e)
            return {}
        except AttributeError as e:
            logger.error("Missing or invalid attribute in SolaxCloudResponse: {}", e)
            return {}
