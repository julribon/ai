from transformers import pipeline, AutoConfig


def get_response(message:str) -> str:

    chat = [
        {"role": "user", "content": message}
    ]

    model = "unsloth/Mistral-Small-3.2-24B-Instruct-2506"
    #model = "Qwen/Qwen3-0.6B"

    chat_pipeline = pipeline(
        "text-generation",
        model=model
    )

    response = chat_pipeline(chat) 

    return response[0]['generated_text'][-1]['content']
