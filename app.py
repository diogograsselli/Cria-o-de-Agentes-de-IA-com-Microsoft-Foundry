import sys
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from groq import Groq

# ==============================================================================
# >>>>> COLE SUA CHAVE DA API GROQ DIRETAMENTE AQUI DENTRO DAS ASPAS <<<<<
GROQ_API_KEY = "cole sua api"
# ==============================================================================

# Prompt Semântico do Alex (PlayZone Games)
SYSTEM_PROMPT = """# ROLE & IDENTITY
Você é Alex, especialista e consultor técnico sênior da PlayZone Games.
Sua missão é atuar como consultor de vendas ativo, compreendendo as necessidades do usuário, esclarecendo dúvidas técnicas de hardware/software e recomendando produtos assertivos.

# CONTEXT & AUDIENCE
Seu público varia desde jogadores casuais até competidores focados em latência, taxa de quadros e ergonomia.
Plataformas cobertas: PC Gamer, PlayStation 5, Xbox Series X/S e Nintendo Switch.

# OPERATIONAL PROTOCOL
1. Perfilamento Inicial: Identifique plataforma e estilo de jogo (competitivo, campanha, coop, etc.).
2. Validação Técnica: Conecte características técnicas aos benefícios práticos (resolução, áudio espacial, taxas de atualização).
3. Venda Consultiva: Proponha periféricos, upgrades ou serviços associados (assinaturas, headsets, ergonomia).
4. Chamada para Ação: Conclua sempre instigando o fechamento da escolha de forma objetiva.

# GUARDRAILS
- Neutralidade absoluta sobre plataformas (sem console wars).
- Nunca invente compatibilidade física ou de requisitos mínimos sem certeza técnica.
- Respostas dinâmicas em no máximo 2 a 3 parágrafos objetivos.
- Tom descontraído, acessível e técnico."""


class PlayZoneChatApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("PlayZone Games - Atendimento Especialista Alex")
        self.geometry("780x640")
        self.minsize(580, 480)

        # Paleta Gamer Dark
        self.bg_main = "#121214"
        self.bg_secondary = "#202024"
        self.bg_accent = "#8257E5"
        self.text_primary = "#E1E1E6"
        self.text_secondary = "#A8A8B3"

        self.configure(bg=self.bg_main)

        # Inicialização do cliente Groq
        self.client = None
        if GROQ_API_KEY and GROQ_API_KEY != "COLE_SUA_CHAVE_GROQ_AQUI":
            try:
                self.client = Groq(api_key=GROQ_API_KEY)
            except Exception as e:
                messagebox.showerror("Erro de Inicialização", f"Falha ao conectar com o Groq: {e}")
        else:
            messagebox.showwarning(
                "Chave Não Configurada",
                "Você esqueceu de colar sua chave do Groq no topo do arquivo app.py!"
            )

        # Histórico da conversa
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

        self.setup_ui()

    def setup_ui(self):
        # Header / Barra Superior
        header_frame = tk.Frame(self, bg=self.bg_secondary, height=60)
        header_frame.pack(fill=tk.X, side=tk.TOP)

        title_label = tk.Label(
            header_frame,
            text="🎮 PLAYZONE GAMES | Alex - Consultoria Gamer",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_secondary,
            fg=self.text_primary
        )
        title_label.pack(side=tk.LEFT, padx=16, pady=12)

        status_label = tk.Label(
            header_frame,
            text="● Llama-3.3-70b Online",
            font=("Segoe UI", 9),
            bg=self.bg_secondary,
            fg="#04D361"
        )
        status_label.pack(side=tk.RIGHT, padx=16, pady=12)

        # Área de Exibição das Mensagens
        self.chat_area = ScrolledText(
            self,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg=self.bg_main,
            fg=self.text_primary,
            insertbackground=self.text_primary,
            relief=tk.FLAT,
            padx=12,
            pady=12
        )
        self.chat_area.pack(expand=True, fill=tk.BOTH, padx=16, pady=(12, 6))

        self.chat_area.tag_configure("user", foreground="#61DAFB", font=("Segoe UI", 10, "bold"))
        self.chat_area.tag_configure("bot", foreground="#04D361", font=("Segoe UI", 10, "bold"))
        self.chat_area.tag_configure("content", foreground=self.text_primary, font=("Segoe UI", 10))
        self.chat_area.configure(state=tk.DISABLED)

        # Mensagem inicial do Alex
        self.append_message("Alex", "Fala! Sou o Alex da PlayZone. O que você está buscando hoje? Novo jogo, headset, controle ou quer montar um setup?")

        # Container Inferior (Campo de texto + Botão Enviar)
        bottom_frame = tk.Frame(self, bg=self.bg_main)
        bottom_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=16, pady=12)

        self.entry_input = tk.Entry(
            bottom_frame,
            font=("Segoe UI", 11),
            bg=self.bg_secondary,
            fg=self.text_primary,
            insertbackground=self.text_primary,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightcolor=self.bg_accent,
            highlightbackground="#29292E"
        )
        self.entry_input.pack(side=tk.LEFT, expand=True, fill=tk.X, ipady=8, padx=(0, 8))
        self.entry_input.bind("<Return>", lambda event: self.send_message())
        self.entry_input.focus_set()

        self.btn_send = tk.Button(
            bottom_frame,
            text="Enviar",
            font=("Segoe UI", 10, "bold"),
            bg=self.bg_accent,
            fg="#FFFFFF",
            relief=tk.FLAT,
            activebackground="#996DFF",
            activeforeground="#FFFFFF",
            cursor="hand2",
            command=self.send_message,
            padx=20,
            pady=4
        )
        self.btn_send.pack(side=tk.RIGHT)

    def append_message(self, sender, text):
        self.chat_area.configure(state=tk.NORMAL)
        tag = "user" if sender == "Você" else "bot"
        self.chat_area.insert(tk.END, f"\n{sender}: ", tag)
        self.chat_area.insert(tk.END, f"{text}\n", "content")
        self.chat_area.configure(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def append_bot_token(self, token):
        self.chat_area.configure(state=tk.NORMAL)
        self.chat_area.insert(tk.END, token, "content")
        self.chat_area.configure(state=tk.DISABLED)
        self.chat_area.see(tk.END)

    def send_message(self):
        user_text = self.entry_input.get().strip()
        if not user_text:
            return

        if not self.client:
            messagebox.showwarning(
                "API Indisponível",
                "Verifique a variável GROQ_API_KEY no início do arquivo app.py."
            )
            return

        self.entry_input.delete(0, tk.END)
        self.append_message("Você", user_text)
        self.messages.append({"role": "user", "content": user_text})

        self.btn_send.configure(state=tk.DISABLED)
        self.entry_input.configure(state=tk.DISABLED)

        # Thread paralela para não congelar o Tkinter durante a resposta
        threading.Thread(target=self.process_groq_stream, daemon=True).start()

    def process_groq_stream(self):
        try:
            self.chat_area.configure(state=tk.NORMAL)
            self.chat_area.insert(tk.END, "\nAlex: ", "bot")
            self.chat_area.configure(state=tk.DISABLED)

            response_stream = self.client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=self.messages,
                temperature=0.6,
                max_tokens=600,
                stream=True
            )

            assistant_reply = ""
            for chunk in response_stream:
                content = chunk.choices[0].delta.content or ""
                assistant_reply += content
                self.append_bot_token(content)

            self.chat_area.configure(state=tk.NORMAL)
            self.chat_area.insert(tk.END, "\n")
            self.chat_area.configure(state=tk.DISABLED)

            self.messages.append({"role": "assistant", "content": assistant_reply})

        except Exception as e:
            self.append_message("Sistema", f"Erro de comunicação: {e}")

        finally:
            self.btn_send.configure(state=tk.NORMAL)
            self.entry_input.configure(state=tk.NORMAL)
            self.entry_input.focus_set()


if __name__ == "__main__":
    app = PlayZoneChatApp()
    app.mainloop()