from typing import List, Tuple, Dict
from laoshu.baml_client.async_client import b
from laoshu.baml_client.types import Prompts

MAX_TOKENS_PER_PROMPT = 128000  # gpt-4o-mini token limit
WORDS_TO_TOKENS_RATIO = 1.3  # rule of thumb for converting words to tokens
TOKEN_BUFFER = 0.8  # 1 - TOKEN_BUFFER: buffer to account for variable token usage and the prompt instructions


class TopicModeling:
    async def describe_prompt_clusters(
        self, text_data: List[str], cluster_ids: List[int]
    ) -> List[Tuple[int, str]]:
        if self.__does_fit_in_one_prompt(text_data):
            return await self.__describe_prompt_clusters_one_by_one(
                text_data, cluster_ids
            )
        else:
            return await self.__describe_prompt_clusters_multiple(
                text_data, cluster_ids
            )

    async def __describe_prompt_clusters_one_by_one(
        self, text_data: List[str], cluster_ids: List[int]
    ) -> List[Tuple[int, str]]:
        clusters = self.__group_by_cluster_id(text_data, cluster_ids)

        results = []
        tasks = []
        for cluster_id, cluster_texts in clusters.items():
            tasks.append((cluster_id, self.__describe_prompt_cluster(cluster_texts)))

        for cluster_id, task in tasks:
            description = await task
            results.append((cluster_id, description))

        return results

    async def __describe_prompt_clusters_multiple(
        self, text_data: List[str], cluster_ids: List[int]
    ) -> List[Tuple[int, str]]:
        clusters = self.__group_by_cluster_id(text_data, cluster_ids)
        cluster_ids_list = list(clusters.keys())

        cluster_contents: List[Prompts] = [
            Prompts(content=clusters[cluster_id]) for cluster_id in cluster_ids_list
        ]
        response = await b.DescribeMultiplePromptsClusters(cluster_contents)
        return list(
            zip(cluster_ids_list, [cluster.description for cluster in response])
        )

    def __does_fit_in_one_prompt(self, text_data: List[str]) -> bool:
        total_words = sum(len(text.split()) for text in text_data)
        total_tokens = total_words * WORDS_TO_TOKENS_RATIO * TOKEN_BUFFER
        return total_tokens <= MAX_TOKENS_PER_PROMPT

    def __group_by_cluster_id(
        self, text_data: List[str], cluster_ids: List[int]
    ) -> Dict[int, List[str]]:
        clusters: Dict[int, List[str]] = {}
        for cluster_id, text in zip(cluster_ids, text_data):
            if cluster_id not in clusters:
                clusters[cluster_id] = []
            clusters[cluster_id].append(text)
        return clusters

    async def __describe_prompt_cluster(self, cluster_texts: List[str]) -> str:
        response = await b.DescribePromptsCluster(Prompts(content=cluster_texts))
        return response.description
