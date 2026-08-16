# langchain-rag-demo
使用langchain实现RAG，其中包含了分割chunk ，embeding等多种技术，调用的是deepseek大模型  实现的本地知识库问答项目。

## 项目介绍
本项目实现了文档加载、文本切分、向量嵌入、向量库存储、检索问答完整的 RAG 流程。

> **注意：模型文件不上传至仓库，请自行下载！**

## 环境依赖
```bash
pip install langchain chromadb sentence-transformers
