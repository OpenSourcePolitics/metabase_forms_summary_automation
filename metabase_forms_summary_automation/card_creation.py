class Filter:
    def __init__(self, filter_type, field, value):
        self.type = filter_type
        self.field= field
        self.value = value
        

class Aggregation:
    def __init__(self, aggregation_type, field):
        self.type = aggregation_type
        self.field = field


class Fields:
    def __init__(self, field_list):
        self.field_list = field_list

class ChartCreator:
    def __init__(self, display, name, forms_summary, **kwargs):
        self.display = display
        self.name = name
        self.mtb = forms_summary.mtb
        self.params = {
                'name': self.name,
                'display': self.display,
                'dataset_query' : {
                    'database': forms_summary.credentials.DATABASE_ID,
                    'query': {
                        'source-table': f'card__{forms_summary.form_model_id}'
                    },
                    'type': 'query'
                }
            }
        self.filter = None
        self.aggregation = None        
            
    def create_chart(self):
        if self.filter:
            self.params['dataset_query']['query']['filter'] = [
                self.filter.type,
                [      
                    'field',     
                    self.filter.field,
                    {'base-type': 'type/Text'}
                ],
                self.filter.value
            ]
        
        if self.aggregation:
            self.params['dataset_query']['query']['aggregation'] = [[self.aggregation.type]]
            self.params['dataset_query']['query']['breakout'] = [[
                "field", self.aggregation.field, { "base-type": "type/Text" }
            ]]

        self.mtb.create_card(custom_json=self.params)

    def set_filter(self, filter):
        assert isinstance(filter, Filter)
        self.filter = filter
        
    def set_aggregation(self, aggregation):
        assert isinstance(aggregation, Aggregation)
        self.aggregation = aggregation


class PieChart(ChartCreator):
    def __init__(self, *args, **kwargs):
        super().__init__('pie',*args,**kwargs)


class Histogram(ChartCreator):
    def __init__(self, *args, **kwargs):
        super().__init__('histogram', *args, **kwargs)