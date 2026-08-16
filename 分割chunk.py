from langchain_community.document_loaders import TextLoader
loader = TextLoader("./藜麦.txt")
documents = loader.load()
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=128,  # 根据嵌入模型调整（如text-embedding-ada-002支持8191）
    chunk_overlap=50,
    separators=["\n\n", "\n", "。 ", "! ", "? ","//"]  # 优化分隔符
)

texts = text_splitter.create_documents([documents[0].page_content],metadatas=[documents[0].metadata])
# 关键步骤: 提取所有文本内容


# =====加上这两行，打印分割结果=====
print(f"一共分割出 {len(texts)} 个块")
for i,chunk in enumerate(texts):
    print(f"\n=====第{i+1}块=====")
    print(chunk.page_content)




