try:
    import tomllib as toml
except ImportError:
    try:
        import toml  # type: ignore
    except ImportError:
        raise ImportError(
            "You need to install the `toml` package to use the toml grant."
            "Or use python 3.11 and higher which comes with the `tomllib` package"
        )


from fakts_next.grants.base import BaseFaktsGrant
from fakts_next.protocols import FaktValue
from typing import Dict


class TomlGrant(BaseFaktsGrant):
    """
    A class used to represent a Grant in a TOML file.

    Attributes
    ----------
    filepath : str
        a formatted string to print out the file path where the TOML file is located

    Methods
    -------
    aload(request: FaktsRequest)
        Asynchronously loads the TOML file and returns the configuration.
    """

    filepath: str

    async def aload(self) -> Dict[str, FaktValue]:
        """Loads the TOML file and returns the configuration.

        Parameters
        ----------
        request : FaktsRequest
            The request object that may contain additional information needed for loading the TOML file.

        Returns
        -------
        dict
            The configuration loaded from the TOML file.
        """
        with open(self.filepath, "r") as file:
            config = toml.load(file)  # type: ignore

        return config
