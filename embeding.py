from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
import os

# 1、加载文档
loader = TextLoader("./藜麦.txt",encoding="utf-8")
documents = loader.load()

# 2、文本分割
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=128,
    chunk_overlap=50,
    separators=["\n\n", "\n", "。", "！", "？"]
)
# 标准分割方法，自动处理全部文档
texts = text_splitter.split_documents(documents)

# 打印分割结果
# print(f"一共分割出 {len(texts)} 个块")
# for i,chunk in enumerate(texts):
#     print(f"\n=====第{i+1}块=====")
#     print(chunk.page_content)

# 3、加载本地Embedding模型
model_path = r"G:\力扣代码集\langchain实现RAG\download_model\m3e-base"
if not os.path.exists(model_path):
    raise FileNotFoundError(f"模型路径不存在: {model_path}")

model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': True}

embedding = HuggingFaceEmbeddings(
    model_name=model_path,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)

# 4、存入Chroma向量库，持久化到本地文件夹
db = Chroma.from_documents(
    texts,
    embedding,
    persist_directory="./chroma_db"
)

# 5、相似度检索
res = db.similarity_search("藜麦的主要病害是什么，如何防治？",k=3)

# print(f"检索到 {len(res)} 条相似内容")

print("\n====检索结果====")
for doc in res:
    print(doc.page_content)





from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

llm = ChatOpenAI(
    model="deepseek-v4-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key="sk-4dd57089c268444aa7f7da008cecff68",
    base_url="https://api.deepseek.com"
)

retriever = db.as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_template("""
你是知识库问答助手，请严格依据下面的上下文回答用户问题。
上下文：{context}
问题：{question}
""")

def format_docs(docs):
    return "\n\n".join([doc.page_content for doc in docs])

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

#提问
result = rag_chain.invoke("藜麦的主要病害是什么，如何防治？")
print(result)





















