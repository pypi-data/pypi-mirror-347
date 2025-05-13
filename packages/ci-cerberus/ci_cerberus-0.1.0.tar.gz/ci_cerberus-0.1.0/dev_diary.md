# Dev Diary
> This file serves as a bit of a thought dump of each session I have while coding this project, to help me remember
> what I did for when it comes to writing the whitepaper


## 16/04/2025 - Getting started

### Summary
- downloaded PyCharm Community Edition & started figuring my way around it
- added a `models` package to hold shared models (CVEs returned from NVD, Actions parsed from GitHub Workflows)
  - used `dataclasses` so that I don't have to bother with `self.field = field` etc...
- created an `httpclients` module containing
  - a `BaseHttpClient` class to handle making `GET`/`POST`
    - some basic logging to refactor later into structured logs
    - some error handling around the `get` method
    - used `urlencode` to make keywords safe to add to query params
  - a `NvdHttpClient` class to make calls to the NVD API
  - a `responsemodels` folder to hold DTOs and handle parsing of the response
- set up a `main.py` file & a run configuration for the project
- added a utils package containing a logging utility method to streamline logging throughout the app. Will make the log level configurable later on

### Thoughts
Started off getting things written, immediately hated not having type hints. Went back and added them all,
so I can hover methods & see what I get back from them.

Happy enough with the progress for a first stab at the NVD API able to make a call using the `keywordSearch` param- would like to some structured logging, and the ability
to set log levels.

_(edit: thought I was done, but was itching to do more so went back and did some tidy up/added logging)_

---

## 17/04/2025 -> 19/04/25 - Parsing actions

### Summary
- Set up a dummy `.github/workflows` folder with a couple of files to get testing
- created an `actionsparser` package to handle reading actions & workflows from a local folder
- created some precommit hooks to automate the fiddly bits of python
  - black - formatter
  - flake8 - linter
  - isort - import sorter (black doesn't make them PEP-8 compliant)

---
