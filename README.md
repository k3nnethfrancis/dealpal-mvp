# dealpal MVP

## install requirements
* `pip install -r backend/requirements.txt`

## environment vars
* update .env.example to .env and add your OPENAI_API_KEY
* also add your SEARCHAPI_API_KEY. Get a free account from https://www.searchapi.io/

## create a new agent
* use existing/update/modify `ari.yaml` in `agents/` folder
* run create.py with `python -m backend.create`

## run the chat
* run chat.py with `python -m backend.chat`

## run the web app
* run app.py with `python -m uvicorn backend.app:app -- reload`

## run the frontend
* run `cd frontend`
* run `npm run dev` in the frontend folder


# To Do
- ~~Fix the error with the frontend~~
- ~~Add file uploads to the frontend~~
- ~~Add file upload for assistant to backend~~
- ~~Add web search tool to backend~~
- Add web search tool to frontend
- Add a way to save the chat history / outputs from the log e.g., click specific message and 'save to drafts'
- add filtering buttons to the frontend