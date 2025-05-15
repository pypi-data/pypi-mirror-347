"""
Static uncertainty report renderer that uses Seaborn for visualizations.
"""

import os
import sys
import logging
import datetime
import traceback
from typing import Dict, List, Any, Optional

# Configure logger
logger = logging.getLogger("deepbridge.reports")
# Ensure logger has a proper handler
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

class StaticUncertaintyRenderer:
    """
    Renderer for static uncertainty test reports using Seaborn charts.
    """
    
    def __init__(self, template_manager, asset_manager):
        """
        Initialize the static uncertainty renderer.
        
        Parameters:
        -----------
        template_manager : TemplateManager
            Manager for templates
        asset_manager : AssetManager
            Manager for assets (CSS, JS, images)
        """
        from .base_static_renderer import BaseStaticRenderer
        self.base_renderer = BaseStaticRenderer(template_manager, asset_manager)
        self.template_manager = template_manager
        self.asset_manager = asset_manager
        
        # Import transformers
        from ...transformers.uncertainty import UncertaintyDataTransformer
        from ...transformers.initial_results import InitialResultsTransformer
        from ...transformers.static.static_uncertainty import StaticUncertaintyTransformer
        self.data_transformer = UncertaintyDataTransformer()
        self.static_transformer = StaticUncertaintyTransformer()
        self.initial_results_transformer = InitialResultsTransformer()
        
        # Import Seaborn chart utilities
        from ...utils.seaborn_utils import SeabornChartGenerator
        self.chart_generator = SeabornChartGenerator()
    
    def render(self, results: Dict[str, Any], file_path: str, model_name: str = "Model",
              report_type: str = "static", save_chart: bool = True) -> str:
        """
        Render static uncertainty report from results data.

        Parameters:
        -----------
        results : Dict[str, Any]
            Uncertainty test results
        file_path : str
            Path where the HTML report will be saved
        model_name : str, optional
            Name of the model for display in the report
        report_type : str, optional
            Type of report to generate ('interactive' or 'static')
        save_chart : bool, optional
            Whether to save charts as separate files (True) or embed them directly (False)

        Returns:
        --------
        str : Path to the generated report

        Raises:
        -------
        FileNotFoundError: If template or assets not found
        ValueError: If required data missing
        """
        logger.info(f"Generating static uncertainty report to: {file_path}")
        # Store the report file path for use in chart generation
        self.report_file_path = file_path
        
        try:
            # Find template through standard search paths
            template_paths = self.template_manager.get_template_paths("uncertainty", "static")
            template_path = self.template_manager.find_template(template_paths)
            
            if not template_path:
                raise FileNotFoundError(f"No suitable template found for uncertainty report")
            
            logger.info(f"Using static template: {template_path}")
            
            # Get CSS content
            css_content = self.base_renderer._load_static_css_content()
            
            # Load the template
            template = self.template_manager.load_template(template_path)
            
            # Transform the uncertainty data
            # First use the standard transformer
            logger.info("Starting data transformation with standard transformer")
            report_data = self.data_transformer.transform(results, model_name)
            logger.info(f"Standard transformer produced data with keys: {list(report_data.keys() if isinstance(report_data, dict) else [])}")

            # Then apply additional transformations for static reports
            report_data = self.static_transformer.transform(results, model_name)
            logger.info(f"Static transformer produced data with keys: {list(report_data.keys() if isinstance(report_data, dict) else [])}")
            
            # Transform initial results data if available
            if 'initial_results' in results:
                logger.info("Found initial_results in results, transforming...")
                initial_results = self.initial_results_transformer.transform(results.get('initial_results', {}))
                report_data['initial_results'] = initial_results
            
            # Create the context for the template
            context = self.base_renderer._create_static_context(report_data, "uncertainty", css_content)

            # Ensure report_data is included in the context
            context['report_data'] = report_data

            # For the static template, ensure correct report type values
            context['report_type'] = 'static'
            context['test_type'] = 'uncertainty'

            # Generate charts for the static report
            try:
                charts = self._generate_charts(report_data, save_chart)
                context['charts'] = charts
                logger.info(f"Generated {len(charts)} charts: {list(charts.keys())}")
            except Exception as e:
                logger.error(f"Error generating charts: {str(e)}")
                context['charts'] = {}
            
            # Extract features list, metrics, and feature subset
            features = self._extract_feature_list(report_data)
            metrics, metrics_details = self._extract_metrics(report_data)
            feature_subset, feature_subset_display = self._extract_feature_subset(report_data)
            
            # Add uncertainty-specific context with default values for None
            context.update({
                # Core metrics
                'uncertainty_score': report_data.get('uncertainty_score', 0),
                'coverage': report_data.get('coverage', 0),
                'mean_width': report_data.get('mean_width', 0),

                # Feature importance data
                'feature_importance': report_data.get('feature_importance', {}),
                'model_feature_importance': report_data.get('model_feature_importance', {}),
                'has_feature_importance': bool(report_data.get('feature_importance')),
                'has_model_feature_importance': bool(report_data.get('model_feature_importance')),

                # Test metadata
                'cal_size': report_data.get('cal_size'),
                'model_type': report_data.get('model_type', 'Unknown'),
                'timestamp': report_data.get('timestamp', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                'current_year': datetime.datetime.now().year,

                # Additional context
                'features': features,
                'metrics': metrics,
                'metrics_details': metrics_details,
                'feature_subset': feature_subset,
                'feature_subset_display': feature_subset_display,

                # Title for the report
                'block_title': f"Uncertainty Analysis: {model_name}"
            })

            # Ensure alternative_models data has all required attributes
            if 'alternative_models' in report_data and isinstance(report_data['alternative_models'], dict):
                for model_name, model_data in report_data['alternative_models'].items():
                    # Ensure coverage and mean_width exist in each model
                    if not isinstance(model_data, dict):
                        report_data['alternative_models'][model_name] = {
                            'uncertainty_score': 0,
                            'coverage': 0,
                            'mean_width': 0
                        }
                    else:
                        if 'coverage' not in model_data:
                            report_data['alternative_models'][model_name]['coverage'] = 0
                        if 'mean_width' not in model_data:
                            report_data['alternative_models'][model_name]['mean_width'] = 0
                        if 'uncertainty_score' not in model_data:
                            report_data['alternative_models'][model_name]['uncertainty_score'] = 0
            
            # Render the template
            rendered_html = self.template_manager.render_template(template, context)

            # Write the report to the file
            return self.base_renderer._write_report(rendered_html, file_path)
            
        except Exception as e:
            logger.error(f"Error generating static uncertainty report: {str(e)}")
            logger.error(f"Error traceback: {traceback.format_exc()}")
            raise ValueError(f"Failed to generate static uncertainty report: {str(e)}")
    
    def _extract_feature_list(self, report_data: Dict[str, Any]) -> List[str]:
        """
        Extract the list of features from the report data.
        
        Parameters:
        -----------
        report_data : Dict[str, Any]
            Transformed report data
            
        Returns:
        --------
        List[str] : List of features
        """
        # Get features directly from report_data if available
        if 'features' in report_data and isinstance(report_data['features'], list):
            return report_data['features']
            
        # If features not found but feature_importance is available, use those keys
        elif 'feature_importance' in report_data and isinstance(report_data['feature_importance'], dict):
            return list(report_data['feature_importance'].keys())
            
        # Return empty list if no features found
        return []
    
    def _extract_metrics(self, report_data: Dict[str, Any]) -> tuple:
        """
        Extract metrics and metrics details from the report data.
        
        Parameters:
        -----------
        report_data : Dict[str, Any]
            Transformed report data
            
        Returns:
        --------
        tuple : (metrics, metrics_details)
        """
        # Simply extract metrics and metrics_details directly from report_data
        metrics = report_data.get('metrics', {})
        metrics_details = report_data.get('metrics_details', {})
        
        return metrics, metrics_details
    
    def _extract_feature_subset(self, report_data: Dict[str, Any]) -> tuple:
        """
        Extract the feature subset and its display string.

        Parameters:
        -----------
        report_data : Dict[str, Any]
            Transformed report data

        Returns:
        --------
        tuple : (feature_subset, feature_subset_display)
        """
        # Get feature subset and display string directly from report data
        feature_subset = report_data.get('feature_subset', [])
        feature_subset_display = report_data.get('feature_subset_display', 'All Features')

        return feature_subset, feature_subset_display

    def _generate_placeholder_chart(self, title, output_path, chart_type="scatter"):
        """
        Generate a placeholder chart when real data is missing or invalid.

        Parameters:
        -----------
        title : str
            Title for the placeholder chart
        output_path : str
            Path where to save the chart
        chart_type : str, optional
            Type of chart to generate (scatter, bar, line)

        Returns:
        --------
        str : Base64 encoded image data
        """
        try:
            import matplotlib.pyplot as plt
            import numpy as np
            import base64
            import io

            # Set style
            plt.style.use('seaborn-v0_8')

            # Create figure
            plt.figure(figsize=(10, 6))

            # Generate some example data
            np.random.seed(42)  # For reproducibility
            x = np.linspace(0, 10, 30)
            y = np.sin(x) + np.random.normal(0, 0.2, size=30)

            # Draw different types of charts
            if chart_type == "bar":
                categories = ['A', 'B', 'C', 'D', 'E']
                values = np.random.rand(5) * 10
                plt.bar(categories, values, color='skyblue')
                plt.axhline(y=np.mean(values), color='r', linestyle='--', label='Average')
                plt.legend()
            elif chart_type == "line":
                plt.plot(x, y, 'o-', label='Data')
                plt.plot(x, np.sin(x), 'r--', label='True Function')
                plt.fill_between(x, np.sin(x)-0.2, np.sin(x)+0.2, color='r', alpha=0.2, label='Uncertainty')
                plt.legend()
            else:  # Default: scatter
                plt.scatter(x, y, alpha=0.7, label='Data Points')
                plt.plot(x, np.sin(x), 'r-', label='Trend')
                plt.legend()

            # Labels and title
            plt.title(f"Example Chart: {title}")
            plt.xlabel("X Axis (Example Values)")
            plt.ylabel("Y Axis (Example Values)")
            plt.grid(True, alpha=0.3)

            # Add watermark
            plt.figtext(0.5, 0.01, "Example data - Generated for demonstration purposes",
                       ha="center", fontsize=8, color="gray")

            # Save to file if path is provided
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                logger.info(f"Saved placeholder chart to {output_path}")

            # Also save to base64 for embedding
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=300, bbox_inches='tight')
            buffer.seek(0)
            plt.close()

            return f"data:image/png;base64,{base64.b64encode(buffer.read()).decode('utf-8')}"
        except Exception as e:
            logger.error(f"Error generating placeholder chart: {str(e)}")
            return None
    
    def _generate_charts(self, report_data: Dict[str, Any], save_chart: bool = True) -> Dict[str, str]:
        """
        Generate all charts needed for the static report.

        Parameters:
        -----------
        report_data : Dict[str, Any]
            Transformed report data
        save_chart : bool, optional
            Whether to save charts as separate files (True) or embed them directly (False)

        Returns:
        --------
        Dict[str, str] : Dictionary of chart names and their base64 encoded images
        """
        # Initialize empty charts dictionary
        charts = {}

        # Create a charts directory if save_chart is True
        if save_chart:
            import os
            # Get the directory of the report file
            report_dir = os.path.dirname(os.path.abspath(self.report_file_path))
            # Create a charts subdirectory
            charts_dir = os.path.join(report_dir, "uncertainty_charts")
            os.makedirs(charts_dir, exist_ok=True)
            logger.info(f"Created chart directory at: {charts_dir}")
        else:
            charts_dir = None

        try:
            # Use the new modular chart generator system
            try:
                from deepbridge.templates.report_types.uncertainty.static.charts import UncertaintyChartGenerator

                # Create chart generator with seaborn fallback
                chart_generator = UncertaintyChartGenerator(self.chart_generator)
                logger.info("Using new modular chart generator system for uncertainty visualization")

                # Generate coverage vs expected coverage chart
                try:
                    # Log data needed for this chart
                    logger.info("DADOS PARA COVERAGE VS EXPECTED CHART:")
                    if 'calibration_results' in report_data:
                        logger.info(f"  - calibration_results disponível: {report_data['calibration_results'].keys() if isinstance(report_data['calibration_results'], dict) else 'não é um dicionário'}")
                        if isinstance(report_data['calibration_results'], dict):
                            for key, value in report_data['calibration_results'].items():
                                if isinstance(value, (list, tuple)):
                                    logger.info(f"  - {key}: {len(value)} valores")
                                else:
                                    logger.info(f"  - {key}: {type(value)}")
                    else:
                        logger.error("  - ERRO: calibration_results não está disponível nos dados")

                    # Check alpha values
                    if 'alpha_levels' in report_data:
                        logger.info(f"  - alpha_levels: {report_data['alpha_levels']}")
                    else:
                        logger.error("  - ERRO: alpha_levels não está disponível nos dados")

                    coverage_chart = chart_generator.generate_coverage_vs_expected(report_data)
                    if coverage_chart:
                        charts['coverage_vs_expected'] = coverage_chart
                        logger.info("Generated coverage vs expected coverage chart")

                        # Save chart to PNG if requested
                        if save_chart and charts_dir:
                            import base64
                            try:
                                # Extract the base64 part
                                if coverage_chart.startswith('data:image/png;base64,'):
                                    img_data = coverage_chart.split('data:image/png;base64,')[1]
                                    # Save to file
                                    with open(os.path.join(charts_dir, 'coverage_vs_expected.png'), 'wb') as f:
                                        f.write(base64.b64decode(img_data))
                                    logger.info(f"Saved coverage_vs_expected.png to {charts_dir}")
                            except Exception as e:
                                logger.error(f"Error saving coverage chart as PNG: {str(e)}")
                except Exception as e:
                    logger.error(f"Error generating coverage vs expected chart: {str(e)}")

                # Generate width vs coverage chart
                try:
                    # Log data needed for this chart
                    logger.info("DADOS PARA WIDTH VS COVERAGE CHART:")
                    if 'calibration_results' in report_data:
                        logger.info(f"  - calibration_results disponível: {report_data['calibration_results'].keys() if isinstance(report_data['calibration_results'], dict) else 'não é um dicionário'}")
                        if isinstance(report_data['calibration_results'], dict):
                            # Check for width values
                            if 'width_values' in report_data['calibration_results']:
                                logger.info(f"  - width_values: {len(report_data['calibration_results']['width_values'])} valores")
                            else:
                                logger.error("  - ERRO: width_values não está disponível em calibration_results")

                            # Check for coverage values
                            if 'coverage_values' in report_data['calibration_results']:
                                logger.info(f"  - coverage_values: {len(report_data['calibration_results']['coverage_values'])} valores")
                            else:
                                logger.error("  - ERRO: coverage_values não está disponível em calibration_results")
                    else:
                        logger.error("  - ERRO: calibration_results não está disponível nos dados")

                    width_chart = chart_generator.generate_width_vs_coverage(report_data)
                    if width_chart:
                        charts['width_vs_coverage'] = width_chart
                        logger.info("Generated width vs coverage chart")

                        # Save chart to PNG if requested
                        if save_chart and charts_dir:
                            import base64
                            try:
                                # Extract the base64 part
                                if width_chart.startswith('data:image/png;base64,'):
                                    img_data = width_chart.split('data:image/png;base64,')[1]
                                    # Save to file
                                    with open(os.path.join(charts_dir, 'width_vs_coverage.png'), 'wb') as f:
                                        f.write(base64.b64decode(img_data))
                                    logger.info(f"Saved width_vs_coverage.png to {charts_dir}")
                            except Exception as e:
                                logger.error(f"Error saving width chart as PNG: {str(e)}")
                except Exception as e:
                    logger.error(f"Error generating width vs coverage chart: {str(e)}")

                # Generate uncertainty metrics chart
                try:
                    # Log data needed for this chart
                    logger.info("DADOS PARA UNCERTAINTY METRICS CHART:")
                    # Check uncertainty metrics
                    if 'uncertainty_score' in report_data:
                        logger.info(f"  - uncertainty_score: {report_data['uncertainty_score']}")
                    else:
                        logger.error("  - ERRO: uncertainty_score não está disponível nos dados")

                    if 'coverage' in report_data:
                        logger.info(f"  - coverage: {report_data['coverage']}")
                    else:
                        logger.error("  - ERRO: coverage não está disponível nos dados")

                    if 'mean_width' in report_data:
                        logger.info(f"  - mean_width: {report_data['mean_width']}")
                    else:
                        logger.error("  - ERRO: mean_width não está disponível nos dados")

                    # Check metrics dictionary
                    if 'metrics' in report_data:
                        logger.info(f"  - metrics disponível: {list(report_data['metrics'].keys()) if isinstance(report_data['metrics'], dict) else 'não é um dicionário'}")
                    else:
                        logger.error("  - ERRO: metrics não está disponível nos dados")

                    metrics_chart = chart_generator.generate_uncertainty_metrics(report_data)
                    if metrics_chart:
                        charts['uncertainty_metrics'] = metrics_chart
                        logger.info("Generated uncertainty metrics chart")

                        # Save chart to PNG if requested
                        if save_chart and charts_dir:
                            import base64
                            try:
                                # Extract the base64 part
                                if metrics_chart.startswith('data:image/png;base64,'):
                                    img_data = metrics_chart.split('data:image/png;base64,')[1]
                                    # Save to file
                                    with open(os.path.join(charts_dir, 'uncertainty_metrics.png'), 'wb') as f:
                                        f.write(base64.b64decode(img_data))
                                    logger.info(f"Saved uncertainty_metrics.png to {charts_dir}")
                            except Exception as e:
                                logger.error(f"Error saving metrics chart as PNG: {str(e)}")
                except Exception as e:
                    logger.error(f"Error generating uncertainty metrics chart: {str(e)}")

                # Generate feature importance chart
                logger.info("DADOS PARA FEATURE IMPORTANCE CHART:")
                if 'feature_importance' in report_data:
                    # Log feature importance structure
                    logger.info(f"  - feature_importance type: {type(report_data['feature_importance'])}")
                    if isinstance(report_data['feature_importance'], dict):
                        logger.info(f"  - feature_importance tem {len(report_data['feature_importance'])} características")
                        # Log some features as examples
                        for i, (feature, importance) in enumerate(report_data['feature_importance'].items()):
                            if i < 5:  # Show first 5 features only
                                logger.info(f"  - Exemplo: {feature}: {importance}")
                            else:
                                break
                    else:
                        logger.error(f"  - ERRO: feature_importance não é um dicionário: {type(report_data['feature_importance'])}")

                    try:
                        importance_chart = chart_generator.generate_feature_importance(report_data)
                        if importance_chart:
                            charts['feature_importance'] = importance_chart
                            logger.info("Generated feature importance chart")

                            # Save chart to PNG if requested
                            if save_chart and charts_dir:
                                import base64
                                try:
                                    # Extract the base64 part
                                    if importance_chart.startswith('data:image/png;base64,'):
                                        img_data = importance_chart.split('data:image/png;base64,')[1]
                                        # Save to file
                                        with open(os.path.join(charts_dir, 'feature_importance.png'), 'wb') as f:
                                            f.write(base64.b64decode(img_data))
                                        logger.info(f"Saved feature_importance.png to {charts_dir}")
                                except Exception as e:
                                    logger.error(f"Error saving importance chart as PNG: {str(e)}")
                    except Exception as e:
                        logger.error(f"Error generating feature importance chart: {str(e)}")
                else:
                    logger.error("  - ERRO: feature_importance não está disponível nos dados")

                # Generate model comparison chart
                try:
                    # Log data needed for this chart
                    logger.info("DADOS PARA MODEL COMPARISON CHART:")
                    if 'alternative_models' in report_data:
                        alt_models = report_data['alternative_models']
                        logger.info(f"  - alternative_models: {len(alt_models) if isinstance(alt_models, dict) else 'não é um dicionário'}")

                        if isinstance(alt_models, dict):
                            # Log model names
                            logger.info(f"  - Modelos alternativos: {list(alt_models.keys())}")

                            # Check if models have necessary metrics
                            for model_name, model_data in alt_models.items():
                                logger.info(f"  - Modelo {model_name}: ")
                                if isinstance(model_data, dict):
                                    if 'uncertainty_score' in model_data:
                                        logger.info(f"    - uncertainty_score: {model_data['uncertainty_score']}")
                                    else:
                                        logger.error(f"    - ERRO: uncertainty_score não disponível para {model_name}")

                                    if 'coverage' in model_data:
                                        logger.info(f"    - coverage: {model_data['coverage']}")
                                    else:
                                        logger.error(f"    - ERRO: coverage não disponível para {model_name}")

                                    if 'mean_width' in model_data:
                                        logger.info(f"    - mean_width: {model_data['mean_width']}")
                                    else:
                                        logger.error(f"    - ERRO: mean_width não disponível para {model_name}")
                                else:
                                    logger.error(f"    - ERRO: dados do modelo não são um dicionário: {type(model_data)}")
                        else:
                            logger.error(f"  - ERRO: alternative_models não é um dicionário: {type(alt_models)}")
                    else:
                        logger.error("  - ERRO: alternative_models não está disponível nos dados")

                    comparison_chart = chart_generator.generate_model_comparison(report_data)
                    if comparison_chart:
                        charts['model_comparison'] = comparison_chart
                        logger.info("Generated model comparison chart")

                        # Save chart to PNG if requested
                        if save_chart and charts_dir:
                            import base64
                            try:
                                # Extract the base64 part
                                if comparison_chart.startswith('data:image/png;base64,'):
                                    img_data = comparison_chart.split('data:image/png;base64,')[1]
                                    # Save to file
                                    with open(os.path.join(charts_dir, 'model_comparison.png'), 'wb') as f:
                                        f.write(base64.b64decode(img_data))
                                    logger.info(f"Saved model_comparison.png to {charts_dir}")
                            except Exception as e:
                                logger.error(f"Error saving comparison chart as PNG: {str(e)}")
                except Exception as e:
                    logger.error(f"Error generating model comparison chart: {str(e)}")

                # Generate performance gap by alpha chart
                try:
                    # Log data needed for this chart
                    logger.info("DADOS PARA PERFORMANCE GAP BY ALPHA CHART:")
                    # Check for alpha levels
                    if 'alpha_levels' in report_data:
                        logger.info(f"  - alpha_levels: {report_data['alpha_levels']}")
                    else:
                        logger.error("  - ERRO: alpha_levels não está disponível nos dados")

                    # Check calibration_results
                    if 'calibration_results' in report_data:
                        cal_results = report_data['calibration_results']
                        logger.info(f"  - calibration_results disponível: {cal_results.keys() if isinstance(cal_results, dict) else 'não é um dicionário'}")

                        # Check for alpha and coverage arrays
                        if isinstance(cal_results, dict):
                            if 'alpha_values' in cal_results and 'coverage_values' in cal_results:
                                logger.info(f"  - alpha_values: {len(cal_results['alpha_values'])} valores")
                                logger.info(f"  - coverage_values: {len(cal_results['coverage_values'])} valores")
                                logger.info(f"  - expected_coverages: {len(cal_results.get('expected_coverages', []))} valores")
                            else:
                                logger.error("  - ERRO: alpha_values, coverage_values ou expected_coverages ausentes em calibration_results")
                    else:
                        logger.error("  - ERRO: calibration_results não está disponível nos dados")

                    # Try to see if signature matches the function
                    import inspect
                    try:
                        from deepbridge.templates.report_types.uncertainty.static.charts import UncertaintyChartGenerator
                        sig = inspect.signature(UncertaintyChartGenerator.generate_performance_gap_by_alpha)
                        logger.info(f"  - Argumentos necessários para generate_performance_gap_by_alpha: {list(sig.parameters.keys())}")
                    except Exception as import_err:
                        logger.error(f"  - Não foi possível inspecionar a assinatura do método: {str(import_err)}")

                    performance_gap_chart = chart_generator.generate_performance_gap_by_alpha(models_data=report_data, title="Performance Gap by Alpha Level", add_annotations=True)
                    if performance_gap_chart:
                        charts['performance_gap_by_alpha'] = performance_gap_chart
                        logger.info("Generated performance gap by alpha chart")

                        # Save chart to PNG if requested
                        if save_chart and charts_dir:
                            import base64
                            try:
                                # Extract the base64 part
                                if performance_gap_chart.startswith('data:image/png;base64,'):
                                    img_data = performance_gap_chart.split('data:image/png;base64,')[1]
                                    # Save to file
                                    with open(os.path.join(charts_dir, 'performance_gap_by_alpha.png'), 'wb') as f:
                                        f.write(base64.b64decode(img_data))
                                    logger.info(f"Saved performance_gap_by_alpha.png to {charts_dir}")
                            except Exception as e:
                                logger.error(f"Error saving performance gap chart as PNG: {str(e)}")
                except Exception as e:
                    logger.error(f"Error generating performance gap by alpha chart: {str(e)}")

            except ImportError as e:
                logger.warning(f"Could not import modular chart generator: {str(e)}")
                logger.warning("Falling back to legacy chart generation")

                # Fallback to legacy chart generation
                # Generate interval widths comparison chart - legacy method
                if 'interval_widths' in report_data:
                    try:
                        from ...utils.uncertainty_charts import generate_interval_widths_comparison
                        import tempfile
                        import os
                        import base64

                        # Use the charts directory if save_chart is True, otherwise use a temp dir
                        if save_chart and charts_dir:
                            chart_dir = charts_dir
                        else:
                            # Create a temporary directory for the chart
                            chart_dir = tempfile.mkdtemp()

                        # Generate the chart
                        chart_path = generate_interval_widths_comparison(report_data, chart_dir)

                        # Add to charts if generated successfully
                        if chart_path and os.path.exists(chart_path):
                            with open(chart_path, 'rb') as img_file:
                                chart_data = base64.b64encode(img_file.read()).decode('utf-8')
                            charts['interval_widths_comparison'] = f"data:image/png;base64,{chart_data}"
                            logger.info(f"Successfully generated interval widths comparison chart at {chart_path}")
                    except Exception as e:
                        logger.error(f"Error generating interval widths chart: {str(e)}")

                # Generate feature reliability chart - legacy method
                if 'feature_reliability' in report_data:
                    try:
                        feature_data = {
                            'Feature': [],
                            'PSI': []
                        }

                        # Extract top features by PSI
                        sorted_features = sorted(
                            [(feature, data.get('psi', 0)) for feature, data in report_data['feature_reliability'].items()],
                            key=lambda x: x[1], reverse=True
                        )[:10]  # Get top 10

                        if sorted_features:
                            feature_data['Feature'] = [feature for feature, _ in sorted_features]
                            feature_data['PSI'] = [score for _, score in sorted_features]

                            charts['feature_reliability'] = self.chart_generator.feature_psi_chart(
                                psi_data=feature_data,
                                title="Feature Reliability"
                            )
                            logger.info("Generated feature reliability chart")
                    except Exception as e:
                        logger.error(f"Error generating feature reliability chart: {str(e)}")

                # Generate additional uncertainty charts if available - legacy method
                try:
                    from ...utils.uncertainty_report_charts import generate_all_uncertainty_charts
                    import tempfile

                    # Use the charts directory if save_chart is True, otherwise use a temp dir
                    if save_chart and charts_dir:
                        additional_charts_dir = charts_dir
                    else:
                        # Create a temporary directory for the charts
                        additional_charts_dir = tempfile.mkdtemp()

                    # Generate charts with real data only, no examples
                    logger.info("Generating static uncertainty charts from real data only")
                    additional_charts = generate_all_uncertainty_charts(additional_charts_dir)

                    if additional_charts:
                        charts.update(additional_charts)
                        logger.info(f"Added {len(additional_charts)} additional uncertainty charts to {additional_charts_dir}")
                    else:
                        logger.warning("No additional charts were generated")
                except (ImportError, AttributeError):
                    logger.info("Additional uncertainty charts module not available")
                except Exception as e:
                    logger.error(f"Error generating additional uncertainty charts: {str(e)}")
                    logger.error(traceback.format_exc())

        except Exception as e:
            logger.error(f"Error generating charts: {str(e)}")
            logger.error(traceback.format_exc())

        return charts