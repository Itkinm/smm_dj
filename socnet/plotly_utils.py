from plotly.offline import iplot, init_notebook_mode
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.io as pio

from django.db.models.functions import TruncDate, TruncWeek
from django.db.models import Count, Sum


def daily_pics(posts):
    file_name = 'post_count.png'
    dates = posts.annotate(date=TruncDate('posted_on'))
    counts= dates.values('date').annotate(count=Count('post_id'))
    data = [go.Bar(
            x=[i['date'] for i in list(counts)],
            y=[i['count'] for i in list(counts)]
            )]
    layout = go.Layout(title='Количество постов')
    fig = go.Figure(data=data, layout=layout)
    pio.write_image(fig, file_name)
    
    return file_name

