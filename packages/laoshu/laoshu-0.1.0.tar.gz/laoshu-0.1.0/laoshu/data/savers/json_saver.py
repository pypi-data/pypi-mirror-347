from laoshu.data import PromptCluster
from typing import List


def save_prompt_clusters(prompt_clusters: List[PromptCluster], file_path: str):
    with open(file_path, "w") as f:
        for prompt_cluster in prompt_clusters:
            f.write(prompt_cluster.model_dump_json())
