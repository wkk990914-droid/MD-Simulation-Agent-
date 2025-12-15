### Tool 4: ensemble_average - Analyze convergence of a property in a simulation
### Function

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

def ensemble_average(filename: str, property: str, tolerance: float = 0.1, window: int = 50, save: bool = True):
    """
    Compute ensemble average of a property from a LAMMPS log file by checking for convergence and plotting the trajectory
    """
    def parse_lammps_log(log_filename: str) -> dict:
        """Parses the LAMMPS log file and extracts data from a Verlet run."""
        data = {}
        in_run = False
        headers = []
        with open(log_filename, 'r') as file:
            for line in file:
                line = line.strip()

                # Identify the start of the Verlet run output
                if line.startswith('Step'):
                    headers = line.split()
                    for header in headers:
                        data[header] = []
                    in_run = True
                    continue

                # If we're inside a run, collect the data
                elif in_run:
                    if not line or line.startswith('Loop time'):
                        in_run = False
                        continue
                    else:
                        values = line.split()
                        if len(values) == len(headers):
                            for i, value in enumerate(values):
                                try:
                                    data[headers[i]].append(float(value))
                                except ValueError:
                                    data[headers[i]].append(value)
                        else:
                            in_run = False
        return data

    converged = False

    # Load the log file
    data = parse_lammps_log(filename)
    header = list(data.keys())

    # Check if the property is in the headers
    if property not in header:
        raise KeyError(f"The property '{property}' is not found in the log file headers: {header}")

    # Get data from log file
    property_data = data[property]
    timestep_data = data['Step']

    # Convert extracted property data into df
    property_df = pd.DataFrame(data=property_data)

    # Calculate cumulative running average
    cum_running_average_df = property_df.expanding().mean()
    cum_running_average = cum_running_average_df.to_numpy().flatten()

    # Looping parameters
    change_of_CRA = []
    time_change_of_CRA = []
    time_change_index = -1
    index_of_tolerance_met = None

    for ii in np.arange(window, len(cum_running_average_df), window):
        point_1 = cum_running_average[ii - window]
        point_2 = cum_running_average[ii]
        percent_change = np.abs(point_1 - point_2) / np.abs(point_2) * 100

        if percent_change >= tolerance:
            time_change_index += 1
            change_of_CRA = np.append(change_of_CRA, percent_change)
            time_change_of_CRA = np.append(time_change_of_CRA, timestep_data[ii])
        else:
            index_of_tolerance_met = ii
            converged = True
            break

    # Graphing
    if save and converged:
        rolling_running_average_df = property_df.rolling(window).mean()
        rolling_running_average = rolling_running_average_df.to_numpy().flatten()

        fig, ax1 = plt.subplots()
        ax1.set_xlabel('Step')
        ax1.set_ylabel(property)
        ax1.plot(timestep_data, property_data, label=property)
        ax1.plot(timestep_data, cum_running_average, label='Cumulative Running Average')
        ax1.plot(timestep_data, rolling_running_average, label='Rolling Running Average', color='black')
        plt.legend(loc="lower right", bbox_to_anchor=(0.4, -0.3))

        ax2 = ax1.twinx()
        ax2.set_ylabel('% Change of Cumulative Running Average')
        ax2.plot(time_change_of_CRA, change_of_CRA, label='% Change of Cumulative Running Average', color='tab:green')

        if converged:
            ax2.plot([time_change_of_CRA[time_change_index], time_change_of_CRA[time_change_index]],
                     [np.min(change_of_CRA), np.max(change_of_CRA)],
                     color='tab:red', label='Cutoff')

        fig.tight_layout()
        plt.legend(loc="lower left", bbox_to_anchor=(0.4, -0.3))
        plt.savefig(os.path.join("generated_files", f"{property}_trajectory.png"))
        plt.close()

    # Extract Production data
    if converged:
        equilibrium_property_data = property_data[index_of_tolerance_met:]
        equilibrium_time_data = timestep_data[index_of_tolerance_met:]
        equilibrium_production_data = np.vstack((equilibrium_time_data, equilibrium_property_data))
        avg_value = np.mean(equilibrium_production_data[1])
        print(f"Ensemble average (converged) of {property}: {avg_value}")
        return avg_value
    else:
        print(f"Property {property} did not converge within the given window/tolerance")
        return converged

    