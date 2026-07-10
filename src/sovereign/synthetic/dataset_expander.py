"""
Convert one structured response into many SFT samples.
"""

from __future__ import annotations


class DatasetExpander:

    def expand(
        self,
        chunk,
        structured: dict,
    ) -> list[dict]:

        samples = []

        summary = structured.get("summary", "").strip()
        qa = structured.get("qa", [])
        mcqs = structured.get("mcqs", [])
        coding_tasks = structured.get("coding_tasks", [])
        best_practices = structured.get("best_practices", [])
        common_mistakes = structured.get("common_mistakes", [])
        explanation = structured.get("explanation", "").strip()

        if summary:

            samples.append(
                {
                    "instruction": f"Summarize {chunk.title}.",
                    "input": "",
                    "output": summary,
                    "metadata": {
                        "task": "summary",
                        "source": chunk.source,
                        "title": chunk.title,
                        "section": chunk.section,
                    },
                }
            )

        if explanation:

            samples.append(
                {
                    "instruction": f"Explain {chunk.title}.",
                    "input": "",
                    "output": explanation,
                    "metadata": {
                        "task": "explanation",
                        "source": chunk.source,
                        "title": chunk.title,
                        "section": chunk.section,
                    },
                }
            )

        elif summary:

            samples.append(
                {
                    "instruction": f"Explain {chunk.title}.",
                    "input": "",
                    "output": summary,
                    "metadata": {
                        "task": "explanation",
                        "source": chunk.source,
                        "title": chunk.title,
                        "section": chunk.section,
                    },
                }
            )

        for item in qa:

            samples.append(
                {
                    "instruction": item["question"],
                    "input": "",
                    "output": item["answer"],
                    "metadata": {
                        "task": "qa"
                    },
                }
            )

        for mcq in mcqs:

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

        for task in coding_tasks:

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

        for practice in best_practices:

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

        for mistake in common_mistakes:

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

        unique = []
        
        seen = set()
        
        for sample in samples:

            key = (

                sample["instruction"].strip().lower(),

                sample["output"].strip().lower(),

            )

            if key in seen:

                continue

            seen.add(key)

            unique.append(sample)
            
        return unique