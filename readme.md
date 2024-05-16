# speech_to_text

Este projeto utiliza a engine Whisper da OpenAI e a biblioteca MoviePy para transcrever áudios de arquivos `.mp4` e gerar arquivos de texto amigáveis ao usuário final. O processo inclui dividir os arquivos de áudio, transcrevê-los e formatar as transcrições.

## Estrutura do Projeto	
peech_to_text/
├── input
│   └── [arquivos .mp4]
├── output
│   └── [arquivos gerados]
├── temp_audio
│   └── [arquivos temporários gerados]
├── main.py
└── README.md

- `input`: Diretório onde você deve colocar os arquivos `.mp4` que serão processados.
- `output`: Diretório onde os arquivos de transcrição formatados serão salvos.
- `temp_audio`: Diretório temporário usado para armazenar clipes de áudio divididos.
- `main.py`: Script principal que executa todo o processo de transcrição.
- `README.md`: Este arquivo de documentação.

## Pré-requisitos

Antes de começar, certifique-se de ter os seguintes softwares instalados:

- Python 3.6 ou superior
- pip (Python package installer)

## Instalação

1. Clone o repositório para o seu ambiente local:
   ``` bash
   git clone https://github.com/seu-usuario/speech_to_text.git
    ```

2.	Navegue até o diretório do projeto:
    ``` bash
    cd speech_to_text
    ```
3.	Crie um ambiente virtual:
    ``` bash
    python -m venv venv
    ``` 
4.	Ative o ambiente virtual:
	
    •	No Windows:
    ``` bash
    venv\Scripts\activate
    ```
    •	No macOS/Linux:
    ``` bash
    source venv/bin/activate
    ```
5.	Instale as dependências necessárias:
    ``` bash
    pip install -r requirements.txt
    ```
## Uso

1.	Coloque os arquivos .mp4 que você deseja processar na pasta input.
2.	Execute o script principal:
    ``` bash
    python main.py
    ```
3.	Os arquivos de transcrição serão gerados na pasta output.


## Estrutura do Código

### Funções Principais

	•	converter_segundos_para_tempo(segundos): Converte segundos em uma string no formato hh:mm:ss.
	•	save_subtitles(list_of_subtitles, path_to_save): Salva a transcrição dos áudios em um único arquivo.
	•	split_audio_file(path, temp_audio_dir): Divide um arquivo de áudio em vários clipes.
	•	transcribe_audio_with_whisper(base_path_to_saved_files, subtitles_path): Transcreve áudios em .mp3 utilizando a engine Whisper da OpenAI.
	•	processar_arquivo_origem(caminho_arquivo_origem): Lê o arquivo de origem e retorna uma lista de textos com marcações de tempo.
	•	escrever_arquivo_destino(textos_com_marcacoes, caminho_arquivo_destino): Escreve os textos com marcações de tempo em um novo arquivo.

### Fluxo do Programa

	1.  Cria as pastas input, output e temp_audio se não existirem.
	2.  Verifica se há arquivos .mp4 na pasta input. Se estiver vazia, informa ao usuário e encerra a execução.
	3.  Para cada arquivo .mp4 na pasta input:
        •   Divide o áudio em clipes menores.
	    •   Transcreve os clipes usando Whisper.
	    •   Formata a transcrição em um arquivo amigável ao usuário.
	    •   Salva os arquivos gerados na pasta output.

## Contribuição

Sinta-se à vontade para contribuir com o projeto. Você pode fazer isso de várias maneiras:

	•	Reportando problemas
	•	Enviando solicitações de funcionalidades
	•	Criando pull requests

## Licença

Este projeto está licenciado sob a MIT License. Veja o arquivo LICENSE para mais detalhes.

Autor: Seu Nome
Contato: seu.email@exemplo.com