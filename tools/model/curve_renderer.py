# {
#     "curve_name": {"template_angle":[], "template_torque":[], "template_time":[]}
# }
###


G_CURVES = {}


def gen_data_points(x, y):
    points = []
    for i in range(min(len(x), len(y))):
        points.append((x[i], y[i]))
    return points


def _get_series(x_key: str, y_key):
    series = []
    for k in G_CURVES.keys():
        curve_data = G_CURVES[k]
        series.append({
            'name': k,
            'type': 'line',
            'yAxisIndex': 0,
            'symbol': 'circle',
            'clip': False,
            'showSymbol': False,
            'itemStyle': {
            },
            'lineStyle': {
                'width': 4
            },
            'label': {'show': False},
            'data': gen_data_points(
                curve_data.get(x_key, []),
                curve_data.get(y_key, [])
            )
        })
    return series


def _get_series_angle_torque():
    return _get_series('template_angle', 'template_torque')


def _get_series_time_torque():
    return _get_series('template_time', 'template_torque')


def _get_series_time_angle():
    return _get_series('template_time', 'template_angle')


series_formatter = {
    'angle_torque': _get_series_angle_torque,
    'time_torque': _get_series_time_torque,
    'time_angle': _get_series_time_angle
}


def get_series_by_type(curve_type: str):
    if not series_formatter.get(curve_type, None):
        return []
    return series_formatter[curve_type]()


def add_curve(curve_name, curve_data):
    global G_CURVES
    G_CURVES[curve_name] = curve_data
    pass


def add_curves(curves):
    global G_CURVES
    for curve_name in curves.keys():
        add_curve(curve_name, curves[curve_name])


def set_curves(curves):
    global G_CURVES
    G_CURVES = {}
    for curve_name in curves.keys():
        add_curve(curve_name, curves[curve_name])
