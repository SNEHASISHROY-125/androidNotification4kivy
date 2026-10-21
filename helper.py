from jnius import autoclass

PythonActivity = autoclass("org.kivy.android.PythonActivity")
RemoteViews = autoclass("android.widget.RemoteViews")

activity = PythonActivity.mActivity
package_name = activity.getPackageName()
resources = activity.getResources()


def get_resource_id(name, resource_type="layout"):
    res_id = resources.getIdentifier(
        name, resource_type, package_name
    )
    if res_id == 0:
        raise ValueError(
            f"Resource not found: {resource_type}/{name}"
        )
    return int(res_id)


def load_remote_views(layout_name):
    layout_id = get_resource_id(layout_name, "layout")
    return RemoteViews(package_name, layout_id)


def set_text(views, view_name, value):
    view_id = get_resource_id(view_name, "id")
    views.setTextViewText(view_id, str(value))


def set_progress(views, view_name, progress, maximum=100):
    view_id = get_resource_id(view_name, "id")
    progress = max(0, min(int(progress), maximum))
    views.setProgressBar(view_id, maximum, progress, False)