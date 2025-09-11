import numpy as np
import pandas as pd
from django.conf import settings
from typing import Dict, List, Any
import logging
import time
from .models import LCACalculation, ProcessStep
from materials.models import Material, MaterialProperty
from processes.models import Process
from ai_models.services import ParameterPredictionService, RecommendationEngine

logger = logging.getLogger(__name__)


class LCACalculationService:
    """Service for performing LCA calculations"""
    
    def __init__(self):
        self.impact_methods = {
            'climate_change': self._calculate_climate_change,
            'fossil_depletion': self._calculate_fossil_depletion,
            'metal_depletion': self._calculate_metal_depletion,
            'water_depletion': self._calculate_water_depletion,
            'acidification': self._calculate_acidification,
            'eutrophication': self._calculate_eutrophication,
            'ozone_depletion': self._calculate_ozone_depletion,
            'land_use': self._calculate_land_use,
            'particulate_matter': self._calculate_particulate_matter,
            'toxicity_human': self._calculate_human_toxicity,
            'toxicity_eco': self._calculate_ecotoxicity,
        }
    
    def calculate_lca(self, calculation: LCACalculation) -> Dict[str, Any]:
        """Main LCA calculation method"""
        start_time = time.time()
        
        try:
            # Get process steps
            process_steps = calculation.process_steps.all().order_by('order')
            
            if not process_steps.exists():
                raise ValueError("No process steps defined for calculation")
            
            # Initialize results
            environmental_impacts = {}
            process_impacts = {}
            circularity_metrics = {}
            
            # Calculate impacts for each step
            for step in process_steps:
                step_impacts = self._calculate_step_impacts(step)
                process_impacts[str(step.id)] = step_impacts
                
                # Aggregate impacts
                for impact, value in step_impacts.items():
                    environmental_impacts[impact] = environmental_impacts.get(impact, 0) + value
            
            # Calculate circularity metrics
            circularity_metrics = self._calculate_circularity_metrics(calculation)
            
            # Prepare results
            results = {
                'lca_results': {
                    'total_impacts': environmental_impacts,
                    'process_breakdown': process_impacts,
                    'functional_unit': calculation.project.functional_unit,
                    'system_boundary': calculation.project.system_boundary,
                },
                'environmental_impacts': environmental_impacts,
                'circularity_metrics': circularity_metrics,
                'calculation_time': time.time() - start_time,
            }
            
            logger.info(f"LCA calculation completed for {calculation.name}")
            return results
            
        except Exception as e:
            logger.error(f"LCA calculation failed: {str(e)}")
            raise
    
    def _calculate_step_impacts(self, step: ProcessStep) -> Dict[str, float]:
        """Calculate environmental impacts for a single process step"""
        impacts = {}
        
        # Get base process data
        try:
            process = Process.objects.get(name__iexact=step.name)
            base_factors = process.impact_factors
        except Process.DoesNotExist:
            logger.warning(f"Process {step.name} not found in database, using defaults")
            base_factors = self._get_default_impact_factors(step.category)
        
        # Calculate impacts based on input materials and energy
        for material_input in step.input_materials:
            material_impacts = self._calculate_material_impacts(material_input)
            for impact, value in material_impacts.items():
                impacts[impact] = impacts.get(impact, 0) + value
        
        # Energy-related impacts
        for energy_input in step.energy_inputs:
            energy_impacts = self._calculate_energy_impacts(energy_input)
            for impact, value in energy_impacts.items():
                impacts[impact] = impacts.get(impact, 0) + value
        
        # Direct emissions
        for emission, amount in step.emissions.items():
            emission_impacts = self._calculate_emission_impacts(emission, amount)
            for impact, value in emission_impacts.items():
                impacts[impact] = impacts.get(impact, 0) + value
        
        return impacts
    
    def _calculate_material_impacts(self, material_input: Dict[str, Any]) -> Dict[str, float]:
        """Calculate impacts from material inputs"""
        impacts = {}
        material_name = material_input.get('material')
        quantity = material_input.get('quantity', 0)
        
        try:
            material = Material.objects.get(name__iexact=material_name)
            
            # Get impact factors per kg
            for impact_category in self.impact_methods.keys():
                try:
                    factor = MaterialProperty.objects.get(
                        material=material,
                        property_name=f"{impact_category}_factor"
                    ).value
                    impacts[impact_category] = quantity * factor
                except MaterialProperty.DoesNotExist:
                    impacts[impact_category] = 0
                    
        except Material.DoesNotExist:
            logger.warning(f"Material {material_name} not found, using defaults")
            # Use default factors based on material type
            default_factors = self._get_default_material_factors(material_name)
            for impact, factor in default_factors.items():
                impacts[impact] = quantity * factor
        
        return impacts
    
    def _calculate_energy_impacts(self, energy_input: Dict[str, Any]) -> Dict[str, float]:
        """Calculate impacts from energy inputs"""
        impacts = {}
        energy_type = energy_input.get('type', 'electricity_grid')
        amount = energy_input.get('amount', 0)  # kWh
        
        # Energy impact factors (per kWh)
        energy_factors = {
            'electricity_grid': {
                'climate_change': 0.5,  # kg CO2-eq/kWh
                'fossil_depletion': 0.15,
                'acidification': 0.002,
                'eutrophication': 0.0001,
            },
            'electricity_renewable': {
                'climate_change': 0.05,
                'fossil_depletion': 0.01,
                'acidification': 0.0002,
                'eutrophication': 0.00001,
            },
            'natural_gas': {
                'climate_change': 0.2,
                'fossil_depletion': 0.3,
                'acidification': 0.001,
                'eutrophication': 0.00005,
            },
            'coal': {
                'climate_change': 1.0,
                'fossil_depletion': 0.4,
                'acidification': 0.005,
                'eutrophication': 0.0002,
            }
        }
        
        factors = energy_factors.get(energy_type, energy_factors['electricity_grid'])
        
        for impact, factor in factors.items():
            impacts[impact] = amount * factor
        
        return impacts
    
    def _calculate_emission_impacts(self, emission_type: str, amount: float) -> Dict[str, float]:
        """Calculate impacts from direct emissions"""
        impacts = {}
        
        # Emission characterization factors
        emission_factors = {
            'CO2': {'climate_change': 1.0},
            'CH4': {'climate_change': 28.0},
            'N2O': {'climate_change': 265.0},
            'SO2': {'acidification': 1.0, 'particulate_matter': 0.5},
            'NOx': {'acidification': 0.7, 'eutrophication': 0.13},
            'NH3': {'acidification': 1.6, 'eutrophication': 0.33},
            'PM2.5': {'particulate_matter': 1.0},
            'PM10': {'particulate_matter': 0.5},
        }
        
        factors = emission_factors.get(emission_type, {})
        
        for impact, factor in factors.items():
            impacts[impact] = amount * factor
        
        return impacts
    
    def _calculate_circularity_metrics(self, calculation: LCACalculation) -> Dict[str, float]:
        """Calculate circularity indicators"""
        metrics = {}
        
        # Get all process steps
        steps = calculation.process_steps.all()
        
        # Recycled content percentage
        total_material_input = 0
        recycled_material_input = 0
        
        for step in steps:
            for material in step.input_materials:
                quantity = material.get('quantity', 0)
                recycled_content = material.get('recycled_content', 0)
                total_material_input += quantity
                recycled_material_input += quantity * (recycled_content / 100)
        
        metrics['recycled_content_percentage'] = (
            (recycled_material_input / total_material_input * 100) 
            if total_material_input > 0 else 0
        )
        
        # End-of-life recovery rate
        eol_steps = steps.filter(category='end_of_life')
        total_waste = 0
        recovered_waste = 0
        
        for step in eol_steps:
            for waste in step.waste_outputs:
                quantity = waste.get('quantity', 0)
                recovery_rate = waste.get('recovery_rate', 0)
                total_waste += quantity
                recovered_waste += quantity * (recovery_rate / 100)
        
        metrics['recovery_rate'] = (
            (recovered_waste / total_waste * 100) 
            if total_waste > 0 else 0
        )
        
        # Material efficiency (output/input ratio)
        total_output = sum(
            sum(material.get('quantity', 0) for material in step.output_materials)
            for step in steps
        )
        
        metrics['material_efficiency'] = (
            (total_output / total_material_input * 100)
            if total_material_input > 0 else 0
        )
        
        # Overall circularity score (weighted average)
        weights = {'recycled_content_percentage': 0.3, 'recovery_rate': 0.4, 'material_efficiency': 0.3}
        metrics['overall_score'] = sum(
            metrics[metric] * weight for metric, weight in weights.items()
        )
        
        return metrics
    
    def sensitivity_analysis(self, calculation: LCACalculation, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Perform sensitivity analysis on key parameters"""
        base_results = self.calculate_lca(calculation)
        sensitivity_results = {}
        
        for param_name, variations in parameters.items():
            param_results = []
            
            for variation in variations:
                # Create modified calculation
                modified_calc = self._modify_calculation_parameter(calculation, param_name, variation)
                modified_results = self.calculate_lca(modified_calc)
                
                # Calculate relative change
                base_value = base_results['environmental_impacts']['climate_change']
                new_value = modified_results['environmental_impacts']['climate_change']
                relative_change = ((new_value - base_value) / base_value * 100) if base_value > 0 else 0
                
                param_results.append({
                    'variation': variation,
                    'impact_change': relative_change,
                    'absolute_impact': new_value
                })
            
            sensitivity_results[param_name] = param_results
        
        # Rank parameters by sensitivity
        sensitivity_ranking = sorted(
            sensitivity_results.items(),
            key=lambda x: max(abs(r['impact_change']) for r in x[1]),
            reverse=True
        )
        
        return {
            'results': sensitivity_results,
            'ranking': [{'parameter': param, 'max_change': max(abs(r['impact_change']) for r in results)} 
                       for param, results in sensitivity_ranking]
        }
    
    def what_if_analysis(self, calculation: LCACalculation, changes: Dict[str, Any]) -> Dict[str, Any]:
        """Perform what-if scenario analysis"""
        # Calculate baseline
        baseline_results = self.calculate_lca(calculation)
        
        # Apply changes and recalculate
        modified_calc = self._apply_scenario_changes(calculation, changes)
        scenario_results = self.calculate_lca(modified_calc)
        
        # Calculate differences
        impact_differences = {}
        for impact in baseline_results['environmental_impacts']:
            baseline_value = baseline_results['environmental_impacts'][impact]
            scenario_value = scenario_results['environmental_impacts'][impact]
            
            impact_differences[impact] = {
                'absolute_change': scenario_value - baseline_value,
                'relative_change': ((scenario_value - baseline_value) / baseline_value * 100) if baseline_value > 0 else 0,
                'baseline': baseline_value,
                'scenario': scenario_value
            }
        
        # Circularity comparison
        circularity_differences = {}
        for metric in baseline_results['circularity_metrics']:
            baseline_value = baseline_results['circularity_metrics'][metric]
            scenario_value = scenario_results['circularity_metrics'][metric]
            
            circularity_differences[metric] = {
                'absolute_change': scenario_value - baseline_value,
                'relative_change': ((scenario_value - baseline_value) / baseline_value * 100) if baseline_value > 0 else 0,
                'baseline': baseline_value,
                'scenario': scenario_value
            }
        
        return {
            'baseline_results': baseline_results,
            'scenario_results': scenario_results,
            'comparison': {
                'environmental_impacts': impact_differences,
                'circularity_metrics': circularity_differences
            },
            'improvements': self._identify_improvements(impact_differences, circularity_differences)
        }
    
    def _get_default_impact_factors(self, process_category: str) -> Dict[str, float]:
        """Get default impact factors for process categories"""
        defaults = {
            'extraction': {
                'climate_change': 2.5,
                'fossil_depletion': 1.8,
                'metal_depletion': 0.5,
                'water_depletion': 10.0,
            },
            'processing': {
                'climate_change': 1.5,
                'fossil_depletion': 1.2,
                'metal_depletion': 0.2,
                'water_depletion': 5.0,
            },
            'manufacturing': {
                'climate_change': 1.0,
                'fossil_depletion': 0.8,
                'metal_depletion': 0.1,
                'water_depletion': 2.0,
            },
            'transport': {
                'climate_change': 0.5,
                'fossil_depletion': 0.6,
                'metal_depletion': 0.05,
                'water_depletion': 0.1,
            },
            'end_of_life': {
                'climate_change': 0.3,
                'fossil_depletion': 0.2,
                'metal_depletion': -0.1,  # Credit for recovery
                'water_depletion': 1.0,
            },
            'recycling': {
                'climate_change': -1.0,  # Credit for avoided primary production
                'fossil_depletion': -0.8,
                'metal_depletion': -0.5,
                'water_depletion': -2.0,
            }
        }
        
        return defaults.get(process_category, defaults['processing'])
    
    def _get_default_material_factors(self, material_name: str) -> Dict[str, float]:
        """Get default material impact factors"""
        # Simplified material factors (per kg)
        material_factors = {
            'aluminum': {
                'climate_change': 8.2,
                'fossil_depletion': 2.5,
                'metal_depletion': 0.5,
                'water_depletion': 15.0,
            },
            'copper': {
                'climate_change': 3.2,
                'fossil_depletion': 1.8,
                'metal_depletion': 0.8,
                'water_depletion': 25.0,
            },
            'steel': {
                'climate_change': 2.1,
                'fossil_depletion': 1.2,
                'metal_depletion': 0.3,
                'water_depletion': 8.0,
            },
            'plastic': {
                'climate_change': 1.8,
                'fossil_depletion': 2.0,
                'metal_depletion': 0.0,
                'water_depletion': 3.0,
            }
        }
        
        # Try to match material name
        for material, factors in material_factors.items():
            if material.lower() in material_name.lower():
                return factors
        
        # Default generic material
        return material_factors['steel']
    
    def _modify_calculation_parameter(self, calculation: LCACalculation, param_name: str, variation: float):
        """Create a modified calculation for sensitivity analysis"""
        # This would create a temporary modified version
        # For now, return the original calculation
        return calculation
    
    def _apply_scenario_changes(self, calculation: LCACalculation, changes: Dict[str, Any]):
        """Apply scenario changes to calculation"""
        # This would create a modified calculation with the specified changes
        # For now, return the original calculation
        return calculation
    
    def _identify_improvements(self, impact_differences: Dict, circularity_differences: Dict) -> List[str]:
        """Identify improvements from scenario analysis"""
        improvements = []
        
        for impact, data in impact_differences.items():
            if data['relative_change'] < -5:  # 5% reduction
                improvements.append(f"Reduced {impact} by {abs(data['relative_change']):.1f}%")
        
        for metric, data in circularity_differences.items():
            if data['relative_change'] > 5:  # 5% improvement
                improvements.append(f"Improved {metric} by {data['relative_change']:.1f}%")
        
        return improvements


class AIRecommendationService:
    """Service for generating AI-driven recommendations"""
    
    def __init__(self):
        if settings.ENABLE_AI_FEATURES:
            self.recommendation_engine = RecommendationEngine()
        else:
            self.recommendation_engine = None
    
    def generate_suggestions(self, calculation: LCACalculation) -> List[Dict[str, Any]]:
        """Generate AI-driven improvement suggestions"""
        if not self.recommendation_engine:
            return self._get_rule_based_suggestions(calculation)
        
        try:
            # Use AI model to generate suggestions
            suggestions = self.recommendation_engine.generate_recommendations(calculation)
            return suggestions
        except Exception as e:
            logger.warning(f"AI recommendation failed, using rule-based: {str(e)}")
            return self._get_rule_based_suggestions(calculation)
    
    def _get_rule_based_suggestions(self, calculation: LCACalculation) -> List[Dict[str, Any]]:
        """Generate rule-based suggestions as fallback"""
        suggestions = []
        
        # Analyze environmental impacts
        impacts = calculation.environmental_impacts
        climate_change = impacts.get('climate_change', 0)
        
        if climate_change > 10:  # High carbon footprint
            suggestions.append({
                'type': 'energy_efficiency',
                'priority': 'high',
                'title': 'Reduce Energy Consumption',
                'description': 'Consider switching to renewable energy sources or improving energy efficiency.',
                'potential_savings': '15-25% CO2 reduction',
                'implementation': 'Switch to renewable electricity, optimize processes'
            })
        
        # Analyze circularity metrics
        circularity = calculation.circularity_metrics
        recycled_content = circularity.get('recycled_content_percentage', 0)
        
        if recycled_content < 30:  # Low recycled content
            suggestions.append({
                'type': 'material_substitution',
                'priority': 'medium',
                'title': 'Increase Recycled Content',
                'description': 'Replace primary materials with recycled alternatives.',
                'potential_savings': '10-20% environmental impact reduction',
                'implementation': 'Source recycled materials, adjust specifications'
            })
        
        recovery_rate = circularity.get('recovery_rate', 0)
        if recovery_rate < 60:  # Low recovery rate
            suggestions.append({
                'type': 'end_of_life',
                'priority': 'medium',
                'title': 'Improve End-of-Life Management',
                'description': 'Enhance recycling and recovery processes.',
                'potential_savings': '5-15% environmental impact reduction',
                'implementation': 'Design for recyclability, partner with recyclers'
            })
        
        return suggestions[:5]  # Limit to top 5 suggestions
