import services.edges
import json


def test_get_edge():

    edge_id = '139806548404171878991929958738371273692'
    edge = services.edges.get_edge(edge_id)
    print('Edge:', edge)
    assert edge['_key'] == edge_id


def test_get_edges():

    node = "p(HGNC:AKT1)"
    (edges, facets) = services.edges.get_edges(node, contains=True)

    print('Edges:\n', json.dumps(edges, indent=4))
    print('Facets:\n', json.dumps(facets, indent=4))
    print('EdgeCnt', len(edges))

    assert False
