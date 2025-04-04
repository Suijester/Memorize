# Memorize 📝

Memorize is a wake-word activated memo app, designed to prevent you from forgetting anything every again. Utilizing speech-to-text models to transcribe your thoughts, Memorize provides a secure and efficient way to locally capture and store information, whether technical, personal, or general. Furthermore, with in-built vector search, Memorize enables verbal querying with text-to-speech responses.

## Features
* Converts spoken memos and audio notes into text utilizing Whisper
* Stores transcribed text locally in a PostgreSQL database
* Enables vector search in response to verbal queries
* Text-to-speech responses for easy reading

## Installation

1. Clone the repository
```bash
git clone https://github.com/akisub/memocorder.git
```

2. Navigate to the repository directory
```bash
cd memocorder
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```

4. Run the app
```bash
python main.py
```


## Requirements

- [Postgres](https://www.postgresql.org/)