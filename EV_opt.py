"""
Optimization qusetion:
How to use EV charging to incentivize more wind and solar
"""

from __future__ import division
from pyomo.environ import *
from pyomo.opt import SolverFactory
import pandas as pd
import os
from datetime import datetime

# ---------- Load data with pandas ----------
cf_df  = pd.read_csv('Data/wind_solar_cf.csv').rename(columns=str.strip)

## constants and assumptions
# capital costs for solar, and energy storage systems
solar_cap_cost 			= 0.8       # $/MW
wind_cap_cost 			= 1.0       # $/MW

# energy storage operational assumptions
ESS_min_level    		= 0.20      # %, minimum level of discharge of the battery
EV_eta_c           	= 0.95      # EV charging efficiency, looses 5% when charging

curtailment_cost        = 0.1     # curtailment penalty $/MWH

# create the model
model = AbstractModel(name = 'EV_opt model')

# create model sets
model.t                 = Set(initialize = [i for i in range(8760)], ordered=True)    
model.tech              = Set(initialize =['s_cap', 'w_cap'], ordered=True)  

# parameters
solar_map = dict(zip(cf_df['t'], cf_df['solar']))
wind_map  = dict(zip(cf_df['t'], cf_df['wind']))
model.solar = Param(model.t, initialize=solar_map, within=NonNegativeReals)
model.wind  = Param(model.t, initialize=wind_map,  within=NonNegativeReals)

model.costs             = Param(model.tech, initialize={'s_cap' : solar_cap_cost, 'w_cap': wind_cap_cost})
model.EV_nrel           = Param(model.t, within=NonNegativeReals, default=0.0)
model.EV_avail          = Param(model.t)
model.SOC_req           = Param(model.t)
model.ev_driving        = Param(model.t)
###
# Power cap (kW) when 100% available; availability will scale it.
model.EV_p_cap = Param(within=NonNegativeReals, mutable=True)
# Energy cap (kWh) as the size of the aggregated EV battery.
model.EV_e_cap = Param(within=NonNegativeReals, mutable=True)
###

# load data into parameters, solar and wind data are houlry capacity factor data
path = 'Data/'
data = DataPortal()
data.load(filename = path + 'wind_solar_cf.csv', select = ('t', 'solar'), param = model.solar, index = model.t)
data.load(filename = path + 'wind_solar_cf.csv', select = ('t', 'wind'), param = model.wind, index = model.t)
data.load(filename = path + 'ev_schedule_clean.csv', select = ('t', 'EV_avail'), param = model.EV_avail, index = model.t)
data.load(filename = path + 'ev_schedule_clean.csv', select = ('t', 'SOC_req'), param = model.SOC_req, index = model.t)
data.load(filename = path + 'ev_schedule_clean.csv', select = ('t', 'driving_loss'), param = model.ev_driving, index = model.t)
data.load(filename = path + 'efs_2024.csv', select = ('t', 'value'), param  = model.EV_nrel, index  = model.t)

## define variables
model.cap               = Var(model.tech, domain = NonNegativeReals)
model.EV_opt            = Var(model.t, domain = NonNegativeReals)
model.curt              = Var(model.t, domain = NonNegativeReals)
model.EV_SOC            = Var(model.t, domain=NonNegativeReals)

# define objective function and contraints

# objective 
def obj_expression(model):
    return sum(model.cap[i] * model.costs[i] for i in model.tech)  \
         + sum(model.curt[t] * curtailment_cost for t in model.t)
model.OBJ = Objective(rule=obj_expression)

# supply/demand match constraint
def match_const(model, i):
    return model.solar[i]*model.cap['s_cap'] \
         + model.wind[i]*model.cap['w_cap'] \
         - model.EV_opt[i] - model.curt[i] == 0
model.match = Constraint(model.t, rule=match_const)

# Ensure total annual EV energy delivered matches baseline
def annual_ev_energy_match(model):
    return sum(model.EV_opt[t] for t in model.t) == sum(model.EV_nrel[t] for t in model.t)
model.annual_ev_energy_match = Constraint(rule=annual_ev_energy_match)

# --- Upper & lower bounds from capacity and schedule floor ---
def ev_soc_upper_rule(m, t):
    return m.EV_SOC[t] <= m.EV_e_cap
model.EV_SOC_upper = Constraint(model.t, rule=ev_soc_upper_rule)

def ev_soc_floor_rule(m, t):
    # SOC_req[t] is a fraction in [0,1] from your CSV
    return m.EV_SOC[t] >= m.SOC_req[t] * m.EV_e_cap
model.EV_SOC_floor = Constraint(model.t, rule=ev_soc_floor_rule)

# --- Availability-limited charging cap (kWh in 1h step == kW) ---
def ev_avail_cap_rule(m, t):
    return m.EV_opt[t] <= m.EV_avail[t] * m.EV_p_cap
model.EV_availability_cap = Constraint(model.t, rule=ev_avail_cap_rule)

# Cyclic EV SOC dynamics (wrap last -> first)
def ev_soc_dyn_cyclic_rule(m, t):
    t0, last = min(m.t), max(m.t)
    prev = last if t == t0 else t - 1
    # all in MWh
    return m.EV_SOC[t] == m.EV_SOC[prev] \
           + EV_eta_c * m.EV_opt[t] \
           - m.ev_driving[t] * m.EV_e_cap
model.EV_SOC_dyn_cyclic = Constraint(model.t, rule=ev_soc_dyn_cyclic_rule)

# create instance of the model (abstract only)
model = model.create_instance(data)

###---------
per_ev_max_kw = 7.2
usable_per_ev_kwh = 75.0 * (1 - 0.20)           # 60 kWh usable
c_rate = per_ev_max_kw / usable_per_ev_kwh      # 1/h

annual_ev_mwh = sum(float(value(model.EV_nrel[t])) for t in model.t)     # MWh
sum_loss_frac  = sum(float(value(model.ev_driving[t])) for t in model.t) # unitless
assert sum_loss_frac > 0

EV_e_cap = (EV_eta_c * annual_ev_mwh) / sum_loss_frac   # MWh 
EV_p_cap_MW = c_rate * EV_e_cap                          # MW 

model.EV_e_cap.set_value(EV_e_cap)
model.EV_p_cap.set_value(EV_p_cap_MW)

implied_num_EVs = (EV_e_cap * 1000.0) / usable_per_ev_kwh  # MWh -> kWh
print(f"Implied EV count ~ {implied_num_EVs:,.0f}")
print(f"EV_e_cap={EV_e_cap / 1000:,.0f} MWh, EV_p_cap={EV_p_cap_MW:,.2f} MW")

###---------

opt = SolverFactory('gurobi')
results = opt.solve(model)
# Collect results
t_list = list(model.t)
tc = results.solver.termination_condition
print("Termination:", tc)
if tc not in (TerminationCondition.optimal, TerminationCondition.feasible):
    raise RuntimeError("Solve did not finish with a feasible solution; variables may be uninitialized.")

out = pd.DataFrame({
    "t": t_list,
    "EV_nrel": [float(value(model.EV_nrel[t])) for t in t_list],           # baseline (Param)
    "EV_opt":  [float(value(model.EV_opt[t]))  for t in t_list],            # optimized charging (kWh/h)
    "EV_SOC":  [float(value(model.EV_SOC[t]))  for t in t_list],            # kWh
    "EV_avail":[float(value(model.EV_avail[t])) for t in t_list],           # fraction
    "SOC_req": [float(value(model.SOC_req[t]))  for t in t_list],           # fraction
    "drive_frac":[float(value(model.ev_driving[t])) for t in t_list],       # fraction of cap
})

# Convert driving fraction to kWh using the sized fleet
EV_e_cap_val = float(value(model.EV_e_cap))
out["driving_kWh"] = out["drive_frac"] * EV_e_cap_val

# Optional: quick annual sums
annuals = {
    "EV_nrel_MWh": out["EV_nrel"].sum(),
    "EV_opt_MWh":  out["EV_opt"].sum(),           # MW * 1h = MWh
    "driving_MWh": out["driving_kWh"].sum() / 1000.0,
}
print(annuals)

# Generate a unique identifier, e.g., date-time string
identifier = datetime.now().strftime("%Y%m%d_%H%M%S")

# Construct the output file path
out_file = os.path.join(results_dir, f"ev_opt_results_{identifier}.csv")

# Save to the output file
out.to_csv(out_file, index=False)

print(f"Results saved to {out_file}")
