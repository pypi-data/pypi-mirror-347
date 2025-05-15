# (C) Copyright 2025- ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.

from functools import partial

import numpy as np

from .accumulation import calculate_online_metric
from .metrics import metrics_dict
from .utils import mask_and_unmask


@mask_and_unmask
def calculate_upstream_metric(
    river_network,
    field,
    metric,
    weights=None,
    mv=np.nan,
    accept_missing=False,
):
    """
    Calculates a metric for the field over all upstream values.

    Parameters
    ----------
    river_network : earthkit.hydro.RiverNetwork
        An earthkit-hydro river network object.
    field : numpy.ndarray
        The input field.
    metric : str
        Metric to compute. Options are "mean", "max", "min", "sum", "product"
    weights : ndarray, optional
        Used to weight the field when computing the metric. Default is None.
    mv : scalar, optional
        Missing value for the input field. Default is np.nan.
    accept_missing : bool, optional
        Whether or not to accept missing values in the input field. Default is False.

    Returns
    -------
    numpy.ndarray
        Output field.

    """

    return calculate_online_metric(
        river_network, field, metric, weights, mv, accept_missing, flow_direction="down"
    )


for metric in metrics_dict.keys():

    func = partial(calculate_upstream_metric, metric=metric)

    globals()[metric] = func
