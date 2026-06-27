killed_nodes = set()
killed_links = set()

def kill_node(node_id):
    if node_id in killed_nodes:
        killed_nodes.remove(node_id)
    else:
        killed_nodes.add(node_id)

def kill_link(node_a, node_b):
    key = "-".join(sorted([node_a, node_b]))
    if key in killed_links:
        killed_links.remove(key)
    else:
        killed_links.add(key)

def restore():
    killed_nodes.clear()
    killed_links.clear()

def get_state():
    return {
        'killedNodes': list(killed_nodes),
        'killedLinks': list(killed_links)
    }
