# Metabase Forms Summary Automation
This project aims to make a summary of a Decidim Form, based on models available on [this project](https://github.com/OpenSourcePolitics/metabase_automation/)

## Requirements
- [Poetry](https://python-poetry.org/)

## Setup
1. Clone repository
2. Run `poetry install`
3. Run `poetry run make_summary`

## TODO
- [x] Connect to Metabase
- [x] Retrieve all forms with provided model ID
- [x] Retrieve specific form information
- [ ] Retrieve all questions of specified form with their types and IDs
- [ ] Create card that gathers answers of the specified question
    - [ ] Short answers
    - [ ] Long answers
    - [x] Single option
    - [x] Multiple option
    - [ ] Sorting
    - [ ] Matrix simple
    - [ ] Matrix multiple
    - [ ] Files

### Improvements
- [ ] Retrieve automatically the models which contains the forms information