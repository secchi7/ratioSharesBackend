from flask import Flask, request
from ratioCalculator import ratio_Calculator
import plotly
from flask_cors import CORS, cross_origin
import pandas as pd
pd.options.plotting.backend = "plotly"


app = Flask(__name__)
cors = CORS(app)
@app.route("/api/ratio", methods=['POST','OPTIONS'])
@cross_origin()
def ratio():
    share=request.get_json("share1")
    share_1=share["Share1"]
    share_2=share["Share2"]
    tickers = [share_1,share_2]
    filtered_df=ratio_Calculator(tickers)
    fig=filtered_df.plot()
    graphJson=plotly.io.to_json(fig,pretty=True)
    return graphJson


if __name__=="__main__":
    app.run()

