import pytest

import polars as pl

from napari_locpix._datastruc import item


def make_minimal_df(x, y, frame, channel, z=None):
    data = {
        "x": x,
        "y": y,
        "frame": frame,
        "channel": channel,
    }
    if z is not None:
        data["z"] = z
    return pl.DataFrame(data)


def test_item_init_raises_if_more_channels_than_labels():
    df = make_minimal_df(
        x=[0.0],
        y=[0.0],
        frame=[0],
        channel=[0],
    )

    with pytest.raises(ValueError, match="more channels than labels"):
        item(
            "test",
            df,
            2,
            channels=[0, 1],
            channel_label=["ch0"],
        )


def test_label_2_chan_returns_index():
    df = make_minimal_df(
        x=[0.0],
        y=[0.0],
        frame=[0],
        channel=[1],
    )

    ds = item(
        "test",
        df,
        2,
        channels=[0, 1, 2],
        channel_label=["ch0", "ch1", "ch2"],
    )

    assert ds.label_2_chan("ch1") == 1


def test_label_2_chan_raises_for_invalid_label():
    df = make_minimal_df(
        x=[0.0],
        y=[0.0],
        frame=[0],
        channel=[0],
    )

    ds = item(
        "test",
        df,
        2,
        channels=[0, 1],
        channel_label=["ch0", "ch1"],
    )

    with pytest.raises(ValueError, match="not present"):
        ds.label_2_chan("ch2")


def test_histogram_uses_3d_branch():
    df = make_minimal_df(
        x=[0.0, 1.0],
        y=[0.0, 1.0],
        z=[0.0, 1.0],
        frame=[0, 1],
        channel=[0, 0],
    )

    ds = item(
        "test",
        df,
        3,
        channels=[0],
        channel_label=["ch0"],
        x_col="x",
        y_col="y",
        z_col="z",
        frame_col="frame",
        chan_col="channel",
    )

    ds.coord_2_histo(histo_size=(10, 10, 10))

    assert ds.dim == 3
