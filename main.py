from simulation_kernel import SimulationKernel
from container import Container
from cup import Cup
from environment import Environment
import pprint

def main():
    sim = SimulationKernel()

    container = Container(
        id="container", temp_init=100, vol_init=1000,
        vol_max=2000, heating_rate=0.005, tea_particle_amount=0,
    )

    sim.add_obj(container)

    env = Environment(
        cooling_rate=0.004,
        ambient_temp=20,
        evap_rate=0.001,
        time_tick=0.001
    )

    sim.config_env(env)
    sim.confirm_setup()

    pp = pprint.PrettyPrinter(indent=3)

    # run simulation for 10s
    for i in range(10000):
        if i % 1000 == 0:
            sim_status = sim.view_status()
            print(f"Time: {i//1000}s")
            pp.pprint(sim_status)
            print()
        sim.advance()

if __name__=="__main__":
    main()