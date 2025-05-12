import os
from dotenv import load_dotenv
import google.generativeai as genai
from git import Repo

def gerar_mensagem_commit():
    load_dotenv()
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("The GEMINI_API_KEY environment variable is not set.")

    genai.configure(api_key=key)
    model = genai.GenerativeModel("gemini-2.0-flash")

    repo = Repo(os.getcwd())

    # Inclui arquivos staged (adicionados ou modificados)
    repo.git.add(all=True)
    diff = repo.git.diff("--cached")

    if not diff.strip():
        return "No changes detected in staged files (git diff --cached). No commit message generated."

    prompt = (
        "Can you write a short and technical commit message with a brief explanation of the changes made in the commit, "
        f"for the following diff:\n{diff}\n It's not necessary to explain the message itself, just present it for me in the format: "
        f"(feat/fix/refactor:) (commit message)\n (more details, like alist on the changhes)\n"
    )

    response = model.generate_content(
        contents=[{"role": "user", "parts": [prompt]}]
    )
    return response.text.strip()
