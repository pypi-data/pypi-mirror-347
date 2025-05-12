from abc import ABC
import dataclasses
from tabulate import tabulate
from typing import Union
import numpy as np


@dataclasses.dataclass
class TableConfig(ABC):
    """
    Configuration class for dataset feature types and missing value handling.

    This class defines the feature types (numerical and categorical),
    strategy for handling missing values, the target variable (optional),
    and a parameter for quantile-based filtering.

    Parameters
    ----------
    categorical : List[str]
        List of categorical feature names.
    numerical : List[str]
        List of numerical feature names.
    nan_strategy : str, optional
        Strategy for handling missing values. Must be either 'fill' or 'remove'. Default is 'fill'.
    target : str, optional
        Target column name if available. Default is 'NOT DEFINED'.
    quantiles_cut : bool or float, optional
        Quantile threshold for filtering data when needed. If float, must be between 0 and 1. Default is False.

    Raises
    ------
    TypeError
        If `nan_strategy` is not 'fill' or 'remove'.
    TypeError
        If `quantiles_cut` is not of type bool or float, or if float not in [0, 1].

    Examples
    --------
    >>> config = TableConfig(
    ...     categorical=["gender", "city"],
    ...     numerical=["age", "income"],
    ...     nan_strategy="fill",
    ...     target="purchase",
    ...     quantiles_cut=0.99
    ... )
    >>> print(config)
    """
    categorical: list[str]
    numerical: list[str]
    datetime: list[str]
    nan_strategy: str = "fill"
    wrong_datatypes: str = "fix"
    target: Union[str] = "NOT DEFINED"
    quantiles_cut: bool | float = False

    if nan_strategy not in ["fill", "remove"]:
        raise TypeError(f"'nan_strategy' could be 'fill' or 'remove' only")

    if not isinstance(quantiles_cut, (bool, float)):
        raise TypeError("`quantiles_cut` should be bool or float type only")
    else:
        if isinstance(quantiles_cut, float):
            if quantiles_cut > 1.0 or quantiles_cut < 0:
                raise TypeError("`quantiles_cut` should be a in range [0;1]")

    def __repr__(self) -> str:
        """
        Return a human-readable summary of the TableConfig instance.

        Returns
        -------
        str
            A formatted table containing configuration data.

        Example
        -------
        >>> print(drifter)
        ╒══════════════════════╤════════════════════════════════════════════════╕
        │ Parameter            │ Value                                          │
        ╞══════════════════════╪════════════════════════════════════════════════╡
        │ Target               │ NOT DEFINED                                    │
        ├──────────────────────┼────────────────────────────────────────────────┤
        │ Categorical Features │ WWW_REG_SHOP, SOURCE_REG                       │
        ├──────────────────────┼────────────────────────────────────────────────┤
        │ Numerical Features   │ ACTIVE_DAYS, TOTAL_SALE, WIN_COUNT, SALE_COUNT │
        ├──────────────────────┼────────────────────────────────────────────────┤
        │ Datetime Features    │ WWW_REG_START_DATE                             │
        ├──────────────────────┼────────────────────────────────────────────────┤
        │ NaN strategy         │ fill                                           │
        ├──────────────────────┼────────────────────────────────────────────────┤
        │ quantiles_cut        │ 0.99                                           │
        ╘══════════════════════╧════════════════════════════════════════════════╛
        """
        data = [
            ["Target", self.target],
            [
                "Categorical Features",
                ", ".join(self.categorical) if self.categorical else "None",
            ],
            [
                "Numerical Features",
                ", ".join(self.numerical) if self.numerical else "None",
            ],
            [
                "Datetime Features",
                ", ".join(self.datetime) if self.datetime else "None",
            ],
            ["NaN strategy", self.nan_strategy],
            ["Wrong datatypes strategy", self.wrong_datatypes],
            ["Quantiles cut", self.quantiles_cut],
        ]
        return tabulate(data, headers=["Parameter", "Value"], tablefmt="fancy_grid")


class GlobalConfig():
    bootstrap_size = 50_000
