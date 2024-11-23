import streamlit as st
import speech_recognition as sr
from groq import Groq
from gtts import gTTS
import numpy as np
from io import BytesIO
import base64

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.groq_client = Groq(api_key="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")

    def transcribe_audio_data(self, audio_bytes):
        try:
            audio_data = sr.AudioData(audio_bytes, sample_rate=44100, sample_width=2)
            texto = self.recognizer.recognize_google(audio_data, language='pt-BR')
            return texto
        except sr.UnknownValueError:
            st.error("Não foi possível entender o áudio")
        except sr.RequestError as e:
            st.error(f"Erro no serviço de reconhecimento de fala: {e}")
        return ""

    def processar_comando(self, texto):
        try:
            resposta = self.groq_client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "Você é um assistente por voz em português"},
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
    st.set_page_config(page_title="Assistente de Voz")
    st.title("Assistente de Voz")

    # Componente JavaScript para gravação
    st.markdown("""
        <script>
        const recordAudio = async () => {
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                const mediaRecorder = new MediaRecorder(stream);
                const audioChunks = [];
                
                mediaRecorder.addEventListener("dataavailable", event => {
                    audioChunks.push(event.data);
                });
                
                mediaRecorder.addEventListener("stop", () => {
                    const audioBlob = new Blob(audioChunks);
                    const reader = new FileReader();
                    reader.readAsDataURL(audioBlob);
                    reader.onloadend = () => {
                        const base64Audio = reader.result.split(',')[1];
                        window.parent.postMessage({
                            type: 'audio_data',
                            data: base64Audio
                        }, '*');
                    };
                });
                
                mediaRecorder.start();
                setTimeout(() => mediaRecorder.stop(), 5000);
            } catch (err) {
                console.error("Erro ao acessar o microfone:", err);
            }
        };

        // Adiciona função ao objeto window para ser chamada pelo botão do Streamlit
        window.startRecording = recordAudio;
        </script>
    """, unsafe_allow_html=True)

    # Botão Streamlit que aciona a gravação
    if st.button("Iniciar Gravação", key="record_button"):
        st.markdown("""
            <script>
            window.startRecording();
            </script>
        """, unsafe_allow_html=True)
        st.info("Gravando... (5 segundos)")
        st.session_state.recording = True

    assistente = VoiceAssistant()

    if 'audio_data' in st.session_state:
        audio_bytes = base64.b64decode(st.session_state.audio_data)
        comando = assistente.transcribe_audio_data(audio_bytes)
        
        if comando:
            st.write(f"Você disse: {comando}")
            
            if comando.lower() in ['sair', 'pare', 'tchau']:
                st.write("Assistente: Até logo!")
                st.stop()
            else:
                resposta = assistente.processar_comando(comando)
                assistente.falar(resposta)

    # Listener para receber os dados do áudio
    st.markdown("""
        <script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'audio_data') {
                window.parent.postMessage({
                    type: 'streamlit:set_session_state',
                    data: { audio_data: event.data.data }
                }, '*');
            }
        });
        </script>
    """, unsafe_allow_html=True)

    # Adiciona um estilo personalizado para o botão
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
