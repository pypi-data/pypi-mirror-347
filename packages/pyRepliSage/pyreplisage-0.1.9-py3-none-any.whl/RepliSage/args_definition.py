import datetime
import re
from dataclasses import dataclass
from math import pi
from typing import Union
import argparse
import openmm as mm
import importlib.resources
from openmm.unit import Quantity

# Dynamically set the default path to the XML file in the package
try:
    with importlib.resources.path('RepliSage.forcefields', 'classic_sm_ff.xml') as default_xml_path:
        default_xml_path = str(default_xml_path)
except FileNotFoundError:
    # If running in a development setup without the resource installed, fallback to a relative path
    default_xml_path = 'RepliSage/forcefields/classic_sm_ff.xml'

# Dynamically set the default path to the XML file in the package
try:
    with importlib.resources.path('RepliSage.data', 'replication_timing_data.parquet') as default_rept_path:
        default_rept_path = str(default_rept_path)
except FileNotFoundError:
    # If running in a development setup without the resource installed, fallback to a relative path
    default_rept_path = 'RepliSage/data/replication_timing_data.parquet'

@dataclass
class Arg(object):
    name: str
    help: str
    type: type
    default: Union[str, float, int, bool, Quantity, None]
    val: Union[str, float, int, bool, Quantity, None]

# Define custom type to parse list from string
def parse_list(s):
    try:
        return [int(x.strip()) for x in s.strip('[]').split(',')]
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid list format. Must be a comma-separated list of integers.")

class ListOfArgs(list):
    quantity_regexp = re.compile(r'(?P<value>[-+]?\d+(?:\.\d+)?) ?(?P<unit>\w+)')

    def get_arg(self, name: str) -> Arg:
        """Stupid arg search in list of args"""
        name = name.upper()
        for i in self:
            if i.name == name:
                return i
        raise ValueError(f"No such arg: {name}")

    def __getattr__(self, item):
        return self.get_arg(item).val

    def parse_args(self):
        parser = argparse.ArgumentParser()
        for arg in self.arg_list:
            parser.add_argument(arg['name'], help=arg['help'], type=arg.get('type', str), default=arg.get('default', ''), val=arg.get('val', ''))

        args = parser.parse_args()
        parsed_args = {arg['name']: getattr(args, arg['name']) for arg in self.arg_list}
        return parsed_args

    def parse_quantity(self, val: str) -> Union[Quantity, None]:
        if val == '':
            return None
        match_obj = self.quantity_regexp.match(val)
        value, unit = match_obj.groups()
        try:
            unit = getattr(mm.unit, unit)
        except AttributeError:
            raise ValueError(f"I Can't recognise unit {unit} in expression {val}. Example of valid quantity: 12.3 femtosecond.")
        return Quantity(value=float(value), unit=unit)

    def to_python(self):
        """Casts string args to ints, floats, bool..."""
        for i in self:
            if i.val == '':
                i.val = None
            elif i.name == "HR_K_PARAM":  # Workaround for complex unit
                i.val = Quantity(float(i.val), mm.unit.kilojoule_per_mole / mm.unit.nanometer ** 2)
            elif i.type == str:
                continue
            elif i.type == int:
                i.val = int(i.val)
            elif i.type == float:
                i.val = float(i.val)
            elif i.type == bool:
                if i.val.lower() in ['true', '1', 'y', 'yes']:
                    i.val = True
                elif i.val.lower() in ['false', '0', 'n', 'no']:
                    i.val = False
                else:
                    raise ValueError(f"Can't convert {i.val} into bool type.")
            elif i.type == Quantity:
                try:
                    i.val = self.parse_quantity(i.val)
                except AttributeError:
                    raise ValueError(f"Can't parse: {i.name} = {i.val}")
            else:
                raise ValueError(f"Can't parse: {i.name} = {i.val}")

    def get_complete_config(self) -> str:
        w = "#######################\n"
        w += "#   RepliSage Model   #\n"
        w += "#######################\n\n"
        w += "# This is automatically generated config file.\n"
        w += f"# Generated at: {datetime.datetime.now().isoformat()}\n\n"
        w += "# Notes:\n"
        w += "# Some fields require units. Units are represented as objects from mm.units module.\n"
        w += "# Simple units are parsed directly. For example: \n"
        w += "# HR_R0_PARAM = 0.2 nanometer\n"
        w += "# But more complex units does not have any more sophisticated parser written, and will fail.'\n"
        w += "# In such cases the unit is fixed (and noted in comment), so please convert complex units manually if needed.\n"
        w += "# <float> and <int> types does not require any unit. Quantity require unit.\n\n"
        w += "# Default values does not mean valid value. In many places it's only a empty field that need to be filled.\n\n"
        w += "#############################################################################################################\n\n"

        w += '[Main]'
        for i in self:
            w += f'; {i.help}, type: {i.type.__name__}, default: {i.default}\n'
            if i.val is None:
                w += f'{i.name} = \n\n'
            else:
                if i.type == Quantity:
                    # noinspection PyProtectedMember
                    w += f'{i.name} = {i.val._value} {i.val.unit.get_name()}\n\n'
                else:
                    w += f'{i.name} = {i.val}\n\n'
        w = w[:-2]
        return w

    def write_config_file(self):
        auto_config_filename = 'config_auto.ini'
        with open(auto_config_filename, 'w') as f:
            f.write(self.get_complete_config())
        print(f"Automatically generated config file saved in {auto_config_filename}")

available_platforms = [mm.Platform.getPlatform(i).getName() for i in range(mm.Platform.getNumPlatforms())]

args = ListOfArgs([
    # Platform settings
    Arg('PLATFORM', help=f"Name of the platform. Available choices: {' '.join(available_platforms)}", type=str, default='CPU', val='CPU'),
    Arg('DEVICE', help="Device index for CUDA or OpenCL (count from 0)", type=str, default='', val=''),
    
    # Input data
    Arg('N_BEADS', help="Number of Simulation Beads.", type=int, default='', val=''),
    Arg('BEDPE_PATH', help="A .bedpe file path with loops. It is required.", type=str, default='', val=''),
    Arg('REPT_PATH', help="The replication timing dataset.", type=str, default='', val=''),
    Arg('SC_REPT_PATH', help="The single cell replication timing dataset.", type=str, default=default_rept_path, val=default_rept_path),
    Arg('OUT_PATH', help="Output folder name.", type=str, default='../results', val='../results'),
    Arg('REGION_START', help="Starting region coordinate.", type=int, default='', val=''),
    Arg('REGION_END', help="Ending region coordinate.", type=int, default='', val=''),
    Arg('CHROM', help="Chromosome that corresponds the the modelling region of interest (in case that you do not want to model the whole genome).", type=str, default='', val=''),
    
    # Replikator
    Arg('REP_WITH_STRESS',help="True in case that you would like to have a helper that sets up the parameters to model replication stress. If it is False, it takes as input REP_T_STD_FACTOR, REP_T_STD_FACTOR, and REP_INIT_RATE_SCALE that user defined.", type=bool, default='False', val='False'),
    Arg('REP_T_STD_FACTOR', help="The factor with which you would like to multiply the standard deviation of replication timing curve.", type=float, default='0.1', val='0.1'),
    Arg('REP_SPEED_SCALE', help="A scale that quantifies the speed of the replication forks.", type=float, default='20', val='20'),
    Arg('REP_INIT_RATE_SCALE', help="A number with which you multiply all values of the experimentally estimated initiation rate.", type=float, default='1.0', val='1.0'),
    
    # Stochastic Simulation parameters
    Arg('LEF_RW', help="True in case that you would like to make cohesins slide as random walk, instead of sliding only in one direction.", type=bool, default='True', val='True'),
    Arg('COHESIN_BLOCKS_CONDENSIN', help="True if cohesins should block condensins during simulation.", type=bool, default='False', val='False'),
    Arg('RANDOM_INIT_SPINS', help="True if the initial distribution of spins should be considered random.", type=bool, default='True', val='True'),
    Arg('P_REW',help="Probability that the Monte Carlo algorithm will propose a rewiring move (move a LEF), instead of epigenetic node state change move.", type=float, default='0.5', val='0.5'),
    Arg('REP_FORK_EPIGENETIC_ORGANIZER', help="If true, it models replication forks as epienetic organizers.", type=bool, default='True', val='True'),
    Arg('REP_START_TIME', help="Time step when the replication starts.", type=int, default='50000', val='50000'),
    Arg('REP_TIME_DURATION', help="Duration of replication.", type=int, default='50000', val='50000'),
    Arg('N_STEPS', help="Number of Monte Carlo steps.", type=int, default='200000', val='200000'),
    Arg('N_LEF', help="Number of loop extrusion factors (condensins and cohesins). If you leave it empty it would add for LEFs twice the number of CTCFs.", type=int, default='', val=''),
    Arg('N_LEF2', help="Number of second family loop extrusion factors, in case that you would like to simulate a second group with different speed.", type=int, default='0', val='0'),
    Arg('MC_STEP', help="Monte Carlo frequency. It should be hundreds of steps so as to avoid autocorrelated ensembles.", type=int, default='200', val='200'),
    Arg('BURNIN', help="Burnin-period (steps that are considered before equillibrium).", type=int, default='1000', val='1000'),
    Arg('T_INIT', help="Initial Temperature of the Stochastic Model.", type=float, default='2.0', val='2.0'),
    Arg('T_FINAL', help="Final Temperature of the Stochastic Model.", type=float, default='1.0', val='1.0'),
    Arg('METHOD', help="Stochastic modelling method. It can be Metropolis or Simulated Annealing.", type=str, default='Annealing', val='Annealing'),
    Arg('FOLDING_COEFF', help="Folding coefficient.", type=float, default='1.0', val='1.0'),
    Arg('FOLDING_COEFF2', help="Folding coefficient for the second family of LEFs.", type=float, default='0.0', val='0.0'),
    Arg('REP_COEFF', help="Replication penalty coefficient.", type=float, default='1.0', val='1.0'),
    Arg('POTTS_INTERACT_COEFF', help="Interaction coefficient of the Potts model.", type=float, default='1.0', val='1.0'),
    Arg('POTTS_FIELD_COEFF', help="Average magnetic field coefficient of the Potts model.", type=float, default='1.0', val='1.0'),
    Arg('CROSS_COEFF', help="LEF crossing coefficient.", type=float, default='1.0', val='1.0'),
    Arg('BIND_COEFF', help="CTCF binding coefficient.", type=float, default='1.0', val='1.0'),
    Arg('SAVE_PLOTS', help="It should be true in case that you would like to save diagnostic plots. In case that you use small MC_STEP or large N_STEPS is better to mark it as False.", type=bool, default='True', val='True'),
    Arg('SAVE_MDT', help="In case that you would like to save metadata of the stochastic simulation.", type=bool, default='True', val='True'),
    
    # Molecular Dynamic Properties
    Arg('INITIAL_STRUCTURE_TYPE', help="you can choose between: rw, confined_rw, self_avoiding_rw, helix, circle, spiral, sphere.", type=str, default='rw', val='rw'),
    Arg('SIMULATION_TYPE', help="It can be either EM (multiple energy minimizations) or MD (one energy minimization and then run molecular dynamics).", type=str, default='', val=''),
    Arg('DCD_REPORTER',help="True if you would like to have a video of the 3D structure in .dcd format.", type=bool, default='False', val='False'),
    Arg('INTEGRATOR_TYPE', help="Type of interator: langevin or brownian.", type=str, default='langevin', val='langevin'),
    Arg('INTEGRATOR_STEP', help="The step of the integrator.", type=Quantity, default='10 femtosecond', val='10 femtosecond'),
    Arg('FORCEFIELD_PATH', help="Path to XML file with forcefield.", type=str, default=default_xml_path, val=default_xml_path),
    Arg('EV_P', help="Probability that randomly excluded volume may be disabled.", type=float, default='0.01', val='0.01'),
    Arg('TOLERANCE', help="Tolerance that works as stopping condition for energy minimization.", type=float, default='1.0', val='1.0'),
    Arg('VIZ_HEATS', help="Visualize the output average heatmap.", type=bool, default='True', val='True'),
    Arg('SIM_TEMP', help="The temperature of the 3D simulation (EM or MD).", type=Quantity, default='310 kelvin', val='310 kelvin'),
    Arg('SIM_STEP', help="This is the amount of simulation steps that are perform each time that we change the loop forces. If this number is too high, the simulation is slow, if is too low it may not have enough time to adapt the structure to the new constraints.", type=int, default='10000', val='10000'),
])
