class FigureParameters(object):
    def __init__(self, size_x=20, size_y=20, scaling=0.15):
        self.size_x = size_x
        self.size_y = size_y
        self.scaling = scaling

class ClusteringFigureParameters(FigureParameters):
    def __init__(self, size_x=20, size_y=20, scaling=0.15, xticklabels=1, xticklabels_size=10, majorticklabels_y_rotation=0, majorticklabels_x_rotation=90):
        super(ClusteringFigureParameters, self).__init__(size_x, size_y, scaling)
        self.xticklabels = xticklabels
        self.xticklabels_size = xticklabels_size
        self.majorticklabels_x_rotation = majorticklabels_x_rotation
        self.majorticklabels_y_rotation = majorticklabels_y_rotation
