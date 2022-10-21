from metabase_forms_summary_automation.forms_summary import FormsSummary
from .credentials import FORM_ID, ANSWERS_MODEL_ID
from .utils import create_dashboard, add_cards_to_dashboard

def start():
    demo_form_id = FORM_ID
    answers_model_id = ANSWERS_MODEL_ID
    f = FormsSummary(form_id=demo_form_id)
    f.get_questions_parameters()

    chart_list = f.create_question_summary()
    dashboard = create_dashboard(f.mtb, "My wonderful dashboard", f.collection_id)
    add_cards_to_dashboard(f.mtb, dashboard, chart_list)