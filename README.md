# Metabase Forms Summary Automation
This project aims to make a summary of a Decidim Form, based on models available on [this project](https://github.com/OpenSourcePolitics/metabase_automation/)

## Requirements
- [Poetry](https://python-poetry.org/)

## Setup
1. Clone repository
2. Run `poetry install`
3. Run `poetry run make_summary`

## TODO
- [ ] Connect to Metabase
- [ ] Retrieve all forms of specified customer
- [ ] Retrieve all questions of specified form with their types and IDs
- [ ] Create card that gathers answers of the specified question
    - [ ] Short answers
    - [ ] Long answers
    - [ ] Single option
    - [ ] Multiple option
    - [ ] Sorting
    - [ ] Matrix simple
    - [ ] Matrix multiple
    - [ ] Files