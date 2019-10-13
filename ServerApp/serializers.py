from ServerApp.models.server import Broker, Server, ServerOption


# Serializers for Consumers

def broker_serializer(broker: Broker):
    return {
        'host': broker.bind_ip,
        'port': broker.bind_port,
        'server_list': [
            server_serializer(server) for server in broker.server_set.all()
        ]

    }


def server_serializer(server: Server):
    return {
        'name': server.name,
        'description': server.description,
        'address': server.bind_ip,
        'port': server.bind_port,
        'utilization': server.player_count,
        'capacity': server.capacity,
        'enabled': server.enable,
        'options': server.options.as_dict
    }





