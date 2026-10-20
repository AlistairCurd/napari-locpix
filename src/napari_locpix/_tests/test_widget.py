import os

import napari
import polars as pl
import pyarrow.parquet as pq
import pytest
from polars.testing import assert_frame_equal
from unittest.mock import MagicMock, patch
from qtpy.QtWidgets import QWidget

from napari_locpix._widget import open_datastruc_widget, DatastrucWidget

# add label adds widget

# render button

# render button annotate


# test load raw
@pytest.mark.gui
def test_load_raw_parquet(make_napari_viewer):

    # test file path
    test_file_path = "src/napari_locpix/_tests/raw_test.parquet"

    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    # create our widget, passing in the viewer
    widget = DatastrucWidget(viewer)

    # call widget method
    widget._load_raw_data(test_file_path)


@pytest.mark.gui
def test_load_raw_csv(make_napari_viewer):

    # test file path
    test_file_path = "src/napari_locpix/_tests/raw_test.csv"

    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    # create our widget, passing in the viewer
    widget = DatastrucWidget(viewer)

    # call widget method
    widget._load_raw_data(test_file_path)

    label_layout = widget.label_widget.layout()
    assert label_layout.itemAtPosition(0, 0).widget().text() == "0"
    assert label_layout.itemAtPosition(1, 0).widget().text() == "1"
    assert label_layout.itemAtPosition(0, 1).widget().text() == "background"
    assert label_layout.itemAtPosition(1, 1).widget().text() == "foreground"


# test load annotate


@pytest.mark.gui
def test_load_annot_parquet(make_napari_viewer):

    # test file path
    test_file_path = "src/napari_locpix/_tests/annot_test.parquet"

    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    # create our widget, passing in the viewer
    widget = DatastrucWidget(viewer)

    # call widget method
    widget._load_annot_data(test_file_path)


@pytest.mark.gui
def test_label_map_widget_loads_parquet_map_and_resets_for_raw_data(
    make_napari_viewer,
):
    widget = DatastrucWidget(make_napari_viewer())
    label_layout = widget.label_widget.layout()
    assert label_layout.itemAtPosition(0, 0).widget().text() == "0"
    assert label_layout.itemAtPosition(1, 0).widget().text() == "1"
    assert label_layout.itemAtPosition(0, 1).widget().text() == "background"
    assert label_layout.itemAtPosition(1, 1).widget().text() == "foreground"

    widget._load_annot_data("src/napari_locpix/_tests/annot_test.parquet")
    label_layout = widget.label_widget.layout()
    assert label_layout.itemAtPosition(0, 1).widget().text() == "background"
    assert label_layout.itemAtPosition(1, 1).widget().text() == "membrane"

    widget._load_raw_data("src/napari_locpix/_tests/raw_test.csv")
    label_layout = widget.label_widget.layout()
    assert label_layout.itemAtPosition(0, 1).widget().text() == "background"
    assert label_layout.itemAtPosition(1, 1).widget().text() == "foreground"


@pytest.mark.gui
def test_write_parquet_saves_label_map_without_labels_layer(
    make_napari_viewer, tmp_path
):
    widget = DatastrucWidget(make_napari_viewer())
    test_file_path = "src/napari_locpix/_tests/raw_test.csv"

    widget._load_raw_data(test_file_path)
    widget._render_button(test_file_path, file_type="csv")
    assert "Labels" not in widget.viewer.layers

    label_layout = widget.label_widget.layout()
    label_layout.itemAtPosition(0, 1).widget().setText("background")
    label_layout.itemAtPosition(1, 1).widget().setText("foreground")

    output_path = tmp_path / "label_map.parquet"
    widget._write_parquet(str(output_path))

    metadata = pq.read_schema(output_path).metadata
    assert metadata[b"gt_label_map"] == (
        b'{"0": "background", "1": "foreground"}'
    )


# def test_load_annot_csv(make_napari_viewer):
#
#    # test file path
#    test_file_path = "src/napari_locpix/_tests/test.csv"
#
#    # make viewer and add an image layer using our fixture
#    viewer = make_napari_viewer()
#
#    # create our widget, passing in the viewer
#    widget = DatastrucWidget(viewer)
#
#    # call widget method
#    widget._load_annot_data(test_file_path)


@pytest.fixture
def setup_test_write_parquet(make_napari_viewer):

    # test file path
    in_test_file_path = "src/napari_locpix/_tests/annot_test.parquet"
    out_test_file_path = "src/napari_locpix/_tests/out_annot_test.parquet"

    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    # create our widget, passing in the viewer
    widget = DatastrucWidget(viewer)

    # call widget method
    widget._load_annot_data(in_test_file_path)

    # render first
    widget._render_button_annot()

    # test write
    widget._write_parquet(out_test_file_path)

    # check two files same
    in_table = pq.read_table(in_test_file_path)
    out_table = pq.read_table(out_test_file_path)

    in_table_schema = in_table.schema
    out_table_schema = out_table.schema

    yield in_table_schema, out_table_schema, in_table, out_table,
    os.remove(out_test_file_path)


@pytest.mark.gui
def test_write_parquet(setup_test_write_parquet):

    (
        in_table_schema,
        out_table_schema,
        in_table,
        out_table,
    ) = setup_test_write_parquet

    assert in_table_schema == out_table_schema

    in_table = pl.from_arrow(in_table)
    out_table = pl.from_arrow(out_table)

    assert_frame_equal(in_table, out_table, check_row_order=False)


@pytest.fixture
def setup_test_write_csv(make_napari_viewer):
    # test file path
    in_test_file_path = "src/napari_locpix/_tests/annot_test.csv"
    out_test_file_path = "src/napari_locpix/_tests/out_raw_test.csv"

    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    # create our widget, passing in the viewer
    widget = DatastrucWidget(viewer)

    # call widget method
    widget._load_annot_data(in_test_file_path)

    # have to render for following to work
    widget._render_button(in_test_file_path, file_type="csv")

    # test write
    widget._write_csv(out_test_file_path)

    # check two files same
    in_table = pl.read_csv(in_test_file_path)
    out_table = pl.read_csv(out_test_file_path)

    yield in_table, out_table
    os.remove(out_test_file_path)


@pytest.mark.gui
@pytest.mark.skip(reason="Loading CSVs with annotation not implemented yet")
def test_write_csv(setup_test_write_csv):

    in_table, out_table = setup_test_write_csv

    assert assert_frame_equal(in_table, out_table)


@pytest.mark.gui
def test_add_labels(make_napari_viewer):

    # test file path
    test_file_path = "src/napari_locpix/_tests/annot_test.parquet"

    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    # create our widget, passing in the viewer
    widget = DatastrucWidget(viewer)

    # call widget method
    widget._load_annot_data(test_file_path)

    # have to render first
    widget._render_button_annot()

    # test add labels button
    widget._wrap_labels()

    # test add label
    widget._add_label()


@pytest.mark.gui
def test_render_button_parquet(make_napari_viewer):

    # test file path
    test_file_path = "src/napari_locpix/_tests/raw_test.parquet"

    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    # create our widget, passing in the viewer
    widget = DatastrucWidget(viewer)

    # load data
    widget._load_raw_data(test_file_path)

    # render
    widget._render_button(test_file_path, file_type="parquet")


@pytest.mark.gui
def test_render_button_csv(make_napari_viewer):

    # test file path
    test_file_path = "src/napari_locpix/_tests/raw_test.csv"

    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    # create our widget, passing in the viewer
    widget = DatastrucWidget(viewer)

    # load data
    widget._load_raw_data(test_file_path)

    # render
    widget._render_button(test_file_path, file_type="csv")


@pytest.mark.gui
def test_render_button_annot_parquet(make_napari_viewer):

    # test file path
    test_file_path = "src/napari_locpix/_tests/annot_test.parquet"

    # make viewer and add an image layer using our fixture
    viewer = make_napari_viewer()

    # create our widget, passing in the viewer
    widget = DatastrucWidget(viewer)

    # load data
    widget._load_annot_data(test_file_path)

    # render
    widget._render_button_annot()


def test_open_datastruc_widget_adds_dock_widget():
    mock_viewer = MagicMock()
    mock_window = MagicMock()
    mock_viewer.window = mock_window

    with patch("napari.current_viewer", return_value=mock_viewer):
        returned = open_datastruc_widget()

    # Return value
    assert isinstance(returned, QWidget)

    # Verify dock widget was added correctly
    mock_window.add_dock_widget.assert_called_once()
    args, kwargs = mock_window.add_dock_widget.call_args

    assert isinstance(args[0], DatastrucWidget)

    # Check name
    assert kwargs["name"] == "Annotate"


def test_open_datastruc_widget_no_viewer(monkeypatch):
    monkeypatch.setattr(napari, "current_viewer", lambda: None)

    with pytest.raises(RuntimeError, match="No active napari viewer"):
        open_datastruc_widget()


# make_napari_viewer is a pytest fixture that returns a napari viewer object
# capsys is a pytest fixture that captures stdout and stderr output streams
# def test_write_parquet(make_napari_viewer, capsys):
#
#
#
#    # make viewer and add an image layer using our fixture
#    viewer = make_napari_viewer()
#
#    # create our widget, passing in the viewer
#    widget = DatastrucWidget(viewer)
#
#    # call widget method
#    widget._write_parquet()
#
#    assert 1 == 2
#
#    #viewer.add_image(np.random.random((100, 100)))
#
#    # create our widget, passing in the viewer
#    #my_widget = ExampleQWidget(viewer)
#
#    # call our widget method
#    #my_widget._on_click()
#
#    # read captured output and check that it's as we expected
#    #captured = capsys.readouterr()
#    #assert captured.out == "napari has 1 layers\n"
