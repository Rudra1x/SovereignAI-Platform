"""
Plugin manager.
"""

from evaluation.plugins.quantum import QuantumPlugin
from evaluation.plugins.coding import CodingPlugin
from evaluation.plugins.reasoning import ReasoningPlugin
from evaluation.plugins.hallucination import HallucinationPlugin
from evaluation.plugins.regression import RegressionPlugin


class PluginManager:

    def __init__(self):

        self.plugins = [

            QuantumPlugin(),

            CodingPlugin(),

            ReasoningPlugin(),

            HallucinationPlugin(),

            RegressionPlugin(),

        ]

    def evaluate(

        self,

        sample,

        prediction,

    ):

        results = {}

        for plugin in self.plugins:

            if plugin.supports(sample):

                results[plugin.name] = (

                    plugin.evaluate(

                        sample,

                        prediction,

                    )

                )

        return results