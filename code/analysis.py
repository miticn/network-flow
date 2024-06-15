import pandas as pd
import matplotlib.pyplot as plt


def generate_graphs():
    data = pd.read_csv('docs/rezultati_analiticki.csv')

    colors = ['b', 'g', 'r']
    symbols = ['o', '^', 's']

    # Parametri za svaku vrednost r
    r_values = data['r'].unique()

    for r in r_values:
        subset = data[data['r'] == r]
        
        plt.figure(figsize=(10, 6))

        plt.plot(subset['K'], subset['Ucpu'], color=colors[0], marker=symbols[0], label='CPU')
        plt.plot(subset['K'], subset['Uds1'], color=colors[1], marker=symbols[1], label='System Disk 1')
        plt.plot(subset['K'], subset['Uds2'], color=colors[1], marker=symbols[2], label='System Disk 2')
        plt.plot(subset['K'], subset['Uds3'], color=colors[1], marker=symbols[0], label='System Disk 3')
        plt.plot(subset['K'], subset['Udu1'], color=colors[2], marker=symbols[1], label='User Disk')

        plt.ylim(0, 1)
        plt.xticks(range(2, 5, 1))
        plt.xlabel('K')
        plt.ylabel('U')
        plt.title(f'r = {r}')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.savefig(f'docs/imgs/U_{r}.png')
        plt.show()



    for r in r_values:
        subset = data[data['r'] == r]
        
        plt.figure(figsize=(10, 6))

        plt.plot(subset['K'], subset['Jcpu']/subset['Xcpu'], color=colors[0], marker=symbols[0], label='CPU')
        plt.plot(subset['K'], subset['Jds1']/subset['Xds1'], color=colors[1], marker=symbols[1], label='System Disk 1')
        plt.plot(subset['K'], subset['Jds2']/subset['Xds2'], color=colors[1], marker=symbols[2], label='System Disk 2')
        plt.plot(subset['K'], subset['Jds3']/subset['Xds3'], color=colors[1], marker=symbols[0], label='System Disk 3')
        plt.plot(subset['K'], subset['Jdu1']/subset['Xdu1'], color=colors[2], marker=symbols[1], label='User Disk')

        plt.xticks(range(2, 5, 1))
        plt.xlabel('K')
        plt.ylabel('T')
        plt.title(f'r = {r}')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.savefig(f'docs/imgs/T_{r}.png')
        plt.show()




    for r in r_values:
        subset = data[data['r'] == r]
        
        plt.figure(figsize=(10, 6))

        # Nacrtajte zavisnosti
        plt.plot(subset['K'], subset['T'], color=colors[0], marker=symbols[0], label='System response time')

        plt.xticks(range(2, 5, 1))
        plt.xlabel('K')
        plt.ylabel('T')
        plt.title(f'r = {r}')
        plt.legend(loc='upper right')
        plt.grid(True)
        plt.savefig(f'docs/imgs/Tsys_{r}.png')
        plt.show()