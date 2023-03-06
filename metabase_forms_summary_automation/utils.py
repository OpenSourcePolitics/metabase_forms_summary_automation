def create_dashboard(mtb, name, collection_id):
    res = mtb.post(
        "/api/dashboard",
        json={
            'name': name,
            'collection_id': collection_id
        }
    )
    
    return res

def add_cards_to_dashboard(mtb, dashboard, chart_list):
    dashboard_id = dashboard["id"]
    for chart in chart_list:
        chart_id = chart["id"]
        mtb.post(
            f"/api/dashboard/{dashboard_id}/cards",
            json={'cardId':chart_id}
        )
