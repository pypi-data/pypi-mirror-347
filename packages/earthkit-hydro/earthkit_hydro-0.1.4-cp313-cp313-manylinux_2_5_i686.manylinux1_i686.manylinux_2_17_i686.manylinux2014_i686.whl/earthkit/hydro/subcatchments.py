# (C) Copyright 2025- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

from functools import partial

import numpy as np

from .catchments import _find_catchments_2D, _find_catchments_ND
from .core import flow
from .metrics import metrics_dict
from .utils import mask_2d, mask_and_unmask, points_to_1d_indices, points_to_numpy
from .zonal import calculate_zonal_metric


@mask_2d
def calculate_subcatchment_metric(
    river_network,
    field,
    points,
    metric,
    weights=None,
    mv=np.nan,
    accept_missing=False,
):
    """
    Calculates the metric over the subcatchments defined by stations.

    Parameters
    ----------
    river_network : earthkit.hydro.RiverNetwork
        An earthkit-hydro river network object.
    field : numpy.ndarray
        The input field.
    stations : list of tuples
        List of tuple indices of the stations.
    metric : str
        Metric to compute. Options are "mean", "max", "min", "sum", "prod",
        "std", "var".
    weights : ndarray
        Used to weight the field when computing the metric. Default is None.
    mv : scalar
        Missing value for the input field. Default is np.nan.
    accept_missing : bool
        Whether or not to accept missing values in the input field. Default is False.

    Returns
    -------
    dict
        Dictionary with (station, catchment_metric) pairs.
    """
    if isinstance(points, np.ndarray):
        initial_field = np.zeros(river_network.n_nodes, dtype=int)
        initial_field[points] = np.arange(points.shape[0]) + 1
        labels = find(river_network, initial_field, skip=True)
        metric_at_stations = calculate_zonal_metric(
            field,
            labels,
            metric,
            weights if weights is not None else None,
            mv,
            0,  # missing labels value
            accept_missing,
        )
        return {x: metric_at_stations[y] for (x, y) in zip(points, labels[points])}

    points = points_to_numpy(points)

    stations_1d = points_to_1d_indices(river_network, points)

    initial_field = np.zeros(river_network.n_nodes, dtype=int)
    unique_labels = np.arange(stations_1d.shape[0]) + 1
    initial_field[stations_1d] = unique_labels
    labels = find(river_network, initial_field, skip=True)
    metric_at_stations = calculate_zonal_metric(
        field,
        labels,
        metric,
        weights if weights is not None else None,
        mv,
        0,  # missing labels value
        accept_missing,
    )
    return {(x, y): metric_at_stations[z] for (x, y, z) in zip(*points, unique_labels)}


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
        return op(river_network, field, grouping, mv, overwrite=False)

    return flow(river_network, field, True, operation, mv)


for metric in metrics_dict.keys():

    func = partial(calculate_subcatchment_metric, metric=metric)

    globals()[metric] = func
