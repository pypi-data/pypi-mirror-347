"""The main process function."""

from multiprocessing import Pool
from typing import Iterator

import pandas as pd

from .feature import Feature
from .mutual_information_process import mutual_information_process
from .pearson_process import pearson_process
from .transforms import TRANSFORMS


def process(
    df: pd.DataFrame,
    predictands: list[str],
    max_window: int,
    max_process_features: int = 10,
) -> Iterator[list[Feature]]:
    """Process the dataframe for tsuniverse features."""
    with Pool() as p:
        for predictand in predictands:
            for transform_name in TRANSFORMS:
                for sub_process in [pearson_process, mutual_information_process]:
                    features = sorted(
                        list(
                            sub_process(df, predictand, max_window, p, transform_name)
                        ),
                        key=lambda x: abs(
                            x["correlation"] if "correlation" in x else 0.0
                        ),
                        reverse=True,
                    )[:max_process_features]
                    yield features
