class WeightedFeatureMatrices(object):
    def __init__(self):
        self._items = []
        self._weights = []

    def add(self, feature_matrice, weight=1.0):
        self._items.append(feature_matrice)
        self._weights.append(weight)

    def get_matrix(self, index):
        return self._items[index]

    def get_weight(self, index):
        return self._weights[index]

    def __len__(self):
        return len(self._items)
