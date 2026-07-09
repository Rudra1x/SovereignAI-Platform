from __future__ import annotations

from collections import Counter

from sovereign.data.dataset.dataset import Dataset


class DatasetStatistics:

    def compute(
        self,
        dataset: Dataset,
    ) -> dict:

        total_samples = len(dataset)

        total_messages = 0
        total_characters = 0

        task_distribution = Counter()
        language_distribution = Counter()

        quality_scores = []

        for record in dataset:

            task_distribution[
                record.sample_type.value
            ] += 1

            language_distribution[
                record.metadata.language
            ] += 1

            quality_scores.append(
                record.metadata.quality_score
            )

            total_messages += len(
                record.conversation.messages
            )

            for message in record.conversation.messages:

                total_characters += len(
                    message.content
                )

        average_messages = (
            total_messages / total_samples
            if total_samples
            else 0
        )

        average_characters = (
            total_characters / total_messages
            if total_messages
            else 0
        )

        average_quality = (
            sum(quality_scores) / len(quality_scores)
            if quality_scores
            else 0
        )

        return {

            "samples": total_samples,

            "messages": total_messages,

            "average_messages": round(
                average_messages,
                2,
            ),

            "average_message_length": round(
                average_characters,
                2,
            ),

            "average_quality": round(
                average_quality,
                4,
            ),

            "task_distribution": dict(
                task_distribution
            ),

            "language_distribution": dict(
                language_distribution
            ),
        }