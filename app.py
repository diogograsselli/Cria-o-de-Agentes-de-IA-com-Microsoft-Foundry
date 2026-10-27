"""Diagnóstico de conexão com Azure OpenAI (rodar localmente)."""
from __future__ import annotations

import os
import sys

import openai
from dotenv import find_dotenv, load_dotenv
from openai import AzureOpenAI



REQUIRED_VARS = (
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_DEPLOYMENT",
)


def load_config() -> dict[str, str]:

        """Carrega e valida as variáveis de ambiente, sem expor a chave."""
        # usecwd=True procura o .env a partir da pasta em que você roda o comando
        env_path = find_dotenv(usecwd=True)
        print(f".env usado: {env_path or 'NENHUM ENCONTRADO'}")

        # override=True: variáveis já definidas no terminal/sistema NÃO vencem o .env.
        # Sem isso, um valor antigo exportado no shell silenciosamente ignora o arquivo.
        load_dotenv(env_path, override=True)

        config: dict[str, str] = {}
        for name in REQUIRED_VARS:
            # strip() remove espaços e aspas que costumam vir de copiar/colar
            value = (os.getenv(name) or "").strip().strip('"').strip("'")
            if not value:
                sys.exit(f"[config] {name} está vazia ou ausente")
            config[name] = value

        endpoint = config["AZURE_OPENAI_ENDPOINT"]
        # O SDK monta o caminho /openai/deployments/... sozinho; só a raiz do recurso entra aqui
        if not endpoint.startswith("https://") or "/openai/" in endpoint:
            sys.exit(f"[config] Endpoint suspeito: {endpoint}\n"
                    "Use só a raiz, ex.: https://meu-recurso.openai.azure.com/")


        return config


def main() -> None:
        while True:

            pergunta =  input('Pergunta: ')
            config = load_config()
            api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2025-04-01-preview").strip()

            client = AzureOpenAI(
                azure_endpoint=config["AZURE_OPENAI_ENDPOINT"],
                api_key=config["AZURE_OPENAI_API_KEY"],
                api_version=api_version,
                timeout=30.0,  # evita ficar pendurado se houver firewall/proxy
            )
            
    
            res = client.chat.completions.create(
                # No Azure, "model" é o NOME DO DEPLOYMENT, não o nome do modelo
                model=config["AZURE_OPENAI_DEPLOYMENT"],
                messages=[{"role":"system", "content": "ok"},{"role": "user", "content": pergunta }],
                # max_completion_tokens funciona em todos os modelos atuais.
                # max_tokens é rejeitado por modelos de raciocínio (o-series, gpt-5...)
                # e um limite de 10 pode ser consumido todo pelo "raciocínio" interno.
                max_completion_tokens=256,
            )
            choice = res.choices[0]
            print(f"{choice.message.content!r}")


main()