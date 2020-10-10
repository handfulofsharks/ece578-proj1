import seaborn as sns
from matplotlib import pyplot as plt

def plot_wrapper(df):
    for metric in get_metrics(df):
        plot_metrics(df, metric)
    
    
def plot_metrics(df, metric):
    ax = sns.lineplot(data=df,x="frame_rate",y=metric, hue="scenario")
    plt.grid(None)
    plt.show()
    
    
def get_scenarios(df):
    return list(set(df.scenario.values.tolist()))


def get_metrics(df):
    return df.columns.values.tolist()[2:]


def get_x_ticks(df):
    return list(set(df.frame_rate.values.tolist()))