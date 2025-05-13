import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.sparse import diags, csr_matrix, lil_matrix
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional, Union, Callable
import numba as nb
from mendeleev import element
import pyamg
from joblib import Parallel, delayed
import multiprocessing

@dataclass
class ElectrodeConfig:
  start: float
  width: float
  ap_start: float
  ap_width: float
  outer_diameter: float
  voltage: float

@dataclass
class MagneticLensConfig:
   start: float
   width: float
   ap_start: float
   ap_width: float
   outer_diameter: float
   mmf: float
   mu_r: float = 1.0

@nb.njit
def get_field(z, r, Ez, Er, Bz, Br, axial_size, radial_size, dz, dr, nz, nr):
  if 0 <= z < axial_size and 0 <= r < radial_size:
      i = int(min(max(0, z / dz), nz - 1))
      j = int(min(max(0, r / dr), nr - 1))
      return Ez[i, j], Er[i, j], Bz[i, j], Br[i, j]
  else:
      return 0.0, 0.0, 0.0, 0.0

@nb.njit
def calc_dynamics(z, r, vz, vr, Ez, Er, Bz, Br, qm, mass, c):
  vsq = vz**2 + vr**2
  csq = c**2
  
  gamma = 1.0 / np.sqrt(1.0 - min(vsq/csq, 0.999))
  
  fz = qm * Ez
  fr = qm * Er
  
  if abs(Bz) > 1e-12 and abs(vz) > 1e-10 and r > 1e-10:
      focusing_factor = qm**2 * Bz**2 / (8 * vz**2)
      fr += -focusing_factor * r
  
  vdotf = vz*fz + vr*fr
  gamma3 = gamma**3
  
  az = fz/gamma - vz * vdotf/(gamma3 * csq)
  ar = fr/gamma - vr * vdotf/(gamma3 * csq)
  
  return np.array([vz, vr, az, ar])

class PotentialField:
  def __init__(self, nz: float, nr: float, axial_size: float, radial_size: float):
      self.nz = int(nz)
      self.nr = int(nr)
      self.axial_size = axial_size
      self.radial_size = radial_size
      self.dz = axial_size / nz
      self.dr = radial_size / nr
      self.potential = np.zeros((self.nz, self.nr))
      self.electrode_mask = np.zeros((self.nz, self.nr), dtype=bool)
      self.Ez = np.zeros((self.nz, self.nr))
      self.Er = np.zeros((self.nz, self.nr))
      self.psi = np.zeros((self.nz, self.nr))
      self.boundary_psi = np.zeros((self.nz, self.nr))
      self.magnetic_mask = np.zeros((self.nz, self.nr), dtype=bool)
      self.mu_r = np.ones((self.nz, self.nr))
      self.Bz = np.zeros((self.nz, self.nr))
      self.Br = np.zeros((self.nz, self.nr))
  
  def add_electrode(self, config: ElectrodeConfig):
      start, width = config.start, config.width
      ap_start, ap_width = config.ap_start, config.ap_width
      outer_diameter = config.outer_diameter
      voltage = config.voltage
      
      ap_center = ap_start + ap_width / 2
      
      r_min = max(0, ap_center - outer_diameter / 2)
      r_max = min(ap_center + outer_diameter / 2, self.nr)
      
      self.potential[int(start):int(start+width), int(r_min):int(r_max)] = voltage
      self.electrode_mask[int(start):int(start+width), int(r_min):int(r_max)] = True
      
      if ap_width > 0:
          self.potential[int(start):int(start+width), int(ap_start):int(ap_start+ap_width)] = 0
          self.electrode_mask[int(start):int(start+width), int(ap_start):int(ap_start+ap_width)] = False

  def add_magnetic_lens(self, config: MagneticLensConfig):
      mu_0 = 4 * np.pi * 1e-7
      
      ap_center = config.ap_start + config.ap_width / 2
      pole_inner = int(max(0, ap_center - config.outer_diameter / 2))
      pole_outer = int(min(ap_center + config.outer_diameter / 2, self.nr))
      
      for i in range(int(config.start), int(config.start + config.width)):
          for j in range(pole_inner, pole_outer):
              if j < int(config.ap_start) or j >= int(config.ap_start + config.ap_width):
                  self.mu_r[i, j] = config.mu_r
                  self.magnetic_mask[i, j] = True
      
      lens_length = config.width * self.dz
      B_gap = mu_0 * config.mu_r * config.mmf / lens_length
      
      for i in range(int(config.start), int(config.start + config.width)):
          for j in range(int(config.ap_start), int(config.ap_start + config.ap_width)):
              psi_value = B_gap * config.ap_width * self.dr * (j - config.ap_start) / config.ap_width
              self.boundary_psi[i, j] = psi_value
              self.magnetic_mask[i, j] = True
  
  def build_laplacian_matrix(self, mask, dirichlet_values=None):
      n = self.nz * self.nr
      A = lil_matrix((n, n))
      b = np.zeros(n)
      
      def idx(i, j):
          return i * self.nr + j
      
      for i in range(self.nz):
          for j in range(self.nr):
              k = idx(i, j)
              
              if mask[i, j]:
                  A[k, k] = 1.0
                  if dirichlet_values is not None:
                      b[k] = dirichlet_values[i, j]
              else:
                  A[k, k] = -4.0
                  
                  if i > 0:
                      A[k, idx(i-1, j)] = 1.0
                  else:
                      A[k, idx(i+1, j)] = 1.0
                      
                  if i < self.nz - 1:
                      A[k, idx(i+1, j)] = 1.0
                  else:
                      A[k, idx(i-1, j)] = 1.0
                      
                  if j > 0:
                      A[k, idx(i, j-1)] = 1.0
                  else:
                      A[k, idx(i, j+1)] = 1.0
                      
                  if j < self.nr - 1:
                      A[k, idx(i, j+1)] = 1.0
                  else:
                      A[k, idx(i, j-1)] = 1.0
      
      return A.tocsr(), b
  
  def build_magnetic_laplacian_matrix(self):
      n = self.nz * self.nr
      A = lil_matrix((n, n))
      b = np.zeros(n)
      
      def idx(i, j):
          return i * self.nr + j
      
      for i in range(self.nz):
          for j in range(self.nr):
              k = idx(i, j)
              r = j * self.dr
              
              if self.magnetic_mask[i, j]:
                  A[k, k] = 1.0
                  b[k] = self.boundary_psi[i, j]
              else:
                  mu_r = self.mu_r[i, j]
                  
                  if r > 1e-10:
                      A[k, k] = -2.0 * (1.0 + self.dr**2/self.dz**2)
                      
                      if i > 0:
                          mu_r_neighbor = self.mu_r[i-1, j]
                          A[k, idx(i-1, j)] = mu_r_neighbor/mu_r * self.dr**2/self.dz**2
                      else:
                          A[k, k] += self.dr**2/self.dz**2
                          
                      if i < self.nz - 1:
                          mu_r_neighbor = self.mu_r[i+1, j]
                          A[k, idx(i+1, j)] = mu_r_neighbor/mu_r * self.dr**2/self.dz**2
                      else:
                          A[k, k] += self.dr**2/self.dz**2
                          
                      if j > 0:
                          A[k, idx(i, j-1)] = 1.0 - 0.5*self.dr/r
                      else:
                          A[k, k] += 1.0 - 0.5*self.dr/r
                          
                      if j < self.nr - 1:
                          A[k, idx(i, j+1)] = 1.0 + 0.5*self.dr/r
                      else:
                          A[k, k] += 1.0 + 0.5*self.dr/r
                  else:
                      A[k, k] = -6.0
                      if i > 0:
                          A[k, idx(i-1, j)] = 1.0
                      if i < self.nz - 1:
                          A[k, idx(i+1, j)] = 1.0
                      if j < self.nr - 1:
                          A[k, idx(i, j+1)] = 4.0
      
      return A.tocsr(), b
  
  def solve_potential(self, max_iterations: float = 2000, convergence_threshold: float = 1e-4):
      A, b = self.build_laplacian_matrix(self.electrode_mask, self.potential)
      
      scale_factor = 1.0 / max(np.max(np.abs(A.data)), 1e-10)
      A_scaled = A * scale_factor
      b_scaled = b * scale_factor
      
      ml = pyamg.smoothed_aggregation_solver(
          A_scaled, 
          max_coarse=10,
          strength='symmetric',
          smooth='jacobi',
          improve_candidates=None
      )
      
      x0 = np.zeros_like(b_scaled)
      x = ml.solve(b_scaled, x0=x0, tol=convergence_threshold, maxiter=int(max_iterations))
      self.potential = x.reshape((self.nz, self.nr))
      
      self.Ez, self.Er = np.gradient(-self.potential, self.dz, self.dr)
      
      if np.any(self.magnetic_mask):
          A_mag, b_mag = self.build_magnetic_laplacian_matrix()
          
          scale_factor_mag = 1.0 / max(np.max(np.abs(A_mag.data)), 1e-10)
          A_mag_scaled = A_mag * scale_factor_mag
          b_mag_scaled = b_mag * scale_factor_mag
          
          ml_mag = pyamg.smoothed_aggregation_solver(
              A_mag_scaled, 
              max_coarse=10,
              strength='symmetric',
              smooth='jacobi',
              improve_candidates=None
          )
          
          x0_mag = np.zeros_like(b_mag_scaled)
          x_mag = ml_mag.solve(b_mag_scaled, x0=x0_mag, tol=convergence_threshold, maxiter=int(max_iterations))
          self.psi = x_mag.reshape((self.nz, self.nr))
          
          for i in range(1, self.nz-1):
              for j in range(1, self.nr-1):
                  self.Bz[i, j] = -(self.psi[i, j+1] - self.psi[i, j-1]) / (2 * self.dr)
                  self.Br[i, j] = (self.psi[i+1, j] - self.psi[i-1, j]) / (2 * self.dz)
      
      return self.potential
  
  def get_field_at_position(self, z: float, r: float) -> Tuple[float, float, float, float]:
      return get_field(z, r, self.Ez, self.Er, self.Bz, self.Br, self.axial_size, self.radial_size, 
                       self.dz, self.dr, self.nz, self.nr)

class ParticleTracer:
  ELECTRON_CHARGE = -1.602e-19 
  ELECTRON_MASS = 9.11e-31
  SPEED_OF_LIGHT = 299792458.0

  def __init__(self, potential_field: PotentialField):
      self.field = potential_field
      self.current_ion = {
          'symbol': 'e-',
          'atomic_number': 0,
          'mass': self.ELECTRON_MASS,
          'charge': self.ELECTRON_CHARGE,
          'charge_mass_ratio': self.ELECTRON_CHARGE / self.ELECTRON_MASS
      }
      self.q_m = self.current_ion['charge_mass_ratio']

  def set_ion(self, symbol: str = 'e-', charge_state: float = 1):
      if symbol == 'e-':
          self.current_ion = {
              'symbol': 'e-',
              'atomic_number': 0,
              'mass': self.ELECTRON_MASS,
              'charge': self.ELECTRON_CHARGE,
              'charge_mass_ratio': self.ELECTRON_CHARGE / self.ELECTRON_MASS
          }
      else:
          elem = element(symbol)
          isotope_mass = elem.mass
          electron_charge = 1.602e-19
          ion_charge = charge_state * electron_charge
          
          self.current_ion = {
              'symbol': f"{symbol}{'+' if charge_state > 0 else '-'}{abs(charge_state)}",
              'atomic_number': elem.atomic_number,
              'mass': isotope_mass * 1.66053906660e-27,
              'charge': ion_charge,
              'charge_mass_ratio': ion_charge / (isotope_mass * 1.66053906660e-27)
          }
      
      self.q_m = self.current_ion['charge_mass_ratio']
      return self

  def get_velocity_from_energy(self, energy_eV: float) -> float:
      kinetic_energy = energy_eV * 1.602e-19
      mass = self.current_ion['mass']
      rest_energy = mass * self.SPEED_OF_LIGHT**2
      total_energy = rest_energy + kinetic_energy
      return self.SPEED_OF_LIGHT * np.sqrt(1 - (rest_energy/total_energy)**2)

  def particle_dynamics(self, t: float, state: List[float]) -> List[float]:
      z, r, vz, vr = state
      Ez, Er, Bz, Br = self.field.get_field_at_position(z, r)
      return calc_dynamics(
          z, r, vz, vr, Ez, Er, Bz, Br,
          self.q_m, self.current_ion['mass'], self.SPEED_OF_LIGHT
      )

  def trace_trajectory(self, 
                 initial_position: Tuple[float, float],
                 initial_velocity: Tuple[float, float],
                 simulation_time: float,
                 method: str = 'BDF',
                 rtol: float = 1e-8,
                 atol: float = 1e-10) -> dict:
      initial_state = [
          initial_position[0], 
          initial_position[1],
          initial_velocity[0], 
          initial_velocity[1]
      ]
  
      solution = solve_ivp(
          self.particle_dynamics,
          (0, simulation_time),
          initial_state,
          method=method,
          rtol=rtol,
          atol=atol)
  
      return solution

class EinzelLens:
  def __init__(self, 
              position: float, 
              width: float, 
              aperture_center: float,
              aperture_width: float,
              outer_diameter: float,
              focus_voltage: float,
              gap_size: int = 1):
      electrode_thickness = (width - 3 * gap_size)/3.0 
      
      self.electrode1 = ElectrodeConfig(
          start=position,
          width=electrode_thickness,
          ap_start=aperture_center - aperture_width/2,
          ap_width=aperture_width,
          outer_diameter=outer_diameter,
          voltage=0
      )
      
      self.electrode2 = ElectrodeConfig(
          start=position + electrode_thickness + gap_size,
          width=electrode_thickness,
          ap_start=aperture_center - aperture_width/2,
          ap_width=aperture_width,
          outer_diameter=outer_diameter,
          voltage=focus_voltage
      )
      
      self.electrode3 = ElectrodeConfig(
          start=position + 2 * electrode_thickness + 2 * gap_size,
          width=electrode_thickness,
          ap_start=aperture_center - aperture_width/2,
          ap_width=aperture_width,
          outer_diameter=outer_diameter,
          voltage=0 
      )
  
  def add_to_field(self, field: PotentialField):
      field.add_electrode(self.electrode1)
      field.add_electrode(self.electrode2)
      field.add_electrode(self.electrode3)

class IonOpticsSystem:
  def __init__(self, nr: float, nz: float, axial_size: float = 0.1, radial_size: float = 0.1):
      self.field = PotentialField(nz, nr, axial_size, radial_size)
      self.tracer = ParticleTracer(self.field)
      self.elements = []

  def add_electrode(self, config: ElectrodeConfig):
      self.field.add_electrode(config)
      self.elements.append(config)
  
  def add_magnetic_lens(self, config: MagneticLensConfig):
      self.field.add_magnetic_lens(config)
      self.elements.append(config)
      
  def add_einzel_lens(self, 
                     position: float, 
                     width: float, 
                     aperture_center: float,
                     aperture_width: float,
                     outer_diameter: float,
                     focus_voltage: float,
                     gap_size: int = 1):
      lens = EinzelLens(
          position, width, aperture_center, aperture_width, 
          outer_diameter, focus_voltage, gap_size
      )
      lens.add_to_field(self.field)
      self.elements.append(lens)
      
  def solve_fields(self):
      return self.field.solve_potential()

  def simulate_beam(self, energy_eV: float, start_z: float,
                       r_range: Tuple[float, float],
                       angle_range: tuple,
                       num_particles: float,
                       simulation_time: float):
      velocity_magnitude = self.tracer.get_velocity_from_energy(energy_eV)
      min_angle_rad = np.radians(angle_range[0])
      max_angle_rad = np.radians(angle_range[1])
      angles = np.linspace(min_angle_rad, max_angle_rad, int(num_particles))
      r_positions = np.linspace(r_range[0], r_range[1], int(num_particles))
  
      trajectories = []
      for r_pos, angle in zip(r_positions, angles):
          vz = velocity_magnitude * np.cos(angle)
          vr = velocity_magnitude * np.sin(angle)
 
          sol = self.tracer.trace_trajectory(
              initial_position=(start_z, r_pos),
              initial_velocity=(vz, vr),
              simulation_time=simulation_time
          )
          trajectories.append(sol)
 
      return trajectories
      
  def simulate_beam_parallel(self, energy_eV: float, start_z: float,
                            r_range: Tuple[float, float],
                            angle_range: tuple,
                            num_particles: float,
                            simulation_time: float,
                            n_jobs: int = -1):
      velocity_magnitude = self.tracer.get_velocity_from_energy(energy_eV)
      min_angle_rad = np.radians(angle_range[0])
      max_angle_rad = np.radians(angle_range[1])
      angles = np.linspace(min_angle_rad, max_angle_rad, int(num_particles))
      r_positions = np.linspace(r_range[0], r_range[1], int(num_particles))
      
      particle_params = []
      for r_pos, angle in zip(r_positions, angles):
          vz = velocity_magnitude * np.cos(angle)
          vr = velocity_magnitude * np.sin(angle)
          particle_params.append((start_z, r_pos, vz, vr))
      
      def trace_particle(params):
          z0, r0, vz0, vr0 = params
          return self.tracer.trace_trajectory(
              initial_position=(z0, r0),
              initial_velocity=(vz0, vr0),
              simulation_time=simulation_time
          )
      
      trajectories = Parallel(n_jobs=n_jobs)(
          delayed(trace_particle)(params) for params in particle_params
      )
      
      return trajectories
      
  def visualize_system(self, 
                     trajectories=None, 
                     r_limits=None,
                     figsize=(15, 6),
                     title="Electron Trajectories"):
      plt.figure(figsize=figsize)
      plt.title(title)
      
      for element in self.elements:
          if isinstance(element, ElectrodeConfig):
              z_start = element.start * self.field.dz
              z_end = (element.start + element.width) * self.field.dz
              
              ap_center = element.ap_start + element.ap_width / 2
              r_inner = element.ap_start * self.field.dr
              r_outer = (element.ap_start + element.ap_width) * self.field.dr
              
              inner_electrode = max(0, (ap_center - element.outer_diameter / 2) * self.field.dr)
              outer_electrode = min((ap_center + element.outer_diameter / 2) * self.field.dr, self.field.radial_size)
              
              plt.fill_between([z_start, z_end], [inner_electrode, inner_electrode], [r_inner, r_inner], 
                             color='#4472C4', alpha=1, linewidth=0)
              plt.fill_between([z_start, z_end], [r_outer, r_outer], [outer_electrode, outer_electrode], 
                             color='#4472C4', alpha=1, linewidth=0)
          
          elif isinstance(element, EinzelLens):
              for electrode in [element.electrode1, element.electrode2, element.electrode3]:
                  z_start = electrode.start * self.field.dz
                  z_end = (electrode.start + electrode.width) * self.field.dz
                  
                  ap_center = electrode.ap_start + electrode.ap_width / 2
                  r_inner = electrode.ap_start * self.field.dr
                  r_outer = (electrode.ap_start + electrode.ap_width) * self.field.dr
                  
                  inner_electrode = max(0, (ap_center - electrode.outer_diameter / 2) * self.field.dr)
                  outer_electrode = min((ap_center + electrode.outer_diameter / 2) * self.field.dr, self.field.radial_size)
                  
                  color = '#4472C4'
                  
                  plt.fill_between([z_start, z_end], [inner_electrode, inner_electrode], [r_inner, r_inner], 
                                 color=color, alpha=1, linewidth=0)
                  plt.fill_between([z_start, z_end], [r_outer, r_outer], [outer_electrode, outer_electrode], 
                                 color=color, alpha=1, linewidth=0)
      
      for element in self.elements:
          if isinstance(element, MagneticLensConfig):
              z_start = element.start * self.field.dz
              z_end = (element.start + element.width) * self.field.dz
              
              ap_center = element.ap_start + element.ap_width / 2
              r_inner = element.ap_start * self.field.dr
              r_outer = (element.ap_start + element.ap_width) * self.field.dr
              
              pole_inner = max(0, (ap_center - element.outer_diameter / 2) * self.field.dr)
              pole_outer = min((ap_center + element.outer_diameter / 2) * self.field.dr, self.field.radial_size)
              
              plt.fill_between([z_start, z_end], [pole_inner, pole_inner], [r_inner, r_inner], 
                             color='#C55A5A', alpha=1, linewidth=0)
              plt.fill_between([z_start, z_end], [r_outer, r_outer], [pole_outer, pole_outer], 
                             color='#C55A5A', alpha=1, linewidth=0)
      
      if trajectories:
          colors = plt.cm.viridis(np.linspace(0, 1, len(trajectories)))
          for i, sol in enumerate(trajectories):
              z_traj = sol.y[0]
              r_traj = sol.y[1]
              plt.plot(z_traj, r_traj, lw=1.5, color=colors[i])
      
      plt.xlabel('z position (meters)')
      plt.ylabel('r position (meters)')
      plt.grid(True, alpha=0.3)
      
      if r_limits:
          plt.ylim(r_limits)
      else:
          plt.ylim(0, self.field.radial_size)
          
      plt.xlim(0, self.field.axial_size)
          
      plt.tight_layout()
      return plt.gcf()