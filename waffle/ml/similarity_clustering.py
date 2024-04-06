# -*- coding: utf-8 -*-


class DerivativeClustering:
    def __init__(self, _data, _threshold, _kernel):
        self.clusters = list()
        self.excludes = list()
        self.files = [data["token"] for data in _data]
        self.content = [data["content"] for data in _data]
        self.threshold = _threshold
        self.kernel = _kernel

    def test(self, content_x, content_y):
        measure = self.kernel(content_x, content_y)
        if measure > self.threshold:
            result = True
        else:
            result = False
        return result

    def find_derivative(self, current_index):
        files = self.content
        cluster = [self.files[current_index]]
        if current_index not in self.excludes:
            for i in range(current_index, (len(files)-1)):
                if (i+1) not in self.excludes:
                    if self.test(files[current_index], files[i+1]):
                        cluster.append(self.files[i+1])
                        self.excludes.append(i+1)
        return cluster

    def clustering(self):
        for i in range(len(self.files)-1):
            if i not in self.excludes:
                self.clusters.append(self.find_derivative(i))
                print("Derivative Clustering Ieration: " + str(i))
        return self.clusters