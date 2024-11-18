
import streamlit as st
import csv
from datetime import datetime

# Configuração inicial do aplicativo
st.set_page_config(page_title="Quiz de Histologia: Tecidos Fundamentais", layout="wide")

# Senha para acessar o quiz
PASSWORD = "histologia2024"
CSV_FILE = "responses.csv"

# Função para verificar a senha
def check_password():
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Quiz de Histologia: Tecidos Fundamentais</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FF5722;'>Digite a senha para acessar o quiz</h3>", unsafe_allow_html=True)

    password = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if password == PASSWORD:
            st.session_state["access_granted"] = True
            st.experimental_rerun()
        else:
            st.error("Senha incorreta. Tente novamente.")

# Função para salvar respostas no CSV
def save_responses_to_csv(responses, score, correct_answers, wrong_answers):
    with open(CSV_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:  # Verifica se o arquivo está vazio para adicionar cabeçalho
            writer.writerow(["Data/Hora", "Pergunta", "Resposta Escolhida", "Resposta Correta", "Pontuação", "Corretas", "Erradas"])
        for response in responses:
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                response["question"],
                response["selected"],
                response["correct"],
                score,
                correct_answers,
                wrong_answers
            ])

# Verificar se o acesso foi concedido
if "access_granted" not in st.session_state or not st.session_state["access_granted"]:
    check_password()
else:
    # Título do jogo
    st.markdown("<h1 style='text-align: center; color: #4CAF50;'>Quiz de Histologia: Tecidos Fundamentais</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #FF5722;'>Teste seus conhecimentos sobre os tecidos epitelial, conjuntivo, muscular e nervoso!</h3>", unsafe_allow_html=True)

    # Introdução
    st.write("Bem-vindo ao Quiz de Histologia! Escolha a alternativa correta para cada pergunta e clique em **Finalizar** ao final para ver seu desempenho.")

    # Lista de perguntas sobre os tecidos fundamentais
    questions = [
        {"question": "Qual é a principal característica do tecido epitelial?",
         "options": ["a) Alta vascularização", "b) Produção de impulsos elétricos", "c) Contração voluntária", "d) Presença de matriz extracelular abundante", "e) Células justapostas e pouca matriz extracelular"],
         "answer": "e) Células justapostas e pouca matriz extracelular"},
        {"question": "Qual tipo de tecido conjuntivo é responsável pelo armazenamento de gordura?",
         "options": ["a) Tecido Cartilaginoso", "b) Tecido Adiposo", "c) Tecido Muscular", "d) Tecido Nervoso", "e) Tecido Epitelial"],
         "answer": "b) Tecido Adiposo"},
        {"question": "Qual tecido é especializado na contração para produzir movimento?",
         "options": ["a) Tecido Epitelial", "b) Tecido Conjuntivo", "c) Tecido Muscular", "d) Tecido Nervoso", "e) Tecido Adiposo"],
         "answer": "c) Tecido Muscular"},
        {"question": "Qual é a função principal do tecido nervoso?",
         "options": ["a) Sustentação mecânica", "b) Condução de impulsos elétricos", "c) Armazenamento de energia", "d) Transporte de nutrientes", "e) Produção de colágeno"],
         "answer": "b) Condução de impulsos elétricos"},
        {"question": "Qual tipo de tecido epitelial reveste os alvéolos pulmonares?",
         "options": ["a) Epitélio Simples Pavimentoso", "b) Epitélio Cilíndrico", "c) Epitélio Estratificado Cuboide", "d) Epitélio de Transição", "e) Epitélio Simples Cuboide"],
         "answer": "a) Epitélio Simples Pavimentoso"}
    ]

    # Variáveis para armazenar pontuação e respostas do usuário
    correct_answers = 0
    wrong_answers = 0
    user_answers = []
    score = 0

    # Exibição das perguntas
    for i, q in enumerate(questions):
        st.markdown(f"<h4 style='color: #2196F3;'>Pergunta {i+1}: {q['question']}</h4>", unsafe_allow_html=True)
        selected = st.radio("", q["options"], key=i)
        user_answers.append({
            "question": q["question"],
            "selected": selected,
            "correct": q["answer"]
        })

    # Botão para finalizar o quiz
    if st.button("Finalizar Quiz"):
        # Verificar respostas
        for response in user_answers:
            if response["selected"] == response["correct"]:
                correct_answers += 1
            else:
                wrong_answers += 1
        score = correct_answers

        # Salvar as respostas no CSV
        save_responses_to_csv(user_answers, score, correct_answers, wrong_answers)

        # Exibir resultado final
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center; color: #4CAF50;'>Resultado Final</h3>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; color: #4CAF50;'>Respostas Corretas: {correct_answers}</h4>", unsafe_allow_html=True)
        st.markdown(f"<h4 style='text-align: center; color: #F44336;'>Respostas Erradas: {wrong_answers}</h4>", unsafe_allow_html=True)

        # Feedback com base no desempenho
        if correct_answers == len(questions):
            st.balloons()
            st.markdown("<h4 style='text-align: center; color: #4CAF50;'>Excelente! Você acertou todas as perguntas!</h4>", unsafe_allow_html=True)
        elif correct_answers > len(questions) // 2:
            st.markdown("<h4 style='text-align: center; color: #FFEB3B;'>Bom trabalho! Continue praticando para melhorar ainda mais.</h4>", unsafe_allow_html=True)
        else:
            st.markdown("<h4 style='text-align: center; color: #F44336;'>Não desista! Revise os conceitos e tente novamente.</h4>", unsafe_allow_html=True)
