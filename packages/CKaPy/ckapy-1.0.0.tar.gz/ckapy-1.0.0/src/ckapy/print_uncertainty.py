import numpy as np


def fitted_parameters(parameter_names, popt, pcov):
    perr = np.sqrt(np.diag(pcov))
    print("==================================")
    print("Fitted Parameters")
    print("==================================")
    for i in range(len(parameter_names)):
        print(parameter_names[i] + " = " + print_uncertainty(popt[i], perr[i]))
    print("==================================")


def compute_value_order(val):
    return int(np.floor(np.log10(np.abs(val))))


def _compute_error_decimals(val, err):
    val_order = compute_value_order(val)
    err_order = compute_value_order(err)
    decimals = -(err_order - val_order)
    return decimals


def _uncertainty_str_bracket(val, err, decimals):
    val_order = compute_value_order(val)
    err_order = compute_value_order(err)
    if decimals is None:
        decimals = _compute_error_decimals(val, err)
    return f"{val * 10**-val_order:.{decimals}f}({err * 10**-err_order:.0f})*10^{val_order:d}"


def _uncertainty_str_plus_minus(val, err, decimals):
    val_order = compute_value_order(val)
    if decimals is None:
        decimals = _compute_error_decimals(val, err)
    return f"({val * 10**-val_order:.{decimals}f} +\- {err * 10**-val_order:.{decimals}f})*10^{val_order:d}"


def print_uncertainty(val, err, decimals=None, format="bracket"):
    if format in ("bracket"):
        return _uncertainty_str_bracket(val, err, decimals)
    elif format in ("plus minus", "pm", "plus/minus"):
        pass
    else:
        print("Format string unrecognized, defaulting to plus/minus.")
    return _uncertainty_str_plus_minus(val, err, decimals)


def print_array_mean_err(array, decimals=None, format="bracket"):
    arr_mean = np.mean(array)
    arr_std = np.std(array)
    return print_uncertainty(arr_mean, arr_std, decimals, format)


def print_decimal_value(value, n_decimals=1):
    whole_value = np.floor(value)
    decimal_value = round(value % 1 * 10**n_decimals, 0)
    return "%dp%d" % (whole_value, decimal_value)
