# CocktailBerry-WebApp
WebApp with API and endpoint for [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry). Have insights into made cocktails.

# Disclaimer

This app is currently still under construction and will get improvements (beta state).

# Getting Started

Either cd into `frontend` or `backend` and run `pip install -r requirements.txt` or use poetry in main folder to install everything for both apps with `poetry install`. Then in the corresponding folder run:

```bash
# omit poetry run if using normal python
poetry run uvicorn main:app --reload # backend
poetry run streamlit run main.py # frontend
```

# Architecture

In this project, [Deta](https://docs.deta.sh/docs/home/) was used for the hosting. The WebApp can be accessed freely over any browser. The API is protected an can be only accessed with an according API key to prevent unauthorized access. To get an API key for your [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry) machine follow the instructions on the website. 

![ProgramSchema](docs/diagrams/out/Schema.svg)

# Access

Simply go to the [site](https://share.streamlit.io/andrewohnsland/cocktailberry-webapp/main/frontend/main.py) and have nice insight into the data. If you have build your [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry) and use the official software, you can get an API key for CocktailBerry to use the prodived endpoint to submit your production data. This way, you can actively participate. 🙌