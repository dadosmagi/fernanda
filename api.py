import requests
import pandas as pd


def get_total_pages(token):
    url = "https://api.pipe.run/v1/deals"

    headers = {
        "accept": "application/json",
        "token": token
    }

    params = {
        "pipeline_id": 86916,
        "show": 100,
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    meta = data['meta']
    total_pages = int(meta['total_pages'])

    print("Total de páginas obtido com sucesso")

    return total_pages


def import_data(page, token):
    url = "https://api.pipe.run/v1/deals"

    headers = {
        "accept": "application/json",
        "token": token
    }

    params = {
        "pipeline_id": 86916,
        "show": 100,
        "page": page,
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    data = data['data']
    df = pd.DataFrame(data)
    df = df[['id', 'title', 'status', 'closed_at', 'value']]

    print(f"Dataframe da página {page} gerado com sucesso!")

    return df

def final_df(token):
    total_pages = get_total_pages(token)

    all_dataframes = []
    for page in range(1, total_pages - 10):
        df = import_data(page, token)
        all_dataframes.append(df)


    final_df = pd.concat(all_dataframes, ignore_index=True)
    final_df['status'] = final_df['status'].replace({
        0: 'aberto',
        1: 'ganho',
        3: 'perdido'
    })

    print("Dados finais e consolidados importados com sucesso!")
    return final_df

