import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot(data, dvar='values', pvar='phase', mvar='mt', 
         colors=None, title=None, xlabel='day', ylabel=None,
         figsize=(10, 6), dpi=100, grid=True, **kwargs):
    """
    Plot single-case data with phase separation lines and labels.
    
    Parameters:
    ----------
    data : pandas.DataFrame or list of pandas.DataFrame
        Single-case data frame(s) containing measurements
    dvar : str, default='values'
        Name of the dependent variable column
    pvar : str, default='phase'
        Name of the phase variable column
    mvar : str, default='mt'
        Name of the measurement time variable column
    colors : dict, optional
        Dictionary mapping phase names to colors (e.g., {'A': 'blue', 'B': 'red'})
    title : str, optional
        Title for the plot
    xlabel : str, default='day'
        Label for x-axis
    ylabel : str, optional
        Label for y-axis (defaults to dvar if None)
    figsize : tuple, default=(10, 6)
        Figure size in inches (width, height)
    dpi : int, default=100
        Resolution of the figure
    grid : bool, default=True
        Whether to show grid lines
    **kwargs : 
        Additional keyword arguments passed to plt.plot()
    
    Returns:
    -------
    matplotlib.figure.Figure
        The created figure object
    """
    # Convert single dataframe to list for consistent handling
    if isinstance(data, pd.DataFrame):
        data = [data]
    
    # Set default colors if not provided
    if colors is None:
        colors = {'A': 'blue', 'B': 'red', 'C': 'green', 'D': 'purple'}
    
    # Create figure
    fig, axes = plt.subplots(len(data), 1, figsize=figsize, dpi=dpi)
    if not isinstance(axes, np.ndarray):
        axes = [axes]
    
    # Plot each dataset
    for idx, (df, ax) in enumerate(zip(data, axes)):
        # Get unique phases in order of appearance
        phases = df[pvar].unique()
        
        # Plot data points for each phase
        for phase in phases:
            phase_data = df[df[pvar] == phase]
            color = colors.get(phase, 'black')
            ax.plot(phase_data[mvar], phase_data[dvar], 'o-', 
                   label=f'Phase {phase}', color=color, **kwargs)
        
        # Add vertical lines between phases
        phase_changes = []
        prev_phase = None
        for i, phase in enumerate(df[pvar]):
            if phase != prev_phase:
                if i > 0:  # Don't add line at the start
                    # Calculate midpoint between current and previous measurement time
                    x_mid = (df[mvar].iloc[i] + df[mvar].iloc[i-1]) / 2
                    phase_changes.append(x_mid)
                prev_phase = phase
        
        # Draw vertical lines at phase changes
        for x in phase_changes:
            ax.axvline(x=x, color='black', linestyle='--', alpha=0.5)
        
        # Add phase labels at the top
        prev_x = df[mvar].iloc[0]
        for i, x in enumerate([*phase_changes, df[mvar].iloc[-1]]):
            phase = df[pvar].iloc[0] if i == 0 else df[df[mvar] > prev_x][pvar].iloc[0]
            mid_x = (prev_x + x) / 2
            ax.text(mid_x, ax.get_ylim()[1], f'{phase}',
                   horizontalalignment='center', verticalalignment='bottom')
            prev_x = x
        
        # Customize plot
        if grid:
            ax.grid(True, alpha=0.3)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel if ylabel is not None else dvar)
        
        if title:
            if len(data) > 1:
                ax.set_title(f'{title} - Series {idx+1}')
            else:
                ax.set_title(title)
    
    # Adjust layout to prevent label overlap
    plt.tight_layout()
    
    return fig

# Example usage:
if __name__ == "__main__":
    import matplotlib.pyplot as plt  # Add explicit import
    
    # Create sample data
    data = pd.DataFrame({
        'mt': range(1, 13),
        'values': [50, 58, 75, 63, 70, 59, 64, 69, 72, 77, 76, 73],
        'phase': ['A1']*3 + ['B1']*3 + ['A2']*3 + ['B2']*3
    })
    
    # Example 1: Basic plot with default colors
    plot(data)
    plt.show()
    
    # Example 2: Custom colors and multiple series
    colors = {'A1': 'lightblue', 'B1': 'lightgreen', 
             'A2': 'skyblue', 'B2': 'lightseagreen'}
    
    data2 = data.copy()
    data2['values'] = data2['values'] - 10  # Create second series
    
    plot([data, data2], colors=colors, title='Multiple Series Example',
         ylabel='Score', figsize=(12, 8))
    plt.show()