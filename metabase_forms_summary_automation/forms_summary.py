from metabase_api import Metabase_API
from metabase_forms_summary_automation.credentials import METABASE_PASSWORD, METABASE_URL, METABASE_USERNAME
from pprint import pprint

mb = Metabase_API(METABASE_URL, METABASE_USERNAME, METABASE_PASSWORD)  # if password is not given, it will prompt for password

#print (mb.get("/api/collection/")[0].keys())

pprint(mb.post("/api/card/3174/query")['data']['rows'])
