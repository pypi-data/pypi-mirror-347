"""
Engine interface: how to implement an aggregate computing engine.
"""
from abc import ABC


class NodeContext(ABC):
    """
    Abstract base class for the node context. This class should be implemented by the user.
    """

    def __init__(self, node_id: int, sensors: dict[str, any] = None):
        """
        Initialize the node context with the node id and sensors.
        :param node_id: The id of the node.
        :param sensors: The sensors of the node.
        """
        self.node_id = node_id
        self.sensors = sensors  # map sensor name to sensor value

    def sense(self, sensor_name: str) -> any:
        """
        Get the value of the sensor.
        :param sensor_name: The name of the sensor.
        :return: The value of the sensor.
        """
        return self.sensors.get(sensor_name)

    def position(self) -> any:
        """
        Get the position of the node.
        :return: The position of the node.
        """
        return self.sensors.get("position")


class Engine(ABC):
    """
    Abstract base class for the engine. This class should be implemented by the user.
    """

    def __init__(self):
        self.node_context: NodeContext | None = None

    def setup(
        self, node_context: NodeContext, messages: dict[int, dict[str, any]], state=None
    ) -> None:
        """
        Setup the engine with the current context.
        :param node_context: the current context of the engine.
        :param messages: The messages to send.
        :param state: The state of the engine.
        """

    def enter(self, name: str) -> None:
        """
        Enter a new context.
        :param name: The name of the context.
        """

    def exit(self) -> None:
        """
        Exit the current context.
        """

    def current_path(self) -> list[str]:
        """
        Get the current path of the engine.
        :return: The current path.
        """

    def write_state(self, value: any, stack: list[str]) -> None:
        """
        Write the state of the engine.
        :param value: The value to write.
        :param stack: The stack of the engine.
        """

    def read_state(self, stack: list[str]) -> any:
        """
        Read the state of the engine.
        :param stack: The stack of the engine.
        :return: The value of the state.
        """

    def state_trace(self) -> dict[str, any]:
        """
        Get the state trace of the engine.
        :return: The state trace.
        """

    def forget(self, _self_path):
        """
        Forget the value store in the engine.
        :param _self_path:
        :return:
        """

    def send(self, data: any) -> None:
        """
        Send data to the engine.
        :param data: The data to send.
        """

    def aligned(self) -> list[int]:
        """
        Get the aligned ids.
        :return: The aligned ids.
        """

    def aligned_values(self, path: list[str]) -> dict[int, any]:
        """
        Get the aligned values.
        :param path: The path of the values.
        :return: The aligned values.
        """

    def cooldown(self) -> None:
        """
        Cooldown the engine.
        :return:
        """
