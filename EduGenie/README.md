# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a FastAPI + HTML/CSS/JavaScript educational assistant based on the supplied project document. It offers question answering, simplified explanations, three-question MCQ quizzes, text summaries, and learning roadmaps.

## Requirements
- Python 3.10 or newer
- A Google Gemini API key for AI-powered responses (create one in Google AI Studio)
- VS Code (recommended)

## Run in VS Code (Windows)
1. Extract the `EduGenie.zip` archive and open the **EduGenie** folder in VS Code.
2. Open **Terminal → New Terminal**.
3. Create and activate a virtual environment:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt instead with `.venv\Scripts\activate.bat`, or run `.venv\Scripts\python.exe -m pip ...` directly.
4. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
5. Create your environment file by copying `.env.example` to `.env` and set `GEMINI_API_KEY` to your own key. Keep `.env` private; it is excluded from Git.
6. Start the server:

   ```powershell
   uvicorn main:app --reload
   ```
7. Open **http://127.0.0.1:8000** in your browser. Interactive API documentation is at **http://127.0.0.1:8000/docs**.

## macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
cp .env.example .env
# Edit .env and set GEMINI_API_KEY
uvicorn main:app --reload
```

## Configure the AI
`.env` settings:
- `GEMINI_API_KEY`: your private Google AI Studio API key.
- `GEMINI_MODEL`: defaults to `gemini-2.5-flash`; set this to a model currently available to your key/account.
- `EXPLANATION_PROVIDER`: `gemini` (recommended default) or `local`.
- `LOCAL_MODEL_FALLBACK=true`: when local model loading fails, use Gemini instead.

The original document names Gemini 1.5 Pro, but model availability changes. Configure a supported model in `.env`; no Python edits are required. The optional local LaMini-Flan-T5 model downloads its weights on first use and may require several GB of free disk space and memory. To install optional local dependencies, run `pip install -r requirements-local.txt`. The app defaults to Gemini for simpler installation.

## API endpoints
All POST endpoints accept JSON and return `{"result": ...}`.

| Method | Endpoint | JSON body |
|---|---|---|
| GET | `/health` | — |
| POST | `/qa` | `{"question":"Which is the largest ocean?"}` |
| POST | `/explain` | `{"text":"Photosynthesis","level":"beginner"}` |
| POST | `/quiz` | `{"text":"The Pythagorean theorem relates the sides of a right triangle."}` |
| POST | `/summarize` | `{"text":"Paste an educational passage here."}` |
| POST | `/learn/recommendations` | `{"text":"SQL","level":"beginner"}` |

## Test
With the virtual environment active:

```bash
pytest -q
```

The tests cover the homepage, health endpoint, input validation, and a mocked Q&A response. They do not call Gemini or require a real API key. To test real AI, set the key in `.env`, start the server, and use the web interface or `/docs`.

Example health check from another terminal:

```bash
curl http://127.0.0.1:8000/health
```

## Troubleshooting
- **Gemini is not configured**: confirm `.env` exists in the project root and `GEMINI_API_KEY` contains your key, then restart Uvicorn.
- **Model not found / unsupported**: change `GEMINI_MODEL` to a currently available model in Google AI Studio.
- **Quota / permission errors**: verify API access and billing/quota status for your key.
- **Port in use**: run `uvicorn main:app --reload --port 8001` and open port 8001.
- **Local model fails to load**: switch `EXPLANATION_PROVIDER=gemini`, or install `requirements-local.txt` and enable fallback.

## Project structure

```text
EduGenie/
├── main.py
├── ai_client.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   └── index.html
├── static/
│   └── style.css
└── tests/
    └── test_api.py
```
