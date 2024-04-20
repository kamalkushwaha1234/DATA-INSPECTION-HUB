# views.py


import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import seaborn as sns

from io import BytesIO
import base64
from django.shortcuts import render

# from scipy.stats import skew, kurtosis
upload_file = None


def generate_pie_chart(data,title):

    labels = list(set(data))
    sizes = [data.count(label) for label in labels]
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.set_title(title)  # Set the title of the chart
    ax.axis('equal')
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    return chart_data

def generate_hist(data, title):
    fig, ax = plt.subplots()
    sns.distplot(data,ax=ax)
    ax.set_title(title)  # Set the title of the chart
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    chart_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    return chart_data

def index1(request):
    if request.method == 'POST':
        global upload_file
        # Get the uploaded file from the request object
        csv_file1 = request.FILES["csvFile"]
        try:
            df= pd.read_csv(csv_file1)
            upload_file=df
            df1=df.head()
            df1= df1.to_html(classes='table table-striped')

            df2=list(df.columns)
            df3=[]
            for i in df2:
                if df[i].dtypes!= 'object':
                    df3.append(i)
            df5=[]
            for i in df2:
                if df[i].dtypes == 'object':
                    df5.append(i)
            df4=[]
            for i in df2:
                if df[i].isnull().any():
                    df4.append(i)
            if len(df4)==0:
                strp="Dataset have not any null value"
            df6 = df.describe()
            df6 = df6.to_html(classes='table table-striped')
            k=df.shape
            row=k[0]
            col=k[1]
            dup=df.duplicated().sum()

            discrete_cols = []
            for col in df.columns:
                if df[col].dtype == 'int64' or df[col].dtype == 'category':
                    if df[col].nunique() < len(df) / 20:
                        discrete_cols.append(col)

            continuous_cols = []
            for col in df.columns:
                if df[col].dtype == 'float64':
                    if df[col].nunique() > len(df) / 20:
                        continuous_cols.append(col)

            ordinal_cols = []
            for col in df.columns:
                if df[col].dtype == 'object':
                    unique_values = df[col].unique()
                    if len(unique_values) > 5 and all(isinstance(val, str) for val in unique_values):
                        ordinal_cols.append(col)

            categorical_cols = []
            for col in df.columns:
                if df[col].dtype == 'object':
                    unique_values = df[col].unique()
                    if len(unique_values) <= 5 or any(isinstance(val, str) for val in unique_values):
                        categorical_cols.append(col)

            boolean_cols = []
            for col in df.columns:
                if df[col].dtype == 'bool':
                    boolean_cols.append(col)

            pie_chart=[]
            for i in df5:
                b_list = df[i].tolist()
                chart = generate_pie_chart(b_list,i)
                pie_chart.append(chart)

            box_chart=[]
            for i in df3:
                b_list = df[i].tolist()
                chart = generate_hist(b_list,i)
                box_chart.append(chart)

            # skew1=[]
            # kurtosis1=[]
            # for i in df5:
            #     data = df[i].tolist()
            #     sk = skew(data)
            #     skew1.append(sk)
            #     ku= kurtosis(data)
            #     kurtosis1.append(ku)
            #
            # headers = ['List 1', 'List 2']
            # table = zip(skew1, kurtosis1)
            # html = tabulate(table, headers=headers, tablefmt='html')
            # html_safe = mark_safe(html)


            return render(request, 'output.html', {'df1':df1,'df2':df2,'df3':df3,'df5':df5,'df4':df4,'strp':strp,'df6':df6,'row':row,'col':col,'dup':dup,'boolean_cols':boolean_cols,
                                                   'categorical_cols':categorical_cols,'ordinal_cols':ordinal_cols,'continuous_cols':continuous_cols,'discrete_cols':discrete_cols,
                                                   'pie_chart':pie_chart,'box_chart': box_chart
                                                   })
        except:
            html_table = "please enter the csv file"
            return render(request, 'index1.html', {'html_table': html_table})
        
    return render(request, 'index1.html')
