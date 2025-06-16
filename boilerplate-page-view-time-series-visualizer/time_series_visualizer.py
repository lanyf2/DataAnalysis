import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',parse_dates=["date"],index_col='date')

# Clean data
df = df[(df['value']>=df['value'].quantile(0.025))&
        (df['value']<=df['value'].quantile(0.975))]


def draw_line_plot():
    # Draw line plot
    fig,ax=plt.subplots(figsize=(14, 6))
    ax.plot(df.index,df['value'],color='red',linewidth=1)
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    ax.set_xlabel('Date')
    ax.set_ylabel('Page Views')



    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['year']=df_bar.index.year
    df_bar['month']=df_bar.index.month_name()
    pivot_df=df_bar.pivot_table(
        index='year',
        columns='month',
        values='value',
        aggfunc='mean'
    )
    print("透视表内容:")
    print(pivot_df.to_string(na_rep='nan'))

    month_order=['January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December']
    pivot_df = pivot_df.reindex(columns=month_order, fill_value=0)
    # Draw bar plot
    fig=pivot_df.plot(kind='bar',figsize=(10, 6)).get_figure()
    plt.title("Average Daily Page Views for Each Month Grouped by Year")
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

     # 美化图表
    plt.tight_layout()


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
    # 确保月份顺序正确
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    
    # 自定义颜色
    year_colors = ["#3274a1", "#e1812c", "#3a923a", "#c03d3e"]  # 年趋势图颜色
    
    # 创建画布和双子图
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # 第一个箱线图：年趋势 - 修复调色板和标签
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0], 
                hue="year", palette=year_colors, legend=False)
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")
    
    # 第二个箱线图：月季节性 - 修复调色板和标签
    sns.boxplot(x="month", y="value", data=df_box, ax=axes[1], 
                order=month_order, hue="month",legend=False)
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # 美化图表
    plt.tight_layout()


    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
