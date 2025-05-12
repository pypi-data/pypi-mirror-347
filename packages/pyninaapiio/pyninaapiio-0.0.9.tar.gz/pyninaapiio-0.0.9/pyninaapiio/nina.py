import base64
import logging
import sys
import traceback
from pprint import pprint as pp

from httpx import ConnectTimeout

from advanced_api_client.api.application import get_version
from advanced_api_client.api.camera import get_equipment_camera_info
from advanced_api_client.api.filter_wheel import get_equipment_filterwheel_info
from advanced_api_client.api.focuser import get_equipment_focuser_info
from advanced_api_client.api.guider import get_equipment_guider_info
from advanced_api_client.api.image import get_image_history, get_image_index
from advanced_api_client.api.mount import get_equipment_mount_info, get_equipment_mount_list_devices
from advanced_api_client.api.switch import get_equipment_switch_info
from advanced_api_client.client import Client
from pyninaapiio.dataclasses import (
    ApplicationData,
    ApplicationDataModel,
    CameraData,
    CameraDataModel,
    FilterWheelData,
    FilterWheelDataModel,
    FocuserData,
    FocuserDataModel,
    GuiderData,
    GuiderDataModel,
    ImageData,
    ImageDataModel,
    MountData,
    MountDataModel,
    NinaDevicesData,
    NinaDevicesDataModel,
    SwitchData,
    SwitchDataModel,
)
from advanced_api_client.models.camera_info import CameraInfo
from advanced_api_client.models.device_list import DeviceList
from advanced_api_client.models.focuser_info import FocuserInfo
from advanced_api_client.models.fw_info import FWInfo
from advanced_api_client.models.get_image_history_response_200 import GetImageHistoryResponse200
from advanced_api_client.models.get_image_index_response_200 import GetImageIndexResponse200
from advanced_api_client.models.get_version_response_200 import GetVersionResponse200
from advanced_api_client.models.guider_info import GuiderInfo
from advanced_api_client.models.mount_info import MountInfo
from advanced_api_client.models.switch_info import SwitchInfo
from advanced_api_client.types import Response
from typeguard import TypeCheckError

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(
    stream=sys.stdout,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s (%(threadName)s) [%(funcName)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

API_TIMEOUT = 3


# async with client as client:
class NinaAPI:
    def __init__(
        self,
        # session: Optional[ClientSession] = None,
        session=None,
        base_url="http://192.168.1.234:1888/v2/api",
        application_enabled=False,
        camera_enabled=False,
        filterwheel_enabled=False,
        focuser_enabled=False,
        guider_enabled=False,
        image_enabled=False,
        mount_enabled=False,
        switch_enabled=False,
    ):
        self._session = session
        self._client = Client(base_url=base_url, timeout=API_TIMEOUT, verify_ssl=False)
        self._application_enabled = application_enabled
        self._camera_enabled = camera_enabled
        self._filterwheel_enabled = filterwheel_enabled
        self._focuser_enabled = focuser_enabled
        self._guider_enabled = guider_enabled
        self._image_enabled = image_enabled
        self._mount_enabled = mount_enabled
        self._switch_enabled = switch_enabled

        # Save last capture
        self._image_index_latest = -1
        self._image_data = b""

        return None

    # #########################################################################
    # Application
    # #########################################################################
    async def application_info(self):
        try:
            _LOGGER.info(f"Retrieve application info")
            _application_info: Response[GetVersionResponse200] = await get_version.asyncio(client=self._client)
            _application_info_data = ApplicationDataModel({"Version": _application_info.response, "Connected": True})

            return ApplicationData(data=_application_info_data)

        except ConnectTimeout as ct:
            _LOGGER.info(f"Nina not available.")
            return ApplicationData(data={"Connected": False})
        except KeyError as ke:
            _LOGGER.info(f"Application not connected.")
            return ApplicationData(data={"Connected": False})

    # #########################################################################
    # Camera
    # #########################################################################
    async def camera_info(self):
        try:
            _LOGGER.info(f"Retrieve camera info")
            _camera_info: Response[CameraInfo] = await get_equipment_camera_info.asyncio(client=self._client)
            _camera_info_data = CameraDataModel(_camera_info.response.to_dict())

            return CameraData(data=_camera_info_data)

        except ConnectTimeout as ct:
            _LOGGER.info(f"Nina not available.")
            return None
        except KeyError as ke:
            _LOGGER.info(f"Camera not connected.")
            return CameraData(data={"Connected": False})

    # #########################################################################
    # FilterWheel
    # #########################################################################
    async def filterwheel_info(self):
        try:
            _LOGGER.info(f"Retrieve filterwheel info")
            _filterwheel_info: Response[FWInfo] = await get_equipment_filterwheel_info.asyncio(client=self._client)
            _filterwheel_info_data = FilterWheelDataModel(_filterwheel_info.response.to_dict())

            return FilterWheelData(data=_filterwheel_info_data)

        except ConnectTimeout as ct:
            _LOGGER.info(f"Nina not available.")
            return None
        except KeyError as ke:
            _LOGGER.info(f"FilterWheel not connected.")
            return FilterWheelData(data={"Connected": False})

    # #########################################################################
    # Focuser
    # #########################################################################
    async def focuser_info(self):
        try:
            _LOGGER.info(f"Retrieve focuser info")
            _focuser_info: Response[FocuserInfo] = await get_equipment_focuser_info.asyncio_detailed(
                client=self._client
            )
            pp(_focuser_info)
            _focuser_info_data = FocuserDataModel(_focuser_info.response.to_dict())

            return FocuserData(data=_focuser_info_data)

        except ConnectTimeout as ct:
            _LOGGER.info(f"Nina not available.")
            return None
        except KeyError as ke:
            _LOGGER.info(f"Focuser not connected.")
            return FocuserData(data={"Connected": False})

    # #########################################################################
    # Guider
    # #########################################################################
    async def guider_info(self):
        try:
            _LOGGER.info(f"Retrieve info")
            _guider_info: Response[GuiderInfo] = await get_equipment_guider_info.asyncio(client=self._client)
            _guider_info_data = GuiderDataModel(_guider_info.response.to_dict())

            return GuiderData(data=_guider_info_data)

        except ConnectTimeout as ct:
            _LOGGER.info(f"Nina not available.")
            return None
        except KeyError as ke:
            _LOGGER.info(f"Guider not connected.")
            return GuiderData(data={"Connected": False})

    # #########################################################################
    # Image
    # #########################################################################
    async def image_latest(self):
        _LOGGER.info(f"Retrieve index of last capture")
        image_history: GetImageHistoryResponse200 = await get_image_history.asyncio(client=self._client, count=True)
        image_index_latest = image_history.response - 1

        if image_index_latest > self._image_index_latest:
            self._image_index_latest = image_index_latest

            _LOGGER.info(f"Retrieve capture with index {image_index_latest}")
            image: GetImageIndexResponse200 = await get_image_index.asyncio(
                index=image_index_latest, client=self._client
            )  # , debayer=True, bayer_pattern=GetImageIndexBayerPattern.RGGB)
            if image.success:
                image_data = base64.b64decode(image.response)
                self._image_data = image_data
            else:
                _LOGGER.error(f"{image.error}")
        else:
            _LOGGER.info(f"Returning previous capture with index {self._image_index_latest}")

        _LOGGER.info(f"Capture Index: {self._image_index_latest}")
        _camera_data = ImageDataModel(
            {
                "Connected": True,
                "DecodedData": self._image_data,
                "DecodedDataLength": len(self._image_data),
                "IndexLatest": self._image_index_latest,
            }
        )
        return ImageData(data=_camera_data)

    # #########################################################################
    # Mount
    # #########################################################################
    # async def mount_list_devices(self):
    #     items = []

    #     try:
    #         _list_devices: Response[DeviceList] = await get_equipment_mount_list_devices.asyncio(client=self._client)

    #         for _, device in enumerate(_list_devices.response):
    #             item = DeviceMountDataModel(device.to_dict())

    #             try:
    #                 items.append(DeviceMountData(data=item))
    #             except TypeError as ve:
    #                 _LOGGER.error(f"Failed to parse device data model data: {item}")
    #                 _LOGGER.error(ve)
    #     except KeyError as ke:
    #         _LOGGER.error(f"KeyError:")

    #     return items

    async def mount_info(self):
        try:
            _LOGGER.info(f"Retrieve info")
            _mount_info: Response[MountInfo] = await get_equipment_mount_info.asyncio(client=self._client)
            _mount_info_data = MountDataModel(_mount_info.response.to_dict())

            return MountData(data=_mount_info_data)

        except ConnectTimeout as ct:
            _LOGGER.info(f"Nina not available.")
            return None
        except KeyError as ke:
            _LOGGER.info(f"Mount not connected.")
            return MountData(data={"Connected": False})

    # #########################################################################
    # Switch
    # #########################################################################
    async def switch_info(self):
        try:
            _LOGGER.info(f"Retrieve info")
            _switch_info: Response[SwitchInfo] = await get_equipment_switch_info.asyncio(client=self._client)
            _switch_info_data = SwitchDataModel(_switch_info.response.to_dict())

            return SwitchData(data=_switch_info_data)

        except ConnectTimeout as ct:
            _LOGGER.info(f"Nina not available.")
            return None
        except KeyError as ke:
            _LOGGER.info(f"Switch not connected.")
            return SwitchData(data={"Connected": False})

    # #########################################################################
    # Nina
    # #########################################################################
    async def nina_info(
        self,
    ):
        # try:
        #     _LOGGER.info(f"Retrieve N.I.N.A. info")
        #     application_data: ApplicationData = await self.application_info()

        #     if application_data.connected is False:
        #         _LOGGER.info(f"Nina not available.")
        #         return NinaDevicesData(data={"Connected": False})
        # except ConnectTimeout as ct:
        #     _LOGGER.info(f"Nina not available.")
        #     return NinaDevicesData(data={"Connected": False})
        # except KeyError as ke:
        #     # traceback.print_exc()
        #     _LOGGER.info(f"Nina not connected.")
        #     return NinaDevicesData(data={"Connected": False})

        _LOGGER.info(f"Connecting to N.I.N.A.")
        application_data: ApplicationData = await self.application_info()

        if application_data.connected is False:
            _LOGGER.info(f"Nina not available.")
            return NinaDevicesData(data={"Connected": False})

        try:
            _LOGGER.info(f"Retrieve N.I.N.A. info")
            _nina = {
                "Application": await self.application_info() if self._application_enabled else None,
                "Camera": await self.camera_info() if self._camera_enabled else None,
                "FilterWheel": await self.filterwheel_info() if self._filterwheel_enabled else None,
                "Focuser": await self.focuser_info() if self._focuser_enabled else None,
                "Guider": await self.guider_info() if self._guider_enabled else None,
                "Image": await self.image_latest() if self._image_enabled else None,
                "Mount": await self.mount_info() if self._mount_enabled else None,
                "Switch": await self.switch_info() if self._switch_enabled else None,
            }
            _nina_info_data = NinaDevicesDataModel(_nina)

            return NinaDevicesData(data=_nina_info_data)

        except ConnectTimeout as ct:
            _LOGGER.info(f"Nina not available.")
            return NinaDevicesData(data={"Connected": False})
        except KeyError as ke:
            # traceback.print_exc()
            _LOGGER.info(f"Nina not connected.")
            return NinaDevicesData(data={"Connected": False})
