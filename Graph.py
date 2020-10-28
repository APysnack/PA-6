import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np;

def build_graph(seq_1, seq_2, graph, arrow_map, solution):
    plt.rcParams["figure.figsize"] = 4,5
    param = {"grid.linewidth" : 1.6,
             "grid.color"     : "lightgray",
             "axes.linewidth" : 1.6,
             "axes.edgecolor" : "lightgray"}
    plt.rcParams.update(param)

    # top header
    headh = list(seq_1)
    n = len(seq_1) + 1

    # left header
    headv = list(seq_2)
    m = len(seq_2) + 1

    # array zeroed out
    v = np.zeros((m,n), dtype=int)

    # fills out the table values with the values from the graph
    for i in range(m):
        for j in range(n):
            v[i,j] = graph[i][j]

    # plot
    fig, ax=plt.subplots()
    ax.set_xlim(-1.5, v.shape[1]-.5 )
    ax.set_ylim(-1.5, v.shape[0]-.5 )
    ax.invert_yaxis()
    for i in range(v.shape[0]):
        for j in range(v.shape[1]):
            ax.text(j,i,v[i,j], ha="center", va="center")
    for i, l in enumerate(headh):
        ax.text(i+1,-1,l, ha="center", va="center", fontweight="semibold")
    for i, l in enumerate(headv):
        ax.text(-1,i+1,l, ha="center", va="center", fontweight="semibold")

    ax.xaxis.set_minor_locator(ticker.FixedLocator(np.arange(-1.5, v.shape[1]-.5,1)))
    ax.yaxis.set_minor_locator(ticker.FixedLocator(np.arange(-1.5, v.shape[1]-.5,1)))
    plt.tick_params(axis='both', which='both', bottom='off', top='off',
                    left="off", right="off", labelbottom='off', labelleft='off')
    ax.grid(True, which='minor')

    # arrow properties
    arrowprops=dict(facecolor='blue',alpha=0.5, lw=0, width=2, connectionstyle="arc3")
    arrowprops_2=dict(facecolor='red',alpha=0.5, lw=0, width=2, connectionstyle="arc3")

    # places arrows at the locations specified by the arrow map (all cells)
    for cell in arrow_map:
        directions = arrow_map[cell]
        # dictionary key that stores the xy coordinates (a=y, b=x)
        a, b = cell[0], cell[1]

        # note: xy is the coordinate of the arrow head, xytext is the tail location
        for dir in directions:
            # checks the values for each key and annotates with the appropriate arrow
            if dir == 'diagonal':
                ax.annotate("", xy=[b, a], xytext=[b-1, a-1], arrowprops=arrowprops)
            elif dir == 'right':
                ax.annotate("", xy=[b, a], xytext=[b - 1, a], arrowprops=arrowprops)
            elif dir == 'down':
                ax.annotate("", xy=[b, a], xytext=[b, a - 1], arrowprops=arrowprops)


    # places arrows at the locations specified by the solution key
    for key in solution:

        # dictionary key that stores the xy coordinates (a=y, b=x)
        a, b = key[0], key[1]

        # checks the values for each key and annotates with the appropriate arrow
        if solution[key] == 'diagonal':
            ax.annotate("", xy=[b, a], xytext=[b - 1, a - 1], arrowprops=arrowprops_2)
        elif solution[key] == 'right':
            ax.annotate("", xy=[b, a], xytext=[b - 1, a], arrowprops=arrowprops_2)
        elif solution[key] == 'down':
            ax.annotate("", xy=[b, a], xytext=[b, a - 1], arrowprops=arrowprops_2)


    plt.show()