class ReportGenerator:

    def summarize(
        self,
        results,
    ):

        summary = {

            "exact_match":

                sum(
                    r["metrics"]["exact_match"]
                    for r in results
                ) / len(results),

            "keyword_recall":

                sum(
                    r["metrics"]["keyword_recall"]
                    for r in results
                ) / len(results),

            "bleu":

                sum(
                    r["metrics"]["bleu"]
                    for r in results
                ) / len(results),

            "bertscore":

                sum(
                    r["metrics"]["bertscore"]
                    for r in results
                ) / len(results),
        }

        return summary