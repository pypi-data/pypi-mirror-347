from math import sqrt
from typing import Optional
import numpy as np
from sklearn.cluster import KMeans  # type: ignore
from sklearn.metrics import silhouette_score  # type: ignore
from laoshu.clustering.embeddings import Embeddings
from typing import List, Union
from laoshu.config import logger
from laoshu.display.progress import ProgressIndicator


class Clustering:
    def __init__(
        self,
        embeddings: Embeddings,
        min_number_of_clusters: int = 3,
        max_number_of_clusters: Union[int, str, None] = "sqrt",
        progress_indicator: Optional[ProgressIndicator] = None,
    ):
        """
        Args:
            embeddings: Embeddings object
            min_number_of_clusters: Minimum number of clusters to try
            max_number_of_clusters: Maximum number of clusters to try
            progress_indicator: Progress indicator to use

            The max number of clusters is either a number or "sqrt" to use the square root of the number of data points.
            When the max number of clusters is None, the range will be from min_number_of_clusters to the number of data points - 1.
        """
        self.embeddings = embeddings
        self.min_number_of_clusters = min_number_of_clusters
        self.max_number_of_clusters = max_number_of_clusters
        self.progress_indicator = (
            progress_indicator
            if progress_indicator is not None
            else ProgressIndicator.create()
        )

    def __get_n_clusters_range(self, data_length: int) -> range:
        if self.max_number_of_clusters == "sqrt":
            return range(self.min_number_of_clusters, int(sqrt(data_length)) + 1)
        elif self.max_number_of_clusters is None:
            return range(self.min_number_of_clusters, data_length + 1)
        else:
            return range(self.min_number_of_clusters, int(self.max_number_of_clusters))

    async def cluster(self, data: List[str]) -> List[int]:
        n_clusters_range = self.__get_n_clusters_range(len(data))
        cluster_with_max_silhouette = (0, 0, None)
        if len(n_clusters_range) == 0:
            raise ValueError(
                "No valid number of clusters found. Increase the number of input data points."
            )

        logger.debug("Embedding data...")
        X = await self.embeddings.embed(data)

        logger.info(
            f"Clustering data with {len(X)} data points into {n_clusters_range} clusters..."
        )
        progress = self.progress_indicator.start(
            "Clustering data...", len(n_clusters_range)
        )

        try:
            for n_clusters in n_clusters_range:
                progress.update()
                logger.info(
                    f"Clustering data with {len(X)} data points into {n_clusters} clusters..."
                )

                kmeans = KMeans(n_clusters=n_clusters, random_state=1234)
                cluster_labels = kmeans.fit_predict(X)

                silhouette_avg = silhouette_score(np.array(X), cluster_labels)
                if silhouette_avg >= cluster_with_max_silhouette[1]:
                    cluster_with_max_silhouette = (
                        n_clusters,
                        silhouette_avg,
                        cluster_labels,
                    )

            if cluster_with_max_silhouette[2] is None:
                raise ValueError("No valid clusters found")

            logger.info(
                f"Found {cluster_with_max_silhouette[0]} clusters with the highest silhouette score of {cluster_with_max_silhouette[1]}"
            )
            return cluster_with_max_silhouette[2].tolist()
        finally:
            progress.finish()
