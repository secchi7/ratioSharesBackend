from flask import Flask, request, jsonify
from ratioCalculator import ratio_Calculator
import plotly
import pandas as pd
pd.options.plotting.backend = "plotly"
from functools import wraps

def backend():
    app = Flask(__name__)
    # Función para habilitar CORS en respuestas
    def enable_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'  # Permitir solicitudes desde cualquier origen
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Permitir los métodos GET, POST y OPTIONS
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'  # Permitir el encabezado Content-Type
        return response

    # Decorador para aplicar la función enable_cors a las rutas
    def crossdomain(origin=None, methods=None, headers=None):
        if methods is not None:
            methods = ', '.join(sorted(x.upper() for x in methods))
        if headers is not None and not isinstance(headers, str):
            headers = ', '.join(x.upper() for x in headers)
        if not isinstance(origin, str):
            origin = ', '.join(origin)
        if isinstance(origin, str) and origin.lower() == 'all':
            origin = '*'
        def decorator(f):
            @wraps(f)
            def wrapped_function(*args, **kwargs):
                # Si la solicitud es OPTIONS, simplemente devolvemos una respuesta vacía con los encabezados CORS
                if request.method == 'OPTIONS':
                    response = jsonify({'message': 'Preflight Request'})
                    return enable_cors(response)
                # Si no es una solicitud OPTIONS, llamamos a la función original y habilitamos los CORS en la respuesta
                result = f(*args, **kwargs)
                if not isinstance(result, response):
                    result = jsonify(result)
                response = enable_cors(result)
                return response
            return wrapped_function
        return decorator

    # Ruta protegida que utiliza el decorador crossdomain
    @app.route('/api/ratio', methods=['GET', 'POST', 'OPTIONS'])
    @crossdomain(origin='*')  # Permitir solicitudes desde cualquier origen
    def ratio():
        share=request.get_json("share1")
        share_1=share["Share1"]
        share_2=share["Share2"]
        tickers = [share_1,share_2]
        filtered_df=ratio_Calculator(tickers)
        fig=filtered_df.plot()
        graphJson=plotly.io.to_json(fig,pretty=True)
        return graphJson

    return app

if __name__=="__main__":
    app=backend()
    app.run(debug=True)
