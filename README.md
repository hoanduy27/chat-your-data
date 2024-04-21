# Chat-Your-Data

Chat with your data.

## Technologies
- LangChain
- FAISS

## How to run

- Get OpenAI API Key, you need to type it inside the app.

- Get LangSmith API Key by registering your account at https://api.smith.langchain.com.

- Create ".env" file and fill the following information

```sh
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY=<YOUR LANGSMITH API KEY>
```

Ok, time to run!

```
docker compose up -d
```

Your application starts at `localhost:8501`. To check log, use:

```
docker logs -f chat-your-data-app-1
```