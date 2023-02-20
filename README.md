<img src="docs/pictures/logo_dashboard.png" alt="CocktailBerry" width="750"/>

![GitHub release (latest by date)](https://img.shields.io/github/v/release/AndreWohnsland/CocktailBerry-WebApp)
![GitHub Release Date](https://img.shields.io/github/release-date/AndreWohnsland/CocktailBerry-WebApp)
![Python Version](https://img.shields.io/badge/python-%3E%3D%203.9-blue)
![GitHub](https://img.shields.io/github/license/AndreWohnsland/CocktailBerry-WebApp)
![GitHub issues](https://img.shields.io/github/issues-raw/AndreWohnsland/CocktailBerry-WebApp)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=AndreWohnsland_CocktailBerry-WebApp&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=AndreWohnsland_CocktailBerry-WebApp)
![GitHub Repo stars](https://img.shields.io/github/stars/AndreWohnsland/CocktailBerry-WebApp?style=social)

[![Buy Me a Coffee](https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow)](https://www.buymeacoffee.com/AndreWohnsland)

WebApp with API and endpoint for [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry). Have insights into made cocktails.


# Getting Started

Either cd into `frontend` or `backend` and run `pip install -r requirements.txt` or use poetry in main folder to install everything for both apps with `poetry install`. Then in the corresponding folder run:

```bash
# omit poetry run if using normal python
poetry run uvicorn main:app --reload # backend
poetry run streamlit run streamlit_app.py # frontend, use in main folder
```

If you want everything to work properly, you need a [deta space account](https://deta.space/) and a collection access token (go to Space>Collection>Your Collection>Collection Settings>Generate Token). Deta is used for Deta Collection e.g. storing of the data and for the later deployment of the API. Don't worry it's free (and will always be that way, according to deta). Copy the `.env.example` in both folders as a `.env` file and change the token dummy to your project access token:

```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Using `DEBUG=1` in the env files will enable some dev features, like the creation of an additional `*_dev` database to let you test anything without changing your main one. The `BACKEND_URL` defaults to localhost (http://127.0.0.1:8000), where the backend runs locally. If you deploy backend and frontend on two different places (like streamlit share and deta space), you need to set this variable in the frontend accordingly. For detailed instruction for deployment, please refer to the according docs of your provider. 

# Architecture

In this project, [Deta](https://deta.space/docs/en/introduction/start) was used for the hosting. The WebApp can be accessed freely over any browser. The API is protected an can be only accessed with an according API key to prevent unauthorized access. To get an API key for your [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry) machine follow the instructions on the website. Alternatively, you can clone this repo, set up your own dashboard with backend and use the according hook endpoint and header values with the CocktailBerry microservice for your own, private dashboard.

![ProgramSchema](docs/diagrams/out/Schema.svg)

# Access

Simply go to the [site](https://stats-cocktailberry.streamlitapp.com/) and have nice insight into the data. If you have build your [CocktailBerry](https://github.com/AndreWohnsland/CocktailBerry) and use the official software, you can get an API key for CocktailBerry to use the provided endpoint to submit your production data. This way, you can actively participate. 🙌

Also, if you directly just want the data for the last 24 hours, for example if you want to give your guest insights in the current developments of the cocktail stats, there is the possibility to add the `?partymode=true` query parameter to the url. This will cause the "Only Show last 24h Data" checkbox to be checked by default.
