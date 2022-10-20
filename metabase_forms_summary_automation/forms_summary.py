from metabase_api import Metabase_API
from metabase_forms_summary_automation import credentials
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
    def __init__(self, form_id, questions=None, dashboard_id=None):
        self.connect(credentials)
        self.form_id = form_id
        self.questions = questions
        self.dashboard_id = dashboard_id
        self.credentials = credentials
        
    def connect(self, credentials):
        self.mtb = Metabase_API(
            credentials.METABASE_URL,
            credentials.METABASE_USERNAME,
            credentials.METABASE_PASSWORD
        )

    def create_form_model(self, answers_model_id, form_name="MODEL - My wonderful form"):
        params = {
            'name': form_name,
            'display': 'table',
            'dataset': True,
            'dataset_query': {
                'database': credentials.DATABASE_ID,
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
        self.form_model_id = res['id']

    def get_questions_parameters(self):
        import pandas as pd
        res = self.mtb.get_card_data(card_id=self.form_model_id)
        df = pd.DataFrame(res)
        
        # Not multilingual-proof ! 
        df = df[['Titre de la question', 'Type de question']].drop_duplicates()
        
        self.questions_parameters = df.values.tolist()
        
    def create_question_summary(self):
        for question in self.questions_parameters:
            question_title, question_type = question
            if question_type in ["short_answer", "long_answer"]:
                table_chart = TableChart(question_title, self)
                table_chart.set_filter(Filter('=', 'question_title', question_title))
                table_chart.set_fields(Fields([{'name':'answer', 'type': 'type/Text'}]))
            
                table_chart.create_chart()
            elif question_type in ["single_option", "multiple_option"]:
                pie_chart = PieChart(question_title, self)
                pie_chart.set_filter(Filter('=','question_title', question_title))
                pie_chart.set_aggregation(
                    Aggregation(
                        ['count'],
                        Fields([{'name':'answer', 'type': 'type/Text'}])
                    )
                )
                pie_chart.create_chart()
            elif question_type in ["matrix_single", "matrix_multiple"]:
                bar_chart = BarChart(question_title, self)
                bar_chart.set_filter(Filter('=', 'question_title', question_title))
                bar_chart.set_aggregation(
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
                bar_chart.set_custom_params(
                    [{
                        "name": "visualization_settings",
                        "value": {
                            "graph.dimensions": ["sub_matrix_question", "answer"],
                            "graph.metrics": ["count"]
                        }
                    }]
                )
                
                bar_chart.create_chart()
            elif question_type in ["files"]:
                table_chart = TableChart(question_title, self)
                table_chart.set_filter(Filter('=', 'question_title', question_title))
                table_chart.set_fields(
                    Fields(
                        [
                            {'name':'answer', 'type': 'type/Text'},
                            {'name':'custom_body', 'type':'type/*'}
                        ]
                    )
                )
            
                table_chart.create_chart()                
            elif question_type in ["sorting"]:
                horizontal_bar_chart = HorizontalBarChart(
                    question_title, self
                )
                horizontal_bar_chart.set_filter(Filter('=', 'question_title', question_title))
                horizontal_bar_chart.set_aggregation(
                    Aggregation(
                        ['sum', Fields([{'name':'sorting_points', 'type': 'type/Integer'}])],
                        Fields([{'name':'answer', 'type': 'type/Text'}])
                    )
                )
                horizontal_bar_chart.set_order(Order('desc'))
                import pdb; pdb.set_trace()
                horizontal_bar_chart.create_chart()
                
                
                