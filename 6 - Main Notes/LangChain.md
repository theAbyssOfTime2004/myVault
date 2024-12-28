2024-12-29 01:21


Tags: [[NLP]] 

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
- 
# References
