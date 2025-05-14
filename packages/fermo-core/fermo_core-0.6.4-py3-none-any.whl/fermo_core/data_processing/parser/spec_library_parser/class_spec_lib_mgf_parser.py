"""Parses a spectral library file in mgf format.

Copyright (c) 2022 to present Mitja Maximilian Zdouc, PhD

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import logging
from pathlib import Path
from typing import Self

import matchms
from pydantic import BaseModel

from fermo_core.data_processing.class_stats import Stats
from fermo_core.input_output.class_parameter_manager import ParameterManager

logger = logging.getLogger("fermo_core")


class SpecLibMgfParser(BaseModel):
    """Interface to parse a spectral library file in mgf format.

    Attributes:
        params: a ParameterManager instance managing the input parameters
        stats: a Stats object instance to store spectral library in
    """

    params: ParameterManager
    stats: Stats

    def return_stats(self: Self) -> Stats:
        """Returns modified stats objects

        Returns:
            The modified stats objects
        """
        return self.stats

    def modify_stats(self: Self, f: Path):
        """Adds spectral library entries to Stats object."""
        mgf_gen = matchms.importing.load_from_mgf(str(f))

        if not self.stats.spectral_library:
            self.stats.spectral_library = []

        for spectrum in mgf_gen:
            try:
                if len(spectrum.peaks.mz) == 0:
                    logger.warning(
                        f"SpecLibMgfParser: spectrum {spectrum.metadata.get('compound_name')} has no ions - SKIP"
                    )
                elif all(x <= 0 for x in spectrum.peaks.intensities):
                    logger.warning(
                        f"SpecLibMgfParser: all fragment ions of spectrum {spectrum.metadata.get('compound_name')} are <= 0 - SKIP"
                    )
                elif not spectrum.metadata.get("precursor_mz"):
                    logger.warning(
                        f"SpecLibMgfParser: spectrum {spectrum.metadata.get('compound_name')} has no pepmass/precursor m/z - SKIP"
                    )
                elif (
                    spectrum.metadata.get("precursor_mz") == 0.0
                    or spectrum.metadata.get("precursor_mz") == 1.0
                ):
                    logger.warning(
                        f"SpecLibMgfParser: pepmass/precursor m/z of spectrum {spectrum.metadata.get('compound_name')} are <= 1 - SKIP"
                    )
                else:
                    self.stats.spectral_library.append(
                        matchms.filtering.add_precursor_mz(
                            matchms.filtering.normalize_intensities(spectrum)
                        )
                    )
            except Exception as e:
                logger.warning(f"SpecLibMgfParser: {e}")

    def parse(self: Self):
        """Parses a spectral library file in mgf format.

        Returns:
            A (modified) Stats object
        """
        logger.info(
            f"'SpecLibMgfParser': started parsing of spectral library files "
            f"'{self.params.SpecLibParameters.dirpath.name}'"
        )

        for f in self.params.SpecLibParameters.dirpath.iterdir():
            if f.suffix == ".mgf":
                self.modify_stats(f)

        logger.info(
            f"'SpecLibMgfParser': completed parsing of spectral library files "
            f"'{self.params.SpecLibParameters.dirpath.name}'"
        )
