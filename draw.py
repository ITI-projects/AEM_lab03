import matplotlib.pyplot as plt


class DrawPlot:
    def __init__(self, coordinates):
        self.x = [e[0] for e in coordinates]
        self.y = [e[1] for e in coordinates]

    def get_all_points(self, visited):
        x_plot = []
        y_plot = []
        for i in range(len(visited)):
            x_plot.append(self.x[visited[i]])
            y_plot.append(self.y[visited[i]])

        x_plot.append(self.x[visited[0]])
        y_plot.append(self.y[visited[0]])

        return x_plot, y_plot

    def draw_results(self, visited, path_to_save, name):
        x_plot, y_plot = self.get_all_points(visited)

        for i, txt in enumerate(visited):
            plt.scatter(x_plot[i], y_plot[i])
            plt.text(x_plot[i], y_plot[i], str(txt), fontsize=9)
        plt.scatter(self.x, self.y)
        plt.title(name)
        plt.plot(x_plot, y_plot)
        plt.xlabel("Oś X")
        plt.ylabel("Oś Y")
        plt.savefig(path_to_save)
        plt.show()
