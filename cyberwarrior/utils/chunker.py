def chunk_code(text: str, chunk_size: int = 300):
    lines = text.split("\n")
    for i in range(0, len(lines), chunk_size):
        yield "\n".join(lines[i:i + chunk_size])
