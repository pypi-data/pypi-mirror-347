from typing import List, Dict
import asyncio
from functools import reduce

from fakts_next.utils import update_nested
from fakts_next.protocols import FaktValue, FaktsGrant
from pydantic import BaseModel, ConfigDict


class ParallelGrant(BaseModel):
    """A grant that loads multiple grants in parallel and merges the results


    Attributes
    ----------
    grants : List[FaktsGrant]
        The grants to load in parallel

    omit_exceptions : bool
        Omit exceptions if any of the grants fail to load (otherwise will raise an exception)

    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    grants: List[FaktsGrant]
    " The grants to load in parallel "
    omit_exceptions: bool = False
    " Omit exceptions if any of the grants fail to load "

    async def aload(self) -> Dict[str, FaktValue]:
        """Loads the configuration from the grants in parallel

        This method will load the configuration from the grants in parallel, and merge the results, updating
        the configuration with the results from each grant.

        Parameters
        ----------
        request : FaktsRequest
            The request object that may contain additional information needed for loading the configuration.

        Returns
        -------
        dict
            The configuration loaded from the grant.


        """
        config_futures = [grant.aload() for grant in self.grants]
        configs = await asyncio.gather(
            *config_futures, return_exceptions=self.omit_exceptions
        )
        # TODO: Check if this is the correct way to merge the configs
        return reduce(lambda x, y: update_nested(x, y), configs, {})  # type: ignore
