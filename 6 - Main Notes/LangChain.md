2024-12-29 01:21

Tags: [[NLP]] , [[DeepLearning]]


# LangChain

### Introduction: 
- Langchain is an open source framework that allows AI developers to combine LLMS like gpt 4 with external sources of computation and data.
- Is currently offered in python and typescript
### Content:
- Langchain allow you to connect alot of LLM to your own sources of data, referencing and linking your own database to the LLM, other than that you can have langchain to take action that you want to take (for instance: send email)
- How it works?
	-  taking document that you want your language model to reference, then slice it into smaller chunks, and store those chunks in a victor database, meaning they are vector embedding of text 
	- when a user ask an initial question, the vector embeddings are extracted from the question and will be used to make a similarity search in the vector database and this allow us to fetch the relevant data from the vector database, then we can use this relevant data to feed the language model now the language model have the initial question and the relevant data from the vector database 
	- ![[Pasted image 20241229014859.png]]
	- Langchain helps build app with pipeline like this, and they can take actions, not only provide answer to questions
### Value Proposition:
- Value proposition can be divided by 3 main concepts below:
![[Pasted image 20241229015147.png]]
- LLM Wrappers:
- Prompt Templates: A prompt template is a pre-defined format used to craft input prompts for the LLM. It helps in fine-tuning the model's performance by controlling what information it considers relevant during inference.
	- for example:
``` python
import os
from apikey import OPENAI_API_KEY
from langchain.llms import OpenAI
from langchain import PromptTemplate

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
# Text model example

llm = OpenAI(model_name="text-ada-001", temperature=0.9)

template = """
    Write a title for a Youtube video about {content} with {style} style.
"""

prompt_template = PromptTemplate(
    input_variables=["content", "style"],
    template=template,
)

# Example format prompt 
print(prompt_template.format(content="Deep Learning in 1 minutes", style="funny"))

```

- Chains: a chain takes a language model and a prompt template and combines them into an interface that takes input from the user and outputs an answer from the language model.
# References
