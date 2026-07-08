class GeneratorPipeline:

    def __init__(self):

        self.generators = []

    def add(self, generator):

        self.generators.append(generator)

        return self

    def run(self, units):

        records = []

        for unit in units:

            for generator in self.generators:

                records.extend(
                    generator.generate(unit)
                )

        return records