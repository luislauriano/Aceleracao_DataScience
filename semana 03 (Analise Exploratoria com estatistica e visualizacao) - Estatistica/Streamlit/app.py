import altair as alt
import  pandas as pd
import streamlit as st

def criar_histograma(coluna, df):
    chart = alt.Chart(df, width=600).mark_bar().encode(
        alt.X(coluna, bin=True),
        y='count()', tooltip=[coluna, 'count()']
    ).interactive()
    return chart


def criar_barras(coluna_num, coluna_cat, df):
    bars = alt.Chart(df, width = 600).mark_bar().encode(
        x=alt.X(coluna_num, stack='zero'),
        y=alt.Y(coluna_cat),
        tooltip=[coluna_cat, coluna_num]
    ).interactive()
    return bars

def criar_boxplot(coluna_num, coluna_cat, df):
    boxplot = alt.Chart(df, width=600).mark_boxplot().encode(
        x=coluna_num,
        y=coluna_cat
    )
    return boxplot

def criar_scatterplot(x, y, color, df):
    scatter = alt.Chart(df, width=800, height=400).mark_circle().encode(
        alt.X(x),
        alt.Y(y),
        color = color,
        tooltip = [x, y]
    ).interactive()
    return scatter

def cria_correlationplot(df, colunas_numericas):
    cor_data = (df[colunas_numericas]).corr().stack().reset_index().rename(columns={0: 'correlation', 'level_0': 'variable', 'level_1': 'variable2'})
    cor_data['correlation_label'] = cor_data['correlation'].map('{:.2f}'.format)  # Round to 2 decimal
    base = alt.Chart(cor_data, width=500, height=500).encode( x = 'variable2:O', y = 'variable:O')
    text = base.mark_text().encode(text = 'correlation_label',color = alt.condition(alt.datum.correlation > 0.5,alt.value('white'),
    alt.value('black')))

# The correlation heatmap itself
    cor_plot = base.mark_rect().encode(
    color = 'correlation:Q')

    return cor_plot + text


def main():
    st.image('logo.png')
    st.title('AceleraDev - Data Science')
    st.image('todo_poderoso.gif')
    st.title('Análise de Dados Exploratória da sua base de dados')
    st.markdown('O objetivo é coletar uma base de dados enviada por você e fazer uma analise exploratoria dos dados, aplicando metodos estatisticos e gráficos.')

    file = st.file_uploader('Escolha a base de dados que deseja analisar (.csv)', type='csv')

    if file is not None:
        st.subheader('Estatística descritiva univariada')
        df = pd.read_csv(file)

        aux = pd.DataFrame({"colunas": df.columns, 'tipos': df.dtypes})

        colunas_numericas = list(aux[aux['tipos'] != 'object']['colunas'])
        colunas_object = list(aux[aux['tipos'] == 'object']['colunas'])
        colunas = list(df.columns)

        col = st.selectbox('Selecione a coluna :', colunas_numericas)

        if col is not None:
                st.markdown('Selecione o que deseja analisar :')

                mean = st.checkbox('Média')
                if mean:
                    st.markdown('A média é uma das principais medidas de tendência central dos dados.  Como geralmente desconhecemos toda população, não conseguimos medir diretamente sua média $\mu$. Para estimarmos o valor dessa estatística populacional, utilizamos estimadores.')
                    st.markdown('A média pode ser calculada como:')
                    st.image('media.jpg')
                    st.markdown('Sua Média: ')
                    st.markdown(df[col].mean())

                median = st.checkbox('Mediana')
                if median:
                    st.markdown('A mediana é o valor que divide os dados ordenados em duas partes iguais (50% dos valores são menores que a mediana e 50% dos valores são maiores que a mediana, Se tivermos um número ímpar (2n+1) de elementos, a mediana é simplesmente o valor que separa n elementos menores que ela, e n elementos maiores que ela, Se tivermos um número par (2n) de elementos, a mediana é a média entre os elementos de índice n-1 e n+1, tal como fizemos acima.')
                    st.markdown('Sua Mediana: ')
                    st.markdown(df[col].median())

                desvio_pad = st.checkbox('Desvio padrão')
                if desvio_pad:
                    st.markdown('O desvio padrão (standard deviation) é a raiz quadrada da variância. Toda discussão em relação à variância populacional x amostral se aplica, mutandi mutandis, ao desvio padrão')
                    st.markdown('O desvio padrão amostral pode ser calculador por: ')
                    st.image('desvio_padrao.jpg')
                    st.markdown('Seu Desvio Padrão: ')
                    st.markdown(df[col].std())

                kurtosis = st.checkbox('Kurtosis')
                if kurtosis:
                    st.markdown('Kurtosis, ou curtose em português, é uma medida que nos ajuda a dar forma à distribuição dos dados. A curtose tenta capturar em uma medida a forma das caudas da distribuição. Ela também possui diferentes definições, mas podemos utilizar a seguinte versão:')
                    st.image('kurtose.jpg')
                    st.markdown('A curtose amostral pode ser obtida com:')
                    st.image('curtose_amostral.jpg')
                    st.markdown('Quando g2>0, temos o caso de uma distribuição leptocúrtica, onde as caudas são mais pesadas e o pico da distribuição mais alto.')
                    st.markdown('Quando g2<0, temos o caso de uma distribuição platicúrtica, onde as caudas são menos pesadas e a distribuição é mais achatada.')
                    valor = (df[col].kurtosis())
                    if valor < 0:
                        st.markdown('Sua distribuição é Platicurtica:')
                        st.markdown(df[col].kurtosis())
                        st.image('platicurtica.jpg', width=300)
                    else:
                        st.markdown('Sua distribuição é Leptocurtica')
                        st.markdown(df[col].kurtosis())
                        st.image('leptocurtica.jpg')

                skewness = st.checkbox('Skewness')
                if skewness:
                    st.markdown('Skewness, ou assimetria em português, é uma medida de... simetria. Ela nos diz o quão simétrica é a distribuição dos dados em torno da média, e junto com a curtose (kurtosis), é uma medida muito boa para informar a aparência ou forma da distribuição dos dados.')
                    st.markdown('A assimetria, γ1, é definida como o terceiro momento padronizado, ou seja:')
                    st.image('assimetria.jpg')
                    st.markdown('Na sua forma amostral, a assimetria pode ser calculada como: ')
                    st.image('assimetria_amostral.jpg')
                    st.markdown('Valores zero da skewness indicam que os dados têm distribuição simétrica em relação ao centro. Valores positivos indicam que a distribuição tem assimetria positiva, ou seja, a cauda direita é mais longa do que a cauda esquerda. Valores negativos indicam que a distribuição tem assimetria negativa, ou seja, a cauda esquerda é mais longa do que a cauda direita.')

                    assimetria = (df[col].skew())
                    if assimetria < 0:
                        st.markdown('Sua distribuição tem assimetria negativa:')
                        st.markdown(df[col].skew())
                        st.markdown('A distribuição possui leve assimetria à esquerda (A cauda esquerda é mais longa do que a cauda direita). Isso é corroborado pelo fato de que a média é inferior à mediana:')
                        st.image('assimetria_negativa.jpg')

                    elif assimetria == 0:
                        st.markdown('Valores zero da skewness indicam que os dados têm distribuição simétrica em relação ao centro.')
                        st.markdown(df[col].skew())
                        st.image('assimetria_zero.jpg')
                    else:
                        st.markdown('Sua distribuição tem assimetria positiva:')
                        st.markdown(df[col].skew())
                        st.markdown('A distribuição possui leve assimetria à direita (A cauda direita é mais longa do que a cauda esquerda). Isso é corroborado pelo fato de que a média é superior à mediana:')
                        st.image('assimetria_positiva.jpg')

                describe = st.checkbox('Describe')
                if describe:
                    st.markdown('O método, describe(), nos dá um resumo estatístico e visão geral das estatísticas como quantidade, média, variância e os quantis das variáveis (colunas) numéricas no data set:')
                    st.table(df[colunas_numericas].describe().transpose())

                st.subheader('Visualização dos dados')
                st.markdown('A visualização de dados é uma etapa que está dentro da análise exploratoria, onde após respondermos as perguntas e hipoteses, precisamos transmitir de forma clara para outras pessoas, tão importante quanto a preparação dos dados. O ser humano tem muito mais facilidade para compreender informação visual do que de qualquer outra forma. Por isso, é sempre bom que analisemos os dados do ponto de vista gráfico: isso nos permite ter insights melhores sobre os nossos dados e também transmitir nossa análise a outras pessoas.')
                st.image('https://media.giphy.com/media/Rkoat5KMaw2aOHDduz/giphy.gif', width=200)
                st.markdown('Selecione a visualizacao')

                histograma = st.checkbox('Histograma')
                if histograma:
                    st.markdown('Esse é um dos gráficos mais conhecidos e úteis na visualização de dados. O histograma nos dá uma boa ideia da distribuição dos dados, melhor ainda que o box plot.')
                    col_num = st.selectbox('Selecione a Coluna Numerica: ', colunas_numericas, key='unique')
                    st.markdown('Histograma da coluna : ' + str(col_num))
                    st.write(criar_histograma(col_num, df))

                barras = st.checkbox('Gráfico de barras')
                if barras:
                    st.markdown('Bar plots são comumente confundidos com histogramas. Nos histogramas, estamos interessados em apenas uma variável. No bar plot, queremos observar a relação entre uma variável qualitativa (categórica) e uma variável quantitativa (numérica).')
                    col_num_barras = st.selectbox('Selecione a coluna numerica: ', colunas_numericas, key='unique')
                    col_cat_barras = st.selectbox('Selecione uma coluna categorica : ', colunas_object, key='unique')
                    st.markdown('Gráfico de barras da coluna ' + str(col_cat_barras) + ' pela coluna ' + col_num_barras)
                    st.write(criar_barras(col_num_barras, col_cat_barras, df))

                boxplot = st.checkbox('Boxplot')
                if boxplot:
                    st.markdown('Box plots são gráficos para visualização da distribuição de uma variável através de seus quantis. Eles são uma forma ágil de enxergar a distribuição dos dados, sem ter que recorrer a histogramas ou gráficos de densidade.')
                    st.markdown('O box plot é um gráfico em forma de retângulo com barrinhas que se prolongam para fora dele. Veja esse exemplo de como funciona a análise de um box plot: ')
                    st.image('boxplot.jpg')
                    st.markdown('A parte inferior do retângulo indica o primeiro quartil (Q1) ou 25º percentil.')
                    st.markdown('A barra dividindo o retângulo indica a mediana ou segundo quartil (Q2) ou 50º percentil.')
                    st.markdown('A parte superior do retângulo indica o terceiro quartil (Q3) ou 75º percentil.')
                    st.markdown('A barrinha (whisker) inferior se prolonga até o menor valor que esteja dentro de Q1−1.5IQR.')
                    st.markdown('A barrinha (whisker) superior se prolonga até o maior valor que esteja dentro de Q3+1.5IQR.')
                    st.markdown('Qualquer observação fora desses limites é considerado um outlier e deve ser indicado por um ponto.')
                    col_num_box = st.selectbox('Selecione a Coluna Numerica:', colunas_numericas, key='unique')
                    col_cat_box = st.selectbox('Selecione uma coluna categorica:', colunas_object, key='unique')
                    st.markdown('Boxplot ' + str(col_cat_box) + ' pela coluna ' + col_num_box)
                    st.write(criar_boxplot(col_num_box, col_cat_box, df))

                scatter = st.checkbox('Scatterplot')
                if scatter:
                    st.markdown('O scatter plot é o tipo de gráfico mais simples. O scatter plot é basicamente um gráfico de dispersão de pontos em um plano.')
                    col_num_x = st.selectbox('Selecione o valor de x ', colunas_numericas, key='unique')
                    col_num_y = st.selectbox('Selecione o valor de y ', colunas_numericas, key='unique')
                    col_color = st.selectbox('Selecione a coluna para cor', colunas)
                    st.markdown('Selecione os valores de x e y')
                    st.write(criar_scatterplot(col_num_x, col_num_y, col_color, df))

                correlacao = st.checkbox('Correlacao')
                if correlacao:
                    st.markdown('É possivel visualizar uma matriz de correlação como um mapa de calor para termos insights ainda mais rápidos sobre as correlações entre as variáveis:')
                    st.markdown('Gráfico de correlação das colunas númericas')
                    st.write(cria_correlationplot(df, colunas_numericas))

                st.markdown('Agradecimento mais que especial aos orientadores da aceleração de Data Science da codenation, Túlio Vieira e Kazuki Yokoyama!')


if __name__ == '__main__':
    main()