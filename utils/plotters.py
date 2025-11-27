import pandas as pd
import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

GACHA_COLORS = {
    'PickupGacha' : 'lightblue',
    'LimitedGacha' : 'orange',
    'FesGacha' : 'pink'
}

EVENT_COLORS = dict(zip(['Collaboration Event', 'Rerun', 'Operation'], sns.color_palette('hls', 3)))

def millions_formatter(x, pos):
    '''
    Format the y-axis ticks to show millions.
    '''
    return f'{x * 1e-6:.1f}M'

def plot_revenue_monthly(df: pd.DataFrame, region: str = 'JP'):
    '''
    Plot the monthly revenue time series with one subplot per year.
    df: revenue DataFrame
    region: string, the region to plot (default is 'JP')
    '''
    # Ensure 'Date' is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort by date
    df = df.sort_values(by='Date')
    
    # Extract unique years
    years = df['Date'].dt.year.unique()
    
    # Create subplots: one row per year
    fig, axes = plt.subplots(len(years), 1, figsize=(12, 4*len(years)), sharey=True)
    
    for ax, year in zip(axes, years):
        subset = df[df['Date'].dt.year == year]
        sns.lineplot(data=subset, x='Date', y=region, ax=ax)
        
        # Format y-axis in millions
        ax.yaxis.set_major_formatter(millions_formatter)
        
        # X-axis: one tick per month
        ax.xaxis.set_major_locator(mdates.MonthLocator())
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

        # Rotate x-axis labels
        ax.tick_params(axis='x', rotation=45)
        
        # Set title
        ax.set_title(f'Revenue for {region} ({year})')

    # Adjust layout
    plt.tight_layout()
    plt.show()

def plot_revenue_yearly(df: pd.DataFrame, region: str = 'JP', events_df: pd.DataFrame = None, step: bool = False, 
                        custom_plotter=None, label: bool = False, legend: bool = False):
    '''
    Plot the yearly revenue time series.

    Parameters
    ----------
    df: pd.DataFrame
        revenue DataFrame

    region: str
        string, the region to plot (default is 'JP')

    events_df: pd.DataFrame, optional
        DataFrame containing event data (default is None)
        Events refer to significant occurrences that may impact revenue (e.g., game releases, updates).

    step: bool
        Whether to use step plotting (default is False)

    custom_plotter: callable, optional
        Optional custom plotting function. Takes matplotlib Axes object and plots extra things.

    label: bool
        Whether to label the events with the custom plotter (default is False)

    legend: bool
        Whether to show the legend (default is False)
    '''

    # Ensure 'Date' is datetime
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Sort by date
    df = df.sort_values(by='Date')

    # Adjust Size
    plt.figure(figsize=(12, 6))
    ax = plt.gca()

    if step:
        # Step plot
        ax.step(df['Date'], df[region], where='post')
    else:
        # Regular lineplot
        sns.lineplot(data=df, x='Date', y=region, ax=ax)

    # Format y-axis in millions
    ax.yaxis.set_major_formatter(millions_formatter)
    
    # X-axis: one tick per year
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y'))

    # Set title
    ax.set_title(f'Revenue for {region}')

    if custom_plotter:
        custom_plotter(ax, events_df, label)

    if legend:
        plt.legend()

    # Adjust layout
    plt.tight_layout()
    plt.show()

def banner_region_plotter(ax: matplotlib.axes.Axes, event_df: pd.DataFrame, label: bool = False):
    '''
    A helper to plot banners on the yearly chart.
    All banners should be of a single type (so for example, event_df 
    can be something like fes_banners_jp, which contains only the 
    fes banners.)

    Parameters          
    ----------
    ax : matplotlib.axes.Axes
        The axes on which to plot the banners.
    event_df : pd.DataFrame
        Banner of a specific type (e.g. FesGacha)
    label: Whether to label the banners.
        Too much labelling might be a little messy.
    '''

    color = GACHA_COLORS.get(event_df['gachaType'].iloc[0], 'gray')

    grouped = (event_df.groupby(['startAt', 'endAt']))['rateups']
    grouped = grouped.apply(lambda x: "\n".join(map(str, x))) # rateups is a list of strings.
    grouped = grouped.reset_index() # removes the multiindex, returning a df
    
    for _, row in grouped.iterrows():
        ax.axvspan(row['startAt'], row['endAt'], color=color, alpha=0.3)
        if label:
            ax.text(
                row['startAt'], # x position
                ax.get_ylim()[1]*0.95,   # y_position (top of the plot)
                row['rateups'], 
                # color=color,
            fontsize=9,
            verticalalignment='top'
        )
            
def story_plotter(ax: matplotlib.axes.Axes, event_df: pd.DataFrame, label: bool = False):
    '''
    A helper to plot the story release dates on the yearly chart.

    Parameters          
    ----------
    ax : matplotlib.axes.Axes
        The axes on which to plot the banners.
    event_df : pd.DataFrame
        df containing story info.
    label: Whether to label the story.
        Too much labelling might be a little messy.
    '''

    labelled_stories = set()
    color_dict = pd.read_pickle('./data/fixtures/story_color_dict.pkl')
    
    for _, row in event_df.iterrows():
        release_date = pd.to_datetime(row['Release Date'])
        story_name = row['Full Name']
        
        if story_name not in labelled_stories: 

            if label:
                ax.text(
                    release_date, # x position
                    ax.get_ylim()[1]*0.95,   # y_position (top of the plot)
                    story_name,
                    fontsize=9,
                    verticalalignment='top'
                )

            ax.axvline(release_date, 
                       color=color_dict[story_name], 
                       alpha=0.85, label=story_name)
            labelled_stories.add(story_name)
        else:
            ax.axvline(release_date, 
                       color=color_dict[story_name], 
                       alpha=0.85)
            
def classify_event(event: str) -> str:
    '''
    Classify the event type based on its name.

    Parameters
    ----------
    event : str
        The name of the event.

    Returns
    -------
    str
        The category of the event.
    '''
    if type(event) is not str:
        return 'Other'
    if 'collab' in event.lower():
        return 'Collaboration Event'
    elif 'rerun' in event.lower():
        return 'Rerun'
    elif 'operation' in event.lower():
        return 'Operation'
    else: 
        return 'Other'
    
def event_plotter(ax: matplotlib.axes.Axes, event_df: pd.DataFrame, label: bool = False):
    '''
    A helper to plot game events on the yearly chart.

    Parameters          
    ----------
    ax : matplotlib.axes.Axes
        The axes on which to plot the banners.
    event_df : pd.DataFrame
        df containing game event information. 
    label: Whether to label the banners.
        Too much labelling might be a little messy.
    '''

    labelled_events = set()
    
    for _, row in event_df.iterrows():
        event_type = classify_event(row['Notes'])
        if event_type not in labelled_events:
            ax.axvspan(row['Start date'], row['End date'], color=EVENT_COLORS.get(event_type, 'gray'), alpha=0.3, label=event_type)
            labelled_events.add(event_type) 
        else: 
            ax.axvspan(row['Start date'], row['End date'], color=EVENT_COLORS.get(event_type, 'gray'), alpha=0.3)

