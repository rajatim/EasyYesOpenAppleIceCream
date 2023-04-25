import Settings
import openai
from spacy.lang.en import English
from spacy.lang.zh import Chinese
import langid
import json


openai.api_key = Settings.CHATGPT_API_KEY

engine="text-davinci-003"
max_tokens = 200
temperature = 0.7
n = 1
stop=None
top_p=1.0
frequency_penalty=1.0
presence_penalty=1.0

want_tokens = 4096
lang = ""
chat_start = "***"
chat_jin = ";;"
chat_end = "---"
chatend_prompt = "。繁體中文，內容開始使用" + chat_start + "，內容結束使用" + chat_end
# chatend_prompt = "When the story ends, use " + chatend + " as the identifier."

def detect_chat_end(text):
    if chat_end in text:
        return True
    else:
        return False
def detect_language(text):
    lang, _ = langid.classify(text)
    return lang
def count_tokens(text):
    lang = detect_language(text)
    # print("Language of text: ", lang)

    if lang == "zh":
        nlp = Chinese()
    else:
        nlp = English()

    doc = nlp(text)
    tokens = [token.text for token in doc]

    return len(tokens)

def chat_with_gpt(prompt):
    curr_token = count_tokens(prompt)
    # print("Request used token {}, left {}".format(curr_token, (max_tokens - curr_token)))

    response = openai.Completion.create(
        engine=engine,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        n=n,
        stop=stop,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty,
    )

    # print(response)
    message = response.choices[0].text.strip()

    if len(response.choices) == 0:
        raise Exception("Exceeded max_tokens")

    return message


def prompt_with_gpt(original_prompt):
    prompt = original_prompt + chatend_prompt
    base_PROMPT = f"{prompt}{chat_jin}{chat_start}"
    while True:
        response = chat_with_gpt(prompt).replace('\n', '')
        prompt = f"{prompt}{chat_jin}{response}"
        if detect_chat_end(response):
            break
    return prompt.lstrip(base_PROMPT).strip(chat_end).replace(chat_jin, "").replace(chat_start, "").replace(chat_end, "").strip()
