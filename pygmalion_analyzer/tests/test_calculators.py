from pygmalion_analyzer.distances.calculators import JensenShannonCalculator
import pandas as pd


def test_1__kld():
    calc = JensenShannonCalculator()
    data = [[0.0, 1.], [0.5, 0.5]]
    data = pd.DataFrame(data)
    kld = calc.run(data)
    assert (kld!=0)