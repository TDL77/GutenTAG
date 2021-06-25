import argparse
from typing import List, Tuple

from gutenTAG import GutenTAG
from gutenTAG.generator import Overview


class BaseAddOn:
    def process(self, overview: Overview, generators: List[GutenTAG], args: argparse.Namespace) -> Tuple[Overview, List[GutenTAG]]:
        """Gets called before `process_generators`"""
        return overview, generators
