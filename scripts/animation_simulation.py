#! /usr/bin/env python3

# Simulation Playback environment

# Project imports

# Python imports

# 3rd-party imports
import numpy as np

def animate_double_pend(theta_array,L1=1, T=10):
    """
    Function to generate web-based animation of single-pendulum system

    Parameters:
    ================================================
    theta_array:
        trajectory of theta1
    L1:
        length of the pendulum
    T:
        length/seconds of animation duration

    Returns: None
    """

    ################################
    # Imports required for animation.
    from plotly.offline import iplot
    import plotly.graph_objects as go

    ###############################################
    # Getting data from pendulum angle trajectories.
    xx1=L1*np.sin(theta_array)
    yy1=-L1*np.cos(theta_array)
    N = len(theta_array) # Need this for specifying length of simulation

    ####################################
    # Using these to specify axis limits.
    xm=np.min(xx1)-0.5
    xM=np.max(xx1)+0.5
    ym=np.min(yy1)-2.5
    yM=np.max(yy1)+1.5

    ###########################
    # Defining data dictionary.
    # Trajectories are here.
    data=[dict(x=xx1, y=yy1, 
               mode='lines', name='Arm', 
               line=dict(width=2, color='blue')
              ),
          dict(x=xx1, y=yy1, 
               mode='lines', name='Mass 1',
               line=dict(width=2, color='purple')
              ),
          dict(x=xx1, y=yy1, 
               mode='markers', name='Pendulum 1 Traj', 
               marker=dict(color="purple", size=2)
              ),
        ]

    ################################
    # Preparing simulation layout.
    # Title and axis ranges are here.
    layout=dict(xaxis=dict(range=[xm, xM], autorange=False, zeroline=False,
                    dtick=1),
                yaxis=dict(range=[ym, yM], autorange=False, zeroline=False,
                    scaleanchor = "x",dtick=1),
                title='Simple Pendulum Simulation', 
                hovermode='closest',
                updatemenus= [{'type': 'buttons',
                               'buttons': [{'label': 'Play',
                                            'method': 'animate',
                                            'args': [None, 
                                                     {'frame': {'duration': T, 
                                                                'redraw': False}}]},
                                           {'label': 'Pause',
                                            'method': 'animate',
                                            'args': [[None], 
                                                     {'frame': {'duration': T, 
                                                                'redraw': False}, 
                                                      'mode': 'immediate',
                                                     'transition': {'duration': 0}}]}
                                          ]
                              }]
               )

    ########################################
    # Defining the frames of the simulation.
    # This is what draws the lines from
    # joint to joint of the pendulum.
    frames=[dict(data=[dict(x=[0,xx1[k]], 
                            y=[0,yy1[k]], 
                            mode='lines',
                            line=dict(color='red', width=3)
                            ),
                       go.Scatter(
                            x=[xx1[k]],
                            y=[yy1[k]],
                            mode="markers",
                            marker=dict(color="blue", size=12)),
                      ]) for k in range(N)]

    #######################################
    # Putting it all together and plotting.
    figure1=dict(data=data, layout=layout, frames=frames)           
    iplot(figure1)

##################################################
# animation awesomeness

theta_trajs = np.array(np.linspace(0, np.pi/2, 50))
animate_double_pend(theta_trajs,L1=1,T=30)