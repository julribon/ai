import lmstudio as lms

def get_response(prompt:str) -> str:

    model = lms.llm("mistralai/mistral-small-3.2")
    response = model.respond(prompt)

    return response.content
