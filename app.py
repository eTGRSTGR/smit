import streamlit as st
from gtts import gTTS
from io import BytesIO
from groq import Groq

class VoiceAssistant:
    def __init__(self):
        self.groq_client = Groq(api_key="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")

    def processar_comando(self, texto):
        try:
            resposta = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "Você é um assistente em português"},
                    {"role": "user", "content": texto}
                ]
            )
            return resposta.choices[0].message.content
        except Exception as e:
            st.error(f"Erro ao processar o comando: {e}")
            return "Desculpe, houve um problema ao processar seu comando."

    def falar(self, texto):
        st.write(f"Assistente: {texto}")
        tts = gTTS(text=texto, lang='pt-br')
        fp = BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        st.audio(fp, format='audio/mp3')

def main():
    st.set_page_config(page_title="Assistente Virtual")
    st.title("Assistente Virtual")

    # Entrada de texto
    user_input = st.text_input("Digite sua mensagem:")
    
    # Botão para enviar
    if st.button("Enviar"):
        if user_input:
            assistente = VoiceAssistant()
            
            # Mostra o que o usuário digitou
            st.write(f"Você: {user_input}")
            
            if user_input.lower() in ['sair', 'pare', 'tchau']:
                st.write("Assistente: Até logo!")
                st.stop()
            else:
                # Processa o comando e gera resposta
                resposta = assistente.processar_comando(user_input)
                assistente.falar(resposta)
        else:
            st.warning("Por favor, digite algo antes de enviar.")

    # Estilo personalizado
    st.markdown("""
        <style>
        .stButton > button {
            background-color: #4CAF50;
            color: white;
            padding: 15px 32px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
            border: none;
        }
        .stButton > button:hover {
            background-color: #45a049;
        }
        </style>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
