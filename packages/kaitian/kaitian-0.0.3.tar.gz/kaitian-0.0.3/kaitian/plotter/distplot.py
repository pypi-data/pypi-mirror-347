"""Dist plot."""

from __future__ import annotations

import logging
from typing import Literal

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import polars as pl
from scipy.stats import gaussian_kde

from .theme import Theme


def plot_dist(
    data: pl.DataFrame,
    ax: plt.Axes,
    series: list[str] | None = None,
    theme: Literal["science", "sharp", "nature", "purple"] = "science",
    fontsize: int | None = None,
    title: str | None = None,
    max_features: int = 5,
) -> plt.Axes:
    logger = logging.getLogger(__name__)
    themer = Theme(theme=theme, fontsize=fontsize)
    if series is None:
        series = data.columns

    series_not_null = []
    for s in series:
        if data[s].drop_nans().drop_nulls().len() == 0:
            logger.warning(f"{s} all empty, skip")
        else:
            series_not_null.append(s)

    if len(series_not_null) == 0:
        logger.error("all series is none")
        return ax

    if len(series_not_null) > max_features:
        logger.warning(
            f"too much features to plot {len(series_not_null)} > {max_features}"
        )
        series_not_null = series_not_null[:max_features]

    legend_handles = []
    for s in series_not_null:
        _feature = data[s].drop_nans().drop_nulls().to_numpy()
        _color = themer.get_color()
        kde = gaussian_kde(_feature)
        x_kde = np.linspace(_feature.min(), _feature.max(), 1000)
        y_kde = kde(x_kde)

        ax.plot(x_kde, y_kde, color=_color, alpha=0.5, linewidth=2, label=s)
        legend_handles.append(mpatches.Patch(color=_color, label=s, alpha=0.5))
        ax.fill_between(x_kde, y_kde, color=_color, alpha=0.5 * 0.5)

    if title is None:
        if len(series) == 1:
            title = f"Distribution of {series[0]}"
        else:
            title = "Distribution"

    ax.set_title(title, fontproperties=themer.font)
    ax.set_xlabel("Value", fontproperties=themer.font)
    ax.set_ylabel("Density", fontproperties=themer.font)
    ax.legend(handles=legend_handles)
    return ax
