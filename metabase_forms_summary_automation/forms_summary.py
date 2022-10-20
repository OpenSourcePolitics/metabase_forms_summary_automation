from metabase_api import Metabase_API
from metabase_forms_summary_automation import credentials
from .card_creation import (
    Filter,
    Aggregation,
    Fields,
    ChartCreator,
    PieChart,
    TableChart,
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
                pie_chart.set_aggregation(Aggregation('count','answer'))
                pie_chart.create_chart()
            elif question_type in ["matrix_single", "matrix_multiple"]:
                pass
            elif question_type in ["files"]:
                pass
            elif question_type in ["sorting"]:
                pass