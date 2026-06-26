"""
_claude.py — Wrapper headless do Claude Code (`claude -p`) com extração de JSON.

Cada agente do pipeline (ORACLE, SCRIPT, INK) usa este wrapper pra fazer
chamadas estruturadas ao Claude e obter JSON validado de volta.
"""
import subprocess
import json
import re
import shlex
from pathlib import Path


class ClaudeError(Exception):
    pass


def call_claude(prompt: str, model: str = "claude-opus-4-7", timeout: int = 180) -> str:
    """Faz uma chamada não-interativa ao Claude e retorna o texto da resposta.

    Args:
        prompt: Prompt completo (system + user)
        model: model id (default opus). Use 'claude-sonnet-4-6' se quiser mais barato/rápido.
        timeout: segundos antes de matar o processo

    Returns:
        Texto cru da resposta (campo `result` do JSON do claude -p)

    Raises:
        ClaudeError se claude falhar ou retornar erro
    """
    try:
        proc = subprocess.run(
            ["claude", "-p", prompt, "--output-format", "json", "--model", model],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        raise ClaudeError(f"claude -p timeout ({timeout}s)")
    except FileNotFoundError:
        raise ClaudeError("claude CLI não encontrado no PATH")

    if proc.returncode != 0:
        raise ClaudeError(f"claude -p falhou (rc={proc.returncode}): {proc.stderr[:500]}")

    try:
        data = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        raise ClaudeError(f"claude retornou stdout não-JSON: {proc.stdout[:300]}")

    if data.get("is_error"):
        raise ClaudeError(f"claude reportou erro: {data.get('result', proc.stdout[:300])}")

    return data["result"]


def extract_json(text: str) -> dict | list:
    """Extrai um objeto JSON de um texto possivelmente com markdown/explicação."""
    # Tenta parse direto
    try:
        return json.loads(text.strip())
    except json.JSONDecodeError:
        pass

    # Tenta extrair de bloco ```json ... ```
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Tenta achar primeiro { ou [ até o último } ou ]
    for open_char, close_char in (("{", "}"), ("[", "]")):
        start = text.find(open_char)
        end = text.rfind(close_char)
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                continue

    raise ClaudeError(f"Não consegui extrair JSON de:\n{text[:500]}")


def call_claude_json(prompt: str, **kwargs) -> dict | list:
    """call_claude + extract_json em um só passo."""
    text = call_claude(prompt, **kwargs)
    return extract_json(text)


def load_prompt_template(name: str) -> str:
    """Carrega um prompt template de prompts/<name>.md."""
    path = Path(__file__).parent / "prompts" / f"{name}.md"
    return path.read_text(encoding="utf-8")
