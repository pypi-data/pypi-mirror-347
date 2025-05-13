from pydantic import ConfigDict, Field
from fakts_next.grants.errors import GrantError
import yaml
from koil.qt import QtCoro, QtFuture
from qtpy import QtWidgets
from fakts_next.protocols import FaktValue
from typing import Dict, Protocol, runtime_checkable, Optional, Type
from pydantic import BaseModel


class NoFileSelected(GrantError):
    """Raised when no file was selected."""

    pass


class QtSelectYaml(QtWidgets.QFileDialog):  # type: ignore
    """
    Represents a File Dialog that selects YAML files.

    Methods
    -------
    ask(parent=None)
        Opens the file dialog and returns the selected file path.
    """

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        """A File Dialog that selects YAML files."""
        super().__init__(*args, **kwargs)  # type: ignore
        self.setFileMode(QtWidgets.QFileDialog.ExistingFile)  # type: ignore
        self.setNameFilter("YAML files (*.yaml)")  # type: ignore

    @classmethod
    def ask(
        cls: Type["QtSelectYaml"], parent: Optional[QtWidgets.QWidget] = None
    ) -> str:
        """
        Opens the file dialog and returns the selected file path.

        Parameters
        ----------
        parent : QWidget, optional
            The parent widget of the file dialog.

        Returns
        -------
        str
            The file path of the selected file.
        """
        filepath, weird = cls.getOpenFileName(parent=parent, caption="Select a Yaml")  # type: ignore
        return filepath if weird else ""  # type: ignore


class WrappingWidget(QtWidgets.QWidget):  # type: ignore
    """
    A Widget that wraps the file selection process.

    Attributes
    ----------
    get_file_coro : QtCoro
        The coroutine that opens the file dialog and returns the selected file path
        (a call to `get_file_coro.acall()` will return a future that resolves to the selected file path
        or rejects with a `NoFileSelected` error).

    Methods
    -------
    open_file(future: QtFuture)
        Opens the file dialog and resolves or rejects the future based on the selected file path.
    """

    def __init__(self, *args, **kwargs) -> None:  # type: ignore
        """A Widget that wraps the file selection process."""
        super().__init__(*args, **kwargs)  # type: ignore
        self.get_file_coro = QtCoro(self.open_file)  # type: ignore

    def open_file(self, future: QtFuture[str]) -> None:  # type: ignore
        """
        Opens the file dialog and resolves or rejects the future based on the selected file path.

        Parameters
        ----------
        future : QtFuture
            The future that will be resolved or rejected based on the selected file path.
        """
        filepath = QtSelectYaml.ask(parent=self)  # type: ignore

        if filepath:
            future.resolve(filepath)
        else:
            future.reject(NoFileSelected("No file selected"))

    async def aask(self) -> str:
        """
        Opens the file dialog and returns the selected file path.

        Returns
        -------
        str
            The file path of the selected file.
        """
        return await self.get_file_coro.acall()  # type: ignore


@runtime_checkable
class FileWidget(Protocol):
    """A Protocol that represents a widget

    that wraps the file selection process.
    It can be used to create a custom widget that wraps the file selection process.

    """

    async def aask(self) -> str:
        """Opens the file dialog and returns the selected file path.

        Parameters
        ----------
        parent : QWidget, optional
            The parent widget of the file dialog.

        Returns
        -------
        str
            The file path of the selected file.
        """
        ...


class QtYamlGrant(BaseModel):
    """
    Represent a Grant that allows the user to select a YAML file.

    Attributes
    ----------
    widget : WrappingWidget
        The widget that wraps the file selection process.

    Methods
    -------
    aload(request: FaktsRequest)
        Asynchronously loads the YAML file and returns the configuration.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    widget: FileWidget = Field(exclude=True)

    async def aload(self) -> Dict[str, FaktValue]:
        """Loads the YAML file and returns the configuration.

        Parameters
        ----------
        request : FaktsRequest
            The request object that may contain additional information needed for loading the YAML file.

        Returns
        -------
        dict
            The configuration loaded from the YAML file.
        """
        filepath = await self.widget.aask()
        with open(filepath, "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)  # type: ignore #TODO: Check why this is not working

        return config
