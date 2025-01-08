import asyncio
import random
import string
from typing import Any, Awaitable, Protocol

from .message import Message, MessageType


def generate_id(length: int = 8) -> str:
    """Generate random device ID using uppercase ASCII letters."""
    return "".join(random.choices(string.ascii_uppercase, k=length))


class Device(Protocol):
    """Protocol defining required methods for IoT devices."""

    async def connect(self) -> None:
        ...

    async def disconnect(self) -> None:
        ...

    async def send_message(self, message_type: MessageType, data: str) -> None:
        ...


async def run_sequence(*functions: Awaitable[Any]) -> None:
    """Execute given async functions in sequence."""
    for function in functions:
        await function


async def run_parallel(*functions: Awaitable[Any]) -> list[Any]:
    """Execute given async functions in parallel."""
    return await asyncio.gather(*functions)


class IOTService:
    """Service for managing IoT devices and message handling."""

    def __init__(self) -> None:
        self.devices: dict[str, Device] = {}

    async def register_device(self, device: Device) -> str:
        """Connect and register new device, return device ID."""
        await device.connect()
        device_id = generate_id()
        self.devices[device_id] = device
        return device_id

    async def unregister_device(self, device_id: str) -> None:
        """Disconnect and remove device from service."""
        await self.devices[device_id].disconnect()
        del self.devices[device_id]

    def get_device(self, device_id: str) -> Device:
        """Retrieve device instance by ID."""
        return self.devices[device_id]

    async def run_program(self, program: list[Message]) -> None:
        """Execute sequence of IoT device messages."""
        print("=====RUNNING PROGRAM======")
        for msg in program:
            await self.send_msg(msg)
        print("=====END OF PROGRAM======")

    async def send_msg(self, msg: Message) -> None:
        """Send message to specified device."""
        await self.devices[msg.device_id].send_message(msg.msg_type, msg.data)
