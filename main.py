import streamlit as st
import api


df = api.final_df(st.secrets["api_key"])
print(df)

def main():
    st.set_page_config(page_title='Dashboard', layout='wide', initial_sidebar_state='collapsed')

    st.markdown('''<h2>Acompanhamento de Informações por Funil</h2>''', unsafe_allow_html=True)

    status_select = st.multiselect("Selecione o Status", options=df['status'].unique(), default=["aberto", "perdido", "ganho"])

    st.dataframe(df[df['status'].isin(status_select)])

    # Agrupa e soma os valores por status
    soma_por_status = df[df['status'].isin(status_select)].groupby('status')['value'].sum()

    # Agrupa e soma os valores por status
    contagem_por_status = df[df['status'].isin(status_select)].groupby('status')['value'].count()

    col1, col2 = st.columns(2)


    # Exibe gráfico de barras
    valor_aberto = df[df['status'] == 'aberto'].groupby('status')['value'].sum().values[0]
    col1.subheader(f"Valores em aberto: R$ {valor_aberto:,.2f}")
    valor_ganho = df[df['status'] == 'ganho'].groupby('status')['value'].sum().values[0]
    col1.subheader(f"Valores em ganho: R$ {valor_ganho:,.2f}")
    valor_perdido = df[df['status'] == 'perdido'].groupby('status')['value'].sum().values[0]
    col1.subheader(f"Valores em perdido: R$ {valor_perdido:,.2f}")
    col1.bar_chart(soma_por_status)

    cont_aberto = df[df['status'] == 'aberto'].groupby('status')['value'].count().values[0]
    col2.subheader(f"Qtd. em aberto: {cont_aberto:,.2f}")
    cont_ganho = df[df['status'] == 'ganho'].groupby('status')['value'].count().values[0]
    col2.subheader(f"Qtd. em ganho: {cont_ganho:,.2f}")
    cont_perdido = df[df['status'] == 'perdido'].groupby('status')['value'].count().values[0]
    col2.subheader(f"Qtd. em perdido: {cont_perdido:,.2f}")

    # Exibe gráfico de barras
    col2.bar_chart(contagem_por_status)




if __name__ == '__main__':
    main()
