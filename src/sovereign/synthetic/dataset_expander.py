"""
Convert one structured response into many SFT samples.
"""

from __future__ import annotations


class DatasetExpander:

    def expand(
        self,
        document_title: str,
        structured: dict,
    ) -> list[dict]:

        samples = []

        samples.append(
            {
                "instruction": f"Summarize {document_title}.",
                "input": "",
                "output": structured["summary"],
                "metadata": {
                    "task": "summary"
                },
            }
        )

        samples.append(
            {
                "instruction": f"Explain {document_title}.",
                "input": "",
                "output": structured["explanation"],
                "metadata": {
                    "task": "explanation"
                },
            }
        )

        for qa in structured["qa"]:

            samples.append(
                {
                    "instruction": qa["question"],
                    "input": "",
                    "output": qa["answer"],
                    "metadata": {
                        "task": "qa"
                    },
                }
            )

        for mcq in structured["mcqs"]:

            text = (
                mcq["question"]
                + "\n\n"
                + "\n".join(mcq["options"])
            )

            samples.append(
                {
                    "instruction": text,
                    "input": "",
                    "output": mcq["answer"],
                    "metadata": {
                        "task": "mcq"
                    },
                }
            )

        for task in structured["coding_tasks"]:

            samples.append(
                {
                    "instruction": task["question"],
                    "input": "",
                    "output": task["solution"],
                    "metadata": {
                        "task": "coding_task"
                    },
                }
            )

        for practice in structured["best_practices"]:

            samples.append(
                {
                    "instruction": "List a best practice.",
                    "input": "",
                    "output": practice,
                    "metadata": {
                        "task": "best_practice"
                    },
                }
            )

        for mistake in structured["common_mistakes"]:

            samples.append(
                {
                    "instruction": "Describe a common mistake.",
                    "input": "",
                    "output": mistake,
                    "metadata": {
                        "task": "common_mistake"
                    },
                }
            )

        return samples