""" Fitting functions """

from __future__ import print_function

import numpy
import scipy.stats
import scipy.integrate
import scipy.optimize

# TODO perhaps remove y0base? Since x_scale seems to work fine.
# TODO compute Chi square


def _genresidualsfunc(func, data, n_vars, fity0=False, y0base=None,
                      aggfunc=None, i_fitvars=None, **kwargs):
    """
    Given a model and a 2D vector of empirical data, return a function that
    computes the residuals of the fit of the ODE model to the empirical data.

    Parameters
    ==========
    func : callable(y, t, ...)
        A function that computes the derivative of y at time t. This argument
        is passed to `scipy.integrate.odeint` for integration. y is a 1-D
        ndarray of size `n_vars`.

    data : ndarray
        A 2D array of size (N, M + 1) of observations. The first column
        corresponds to time values. The M remaining columns are observable
        variables. It must be `n_vars` >= M.

    n_vars : int
        Number of state variables of the model.

    fity0 : bool
        See `fitone`.

    y0base : float
        See `fitone`.

    aggfunc : callable(y)
        See `fitone`

    i_fitvars : list
        See `fitone`

    Additional keyword arguments are passed to `scipy.integrate.odeint`.

    Returns
    =======
    _fitresiduals : callable(x)
        Returns the residuals of the fit with parameter vector x. This
        functions is suitable for use with `scipy.optimize.least_squares`.
    """
    def _fitresiduals(x):
        if fity0:
            y0 = x[:n_vars]
            args = x[n_vars:]
        else:
            y0 = y[0]
            n = n_vars - len(y0)
            y0 = numpy.hstack([y0, x[:n]])
            args = x[n:]
        assert len(y0) == n_vars
        if y0base is not None:
            y0 = numpy.power(y0base, y0)
        yhat = scipy.integrate.odeint(func, y0, t, args=tuple(args), **kwargs)
        # aggregate result of the integration. Needed with the segregated
        # model.
        if aggfunc is not None:
            yhat = aggfunc(yhat)
        # select observable variables for residuals
        if i_fitvars is not None:
            # user specified column indices
            assert len(i_fitvars) == n_datavars, "Error: must match number "\
                "of data variables: {}".format(i_fitvars)
            yhat = yhat[:, i_fitvars]
        else:
            # by default use the fist n_datavars
            yhat = yhat[:, :n_datavars]
        yres = yhat - y
        return yres.ravel()
    if n_vars <= 0:
        raise ValueError('Error: n_vars must be > 0: {}'.format(n_vars))
    data = numpy.atleast_2d(data)
    t = data[:, 0]
    y = data[:, 1:]
    _, n_datavars = y.shape
    if n_vars < n_datavars:
        raise ValueError("Error: Not enough variables to fit (needs {}): "
                         "{}".format(n_datavars, n_vars))
    return _fitresiduals


def fitone(data, modelfunc, n_vars, bounds, nrep=25, fity0=False,
           y0base=None, aggfunc=None, i_fitvars=None, **kwargs):
    """
    Fit one dataset to an ODE model. Performs the fit by minimizing a loss
    function of the residuals between the model and the data.

    Parameters
    ==========

    data : ndarray
        A 2D array of shape (N, M + 1), where N is the number of observations.
        Each observations is of the form:
            (t, y_1(t), ..., y_M(t))
        where the first element is the time, and y_i(t) is the value of the
        i-th variable at time t.

    modelfunc : callable(y, t, ...)
        The ODE model. Computes the derivative of y at t. y can be an array of
        shape (M,).

    n_vars : int
        Number of state variables of the model

    bounds : list
        A list of pairs `(lower, upper)` specifying bounds for each parameter
        of the model.

    nrep : int
        Call `least_squares` multiple time sampling the starting conditions
        uniformly at random from the hypercube identified by `bounds` and pick
        the solution with the smallest error.

    fity0 : bool
        Optional; if True, estimate y0 as fit parameters. If False, take y0
        from the data. Default: False.

    y0base : int
        Optional; treat y0 as log-transformed in this base. To compute actual
        y0 needed to integrate, raise this base to the power of each exponent.
        The default is to not to use a log-transformation.

    aggfunc : callable(y)
        User-defined function that aggregates the integrated function before
        computing residuals.

    i_fitvars : sequence of ints
        Optional; indices for the columns of the variables to use in the fit.
        By default the first leftmost variables returned by the model are used.

    Additional keyword arguments will be passed to
    `scipy.optimize.least_squares`.

    Returns
    =======
    xopt : ndarray
        Array of fitted parameter values.

    erropt : ndarray
        Standard errors of the fitted values
    """
    lower_bounds, upper_bounds = zip(*bounds)
    size = (nrep, len(bounds))
    x0arr = scipy.stats.uniform.rvs(lower_bounds, upper_bounds, size)
    x_scale = numpy.diff(bounds, axis=1).ravel()
    tmp = []
    for i in range(nrep):
        x0 = x0arr[i]
        _resid = _genresidualsfunc(modelfunc, data, n_vars, fity0=fity0,
                                   y0base=y0base, aggfunc=aggfunc,
                                   i_fitvars=i_fitvars)
        res = scipy.optimize.least_squares(_resid, x0, x_scale=x_scale,
                                           bounds=(lower_bounds, upper_bounds),
                                           **kwargs)
        tmp.append(res)
    best_res = min(tmp, key=lambda k: k.cost)
    return best_res.x, _stderr(best_res)


def _stderr(res):
    """
    Compute standard error of the fitted parameters
    """
    # Code adapted from: scipy.optimize.curve_fit
    # Do Moore-Penrose inverse discarding zero singular values.
    from scipy.linalg import svd
    _, s, VT = svd(res.jac, full_matrices=False)
    threshold = numpy.finfo(float).eps * max(res.jac.shape) * s[0]
    s = s[s > threshold]
    VT = VT[:s.size]
    pcov = numpy.dot(VT.T / s**2, VT)
    return 1.96 * numpy.sqrt(numpy.diag(pcov))


def relabserr(data, modelfunc, x):
    """
    Relative absolute error
    """
    t = data[:, 0]
    y = data[:, 1:]
    yh = modelfunc(y, t, x)
    e = numpy.ravel(numpy.abs((y - yh) / y)).sum() / data.size
    return e


def fitmany(datasets, modelfunc, n_vars, bounds, nrep=25, fity0=False,
            y0base=None, aggfunc=None, **kwargs):
    """
    Applies `fitone` to all data arrays in the `datasets`.

    Arguments
    =========

    datasets - sequence
        A list/sequence of data arrays (see `fitone`)

    ...
        See `fitone`

    Returns
    =======
    A list of results from `fitone`.

    """
    tmp = []
    for data in datasets:
        res = fitone(data, modelfunc, n_vars, bounds, nrep=nrep, fity0=fity0,
                     y0base=y0base, aggfunc=aggfunc, **kwargs)
        tmp.append(res)
    return tmp
