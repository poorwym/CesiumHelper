# CesiumHelper

这个是非常可怜的poorwym制作的CesiumHelper。

请按照以下步骤克隆仓库

```
git clone https://github.com/poorwym/CesiumHelper.git
cd CesiumHelper
git submodule update --init --recursive
```

项目分为三部分；
- 1、URLcollection
用于从html中提取所有的url。
具体参照那个文件夹下的README.md
- 2、web2embeddings
用于将大量网站列表转化成embedding
但是只需要到全部转化成markdown文档那步即可。
- 3、CesiumRAG
用于构建RAG与交互。

所有的操作都要在对应部分的文件夹内完成。
