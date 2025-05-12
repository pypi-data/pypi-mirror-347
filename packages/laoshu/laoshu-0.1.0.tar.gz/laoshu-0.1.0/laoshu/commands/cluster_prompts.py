from typing import List
from laoshu.clustering.clustering import Clustering
from laoshu.clustering.embeddings import Embeddings
from laoshu.clustering.topic_modeling import TopicModeling
from laoshu.data import InputData, PromptCluster
from laoshu.display.progress import ProgressIndicator
from laoshu.prompts import render_template
from laoshu.clustering.grouping import group_by


class ClusterPromptsCommand:
    def __init__(self, progress: ProgressIndicator):
        self.progress = progress
        self.clustering = Clustering(
            embeddings=Embeddings.get_embeddings(),
            min_number_of_clusters=3,
            max_number_of_clusters="sqrt",
        )
        self.topic_modeling = TopicModeling()

    async def execute(self, input_data: InputData) -> List[PromptCluster]:
        self.input_data = input_data

        task = self.progress.start("Clustering prompts")
        try:
            rendered_prompts = [
                render_template(self.input_data, session)
                for session in self.input_data.sessions
            ]
            clusters = await self.clustering.cluster(rendered_prompts)

            sessions_with_cluster_id = [
                (session.id, cluster)
                for session, cluster in zip(self.input_data.sessions, clusters)
            ]
            session_ids_grouped_by_cluster_id = group_by(
                sessions_with_cluster_id, key=lambda x: x[1], value=lambda x: x[0]
            )

            cluster_topics = await self.topic_modeling.describe_prompt_clusters(
                rendered_prompts, clusters
            )

            result = []
            for cluster_id, cluster_topic in cluster_topics:
                result.append(
                    PromptCluster(
                        cluster_id=cluster_id,
                        description=cluster_topic,
                        session_ids=session_ids_grouped_by_cluster_id[cluster_id],
                    )
                )
            return result
        except Exception as e:
            raise e
        finally:
            task.finish()
