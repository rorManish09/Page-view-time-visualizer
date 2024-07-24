import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv')
df['date'] = pd.to_datetime(df['date'])

df=df.set_index('date')


# Clean data
all_rows = df['value']
top_rows = all_rows.quantile(.025)
bottom_rows = all_rows.quantile(.975)

df = df.loc[(all_rows>=top_rows)&(all_rows<=bottom_rows)]


def draw_line_plot():
    # Draw line plot

    fig,ax = plt.subplots(figsize=(30,10),dpi=100)
    ax.set_ylabel('Page Views')
    ax.set_xlabel('Date')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    sns.lineplot(data=df)
    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Years'] = df_bar.index.year
    df_bar['Months'] = df_bar.index.month_name()

    df_bar = pd.DataFrame(df_bar.groupby(['Years','Months'],sort=False)['value'].mean().round().reset_index())

    df_bar = df_bar.rename(columns={'value':"Average Page Views"})


    missing_values ={
        'Years': [2016, 2016, 2016, 2016],
        "Months" : ['January', 'February', 'March', 'April'],
        'Average Page Views': [0,0,0,0]
    }
    df_bar = pd.concat([pd.DataFrame(missing_values), df_bar])
    # Draw bar plot

    fig,ax = plt.subplots(figsize=(20,8),dpi=100)
    sns.barplot(data=df_bar, x="Years", y="Average Page Views", hue="Months")
    # Save image and return fig (don't change this part)

    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    fig,ax = plt.subplots(1,2,figsize=(20,10),dpi=100)

    sns.boxplot(data= df_box,x='year',y='value',ax=ax[0])

    ax[0].set_xlabel('Year')
    ax[0].set_ylabel('Page Views')
    ax[0].set_title("Year-wise Box Plot (Trend)")

    order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data=df_box, x="month", y="value",order=order, ax=ax[1])
    ax[1].set_title("Month-wise Box Plot (Seasonality)")
    ax[1].set_xlabel("Month")
    ax[1].set_ylabel("Page Views")

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
