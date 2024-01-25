import pandas as pd
import streamlit as st
import openpyxl

st.write("""
# CALCULADORA: TAXA INTERNA DE RETORNO (TIR)

Vamos gerar um gráfico da taxa interna de retorno (TIR) vs o VPL

""")

# Título do aplicativo
st.markdown('## UPLOAD ARQUIVO EXCEL')
st.markdown(f"Dúvidas em como fazer o upload do arquivo? Acesse o link: [{'AQUI'}]({'https://docs.google.com/presentation/d/19dOVy95LsEhf09rUs6xxJZTPWT9TdmLWjTBtVEhqlFc/edit?usp=sharing'})", unsafe_allow_html=True)

# Widget de upload de arquivo XLSX
file = st.file_uploader("", type=["xlsx"])

# Verifica se um arquivo foi enviado
if file is not None:
    # Lê o arquivo XLSX em um DataFrame do Pandas
    df = pd.read_excel(file)
    wb = openpyxl.load_workbook(file) #starta openxyl
    # Exibe o DataFrame
    st.write("**Fluxo de caixa abaixo:**")
    st.write(df)


    tam = len(df)
    lista_P = []
    lista_K = []
    vpl = 0

    for l in range(0,350000,1):
        vpl=0
        lista_P.append(l)

        for i in range(0,tam,1):
            pk = df["FLUXO DE CAIXA FINAL"][i] / ((1+(l/100000))**i)
            vpl = pk + vpl

        lista_K.append(round(vpl,0))

    print(lista_K)
    print(lista_P)

    lista_P1 =[]

    for x in range(0,len(lista_P),1):
        lista_P1.append(lista_P[x]/100000)


    df2 = pd.DataFrame({"Juros":lista_P1,
                         "VPL":lista_K})

    with st.container():
        st.markdown('## ANALISANDO VALOR PRESENTE LÍQUIDO')
        st.text("Gráfico de linhas: VPL vs JUROS")
        st.line_chart(df2.set_index("Juros"))

    lista_valores = df2["VPL"]
    # Inicialize as variáveis para armazenar o valor mais próximo e a distância mínima
    valor_mais_proximo = lista_valores[0]
    distancia_minima = abs(lista_valores[0] - 0)

    # Itere sobre os valores restantes
    for valor in lista_valores[1:]:
        distancia_atual = abs(valor - 0)

        # Verifique se o valor atual é mais próximo de zero
        if distancia_atual < distancia_minima:
            valor_mais_proximo = valor
            distancia_minima = distancia_atual

    # Filtrar o DataFrame para obter as linhas onde 'VPL' é igual ao valor mais próximo
    linhas_mais_proximas = df2[df2['VPL'] == valor_mais_proximo]

    # Obter os valores correspondentes da coluna 'Juros'
    juros_mais_proximos = linhas_mais_proximas['Juros'].tolist()
    juros_mais_proximos = juros_mais_proximos[0]
    juros_percentual = juros_mais_proximos * 100
    # Imprimir os valores de 'Juros' correspondentes ao valor mais próximo de 'VPL'

    with st.container():
        st.text(f" O valor de juros ideal é aproximadamente (TIR): {round(juros_percentual,3)}%.\n "
            f"Para valores de juros abaixo de {round(juros_percentual,3)}%, o VPL será positivo.(GANHO) \n "
            f"Para valores de juros acima de {round(juros_percentual,3)}%, o VPL será negativo. (PERDA)")

    with st.container():
        st.markdown('## SIMULADOR DE VALOR PRESENTE LÍQUIDO')
        juros_simulador = st.number_input("Digite uma porcentagem (JUROS):", min_value=0.0, max_value=100.0, step=0.1)
        st.write(f"Você digitou a seguinte porcentagem: {juros_simulador}%")
        juros_percentual = juros_simulador/100

        if juros_percentual > 0:
             vpl1 = 0
             for k in range(0, len(df), 1):
                 pk1 = df["FLUXO DE CAIXA FINAL"][k] / ((1 + (juros_percentual)) ** k)
                 vpl1 = pk1 + vpl1

             st.write(f"Com o juros de {juros_simulador}%, o VPL é de R$ {round(vpl1,2)}")