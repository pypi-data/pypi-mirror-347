from importlib import metadata as _md
from matplotlib.colors import LinearSegmentedColormap as _lsc

__name__ = "paulaner_colormaps"
__version__ = _md.version("paulaner_colormaps")

spezi = _lsc.from_list(
    "spezi",
    [
        "#4b1e7d",
        "#e30083",
        "#e6001c",
        "#ec6400",
        "#f9b700",
    ],
)

orange = _lsc.from_list(
    "orange",
    [
        "#eb0029",
        "#ff4713",
        "#ff6c0d",
        "#ff9e19",
        "#ffc600",
    ],
)

zitrone = _lsc.from_list(
    "zitrone",
    [
        "#00a441",
        "#6fb634",
        "#b1bf14",
        "#d4c31e",
        "#fcc600",
    ],
)

__all__ = [
    orange,
    spezi,
    zitrone,
]
