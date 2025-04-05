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
git clone https://github.com/Suijester/memocorder.git
```

2. Navigate to the repository directory
```bash
cd memocorder
```

3. Install the dependencies
```bash
pip install -r requirements.txt
```

4. Initialize the models
```bash
python initializeModels.py
```

5. Download Postgres
```bash
brew install postgresql
```

6. Create the 'memos' database
```bash
createdb memos
```

7. Run the app whenever you want to generate memos
```bash
python main.py
```

## Usage

1. Run the app whenever you want to generate, delete, or query memos
```bash
python main.py
```

2. While the app is listening, either say 'start memo' to record, 'delete memo' to delete, or 'query' to query

3. If recording a new memo, the app will transcribe the audio and save it to the database either when the user goes quiet or says 'end memo'

4. If deleting a memo, say 'delete memo' and then ask your question, the app will delete the most relevant memo based on keywords (so the memo most similar to your query for deletion, e.g. 'delete the memo where I talked about keys', and it'll look for the memo most similar) from the database and remove the audio file either when the user goes quiet or says 'end deletion'

5. If querying, say 'query' and then ask your question, the app will return the most relevant memo based on the query, utilizing vector search (effectiveness may vary, due to embedding quality of 768 dimensions)

## Requirements

- [Postgres](https://www.postgresql.org/)
- [Python](https://www.python.org/)

## Acknowledgements

- [Whisper](https://github.com/openai/whisper)
- [pgvector](https://github.com/pgvector/pgvector)
- [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy)
- [SimpleAudio](https://github.com/simpleaudio/simpleaudio)
- [SoundDevice](https://github.com/sounddevice/sounddevice)
- [Wave](https://github.com/PyCQA/wave) 