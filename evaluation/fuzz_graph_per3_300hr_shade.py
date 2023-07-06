#!/usr/bin/python3
import sys
import matplotlib.pyplot as plt

def main():
    colors = ['y','y','y','b','b','b','g','g','g','r','r','r','orange','orange','orange','c','c','c','m','m','m','k','k','k','purple','purple','purple','brown','brown','brown']
    colors = ['silver','silver','silver','olive','olive','olive','gold','gold','gold','orangered','orangered','orangered','thistle','thistle','thistle']
    colors = ['blueviolet','blueviolet','blueviolet','orange','orange','orange','crimson','crimson','crimson','dimgray','dimgray','dimgray','cadetblue','cadetblue','cadetblue']
    #colors = ['blueviolet','blueviolet','blueviolet','orange','orange','orange','red','red','red','dimgray','dimgray','dimgray','green','green','green']
    c = 0
    shade_y_max = [0] * (3600 * 301 + 1)
    shade_y_min = [100000] * (3600 * 301 + 1)
    shade_y_min[0] = 0
    shade_x = list(range(3600*301 + 1))
    xs = [[],[],[]]
    ys = [[],[],[]]
    for i in range(len(shade_x)):
        shade_x[i] /= 3600

    print(shade_x[-1])
    if len(sys.argv) < 2:
        print("Usage: ./fuzz_graph.py [queue1_plot_data] [plot_data_label1] [queue2_plot_data] [plot_data_label2]... [title]")
    else:
        for i in range(1, len(sys.argv)-1, 2):
            init_time = 0
            x = []
            y = []
            print(sys.argv[i])
            f = open(sys.argv[i], 'r')
            lines = f.readline()  
            lines = f.readlines()
            f.close()
                
            for line in lines:
                if(init_time == 0):
                    init_time = int(line.split(',', 13)[0].strip())
                time_sec = int(line.split(',', 13)[0].strip()) - init_time
                time = (int(line.split(',', 13)[0].strip()) - init_time) / 3600
                if time >= 300:
                    break
        
                x.append(time)
                map_size_percentage = line.split(',', 13)[6].strip().replace("%", "")
                map_size = float(map_size_percentage) * 65536 / 100
                y.append(map_size)
                shade_y_max[time_sec] = max(map_size,shade_y_max[time_sec])
                shade_y_min[time_sec] = min(map_size,shade_y_min[time_sec])
            
            
            #plt.plot(x, y, label = sys.argv[i+1], color=colors[c])
            xs[c%3] = x
            ys[c%3] = y
            if c%3==2:
                for j in range(3600*301 + 1):
                    if shade_y_min[j]==100000:
                        shade_y_min[j] = shade_y_min[j-1]

                    if shade_y_max[j]==0:                      
                        shade_y_max[j] = shade_y_max[j-1]

                plt.plot(shade_x[::10], shade_y_min[::10], shade_x[::10], shade_y_max[::10], color=colors[c], alpha=0.13)
                plt.fill_between(shade_x[:3600*300][::10],shade_y_min[:3600*300][::10],shade_y_max[:3600*300][::10], facecolor=colors[c], alpha=0.13, interpolate=True)

                if (ys[0][-1] <= ys[1][-1] and ys[0][-1] >= ys[2][-1]) or (ys[0][-1] >= ys[1][-1] and ys[0][-1] <= ys[2][-1]):
                    plt.plot(xs[0], ys[0], label = sys.argv[i+1], color=colors[c])
                elif (ys[1][-1] <= ys[0][-1] and ys[1][-1] >= ys[2][-1]) or (ys[1][-1] >= ys[0][-1] and ys[1][-1] <= ys[2][-1]):
                    plt.plot(xs[1], ys[1], label = sys.argv[i+1], color=colors[c])
                else:
                    plt.plot(xs[2], ys[2], label = sys.argv[i+1], color=colors[c])

                shade_y_max = [0] * (3600 * 301 + 1)
                shade_y_min = [100000] * (3600 * 301 + 1)
            c+=1

        # naming the x axis
        plt.xlabel('t(Hour)')
        # naming the y axis
        plt.ylabel('AFL bitmap size')
        # giving a title to my graph
        plt.title(sys.argv[len(sys.argv)-1])

        
        # show a legend on the plot
        plt.legend()
        
        # function to show the plot
        plt.show()
if __name__ == "__main__":
    main()
