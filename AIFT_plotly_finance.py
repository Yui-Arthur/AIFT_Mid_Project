import plotly.graph_objects as go
import pandas as pd
import plotly.io as pio
from plotly.subplots import make_subplots

def draw_Candlestick(data , draw_MA = False , draw_BollingerBands = False , draw_TwoMA = False , save_path = None):
    fig = go.Figure(data=[go.Candlestick(
    x = data['Date'],
    open = data['Open'],
    high = data['High'],
    low = data['Low'],
    close = data['Close'],
    increasing_line_color= 'red', 
    decreasing_line_color= 'green')])#修改上漲為紅K 下跌為綠K

    if draw_MA:
        add_MA(fig , data)
    if draw_BollingerBands:
        add_BollingerBands(fig , data)
    if draw_TwoMA:
        add_TwoMA(fig , data)

    layout = go.Layout(
        # plot_bgcolor='#efefef',
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )


    # Update options and show plot
    fig.update_layout(layout)


    fig.show()

    if save_path != None:
        pio.write_image(fig , save_path+".png" , width = 1980, height = 1080)

def draw_combin_fig(data , draw_MA = False , draw_BollingerBands = False , draw_TwoMA = False , save_path = None):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
      go.Candlestick(
      x = data['Date'],
      open = data['Open'],
      high = data['High'],
      low = data['Low'],
      close = data['Close'],
      increasing_line_color= 'red', 
      decreasing_line_color= 'green',
      ),
    #   go.Scatter(x=[1, 2, 3], y=[40, 50, 60], name="yaxis data"),
      secondary_y=False,
      
    )

    if draw_MA:
        add_MA(fig , data)
    if draw_BollingerBands:
        add_BollingerBands(fig , data)
    if draw_TwoMA:
        add_TwoMA(fig , data)

    layout = go.Layout(
        # plot_bgcolor='#efefef',
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )

    fig.add_trace(

        go.Bar(
            x=data["Date"], 
            y=data["Money"],
            marker_color = "rgb(199, 0, 133)"
        # text=y,
        # textposition='auto'
        ),
        secondary_y=True,
    )

   
    # fig.add_trace(
    #     go.Scatter(
    #     x=data["Date"] ,
    #     y=data["Money"] ,
    #     # fill='tonexty',
    #     # fillcolor='rgba(7,128,235,0.2)',
    #     line_color='#FD7800',
    #     line_width = 4,
    #     showlegend=True,
    #     name='Accumulated Capital',
    #     ),
    #     secondary_y=True,
    # )


    # Update options and show plot
    fig.update_layout(layout)

    fig.update_layout(yaxis2 = dict(range=[5000, 200000]))

    fig.show()

    if save_path != None:
        pio.write_image(fig , save_path+".png" , width = 1980, height = 1080)


def add_MA(fig , data):
    fig.add_trace(go.Scatter(
        x=data["Date"] ,
        y=data["MA"] ,
        # fill='tonexty',
        # fillcolor='rgba(100,100,80,0.2)',
        line_color='rgba(0,0,238,0.5)',
        line_width = 2,
        showlegend=True,
        name='MA'
    ))
    return

def add_BollingerBands(fig , data):
    # fig.show()

    fig.add_trace(go.Scatter(
        x=data["Date"] ,
        y=data["down_line"] ,
        # fill='tonexty',
        # fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(255, 189, 116 , 0.7)',
        line_width = 2,
        showlegend=True,
        name='Down line',
    ))

    fig.add_trace(go.Scatter(
        x=data["Date"] ,
        y=data["mid_line"] ,
        # fill='tonexty',
        # fillcolor='rgba(0,100,80,0.2)',
        fill='tonexty',
        fillcolor='rgba(255,184,66,0.2)',
        line_color='rgb(255, 163, 63)',
        line_width = 2,
        showlegend=True,
        name='Mid line',
    ))


    fig.add_trace(go.Scatter(
        x=data["Date"] ,
        y=data["up_line"] ,
        fill='tonexty',
        fillcolor='rgba(255,184,66,0.2)',
        line_color='rgba(255, 219, 72 , 0.7)',
        line_width = 2,
        showlegend=True,
        name='Up line',
    ))

    # fig.show()


def add_TwoMA(fig , data):
    fig.add_trace(go.Scatter(
        x=data["Date"] ,
        y=data["Small MA"] ,
        # fill='tonexty',
        # fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(155,48,255,0.7)',
        line_width = 2,
        showlegend=True,
        name='Short MA',
    ))

    fig.add_trace(go.Scatter(
        x=data["Date"] ,
        y=data["Long MA"] ,
        # fill='tonexty',
        # fillcolor='rgba(100,100,80,0.2)',
        line_color='rgb(7, 128, 235)',
        line_width = 2,
        showlegend=True,
        name='Long MA',
    ))

def draw_KD(data , save_path = None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Date"] ,
        y=data["K"] ,
        # fill='tonexty',
        # fillcolor='rgba(0,100,80,0.2)',
        line_color='rgb(173, 110, 255)',
        showlegend=True,
        name='K',
    ))

    fig.add_trace(go.Scatter(
        x=data["Date"] ,
        y=data["D"] ,
        # fill='tonexty',
        # fillcolor='rgba(0,100,80,0.2)',
        line_color='rgb(255, 163, 63)',
        showlegend=True,
        name='D',
    ))

    layout = go.Layout(
        # plot_bgcolor='#efefef',
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )


    # Update options and show plot
    fig.update_layout(layout)
    

    fig.show()

    if save_path != None:
        pio.write_image(fig , save_path+".png" , width = 1980, height = 1080)


def draw_MACD(data , save_path = None):
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data['macd'],
            line=dict(color='rgb(173, 110, 255)', width=2),
            name='macd',
            # showlegend=False,
            
        )
    )
    # Slow signal (%d)
    fig.add_trace(
        go.Scatter(
            x=data["Date"],
            y=data['signal'],
            line=dict(color='rgb(255, 163, 63)', width=2),
            name='signal'
        )
    )
    # Colorize the histogram values
    colors = np.where(data['hist'] < 0, 'rgb(121, 244, 189)', 'rgb(255, 128, 132)')
    # Plot the histogram
    fig.add_trace(
        go.Bar(
            x=data["Date"],
            y=data['hist'],
            name='histogram',
            marker_color=colors,
        )
    )
    # Make it pretty
    layout = go.Layout(
        # plot_bgcolor='#efefef',
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )


    # Update options and show plot
    fig.update_layout(layout)
    fig.show()

    if save_path != None:
        pio.write_image(fig , save_path+".png" , width = 1980, height = 1080)

def draw_RSI(data , lower_bound , upper_bound , save_path = None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Date"] ,
        y=data["RSI"] ,
        # fill='tonexty',
        # fillcolor='rgba(0,100,80,0.2)',
        line_color='rgba(173, 110, 255 , 0.7)',
        showlegend=True,
        name='RSI',
    ))

    # fig.update_layout(
    #     title='RSI', title_x=0.5, #標題致中
    #     font_color='#000000',
    #     # yaxis=dict(tickformat="4f") #輸出型式
    # )
    fig.add_hline(y=lower_bound, line_width=3, line_dash="dash", line_color="rgba(255, 128, 132 , 0.7)")
    fig.add_hline(y=upper_bound, line_width=3, line_dash="dash", line_color="rgba(121, 244, 189 , 1)")

    layout = go.Layout(
        # plot_bgcolor='#efefef',
        # Font Families
        font_family='Monospace',
        font_color='#000000',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )


    # Update options and show plot
    fig.update_layout(layout)

    fig.show()

    if save_path != None:
        pio.write_image(fig , save_path+".png" , width = 1980, height = 1080)
        
def draw_accumulated_capital(data , lump_sum = pd.DataFrame() , DCA = pd.DataFrame() , save_path = None):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["Date"] ,
        y=data["Money"] ,
        fill='tonexty',
        fillcolor='rgba(7,128,235,0.2)',
        line_color='rgba(7,128,235,0.7)',
        showlegend=True,
        name='Accumulated Capital',
    ))

    layout = go.Layout(
        # plot_bgcolor='#efefef',
        # Font Families
        title='損益表', title_x=0.5,
        font_family='Monospace',
        font_color='#000000',
        font_size=20,
        xaxis=dict(
            rangeslider=dict(
                visible=False
            )
        )
    )

    if not lump_sum.empty:
        add_compare(fig , lump_sum , "Lump Sum" , "rgba(173,110,255,0.7)" , "rgba(173,110,255,0.2)")

    if not DCA.empty:
        add_compare(fig , DCA , "DCA" , "rgba(255,163,63,0.7)" , "rgba(255,163,63,0.2)")


    # Update options and show plot
    fig.update_layout(layout)
    fig.show()
    
    if save_path != None:
        pio.write_image(fig , save_path+".png" , width = 1980, height = 1080)

def add_compare(fig , data , name , color , fillcolor):
    fig.add_trace(go.Scatter(
        x=data["Date"] ,
        y=data["Money"] ,
        fill='tonexty',
        fillcolor=fillcolor,
        line_color=color,
        showlegend=True,
        name= name,
    ))
    