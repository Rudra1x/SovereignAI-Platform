"""
Visualization utilities.
"""

from __future__ import annotations

import matplotlib.pyplot as plt


class Visualizer:

    def bar_chart(
        self,
        labels,
        values,
        title,
        output,
    ):

        plt.figure(
            figsize=(10,5)
        )

        plt.bar(
            labels,
            values,
        )

        plt.title(
            title
        )

        plt.tight_layout()

        plt.savefig(
            output
        )

        plt.close()