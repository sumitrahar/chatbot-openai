# Simple Chatbot

A natural language to SQL query conversion system using OpenAI's GPT model and PostgreSQL database.

## Features

- Natural language to SQL conversion
- PostgreSQL database integration
- Interactive chatbot interface
- Secure credential management

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your credentials:
```
DB_HOST=127.0.0.1
DB_NAME=nba_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_PORT=5432

OPENAI_API_TYPE=azure
OPENAI_API_BASE=your_api_base
OPENAI_API_KEY=your_api_key
OPENAI_API_VERSION=2023-09-01-preview
```

3. Run the application:
```bash
python main.py
```

## Usage

Ask questions in natural language, for example:
- "What is Ram's salary from the CSE department?"
- "Show all employees in the IT department"

## License

MIT License 