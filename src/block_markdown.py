def markdown_to_blocks(markdown:str)->list[str]:
    blocks = markdown.split("\n\n")
    blocks = list(map(lambda block: block.strip(), blocks))
    result = []
    for block in blocks:
        if block != "":
            result.append(block)
    return result