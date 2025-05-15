import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from labchain.simulator import Simulator

def test_yield():
    sim = Simulator(temperature=30)
    sim.add_reagent("Acetic Acid", 0.5)
    sim.add_reagent("Ethanol", 0.5)
    yield_ = sim.calculate_yield()
    assert yield_ > 0
