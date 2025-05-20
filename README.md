# 🧾 RPA Challenge - Extração de Faturas

Este projeto é parte de um teste técnico para a vaga de Desenvolvedor RPA Júnior. O objetivo é automatizar o processo de **extração de faturas** (imagens) a partir de uma página web, armazenando os arquivos localmente e consolidando os dados em um arquivo `.csv`.

---

## 📌 Objetivos

- Acessar uma página web com uma lista de faturas.
- Realizar o download das imagens (faturas).
- Salvar os arquivos localmente.
- Gerar um arquivo csv.

---

## ⚙️ Tecnologias Utilizadas

- Python 3.11
- `aiohttp` – para download assíncrono das faturas
- `asyncio` – para execução paralela
- `pandas` – para geração do arquivo CSV
- `selenium` – para automação de navegador

---

## 🔧 Como Executar

### 1. Clone o repositório

### 2. Instale as dependencias
pip install -r requirements.txt

### 3. Execute a aplicação
python main.py ou python3 main.py

### 4. Resultados
A aplicação criará uma pasta chamada invoices contendo o csv e as faturas baixadas


