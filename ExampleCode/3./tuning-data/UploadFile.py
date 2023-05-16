import os
import openai
openai.api_key = ''
openai.File.create(
  file=open("qa_data_prepared.jsonl", "rb"),
  purpose='fine-tune'
)
