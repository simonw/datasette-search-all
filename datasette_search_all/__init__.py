from datasette import hookimpl
from .app import SearchAll


@hookimpl
def asgi_wrapper(datasette):
    SearchAll.datasette = datasette

    def wrap_with_app(app):
        async def wrapped_app(scope, receive, send):
            path = scope["path"]
            if path == "/-/search":
                await SearchAll(scope, receive, send)
            else:
                await app(scope, receive, send)

        return wrapped_app

    return wrap_with_app
