import os
from flask import Flask, render_template
from deta import Deta
from dotenv import load_dotenv
from aggregations import generate_df, sum_volume

load_dotenv()

app = Flask(__name__)
isDev = os.getenv("DEBUG") is not None
TABLE_NAME = "cocktails" + ("_dev" if isDev else "")
deta = Deta(os.getenv("DETA_PROJECT_KEY"))
cocktail_deta = deta.Base(TABLE_NAME)


@app.route('/', methods=["GET"])
def hello_world():
    df = generate_df(cocktail_deta)
    sumdata = sum_volume(df)
    return render_template(
        'index.html', tables=[df.to_html(classes='data', index=False)], titles=df.columns.values,
        sumdata=[sumdata.to_html(index=False)]
    )


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
