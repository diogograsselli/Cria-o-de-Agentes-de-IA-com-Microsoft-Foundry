[CONTEXT]
Você é um desenvolvedor de software responsável por criar e colocar em produção uma aplicação de Agente de IA com AZURE FOUNDRY
A aplicação utilizará um banco de dados local SQLite (` .db`) para gerenciar informações do sistema e precisará ter suas ferramentas (functions) devidamente mapeadas e documentadas antes de ir para o ar.


[OBJECTIVE]
Criar todo o código da aplicação, o banco de dados, o arquivo de documentação `README.md` e os arquivos de configuração para colocar o projeto em produção no Render.
É um sistema de agente que de IA com apis da froudry, com banco de dados sqlite3. para guardar os promts do usuario, guardar também a saida, data e hora, agente 



Sua entrega deve cobrir:


1. Mapeamento das Ferramentas: Definir a assinatura e a descrição exata em Python de 2 funções:
    - `consultar_prompt(item_id: int)` # sua aplicação vai ter a função de acordo com o seu tema
    - `verificar_prompt(item_id: int)`



2. Banco de Dados SQLite: Script de criação da tabela 'produtos' e a implementação das 2 funções realizando operações de leitura e atualização diretamente no banco `seu tema.db`.
3. Documentação Local: Um arquivo `README.md` estruturado contendo o nome do agente, suas instruções principais (System Prompt) e o detalhamento das ferramentas mapeadas.
4. Preparação para Produção no Render: Estrutura completa de arquivos para o deploy (código principal, `requirements.txt` e configurações de execução na plataforma).


[STYLE]
Código Python modular, limpo (PEP 8), com tratamento de exceções para manipulação do SQLite e comentários explicativos, interface grafica streamlit. 


[TONE]
Técnico, direto e focado em boas práticas de desenvolvimento e DevOps.


[AUDIENCE]
Avaliadores de código e ambiente de homologação/produção da plataforma Render.


[RESPONSE FORMAT]
Forneça a solução dividida estritamente nas seguintes seções:


1. **MAPEAMENTO DAS FERRAMENTAS (Python)**
    - Código das funções `funções_ relacionadas ao seu tema` e `funçao relacionada ao seu tema` integradas ao SQLite.
    - Script de inicialização da base de dados e inserção de dados de teste.
2. **DOCUMENTAÇÃO (`README.md`)**
    - Bloco de texto em Markdown pronto para salvar no repositório.
3. **CONFIGURAÇÃO PARA PRODUÇÃO (Render)**
    - Arquivo `requirements.txt`.
    - Instruções passo a passo de como subir no Render (Build Command, Start Command e observações sobre persistência do SQLite).
    - template -  streamlit


4- ** VARIAVEIS DO AMBIENTE **    
    - AZURE_OPENAI_ENDPOINT=
    - AZURE_OPENAI_API_KEY= 
    - AZURE_OPENAI_DEPLOYMENT=
    - AZURE_OPENAI_API_VERSION=



