import pandas as pd


def pagerank(graph, damping=0.85, iterations=30):
    nodes = list(graph.keys())
    count = len(nodes)

    ranks = {node: 1 / count for node in nodes}

    for _ in range(iterations):
        new_ranks = {
            node: (1 - damping) / count
            for node in nodes
        }

        for node in nodes:
            neighbors = graph[node]
            total_weight = sum(neighbors.values())

            if total_weight == 0:
                continue

            for neighbor, weight in neighbors.items():
                new_ranks[neighbor] += (
                    damping
                    * ranks[node]
                    * weight
                    / total_weight
                )

        ranks = new_ranks

    return ranks


def get_top_products(df, limit=10):
    graph_df = df[
        ['CustomerID', 'ProductID', 'Quantity']
    ].dropna().copy()

    graph_df['Quantity'] = pd.to_numeric(
        graph_df['Quantity'],
        errors='coerce'
    )

    graph_df = graph_df[graph_df['Quantity'] > 0]

    graph_df = graph_df.groupby(
        ['CustomerID', 'ProductID'],
        as_index=False
    )['Quantity'].sum()

    graph = {}

    for _, row in graph_df.iterrows():
        customer = ('customer', row['CustomerID'])
        product = ('product', row['ProductID'])
        weight = row['Quantity']

        graph.setdefault(customer, {})
        graph.setdefault(product, {})

        graph[customer][product] = weight
        graph[product][customer] = weight

    if not graph:
        return []

    ranks = pagerank(graph)

    product_ranks = [
        {
            'ProductID': node[1],
            'PageRank': rank
        }
        for node, rank in ranks.items()
        if node[0] == 'product'
    ]

    product_ranks.sort(
        key=lambda item: item['PageRank'],
        reverse=True
    )

    return product_ranks[:limit]