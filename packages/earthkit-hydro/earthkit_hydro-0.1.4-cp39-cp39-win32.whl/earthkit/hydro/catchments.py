# (C) Copyright 2025- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

from functools import partial

import numpy as np

from .core import flow
from .metrics import metrics_dict
from .upstream import calculate_upstream_metric
from .utils import (
    is_missing,
    mask_2d,
    mask_and_unmask,
    points_to_1d_indices,
    points_to_numpy,
)


@mask_2d
def calculate_catchment_metric(
    river_network,
    field,
    points,
    metric,
    weights=None,
    mv=np.nan,
    accept_missing=False,
):
    """
    Calculates the metric over the catchments defined by the points.

    Parameters
    ----------
    river_network : earthkit.hydro.RiverNetwork
        An earthkit-hydro river network object.
    field : numpy.ndarray
        The input field.
    points : list of tuples
        List of tuple indices of the points.
    metric : str
        Metric to compute. Options are "mean", "max", "min", "sum", "prod",
        "std", "var".
    weights : ndarray, optional
        Used to weight the field when computing the metric. Default is None.
    mv : scalar, optional
        Missing value for the input field. Default is np.nan.
    accept_missing : bool, optional
        Whether or not to accept missing values in the input field. Default is False.

    Returns
    -------
    dict
        Dictionary with (station, catchment_metric) pairs.

    """
    # TODO: Future idea could be to find all
    # nodes relevant for computing upstream
    # average, then creating a river subnetwork
    # and calculating upstream metric only there
    # (should be quicker, particularly for
    # small numbers of points)

    if isinstance(points, np.ndarray):
        upstream_metric_field = calculate_upstream_metric(
            river_network,
            field,
            metric,
            weights,
            mv,
            accept_missing,
            skip=True,
        )
        upstream_field_at_stations = upstream_metric_field[..., points]
        upstream_field_at_stations = np.moveaxis(upstream_field_at_stations, -1, 0)

        return dict(zip(points, upstream_field_at_stations))

    points = points_to_numpy(points)

    stations_1d = points_to_1d_indices(river_network, points)

    upstream_metric_field = calculate_upstream_metric(
        river_network,
        field,
        metric,
        weights,
        mv,
        accept_missing,
        skip=True,
    )

    metric_at_stations = upstream_metric_field[..., stations_1d]

    return {(x, y): metric_at_stations[..., i] for i, (x, y) in enumerate(zip(*points))}


@mask_and_unmask
def find(river_network, field, mv=0, in_place=False):
    """Labels the catchments given a field of labelled sinks.

    Parameters
    ----------
    river_network : earthkit.hydro.RiverNetwork
        An earthkit-hydro river network object.
    field : numpy.ndarray
        The input field.
    mv : scalar, optional
        The missing value indicator. Default is 0.
    in_place : bool, optional
        If True, modifies the input field in place. Default is False.

    Returns
    -------
    numpy.ndarray
        The field values accumulated downstream.

    """
    if not in_place:
        field = field.copy()

    if len(field.shape) == 1:
        op = _find_catchments_2D
    else:
        op = _find_catchments_ND

    def operation(river_network, field, grouping, mv):
        return op(river_network, field, grouping, mv, overwrite=True)

    return flow(river_network, field, True, operation, mv)


for metric in metrics_dict.keys():

    func = partial(calculate_catchment_metric, metric=metric)

    globals()[metric] = func


def _find_catchments_2D(river_network, field, grouping, mv, overwrite):
    """Updates field in-place with the value of its downstream nodes, dealing
    with missing values for 2D fields.

    Parameters
    ----------
    river_network : earthkit.hydro.RiverNetwork
        An earthkit-hydro river network object.
    field : numpy.ndarray
        The input field.
    grouping : numpy.ndarray
        The array of node indices.
    mv : scalar
        The missing value indicator.
    overwrite : bool
        If True, overwrite existing non-missing values in the field array.

    Returns
    -------
    None

    """
    valid_group = grouping[
        ~is_missing(field[..., river_network.downstream_nodes[grouping]], mv)
    ]  # only update nodes where the downstream belongs to a catchment
    if not overwrite:
        valid_group = valid_group[is_missing(field[..., valid_group], mv)]
    field[..., valid_group] = field[..., river_network.downstream_nodes[valid_group]]


def _find_catchments_ND(river_network, field, grouping, mv, overwrite):
    """Updates field in-place with the value of its downstream nodes, dealing
    with missing values for ND fields.

    Parameters
    ----------
    river_network : earthkit.hydro.RiverNetwork
        An earthkit-hydro river network object.
    field : numpy.ndarray
        The input field.
    grouping : numpy.ndarray
        The array of node indices.
    mv : scalar
        The missing value indicator.
    overwrite : bool
        If True, overwrite existing non-missing values in the field array.

    Returns
    -------
    None

    """
    field = field.T
    valid_mask = ~is_missing(field[river_network.downstream_nodes[grouping]], mv)
    valid_indices = np.array(np.where(valid_mask))
    valid_indices[0] = grouping[valid_indices[0]]
    if not overwrite:
        temp_valid_indices = valid_indices[0]
        valid_mask = is_missing(field[tuple(valid_indices)], mv)
        valid_indices = np.array(np.where(valid_mask))
        valid_indices[0] = temp_valid_indices[valid_indices[0]]
    downstream_valid_indices = valid_indices.copy()
    downstream_valid_indices[0] = river_network.downstream_nodes[
        downstream_valid_indices[0]
    ]
    field[tuple(valid_indices)] = field[tuple(downstream_valid_indices)]
    return field.T
