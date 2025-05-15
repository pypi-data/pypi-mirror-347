# Chat

Methods:

- <code title="post /api/chat/completions">client.chat.<a href="./src/scholarai/resources/chat.py">create_completion</a>(\*\*<a href="src/scholarai/types/chat_create_completion_params.py">params</a>) -> None</code>

# Fulltext

Types:

```python
from scholarai.types import PaperContent
```

Methods:

- <code title="get /api/fulltext">client.fulltext.<a href="./src/scholarai/resources/fulltext.py">retrieve</a>(\*\*<a href="src/scholarai/types/fulltext_retrieve_params.py">params</a>) -> <a href="./src/scholarai/types/paper_content.py">PaperContent</a></code>

# Question

Methods:

- <code title="get /api/question">client.question.<a href="./src/scholarai/resources/question.py">ask</a>(\*\*<a href="src/scholarai/types/question_ask_params.py">params</a>) -> <a href="./src/scholarai/types/paper_content.py">PaperContent</a></code>

# Abstracts

Types:

```python
from scholarai.types import PaperMetadata, AbstractSearchResponse
```

Methods:

- <code title="get /api/abstracts">client.abstracts.<a href="./src/scholarai/resources/abstracts.py">search</a>(\*\*<a href="src/scholarai/types/abstract_search_params.py">params</a>) -> <a href="./src/scholarai/types/abstract_search_response.py">AbstractSearchResponse</a></code>

# Patents

Types:

```python
from scholarai.types import PatentListResponse
```

Methods:

- <code title="get /api/patents">client.patents.<a href="./src/scholarai/resources/patents.py">list</a>(\*\*<a href="src/scholarai/types/patent_list_params.py">params</a>) -> <a href="./src/scholarai/types/patent_list_response.py">PatentListResponse</a></code>

# SaveCitation

Types:

```python
from scholarai.types import SaveCitationRetrieveResponse
```

Methods:

- <code title="get /api/save-citation">client.save_citation.<a href="./src/scholarai/resources/save_citation.py">retrieve</a>(\*\*<a href="src/scholarai/types/save_citation_retrieve_params.py">params</a>) -> <a href="./src/scholarai/types/save_citation_retrieve_response.py">SaveCitationRetrieveResponse</a></code>

# AddToProject

Types:

```python
from scholarai.types import AddToProjectCreateResponse, AddToProjectRetrieveResponse
```

Methods:

- <code title="post /api/add_to_project">client.add_to_project.<a href="./src/scholarai/resources/add_to_project.py">create</a>(\*\*<a href="src/scholarai/types/add_to_project_create_params.py">params</a>) -> <a href="./src/scholarai/types/add_to_project_create_response.py">AddToProjectCreateResponse</a></code>
- <code title="get /api/add_to_project">client.add_to_project.<a href="./src/scholarai/resources/add_to_project.py">retrieve</a>(\*\*<a href="src/scholarai/types/add_to_project_retrieve_params.py">params</a>) -> <a href="./src/scholarai/types/add_to_project_retrieve_response.py">AddToProjectRetrieveResponse</a></code>

# CreateProject

Methods:

- <code title="post /api/create_project">client.create_project.<a href="./src/scholarai/resources/create_project.py">create</a>(\*\*<a href="src/scholarai/types/create_project_create_params.py">params</a>) -> None</code>

# AnalyzeProject

Types:

```python
from scholarai.types import AnalyzeProjectBatchAnalyzeResponse
```

Methods:

- <code title="get /api/analyze_project">client.analyze_project.<a href="./src/scholarai/resources/analyze_project.py">batch_analyze</a>(\*\*<a href="src/scholarai/types/analyze_project_batch_analyze_params.py">params</a>) -> <a href="./src/scholarai/types/analyze_project_batch_analyze_response.py">AnalyzeProjectBatchAnalyzeResponse</a></code>
