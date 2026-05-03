from transformers import AutoModel
import torch

model = AutoModel.from_pretrained(
    "jinaai/jina-embeddings-v5-text-small",
    trust_remote_code=True,
    _attn_implementation="flash_attention_2",  # Recommended but optional
    dtype=torch.bfloat16,  # Recommended for GPUs
)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = model.to(device=device)

# Optional: set truncate_dim and max_length in encode() to control embedding size and input length

# ========================
# 1. Retrieval Task
# ========================
# Encode query
query_embeddings = model.encode(
    texts=["Overview of climate change impacts on coastal cities"],
    task="retrieval",
    prompt_name="query",
)
# Encode document
document_embeddings = model.encode(
    texts=[
        "Climate change has led to rising sea levels, increased frequency of extreme weather events..."
    ],
    task="retrieval",
    prompt_name="document",
)

# ========================
# 2. Text Matching Task
# ========================
texts = [
    "غروب جميل على الشاطئ",  # Arabic
    "海滩上美丽的日落",  # Chinese
    "Un beau coucher de soleil sur la plage",  # French
    "Ein wunderschöner Sonnenuntergang am Strand",  # German
    "Ένα όμορφο ηλιοβασίλεμα πάνω από την παραλία",  # Greek
    "समुद्र तट पर एक खूबसूरत सूर्यास्त",  # Hindi
    "Un bellissimo tramonto sulla spiaggia",  # Italian
    "浜辺に沈む美しい夕日",  # Japanese
    "해변 위로 아름다운 일몰",  # Korean
]
text_embeddings = model.encode(texts=texts, task="text-matching")

# ========================
# 3. Classification Task
# ========================
texts = [
    "My order hasn't arrived yet and it's been two weeks.",
    "How do I reset my password?",
    "I'd like a refund for my recent purchase.",
    "Your product exceeded my expectations. Great job!",
]
classification_embeddings = model.encode(texts=texts, task="classification")

# ========================
# 4. Clustering Task
# ========================
texts = [
    "We propose a novel neural network architecture for image segmentation.",
    "This paper analyzes the effects of monetary policy on inflation.",
    "Our method achieves state-of-the-art results on object detection benchmarks.",
    "We study the relationship between interest rates and housing prices.",
    "A new attention mechanism is introduced for visual recognition tasks.",
]
clustering_embeddings = model.encode(texts=texts, task="clustering")
