from metabase_api import Metabase_API
from .card_creation import (
    Filter,
    Aggregation,
    Fields,
    Order,
    ChartCreator,
    PieChart,
    TableChart,
    BarChart,
    HorizontalBarChart
)
from pprint import pprint

#print (mtb.get("/api/collection/")[0].keys())

class FormsSummary:
    def __init__(self, form_id, credentials):
        self.credentials = credentials
        self.connect()
        self.form_id = form_id
        
        self.get_database_id()
        self.collection_id = credentials.COLLECTION_ID
        self.create_form_model(credentials.ANSWERS_MODEL_ID, name=credentials.FORM_NAME)
        self.get_questions_parameters()
    
    def connect(self):
        self.mtb = Metabase_API(
            self.credentials.METABASE_URL,
            self.credentials.METABASE_USERNAME,
            self.credentials.METABASE_PASSWORD
        )

    def get_database_id(self):
        self.database_id = self.mtb.get_item_info('card', self.credentials.ANSWERS_MODEL_ID)["database_id"]

    # TODO : move to table chart with dataset = True
    def create_form_model(self, answers_model_id, name="MODEL - My wonderful form"):
        params = {
            'name': name,
            'display': 'table',
            'dataset': True,
            'dataset_query': {
                'database': self.database_id,
                'query': 
                    {'filter': 
                        [
                            '=',
                            [
                                'field',
                                'decidim_questionnaire_id',
                                {'base-type': 'type/Integer'}
                            ],
                            self.form_id
                        ],
                        'source-table': f'card__{answers_model_id}'
                    },
                'type': 'query'
            }
        }
       
        res = self.mtb.create_card(custom_json=params, return_card=True)
        self.form_model_info = res
        self.form_model_id = res['id']

    def get_questions_parameters(self):
        import pandas as pd
        res = self.mtb.get_card_data(card_id=self.form_model_id)
        df = pd.DataFrame(res)
        
        # Not multilingual-proof ! 
        df = df[['Titre de la question', 'Type de question', 'Position']].drop_duplicates()
        
        self.questions_parameters = df.values.tolist()
        
    def create_question_summary(self):
        chart_list = []
        for question in self.questions_parameters:
            question_title, question_type, position = question
            chart = None
            chart_filter = Filter('=', 'position', position)
            question_name = f"{position}. {question_title}"
            if question_type in ["short_answer", "long_answer"]:
                chart = TableChart(question_name, self)
                chart.set_filter(chart_filter)
                chart.set_fields(Fields([{'name':'answer', 'type': 'type/Text'}]))

            elif question_type in ["single_option", "multiple_option"]:
                chart = PieChart(question_name, self)
                chart.set_filter(chart_filter)
                chart.set_aggregation(
                    Aggregation(
                        ['count'],
                        Fields([{'name':'answer', 'type': 'type/Text'}])
                    )
                )
            elif question_type in ["matrix_single", "matrix_multiple"]:
                chart = BarChart(question_name, self)
                chart.set_filter(chart_filter)
                chart.set_aggregation(
                    Aggregation(
                        ['count'],
                        Fields(
                            [
                                {'name':'sub_matrix_question', 'type':'type/Text'},
                                {'name':'answer', 'type': 'type/Text'}
                            ]
                        )
                    )
                )
                chart.set_custom_params(
                    [{
                        "name": "visualization_settings",
                        "value": {
                            "graph.dimensions": ["sub_matrix_question", "answer"],
                            "graph.metrics": ["count"]
                        }
                    }]
                )
            elif question_type in ["files"]:
                chart = TableChart(question_name, self)
                chart.set_filter(chart_filter)
                chart.set_fields(
                    Fields(
                        [
                            {'name':'answer', 'type': 'type/Text'},
                            {'name':'custom_body', 'type':'type/*'}
                        ]
                    )
                )
            elif question_type in ["sorting"]:
                chart = HorizontalBarChart(question_name, self)
                chart.set_filter(chart_filter)
                chart.set_aggregation(
                    Aggregation(
                        ['sum', Fields([{'name':'sorting_points', 'type': 'type/Integer'}])],
                        Fields([{'name':'answer', 'type': 'type/Text'}])
                    )
                )
                chart.set_order(Order('desc'))
            created_chart = chart.create_chart()
            chart_list.append(created_chart)
        # else: 
        #     print(f"Ce type de diagramme n'est pas pris en compte: {question_type}")
        return chart_list
