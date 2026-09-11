import os


def load_prompt_template(template_name: str, base_path: str) -> str:
    file_path = os.path.join(base_path, f"{template_name}.txt")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Prompt template not found at {file_path}")
        return ""
