from metabase_forms_summary_automation.forms_summary import FormsSummary
from .utils import create_dashboard, add_cards_to_dashboard
from metabase_forms_summary_automation import credentials

def make_summary():
    demo_form_id = credentials.FORM_ID
    answers_model_id = credentials.ANSWERS_MODEL_ID
    form_name = credentials.FORM_NAME
    f = FormsSummary(form_id=demo_form_id, credentials=credentials)
    f.get_questions_parameters()

    chart_list = f.create_question_summary()
    dashboard = create_dashboard(f.mtb, form_name, f.collection_id)
    add_cards_to_dashboard(f.mtb, dashboard, chart_list)
