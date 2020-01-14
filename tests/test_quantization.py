import geomstats.tests

import geomstats.backend as gs

from geomstats.geometry.hypersphere import Hypersphere
from geomstats.learning.quantization import Quantization


class TestQuantizationMethods(geomstats.tests.TestCase):
    _multiprocess_can_split_ = True

    def setUp(self):
        gs.random.seed(1234)

        self.dimension = 2
        self.space = Hypersphere(dimension=self.dimension)
        self.metric = self.space.metric
        self.data = self.space.random_von_mises_fisher(
            kappa=100, n_samples=50)

    def test_fit(self):
        X = self.data
        clustering = Quantization(metric=self.metric, n_clusters=1,
                                  n_repetitions=1)
        clustering.fit(X)

        center = clustering.cluster_centers_
        mean = self.metric.mean(X)
        result = self.metric.dist(center, mean)
        expected = 0.
        self.assertAllClose(expected, result, atol=1e-2)

    def test_predict(self):
        X = self.data
        clustering = Quantization(metric=self.metric, n_clusters=3,
                                  n_repetitions=1)
        clustering.fit(X)

        point = self.data[0, :]
        prediction = clustering.predict(point)

        result = prediction
        expected = clustering.labels_[0]
        self.assertAllClose(expected, result)


if __name__ == '__main__':
    geomstats.tests.main()