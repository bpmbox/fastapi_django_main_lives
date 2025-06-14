import os

from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from groq import Groq

def test_prompt(prompt,question):
    client = Groq(api_key=os.getenv("api_key"))
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": prompt+"　毎回日本語で答える事"
            },
            {
                "role": "user",
                "content": question
            },
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    print(completion.choices[0].message)
    return completion.choices[0].message.content
        


def prompt_genalate(word,sys_prompt="あなたはプロンプト作成の優秀なアシスタントです。答えは日本語で答えます"):
    # Get Groq API key
    groq_api_key = os.getenv("api_key")
    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name="llama3-70b-8192")

    system_prompt = sys_prompt
    conversational_memory_length = 50

    memory = ConversationBufferWindowMemory(
        k=conversational_memory_length, memory_key="chat_history", return_messages=True
    )

    #while True:
    user_question = word#input("質問を入力してください: ")

    #if user_question.lower() == "exit":
    #    print("Goodbye!")
    #    break

    if user_question:
        # Construct a chat prompt template using various components
        prompt = ChatPromptTemplate.from_messages(
            [
                # 毎回必ず含まれるSystemプロンプトを追加
                SystemMessage(content=system_prompt),
                # ConversationBufferWindowMemoryをプロンプトに追加
                MessagesPlaceholder(variable_name="chat_history"),
                # ユーザーの入力をプロンプトに追加
                HumanMessagePromptTemplate.from_template("{human_input}"),
            ]
        )
        

        # プロンプトを文字列としてフォーマット
        #formatted_prompt = prompt.format(chat_history=memory.load_memory_variables(), human_input=user_question)

        #print("Formatted Prompt:\n", formatted_prompt)


        conversation = LLMChain(
            llm=groq_chat,
            prompt=prompt,
            verbose=False,
            memory=memory,
        )
        response = conversation.predict(human_input=user_question)

        print("User: ", user_question)
        print("Assistant:", response)

        return user_question,user_question+"\r\n[役割]\r\n"+response
