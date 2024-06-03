import pandas as pd
import yfinance as yf

# class RatioCalculator:
def ratio_Calculator(tickers):
    dfs = {} #Inicializo diccionario en blanco (el dict permite guardar mas de un dataframe dentro)

    for ticker in tickers:
        ticker_data = yf.Ticker(ticker)
        dfs[ticker] = ticker_data.history(period="max")
        dfs[ticker].index = pd.to_datetime(dfs[ticker].index, utc=True)
    #Segrego en dataframes desde el diccionario

    share_1_df = dfs[tickers[0]]
    share_1_suffixes=f"_{tickers[0]}"
    share_1_close=f"Close_{tickers[0]}"

    share_2_df = dfs[tickers[1]]
    share_2_suffixes=f"_{tickers[1]}"
    share_2_close=f"Close_{tickers[1]}"

    #CALCULOS
    # Arreglo DF entre MSFT y GOOGLE
    merged_df = pd.merge(share_1_df, share_2_df, left_index=True, right_index=True, suffixes=(share_1_suffixes, share_2_suffixes))

    # Calculo el ratio
    merged_df['Close_ratio'] = merged_df[share_1_close] / merged_df[share_2_close]

    # Muestro el resultado preliminar
    merged_df = merged_df[['Close_ratio']]

    # Asegurarse de que 'merged_df' solo contenga la columna 'Close_ratio'
    merged_df = merged_df[['Close_ratio']]

    # Calcula la EMA de 10
    merged_df['EMA_10'] = merged_df['Close_ratio'].ewm(span=10, adjust=False).mean()

    # Calcula la EMA de 20
    merged_df['EMA_20'] = merged_df['Close_ratio'].ewm(span=20, adjust=False).mean()

    # Filtra el DataFrame para el último año
    last_year = pd.Timestamp.now(tz='UTC') - pd.DateOffset(years=1)
    filtered_df = merged_df[merged_df.index >= last_year]

    return filtered_df
