# per 1k token pricing
MODEL_TO_PRICING: dict[str, float] = {
    "Embeddings": {
        "text-embedding-ada-002": 0.0004,
    },
    # text
    "Text": {
        "davinci": 0.02,
        "curie": 0.002,
        "babbage": 0.0005,
        "ada": 0.0004,
        # "text-davinci-003": "p50k_base",
        # "text-davinci-002": "p50k_base",
        # "text-davinci-001": "r50k_base",
        # "text-curie-001": "r50k_base",
        # "text-babbage-001": "r50k_base",
        # "text-ada-001": "r50k_base",
    },
    # code
    # "code-davinci-002": "p50k_base",
    # "code-davinci-001": "p50k_base",
    # "code-cushman-002": "p50k_base",
    # "code-cushman-001": "p50k_base",
    # "davinci-codex": "p50k_base",
    # "cushman-codex": "p50k_base",

    # edit
    # "text-davinci-edit-001": "p50k_edit",
    # "code-davinci-edit-001": "p50k_edit",
    # embeddings

    # old embeddings
    # "text-similarity-davinci-001": "r50k_base",
    # "text-similarity-curie-001": "r50k_base",
    # "text-similarity-babbage-001": "r50k_base",
    # "text-similarity-ada-001": "r50k_base",
    # "text-search-davinci-doc-001": "r50k_base",
    # "text-search-curie-doc-001": "r50k_base",
    # "text-search-babbage-doc-001": "r50k_base",
    # "text-search-ada-doc-001": "r50k_base",
    # "code-search-babbage-code-001": "r50k_base",
    # "code-search-ada-code-001": "r50k_base",
    # open source
    # "gpt2": "gpt2",
}
