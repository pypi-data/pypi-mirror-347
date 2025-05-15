import logging
import warnings
from pathlib import Path

import pandas as pd
import yaml
from joblib import Parallel, delayed
from tableone import TableOne

from ._janitor import get_outliers, infer_types, replace_missing
from ..utils.pdf import generate_analysis_report_pdf
from ..utils.plot import (
    plot_corr,
    plot_frequency_table,
    plot_kaplan_meier_by_category,
    plot_one_multiplot,
    plot_pairplot,
    plot_umap,
)

logging.basicConfig(filename=(Path.cwd() / "warnings.log"), level=logging.INFO)

def custom_warning_handler(message, category, filename, lineno, file=None, line=None) -> None:
    log_message = f"{category.__name__}: {message} in {filename} at line {lineno}"
    logging.warning(log_message)

warnings.showwarning = custom_warning_handler

class Analyzer:
    """
    A data analysis and cleaning tool for preprocessing datasets, generating reports, and visualizations.

    Features:
        - Handles missing values and outliers.
        - Infers column types (categorical, continuous, date).
        - Supports one-hot encoding and survival analysis.
        - Generates summary statistics and correlation plots.
        - Produces a comprehensive PDF analysis report.

    Attributes:
        data (pd.DataFrame): Input dataset.
        target_variable (str, optional): Target variable in the dataset.
        task (str, optional): Type of analysis task.
        one_hot_encode (bool, optional): Whether to one-hot encode categorical columns.
        config (str | Path, optional): Path to a YAML configuration file.
        output_dir (str | Path, optional): Directory to save outputs. Default is the current directory.

    Example:
        ```python
        from jarvais.analyzer import Analyzer
        import pandas as pd

        data = pd.DataFrame({
            "age": [25, 32, 40],
            "income": [50000, 60000, 75000],
            "category": ["A", "B", "A"]
        })

        analyzer = Analyzer(data, target_variable="income", task="regression")
        analyzer.run()
        ```
    """
    def __init__(
            self,
            data: pd.DataFrame,
            target_variable: str | None = None,
            task: str | None = None,
            one_hot_encode: bool = False,
            config: str | Path = None,
            output_dir: str | Path = None
        ) -> None:

        self.data = data
        self.target_variable = target_variable
        self.task = task
        self.one_hot_encode = one_hot_encode

        assert_message = "When setting task to 'survival', target_variable must be 'event' and 'time' must be in data"
        if self.task == 'survival':
            assert target_variable == 'event' and 'time' in data.columns, assert_message

        self.output_dir = Path.cwd() if output_dir is None else Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        if config is not None:
            config = Path(config)
            if config.is_file():
                with config.open('r') as file:
                    self.config = yaml.safe_load(file)
            else:
                raise ValueError(f'Config file does not exist at {config}')
        else:
            self.config = config

        self.outlier_analysis = '' # Used later when writing to PDF

    def _create_config(self) -> None:
        """
        Create and save a configuration file for column types, outlier handling, and missing value strategies.

        Steps:
        1. **Infer Column Types**: Identifies categorical, continuous, and date columns using `infer_types`.
        2. **Handle NaN Columns**: Drops columns entirely filled with NaN and updates the continuous column list.
        3. **Outlier Detection**: Identifies outliers in categorical columns and stores the mappings.
        4. **Missing Value Strategy**: Sets default imputation strategies for categorical and continuous variables.
        """
        print('Config file not found. Creating custom...')

        self.config = {}
        columns = {}

        self.categorical_columns, self.continuous_columns, self.date_columns = infer_types(self.data)
        # Replace all non numerical values with NaN
        self.data[self.continuous_columns] = self.data[self.continuous_columns].apply(pd.to_numeric, errors='coerce')

        nan_ = self.data.apply(lambda col: col.isna().all())
        nan_columns = nan_[nan_].index.tolist()
        if len(nan_columns) > 0:
            print("Columns that are all NaN(probably ID columns) dropping...: ", nan_columns)
            self.continuous_columns = list(set(self.continuous_columns) - set(nan_columns))

        print("Used a heuristic to define categorical and continuous columns. Please review!")
        
        columns['categorical'] = self.categorical_columns
        columns['continuous'] = self.continuous_columns
        columns['date'] = self.date_columns
        columns['other'] = nan_columns

        self.config['columns'] = columns

        outlier_analysis, mapping = get_outliers(self.data, self.categorical_columns)

        self.outlier_analysis += outlier_analysis
        self.config['mapping'] = mapping

        self.config['missingness_strategy'] = {}
        # Defining default replacement for each missing categorical variable
        self.config['missingness_strategy']['categorical'] = {cat :'Unknown' for cat in self.categorical_columns}
        # Defining default replacement for each missing continuous variable
        self.config['missingness_strategy']['continuous'] = {cont :'median' for cont in self.continuous_columns}

    def _apply_config(self) -> None:

        print('Applying changes from config...\n')

        for key in self.config['mapping'].keys():
            assert key in self.data.columns, f"{key} in mapping file not found data"
            self.data.loc[:, key] = self.data.loc[:, key].replace(self.config['mapping'][key])

        self.data = replace_missing(self.data, self.categorical_columns, self.continuous_columns, self.config)

    def _create_multiplots(self, figures_dir: Path) -> None:
        """Generate and save multiplots for each categorical variable against all continuous variables."""
        self.multiplots = [] # Used to save in PDF later

        (figures_dir / 'multiplots').mkdir(parents=True, exist_ok=True)

        self.multiplots = Parallel(n_jobs=-1)(
            delayed(plot_one_multiplot)(
                self.data,
                self.umap_data,
                var,
                self.continuous_columns,
                figures_dir
            ) for var in self.categorical_columns
        )

    def run(self) -> None:
        """Run the data cleaning and visualization process."""
        if self.config is None:
            self._create_config()
        else:
            self.continuous_columns = self.config['columns']['continuous']
            self.categorical_columns = self.config['columns']['categorical']
            # Replace all non numerical values with NaN
            self.data[self.continuous_columns] = self.data[self.continuous_columns].apply(pd.to_numeric, errors='coerce')
            self.outlier_analysis, _ = get_outliers(self.data, self.categorical_columns)

        print(f"Feature Types:\n  - Categorical: {self.categorical_columns}\n  - Continuous: {self.continuous_columns}")
        print(f"\n\nOutlier Analysis:\n{self.outlier_analysis}")

        with open(self.output_dir / 'config.yaml', 'w') as f:
            yaml.dump(self.config, f)

        self._apply_config()

        # Create Table One
        df_keep = self.data[self.continuous_columns + self.categorical_columns]

        self.mytable = TableOne(df_keep, categorical=self.categorical_columns, pval=False)
        print(self.mytable.tabulate(tablefmt = "grid"))
        self.mytable.to_csv(self.output_dir / 'tableone.csv')

        # PLOTS
        figures_dir = self.output_dir / 'figures'
        figures_dir.mkdir(exist_ok=True, parents=True)

        if self.task == 'survival':
            data_x = self.data.drop(columns=['time', 'event'])
            data_y = self.data[['time', 'event']]
            categorical_columns  = [cat for cat in self.categorical_columns if cat != 'event']
            plot_kaplan_meier_by_category(
                data_x, data_y,
                categorical_columns,
                figures_dir / 'kaplan_meier'
            )

        # Correlation Plots
        p_corr = self.data[self.continuous_columns].corr(method="pearson")
        s_corr = self.data[self.continuous_columns].corr(method="spearman")
        size = 1 + len(self.continuous_columns)*1.2
        plot_corr(p_corr, size, file_name='pearson_correlation.png', output_dir=figures_dir, title="Pearson Correlation")
        plot_corr(s_corr, size, file_name='spearman_correlation.png', output_dir=figures_dir, title="Spearman Correlation")

        # Categorical cross frequency table
        plot_frequency_table(self.data, self.categorical_columns, figures_dir)

        # UMAP reduced data + Plots
        self.umap_data = plot_umap(self.data, self.continuous_columns, figures_dir)

        # Plot pairplot: keeping only the top ten correlated pairs in the pair plot
        if self.target_variable in self.categorical_columns:
            plot_pairplot(self.data, self.continuous_columns, output_dir=figures_dir, target_variable=self.target_variable)
        else:
            plot_pairplot(self.data, self.continuous_columns, output_dir=figures_dir)

        # Create Multiplots
        self._create_multiplots(figures_dir)

        if self.one_hot_encode:
            self.data = pd.get_dummies(
                self.data,
                columns=[cat for cat in self.categorical_columns if cat != self.target_variable],
                dtype=float,
                prefix_sep='|' # Using this to make it obvious OHE features
            )

        self.data.to_csv(self.output_dir / 'updated_data.csv')

        # Create Output PDF
        generate_analysis_report_pdf(
            self.outlier_analysis,
            self.multiplots,
            self.categorical_columns,
            self.continuous_columns,
            self.output_dir
        )

    @classmethod
    def dry_run(cls, data: pd.DataFrame) -> dict:
        """Simply returns generated config and displays TableOne."""
        analyzer = cls(data)
        analyzer._create_config()

        df_keep = analyzer.data[analyzer.continuous_columns + analyzer.categorical_columns]

        print(f"\n\nFeature Types:\n  - Categorical: {analyzer.categorical_columns}\n  - Continuous: {analyzer.continuous_columns}")
        print(f"\n\nOutlier Analysis:\n{analyzer.outlier_analysis}")

        mytable = TableOne(df_keep, categorical=analyzer.categorical_columns, pval=False)
        print(mytable.tabulate(tablefmt = "grid"))

        return analyzer.config


