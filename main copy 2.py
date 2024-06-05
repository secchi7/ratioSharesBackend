from flask import Flask, request, make_response, jsonify
from ratioCalculator import ratio_Calculator
import plotly
# from flask_cors import CORS, cross_origin
import pandas as pd
pd.options.plotting.backend = "plotly"

def backend():
    app = Flask(__name__)
    # cors = CORS(app)
    @app.route("/api/ratio", methods=['POST','OPTIONS'])
    # @cross_origin()






    
    def ratio():
        if request.method == "OPTIONS": # CORS preflight
            return _build_cors_preflight_response()
        elif request.method == "POST": # The actual request following the preflight
            share=request.get_json("share1")
            share_1=share["Share1"]
            share_2=share["Share2"]
            tickers = [share_1,share_2]
            filtered_df=ratio_Calculator(tickers)
            fig=filtered_df.plot()
            graphJson=plotly.io.to_json(fig,pretty=True)
            return _corsify_actual_response(graphJson)
        else:
            raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))
    # def api_create_order():
    #     if request.method == "OPTIONS": # CORS preflight
    #         return _build_cors_preflight_response()
    #     elif request.method == "POST": # The actual request following the preflight
    #         plot = ratio()
    #         return _corsify_actual_response(plot)
    #     else:
    #         raise RuntimeError("Weird - don't know how to handle method {}".format(request.method))

    # def _build_cors_preflight_response():
    #     response = make_response()
    #     response.headers.add("Access-Control-Allow-Origin", "*")
    #     response.headers.add('Access-Control-Allow-Headers', "*")
    #     response.headers.add('Access-Control-Allow-Methods', "*")
    #     return response

    # def _corsify_actual_response(response):
    #     response.headers.add("Access-Control-Allow-Origin", "*")
    #     return response

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
                if not isinstance(result, Response):
                    result = jsonify(result)
                response = enable_cors(result)
                return response
            return wrapped_function
        return decorator

    # Ruta protegida que utiliza el decorador crossdomain
    @app.route('/api/data', methods=['GET', 'POST', 'OPTIONS'])
    @crossdomain(origin='*')  # Permitir solicitudes desde cualquier origen
    def get_data():
        data = {'example': 'data'}
        return data
    return app

if __name__=="__main__":
    app=backend()
    app.run()

