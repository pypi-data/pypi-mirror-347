from itertools import product

from beaverfe.auto_parameters.shared import evaluate_model
from beaverfe.auto_parameters.shared.utils import is_score_improved
from beaverfe.transformations import NumericalBinning
from beaverfe.transformations.utils import dtypes
from beaverfe.utils.verbose import VerboseLogger


class NumericalBinningParameterSelector:
    STRATEGIES = ["uniform", "quantile"]
    BIN_COUNTS = [3, 8, 20]

    def select_best_parameters(
        self, x, y, model, scoring, direction, cv, groups, logger: VerboseLogger
    ):
        columns = dtypes.numerical_columns(x)
        total_columns = len(columns)
        best_transformations = {}
        all_combinations = list(product(self.STRATEGIES, self.BIN_COUNTS))

        logger.task_start("Starting numerical binning search")

        base_score = evaluate_model(x, y, model, scoring, cv, groups)
        logger.baseline(f"Base score: {base_score:.4f}")

        for i, column in enumerate(columns, start=1):
            n_unique = x[column].nunique()
            logger.task_update(f"[{i}/{total_columns}] Evaluating column: '{column}'")

            best_score = base_score
            best_column_params = None

            for strategy, n_bins in all_combinations:
                if n_unique <= n_bins:
                    continue

                transformation_option = {column: (strategy, n_bins)}
                transformer = NumericalBinning(transformation_option)

                score = evaluate_model(x, y, model, scoring, cv, groups, transformer)
                logger.progress(
                    f"   ↪ Tried strategy='{strategy}', bins={n_bins} → Score: {score:.4f}"
                )

                if is_score_improved(score, best_score, direction):
                    best_score = score
                    best_column_params = (strategy, n_bins)

            if best_column_params:
                strategy, n_bins = best_column_params
                logger.task_result(
                    f"Selected binning for '{column}': strategy='{strategy}', bins={n_bins}"
                )
                best_transformations[column] = best_column_params

        if best_transformations:
            logger.task_result(
                f"Numerical binning applied to {len(best_transformations)} column(s)"
            )
            transformer = NumericalBinning(best_transformations)
            return {
                "name": transformer.__class__.__name__,
                "params": transformer.get_params(),
            }

        logger.warn("No numerical binning was applied to any column")
        return None
