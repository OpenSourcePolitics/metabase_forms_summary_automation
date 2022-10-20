class Filter:
    def __init__(self, filter_type, field, value):
        self.type = filter_type
        self.field= field
        self.value = value
        
    def to_params(self):
        pass

class Aggregation:
    def __init__(self, aggregation_type, fields):
        self.type = aggregation_type
        self.fields = fields

    def to_params(self):
        params = []
        if self.type[0] == 'count':
            aggregation = [[self.type]]
        #TODO : improve aggregation
        elif self.type[0] == 'sum':
            aggregation_type = 'sum'
            aggregation_field = self.type[1]
            aggregation = aggregation_field.to_params()
            aggregation.insert(0, 'sum')
        breakout = self.fields.to_params()
        return aggregation, breakout

class Fields:
    def __init__(self, field_list):
        self.field_list = field_list
        
    def to_params(self):
        params = []
        for field in self.field_list:
            params.append([
                "field",field["name"], { "base-type": field["type"]}
            ])
        return params


class Order:
    def __init__(self, order_direction='asc', criteria=None):
        self.order_direction = order_direction
        #TODO
        self.criteria = criteria

    def to_params(self):
        params=[]
        params.append([
            self.order_direction,
            ["aggregation", 0, None]
        ])
        return params

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
        self.fields = None
        self.order = None
        self.custom_params = None
            
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
            aggregation, breakout = self.aggregation.to_params()
            self.params['dataset_query']['query']['aggregation'] = aggregation
            self.params['dataset_query']['query']['breakout'] = breakout
            
        if self.fields:
            self.params['dataset_query']['query']['fields'] = self.fields.to_params()

        if self.custom_params:
            for custom_param in self.custom_params:
                self.params[custom_param["name"]] = custom_param["value"]
        
        if self.order:
            self.params['dataset_query']['query']['order_by'] = self.order.to_params()
        
        self.mtb.create_card(custom_json=self.params)

    def set_filter(self, filter):
        assert isinstance(filter, Filter)
        self.filter = filter
        
    def set_aggregation(self, aggregation):
        assert isinstance(aggregation, Aggregation)
        self.aggregation = aggregation
        
    def set_fields(self, fields):
        assert isinstance(fields, Fields)
        self.fields = fields
        
    def set_order(self, order):
        assert isinstance(order, Order)
        self.order = order

    def set_custom_params(self, kwargs_list):
        self.custom_params = kwargs_list
class PieChart(ChartCreator):
    def __init__(self, *args, **kwargs):
        super().__init__('pie',*args,**kwargs)


class TableChart(ChartCreator):
    def __init__(self, *args, **kwargs):
        super().__init__('table', *args, **kwargs)


class BarChart(ChartCreator):
    def __init__(self, *args, **kwargs):
        super().__init__('bar', *args, **kwargs)


class HorizontalBarChart(ChartCreator):
    def __init__(self, *args, **kwargs):
        super().__init__('row',*args, **kwargs)
