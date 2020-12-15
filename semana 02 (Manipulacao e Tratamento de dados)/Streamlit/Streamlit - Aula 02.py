import streamlit as st

def main():
    st.title('Hello World')

    st.markdown('Botao')
    botao = st.button('Botao')
    if botao:
        st.markdown('clicado')

    st.markdown('Checkbox')
    check = st.checkbox('Checkbox')
    if check:
        st.markdown('clicado')

    st.markdown('Radio')
    radio = st.radio('escolha as opcoes', ('opt1', 'opt2'))
    if radio == 'opt1':
        st.markdown('opt1')
    if radio == 'opt2':
         st.markdown('opt2')

    st.markdown('Selectbox')
    select = st.selectbox('Escolha as opçoes', ('opt1', 'opt2'))
    if select == 'opt1':
        st.markdown('opt1')
    if select == 'opt2':
        st.markdown('opt2')

    multi = st.multiselect('Escolha', ('opt1', 'opt2'))
    if multi == 'opt1':
        st.markdown('opt1')
    if multi == 'opt2':
        st.markdown('opt2')

    st.markdown('Upload')
    file = st.file_uploader('Chose your file', type='csv')
    if file is not None:
        st.markdown('não esta vazio')


if __name__ == '__main__':
    main()