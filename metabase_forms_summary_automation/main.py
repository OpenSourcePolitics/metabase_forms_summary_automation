from metabase_forms_summary_automation.forms_summary import FormsSummary
from .credentials import FORM_ID, ANSWERS_MODEL_ID

def start():
    demo_form_id = FORM_ID
    answers_model_id = ANSWERS_MODEL_ID
    f = FormsSummary(form_id=demo_form_id)
    f.create_form_model(answers_model_id, "MODÈLE - Questionnaire open-data")
    f.get_questions_parameters()

    f.create_question_summary()