# (C) Copyright 2025- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

import numpy as np

from .accumulation import flow_downstream, flow_upstream
from .utils import mask_2d, points_to_1d_indices, points_to_numpy


@mask_2d
def min(
    river_network, points, weights=None, upstream=False, downstream=True, mv=np.nan
):
    """
    Calculate the minimum distance to a set of points in a river network.
    The distance is calculated along the river network, and can be
    computed in both/either upstream and downstream directions.

    Parameters
    ----------
    river_network : earthkit.hydro.RiverNetwork
        An earthkit-hydro river network object.
    points : list of tuples
        List of tuple indices of the points.
    weights : numpy.ndarray, optional
        Distance to the downstream point. Default is None, which
        corresponds to a unit distance for all points.
    upstream : bool, optional
        If True, calculates the distance in the upstream direction.
        Default is False.
    downstream : bool, optional
        If True, calculate the distance in the downstream direction.
        Default is True.
    mv : scalar, optional
        The missing value indicator. Default is np.nan.

    Returns
    -------
    numpy.ndarray
        The distance to the points in the river network.
    """

    if weights is None:
        weights = np.ones(river_network.n_nodes)
    else:
        # maybe check sinks are all zero or nan distance
        pass
    field = np.empty(river_network.n_nodes)
    field.fill(np.inf)

    if isinstance(points, np.ndarray):
        points_1d = points
    else:
        points = points_to_numpy(points)
        points_1d = points_to_1d_indices(river_network, points)

    field[points_1d] = 0
    if downstream:
        field = flow_downstream(
            river_network,
            field,
            mv,
            ufunc=np.minimum,
            additive_weight=weights,
            modifier_use_upstream=True,
        )
    if upstream:
        field = flow_upstream(
            river_network,
            field,
            mv,
            ufunc=np.minimum,
            additive_weight=weights,
            modifier_use_upstream=True,
        )

    out_field = np.empty(river_network.shape, dtype=field.dtype)
    out_field[..., river_network.mask] = field
    out_field[..., ~river_network.mask] = mv

    return out_field


@mask_2d
def max(
    river_network, points, weights=None, upstream=False, downstream=True, mv=np.nan
):
    """
    Calculate the maximum distance to a set of points in a river network.
    The distance is calculated along the river network, and can be
    computed in both/either upstream and downstream directions.

    Parameters
    ----------
    river_network : earthkit.hydro.RiverNetwork
        An earthkit-hydro river network object.
    points : list of tuples
        List of tuple indices of the points.
    weights : numpy.ndarray, optional
        Distance to the downstream point. Default is None, which
        corresponds to a unit distance for all points.
    upstream : bool, optional
        If True, calculates the distance in the upstream direction.
        Default is False.
    downstream : bool, optional
        If True, calculate the distance in the downstream direction.
        Default is True.
    mv : scalar, optional
        The missing value indicator. Default is np.nan.

    Returns
    -------
    numpy.ndarray
        The distance to the points in the river network.
    """

    if upstream and downstream:
        # TODO: define how this should work
        # can one overwrite a starting station's distance?
        #
        # NB: there is no nice way to do this as downstream
        # and then upstream like for min
        # because we would need to know the paths
        # to avoid looping over each other
        # Only way I think can think is doing each station
        # separately, but this will be very slow...
        raise NotImplementedError(
            "Max distance both upstream and downstream is not yet implemented."
        )

    weights = np.ones(river_network.n_nodes) if weights is None else weights

    field = np.empty(river_network.n_nodes)
    field.fill(-np.inf)

    if isinstance(points, np.ndarray):
        points_1d = points
    else:
        points = points_to_numpy(points)
        points_1d = points_to_1d_indices(river_network, points)

    field[points_1d] = 0

    if downstream:
        field = flow_downstream(
            river_network,
            field,
            mv,
            ufunc=np.maximum,
            additive_weight=weights,
            modifier_use_upstream=True,
        )
    if upstream:
        field = flow_upstream(
            river_network,
            field,
            mv,
            ufunc=np.maximum,
            additive_weight=weights,
            modifier_use_upstream=True,
        )

    field = np.nan_to_num(field, neginf=np.inf)

    out_field = np.empty(river_network.shape, dtype=field.dtype)
    out_field[..., river_network.mask] = field
    out_field[..., ~river_network.mask] = mv

    return out_field


def to_sink(river_network, weights=None, path="shortest", mv=np.nan):
    """
    Calculate the minimum or maximum distance to the sinks of a river network.
    The distance is calculated along the river network.

    Parameters
    ----------
    river_network : earthkit.hydro.RiverNetwork
        An earthkit-hydro river network object.
    weights : numpy.ndarray, optional
        Distance to the downstream point. Default is None, which
        corresponds to a unit distance for all points.
    path : str, optional
        Whether to find the distance of the shortest or longest path.
        Default is 'shortest'.
    mv : scalar, optional
        The missing value indicator. Default is np.nan.

    Returns
    -------
    numpy.ndarray
        The distance to the points in the river network.
    """

    if path == "shortest":
        return min(
            river_network,
            river_network.sinks,
            weights,
            upstream=True,
            downstream=False,
            mv=mv,
        )
    elif path == "longest":
        return max(
            river_network,
            river_network.sinks,
            weights,
            upstream=True,
            downstream=False,
            mv=mv,
        )
    else:
        raise ValueError("Path must be one of 'shortest' or 'longest'.")


def to_source(river_network, weights=None, path="shortest", mv=np.nan):
    """
    Calculate the minimum or maximum distance to the sources of a river network.
    The distance is calculated along the river network.

    Parameters
    ----------
    river_network : earthkit.hydro.RiverNetwork
        An earthkit-hydro river network object.
    weights : numpy.ndarray, optional
        Distance to the downstream point. Default is None, which
        corresponds to a unit distance for all points.
    path : str, optional
        Whether to find the distance of the shortest or longest path.
        Default is 'shortest'.
    mv : scalar, optional
        The missing value indicator. Default is np.nan.

    Returns
    -------
    numpy.ndarray
        The distance to the points in the river network.
    """

    if path == "shortest":
        return min(
            river_network,
            river_network.sources,
            weights,
            upstream=False,
            downstream=True,
            mv=mv,
        )
    elif path == "longest":
        return max(
            river_network,
            river_network.sources,
            weights,
            upstream=False,
            downstream=True,
            mv=mv,
        )
    else:
        raise ValueError("Path must be one of 'shortest' or 'longest'.")
