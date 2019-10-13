from django.db import close_old_connections


class CustomAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        close_old_connections()

        uuid = None
        token = None
        auth_type = None

        for header in scope["headers"]:
            if header[0] == b'auth-uuid':
                uuid = header[1].decode()
            elif header[0] == b'auth-token':
                token = header[1].decode()
            elif header[0] == b'auth-type':
                auth_type = header[1].decode()

        if not uuid or not token or not auth_type:
            raise LookupError("Invalid Parameters")

        if auth_type.lower() == 'broker':
            from ServerApp.models.server import Broker

            return self.inner(dict(scope, broker=Broker.objects.get(uuid=uuid, token=token)))

        elif auth_type.lower() == 'server':
            from ServerApp.models.server import Server

            return self.inner(dict(scope, server=Server.objects.get(uuid=uuid, token=token)))
        else:
            raise TypeError("Invalid Authorization Scheme")
