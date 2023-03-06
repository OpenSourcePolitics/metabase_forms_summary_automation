def create_dashboard(mtb, name, collection_id):
    res = mtb.post(
        "/api/dashboard",
        json={
            'name': name,
            'collection_id': collection_id,
            'collection_position':1
        }
    )
    
    return res

def add_cards_to_dashboard(mtb, dashboard, chart_list):
    for chart, created_chart in chart_list:
        res = mtb.post(
            f"/api/dashboard/{dashboard['id']}/cards",
            json={
                'cardId':created_chart['id'],
                'row':chart.row,
                'col':chart.col,
                'size_x':chart.size_x,
                'size_y':chart.size_y
            }
        )
        assert res is not False
