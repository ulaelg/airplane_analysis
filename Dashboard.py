import dash
from dash import dcc, html, Output, Input,dash_table
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import numpy as np
##############################################################################################################################
# Load the data for the dashboard
airplane_data = pd.read_csv("Data/Airplane_Crashes_and_Fatalities_Since_1908.csv")
airplane_data_clean = pd.read_csv("Data/cleaned_airplane_crashes.csv")

#############################################################################################################################
# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

##############################################################################################################################
#define styles for the app
app.title = "Airplane Crashes Analysis Dashboard"
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>

        <!-- Google Fonts: Source Sans Pro -->
        <link href="https://fonts.googleapis.com/css2?family=Source+Sans+Pro:wght@300;400;600;700&display=swap" rel="stylesheet">

        {%css%}
        <style>
            body {
                margin: 0 !important;
                padding: 0 !important;
                background-color: #0E1117 !important;
                font-family: 'Source Sans Pro', sans-serif !important;
                color: #FAFAFA;
            }

            #react-entry-point {
                margin: 0 !important;
                padding: 0 !important;
                background-color: #0E1117 !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''
tab_style = {
    "backgroundColor": "transparent",
    "border": "none",
    "borderBottom": "2px solid transparent",
    "color": "#FAFAFA",
    "fontSize": "19px",
    "fontWeight": "500",
    "padding": "12px 20px",
    "outline": "none"
}
q_style={
        "textAlign": "left",
        "color": "#FAFAFA",
        "fontSize": "18px",
        "marginTop": "10px",
        "borderLeft": "4px solid #FF4B4B",
        "padding": "15px",
        "paddingLeft": "20px",
        "fontStyle": "italic",
        "backgroundColor": "rgba(255, 75, 75, 0.1)",
        "fontSize":"23px"
    }
selected_tab_style = {
    "backgroundColor": "transparent",
    "border": "none",
    "borderBottom": "2px solid #FF4B4B",
    "color": "#FF4B4B",
    "fontSize": "28px",
    "fontWeight": "600",
    "padding": "12px 20px",
    "outline": "none"
}
title_style = {
    "color": "#FFFFFF",
    "fontSize": "28px",
    "fontWeight": "500",
    "marginBottom": "20px",
    "textAlign": "left",
    "fontFamily": "Source Sans Pro"
}

##############################################################################################################################
# Define the Home tab content
def home_tab():
    return html.Div([
        html.H2([
            "Welcome to the Airplane Crashes Analysis Dashboard – ",
            html.Strong(
                "an interactive exploration of aviation accident data.",
                style={
                    "borderBottom": "2px solid #FF4B4B",
                    "display": "inline-block",
                    "paddingBottom": "2px",
                    "color": "#FFFFFF",
                    "fontWeight": "200",
                    "fontFamily": "Inter",
                    "fontSize": "22px"
                }
            )
        ], style={
            "color": "#FFFFFF",
            "fontSize": "28px",
            "fontWeight": "300",
            "marginBottom": "20px",
            "textAlign": "left",
            "fontFamily": "Source Sans Pro"
        }),

        html.P(
            [
                "Since the early 20th century, humans have been seeking new forms of transportation to save time. This goal became a reality thanks to Orville and Wilbur Wright, ",
                "who made the first successful flight in the history of self-propelled, heavier-than-air aircraft on December 17, 1903. Orville piloted the gasoline-powered, ",
                "propeller-driven biplane, which stayed aloft for 12 seconds and covered 120 feet during its inaugural flight. ",
                "It was a short trip—but it opened the door to a new era of transportation. Today, there are more than 100,000 flights per day worldwide (based on international statistics from 2019). ",
                "Although air travel is now considered one of the safest modes of transportation, its early days were marked by many tragic accidents. Let's take a closer look at this history!"
            ],
            style={
                "color": "#FAFAFA",
                "fontSize": "20px",
                "fontFamily": "Source Sans Pro",
                "marginBottom": "30px",
                "lineHeight": "1.6",
                "textIndent": "20px"
            }
        ),

        html.H3("🧭 How to Navigate:", style=title_style),

        html.Ol([
            html.Li([
                html.Span(
                    "Use the navigation tabs above to explore different sections of the dashboard:",
                    style={"color": "#FAFAFA", "fontSize": "20px", "fontFamily": "Source Sans Pro"}
                ),
                html.Ul([
                    html.Li([
                        html.Strong(
                            "Exploratory Data Analysis (EDA): ",
                            style={"color": "#FAFAFA", "fontSize": "20px", "fontFamily": "Source Sans Pro"}
                        ),
                        html.Span(
                            "Visualize key statistics, trends, and patterns in the dataset.",
                            style={"color": "#FAFAFA", "fontSize": "20px", "fontFamily": "Source Sans Pro"}
                        )
                    ], style={"marginBottom": "8px"}),
                    html.Li([
                        html.Strong(
                            "Insights & Recommendations: ",
                            style={"color": "#FAFAFA", "fontSize": "20px", "fontFamily": "Source Sans Pro"}
                        ),
                        html.Span(
                            "Discover actionable insights and data-driven suggestions based on the analysis.",
                            style={"color": "#FAFAFA", "fontSize": "20px", "fontFamily": "Source Sans Pro"}
                        )
                    ], style={"marginBottom": "8px"})
                ], style={"marginLeft": "20px", "marginTop": "10px", "marginBottom": "15px"})
            ], style={"marginBottom": "15px", "color": "#FAFAFA", "fontSize": "20px", "fontFamily": "Source Sans Pro"}),

            html.Li(
                "Engage with interactive charts to uncover deeper insights into aviation incidents.",
                style={"marginBottom": "15px", "color": "#FAFAFA", "fontSize": "20px", "fontFamily": "Source Sans Pro"}
            ),

            html.Li(
                "Review the summaries and findings to better understand the key takeaways from the data.",
                style={"marginBottom": "15px", "color": "#FAFAFA", "fontSize": "20px", "fontFamily": "Source Sans Pro"}
            )
        ], style={"marginLeft": "20px", "lineHeight": "1.6"}),

        html.H3("📦 Dataset Overview:", style=title_style),
        html.Div([
            # Total Records Box
            html.Div([
                html.Div("Total Records", style={"color": "#FAFAFA", "fontSize": "24px", "marginBottom": "10px"}),
                html.Div(f"{len(airplane_data):,}", style={"color": "#FF4B4B", "fontWeight": "bold", "fontSize": "24px"})
            ], style={
                "width": "20%",
                "display": "inline-block",
                "textAlign": "center",
                "backgroundColor": "#0E1117",
                "borderRadius": "12px",
                "padding": "18px 13px",
                "margin": "0 1.5%",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.2)"
            }),

            # Columns Box
            html.Div([
                html.Div("Columns", style={"color": "#FAFAFA", "fontSize": "24px", "marginBottom": "10px"}),
                html.Div(f"{len(airplane_data.columns)}", style={"color": "#FF4B4B", "fontWeight": "bold", "fontSize": "24px"})
            ], style={
                "width": "20%",
                "display": "inline-block",
                "textAlign": "center",
                "backgroundColor": "#0E1117",
                "borderRadius": "12px",
                "padding": "18px 13px",
                "margin": "0 6%",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.2)"
            }),

            # Date Range Box
            html.Div([
                html.Div("Date Range", style={"color": "#FAFAFA", "fontSize": "24px", "marginBottom": "10px"}),
                html.Div("1908 - 2009", style={"color": "#FF4B4B", "fontWeight": "bold", "fontSize": "24px"})
            ], style={
                "width": "20%",
                "display": "inline-block",
                "textAlign": "center",
                "backgroundColor": "#0E1117",
                "borderRadius": "12px",
                "padding": "18px 13px",
                "margin": "0 1.5%",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.2)"
            })
        ], style={
            "marginTop": "20px",
            "marginBottom": "40px",
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center"
        }),

        html.H4(
            "Sample Data (First 10 Records):",
            style={
                "color": "#FFFFFF",
                "fontSize": "20px",
                "fontWeight": "600",
                "marginBottom": "15px",
                "fontFamily": "Source Sans Pro"
            }
        ),

        html.Div(id='data-table-container'),

        html.Div([
            html.Div([
                html.H3("📘 Dataset Dictionary:", style=title_style),

                html.P(
                    "The dataset contains the following columns:",
                    style={"color": "#FAFAFA", "fontSize": "20px", "marginBottom": "20px"}
                ),

                html.Ul([
                    html.Li([html.Strong("Date: ", style={"color": "#FF4B4B"}), html.Span("The date when the airplane crash occurred.")]),
                    html.Li([html.Strong("Time: ", style={"color": "#FF4B4B"}), html.Span("The time of day the crash happened (if available).")]),
                    html.Li([html.Strong("Location: ", style={"color": "#FF4B4B"}), html.Span("The geographic location where the crash occurred.")]),
                    html.Li([html.Strong("Operator: ", style={"color": "#FF4B4B"}), html.Span("The airline or company operating the aircraft.")]),
                    html.Li([html.Strong("Flight #: ", style={"color": "#FF4B4B"}), html.Span("The flight number assigned to the aircraft.")]),
                    html.Li([html.Strong("Route: ", style={"color": "#FF4B4B"}), html.Span("The intended or actual flight route.")]),
                    html.Li([html.Strong("Type: ", style={"color": "#FF4B4B"}), html.Span("The aircraft model involved in the crash.")]),
                    html.Li([html.Strong("Registration: ", style={"color": "#FF4B4B"}), html.Span("The aircraft's registration ID.")]),
                    html.Li([html.Strong("cn/In: ", style={"color": "#FF4B4B"}), html.Span("Construction or serial number.")]),
                    html.Li([html.Strong("Aboard: ", style={"color": "#FF4B4B"}), html.Span("Total number of people aboard.")]),
                    html.Li([html.Strong("Fatalities: ", style={"color": "#FF4B4B"}), html.Span("Number of people who died.")]),
                    html.Li([html.Strong("Ground: ", style={"color": "#FF4B4B"}), html.Span("Number of ground fatalities or injuries.")]),
                    html.Li([html.Strong("Summary: ", style={"color": "#FF4B4B"}), html.Span("Brief description of the incident.")])
                ], style={"color": "#FAFAFA", "lineHeight": "1.8", "fontSize": "20px", "marginBottom": "60px","marginRight":'-20px'}),

                html.H3("📄 Project Info:", style=title_style),

                html.P([
                    html.Strong("Author: ", ),
                    html.Span("Khaoula - Data Scientist", style={"color": "#FAFAFA"})
                ], style={"color": "#FAFAFA", "fontSize": "20px", "marginBottom": "10px","marginRight":'-10px'}),

                html.P([
                    html.Strong("GitHub Repository: ", ),
                    html.A(
                        "View Full Code on GitHub",
                        href="https://github.com/KhElgoumiri/airplane_analysis",
                        target="_blank",
                        style={"color": "#FF4B4B", "textDecoration": "underline"}
                    )
                ], style={"color": "#FAFAFA", "fontSize": "20px"}),

                html.P([
                    html.Span("Feel free to explore, fork, or contribute to the project.", style={"color": "#FAFAFA"})
                ], style={"fontSize": "20px", "marginTop": "10px"})
            ], style={
                "width": "60%",
                "display": "inline-block",
                "verticalAlign": "middle",
                "paddingRight": "-50px",
                "marginBottom": "-70px",
            }),

            # Image on the right
            html.Div([
                html.Img(
                    src="/assets/—Pngtree—damaged warplane mid-flight trailing smoke_21098862.png",
                    style={
                        "height": "500px",
                        "width": "500px",
                        "objectFit": "contain",
                        "marginBottom": "10px",
                        "paddingLeft":"-90px"
                    }
                )
            ], style={
                "width": "40%",
                "display": "inline-block",
                "verticalAlign": "center",
                "paddingLeft": "10px"
            })
        ], style={"marginTop": "0px", "display": "flex",  "gap": "0px"})
    ]),


# Define the EDA tab content
def eda_tab():
    return html.Div([
        html.P([
            "Airplane crashes have long captured public attention due to their tragic consequences and complex causes. This dashboard takes you on an "
            "interactive journey to explore aviation accidents through three essential questions:", html.Strong(" When "), "did they occur? ", html.Strong("Where "), " did they happen? And ", html.Strong("Why?"),
            " By answering these, we uncover patterns that can lead to deeper insights—and better safety in the skies.",
        ], style={"color": "#FAFAFA", "fontSize": "20px", "textIndent": "20px"}),

        html.P([
            "First things first—let's look at some quick stats."], style={"color": "#FAFAFA", "fontSize": "20px", "textIndent": "20px"}),
        html.H3("📊 Dataset Quick Summary:", style={"color": "#FFFFFF", "fontSize": "26px", "fontWeight": "600", "marginTop": "20px"}),

        html.Div([
            html.Div([
                html.P("📅 Date Range:", style={"color": "#888", "fontSize": "20px","color": "#ECECEC"}),
                html.P("1908 - 2009", style={"color": "#FF4B4B", "fontSize": "25px", "fontWeight": "bold"})
            ], style={"width": "20%", "display": "inline-block", "textAlign": "center"}),

            html.Div([
                html.P("✈️ Total Crashes:", style={"color": "#888", "fontSize": "20px","color": "#ECECEC"}),
                html.P(f"{len(airplane_data_clean):,}", style={"color": "#FF4B4B", "fontSize": "24px", "fontWeight": "bold"})
            ], style={"width": "20%", "display": "inline-block", "textAlign": "center"}),

            html.Div([
                html.P("💀 Total Fatalities:", style={"color": "#888", "fontSize": "20px","color": "#ECECEC"}),
                html.P(f"{int(airplane_data_clean['Fatalities'].sum()):,}", style={"color": "#FF4B4B", "fontSize": "25px", "fontWeight": "bold"})
            ], style={"width": "20%", "display": "inline-block", "textAlign": "center"}),

            html.Div([
                html.P("📈 Avg Fatality Rate:", style={"color": "#888", "fontSize": "20px","color": "#ECECEC"}),
                html.P(f"{airplane_data_clean['Fatality_Rate'].mean():.2%}", style={"color": "#FF4B4B", "fontSize": "25px", "fontWeight": "bold"})
            ], style={"width": "20%", "display": "inline-block", "textAlign": "center"}),

            html.Div([
                html.P("🧭 Common Operator Type:", style={"color": "#888", "fontSize": "20px","color": "#ECECEC"}),
                html.P(f"{airplane_data_clean['Operator_Type'].mode()[0]}", style={"color": "#FF4B4B", "fontSize": "25px", "fontWeight": "bold"})
            ], style={"width": "20%", "display": "inline-block", "textAlign": "center"}),
        ], style={
            "marginTop": "20px",
            "marginBottom": "40px",
            "backgroundColor": "#0E1117",
            "borderRadius": "12px",
            "padding": "25px 0",
            "boxShadow": "0 4px 8px rgba(0,0,0,0.2)"
        }),

        html.Div([
            html.Div(
                html.P("Are there specific periods when airplane crashes were more frequent? This section breaks down the data by year, month, and time of day to uncover temporal patterns and trends. "
                       "Explore how aviation safety has evolved over the decades and which times pose greater risks."),
                style={"height": "100px",
                       "fontSize": "20px",
                       "marginTop": "-30px",
                       "marginBottom": "-15px",
                       "textIndent": "20px"}),
            html.H3("📅 Time:", style={"color": "#FFFFFF", "fontSize": "26px", "fontWeight": "600", "marginTop": "10px"}),
            html.P("When did crashes happen?", style=q_style),
            html.H5("Crashes Over Time:", style={"color": "#FFFFFF", "fontSize": "24px", "fontWeight": "600", "marginTop": "20px"}),
            dcc.Checklist(
                id='metric-selector',
                options=[
                    {'label': 'Number of Accidents', 'value': 'Accidents'},
                    {'label': 'Number of Fatalities', 'value': 'Fatalities'},
                ],
                value=['Accidents'],   # default
                labelStyle={'display': 'inline-block', 'marginRight': '20px',"fontSize": "19px"},
                style={'color': 'white', 'marginBottom': '5px'}
            ),
            dcc.Graph(id='accident-time-series', style={"height": "500px"}),

            html.Div([
                dcc.Checklist(
                    id='operator-type-selector',
                    options=[
                        {"label": "Civilian", "value": "Civilian"},
                        {"label": "Military", "value": "Military"}
                    ],
                    value=["Civilian", "Military"],
                    labelStyle={"display": "inline-block", "marginRight": "15px","fontSize": "19px"},
                    inputStyle={"marginRight": "5px"},
                    style={"color": "white", "marginBottom": "20px"}
                ),
                html.Div([
                    html.Div([
                        dcc.Graph(id="crash-time-pie-chart")
                    ], style={"width": "38%", "padding": "10px"}),
                    html.Div([
                        dcc.Graph(id="monthly-crash-bar-chart")
                    ], style={"width": "58%", "padding": "10px"})
                ], style={"display": "flex", "justifyContent": "space-between", "flexWrap": "wrap"})
            ]),

            html.Div([
                html.H3(
                    "🔍Search Accidents by Date:",
                    style={
                        "color": "#FFFFFF",
                        "fontSize": "24px",
                        "fontWeight": "400",
                        "marginTop": "40px"
                    }
                ),
                dcc.DatePickerSingle(
                    id='date-picker',
                    min_date_allowed=airplane_data_clean['Date'].min(),
                    max_date_allowed=airplane_data_clean['Date'].max(),
                    initial_visible_month=airplane_data_clean['Date'].max(),
                    date="06/08/2009",
                    style={"marginBottom": "20px"}
                ),
                html.Div(id='date-search-result')
            ], style={
                "backgroundColor": "#0C1016",
                "padding": "30px",
                "borderRadius": "10px",
                "marginTop": "-10px",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)"
            })
        ], style={
            "backgroundColor": "#0E1117",
            "padding": "50px",
            "marginTop": "-25px",
            "borderRadius": "10px",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)"
        }),
       html.Div([],style={"height": "50px"}),

        html.Div([
            html.Div(
                html.P("We've seen that accidents peaked during specific time periods—but where exactly did they occur? Are certain countries more prone to airplane crashes than others?"
                       " This section maps the global distribution of aviation incidents to uncover regional patterns and identify high-risk areas."),
                style={"height": "100px",
                       "fontSize": "21px",
                       "marginTop": "-30px",
                       "marginBottom": "-10px",
                       "textIndent": "20px"}),
            html.H3(
                "🌍 Location:",
                style={
                    "color": "#FFFFFF",
                    "fontSize": "26px",
                    "fontWeight": "600",
                    "marginTop": "40px"
                }
            ),
            html.P("Where did they happen?", style=q_style),
            html.H5(
                "Geographical Distribution of Crashes:",
                style={
                    "color": "#FFFFFF",
                    "fontSize": "24px",
                    "fontWeight": "600",
                    "marginTop": "20px"
                }
            ),
            html.Div([
                dcc.Graph(id='world-map')
            ], style={"height": "600px", "marginTop": "20px"}),

            html.Div([
                html.Div([
                    html.Div([
                        html.H3(
                            "🔍 Search Accidents by Country:",
                            style={
                                "color": "#FFFFFF",
                                "fontSize": "24px",
                                "fontWeight": "400",
                                "marginTop": "40px"
                            }
                        ),
                        dcc.Input(
                            id='country-input',
                            type='text',
                            placeholder='Enter a country name...',
                            style={
                                "width": "100%",
                                "padding": "12px",
                                "borderRadius": "5px",
                                "marginBottom": "20px",
                                "fontSize": "16px",
                                "backgroundColor": "#1E222C",
                                "color": "#FFFFFF",
                                "border": "0px solid #444",
                            }
                        ),
                        html.Div(id='country-search-result')
                    ], style={
                        "padding": "40px",
                        "paddingright": "40px",
                        "borderRadius": "10px",
                        "marginTop": "30px",
                        "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)"
                    }),
                    html.Div([
                        dcc.Graph(id="top-countries-bar-chart")
                    ], style={"width": "58%", "padding": "10px"})
                ], style={"display": "flex", "justifyContent": "space-between", "flexWrap": "wrap"})
            ]),

        ], style={
            "backgroundColor": "#0E1117",
            "padding": "50px",
            "marginTop": "-25px",
            "borderRadius": "10px",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)"
        }),
        html.Div([],style={"height": "10px"}),
        html.Div([
            html.Div(
                html.P("Though the United States tops the list in crash count, this could be a reflection of its flight volume—or something more. What's really driving these numbers?"),
                style={"height": "100px", "fontSize": "21px",
                       "marginTop": "-10px", "marginBottom": "-50px",
                       "textIndent": "20px"}),
            html.H3(
                "💥 Causes:",
                style={
                    "color": "#FFFFFF",
                    "fontSize": "26px",
                    "fontWeight": "600",
                    "marginTop": "40px"
                }
            ),
            html.P("Why did they happen?", style=q_style),

            html.Div([
                html.H3(
                    "Common Words in Accident Summaries:",
                    style={"color": "white", "marginBottom": "30px", "fontWeight": "600", }
                ),
                html.Img(
                    src="/assets/wordcloud_summary.png",
                    style={"width": "100%", "borderRadius": "20px", }
                )
            ], style={"marginBottom": "30px"}),

            html.Div([
                html.H5(
                    "Causes of Airplane Crashes:",
                    style={
                        "color": "#FFFFFF",
                        "fontSize": "26px",
                        "fontWeight": "600",
                        "marginBottom": "20px"
                    }
                ),
                dcc.Graph(id="cause-pie-chart")
            ], style={
                "backgroundColor": "#0E1117"
            }),

            html.Div([
                html.H3(
                    "🔍 Explore Crashes by Cause:",
                    style={
                        "color": "#FFFFFF",
                        "fontSize": "24px",
                        "marginBottom": "20px",
                        "fontWeight": "400"
                    }
                ),
                dcc.Dropdown(
                    id="cause-dropdown",
                    options=[
                        {"label": cause, "value": cause}
                        for cause in sorted(airplane_data_clean['Causes'].dropna().unique())
                    ],
                    value=None,
                    placeholder="Select a cause...",
                    style={
                        "backgroundColor": "#1e222c",
                        "color": "#0A0A0A",
                        "borderRadius": "2px",
                        "padding": "3px",
                        "fontSize": "18px",
                        "border": "0px solid #444",
                        "borderRadius": "5px",
                    }
                ),

                html.Div(id="cause-stats", style={"color": "#FFFFFF", "marginTop": "20px", "fontSize": "18px"}),

            ], style={
                "backgroundColor": "#0E1117",
                "padding": "50px",
                "marginTop": "-25px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)"
            }),
            html.Div(
                html.P("Looking for conclusions and practical takeaways? Don't miss the Insights & Recommendations at the end."),
                style={"height": "100px", "fontSize": "21px",
                       "marginTop": "50px", "marginBottom": "-10px",
                       "textIndent": "20px"}),
        ], style={
            "backgroundColor": "#0E1117",
            "padding": "50px",
            "marginTop": "15px",
            "borderRadius": "10px",
            "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.2)"
        })
    ])


# Define the Recommendations tab content
def recommendations_tab():
    return html.Div([

        html.P([
            "After exploring the temporal, geographical, and causal dimensions of airplane crashes, we now highlight the most "
            "important findings and propose data-driven recommendations for future improvements.",
        ], style={"color": "#FAFAFA", "fontSize": "20px", "textIndent": "20px"}),

        html.H3('📊 Key Insights:', style={"color": "#FFFFFF", "fontSize": "26px", "fontWeight": "600", "marginTop": "20px"}), 

        html.Ul([   
            html.Li("Airplane crashes have steadily declined over the decades, with the highest number of incidents occurring during the 1970s and 1980s. This long-term drop reflects significant improvements in aviation safety, technology, and regulation."),            
            html.Li("The United States reports the highest number of crashes, likely due to its high air traffic volume rather than poor safety performance."),
            html.Li("Pilot error, mechanical failure, and weather conditions are the most frequently reported causes of accidents."),        
            html.Li("Crashes are more frequent during the summer and fall, suggesting possible seasonal operational challenges."),   
            html.Li("Most crashes occur during the day, especially in the early morning hours, indicating that visibility isn't always a determining safety factor."),
        ], style={"color": "#FAFAFA", "fontSize": "20px", "marginLeft": "20px", "lineHeight": "1.6"}),

        html.H3('🎯 Recommendations:', style={"color": "#FFFFFF", "fontSize": "26px", "fontWeight": "600", "marginTop": "20px"}), 
        html.Ul([
            html.Li("Continue investing in pilot training programs, focusing on decision-making and emergency response to reduce pilot error incidents."),
            html.Li("Enhance aircraft maintenance protocols and invest in predictive maintenance technologies to minimize mechanical failures."),
            html.Li("Implement advanced weather forecasting and monitoring systems to improve flight planning and safety during adverse weather conditions."),
            html.Li("Increase safety measures and operational protocols during peak crash seasons (summer and fall) to mitigate risks associated with seasonal challenges."),
            html.Li("Promote the use of flight data monitoring systems to analyze flight operations and identify potential safety issues before they lead to accidents."),
            html.Li("Raise awareness among passengers about the importance of following in-flight safety instructions and crew guidance, especially during takeoff, landing, and emergencies, to improve survivability and reduce panic during incidents.")
        ], style={"color": "#FAFAFA", "fontSize": "20px", "marginLeft": "20px", "lineHeight": "1.6"}),
        html.H3("📚 Conclusion:", style={"color": "#FFFFFF", "fontSize": "26px", "fontWeight": "600", "marginTop": "20px"}),
        html.P([
            "This dashboard provides a comprehensive overview of airplane crashes, revealing trends and patterns that can inform future safety measures. By understanding when, where, and why crashes occur, we can take proactive steps to enhance aviation safety and reduce"
            " the risk of future incidents. The insights gained from this analysis can help stakeholders in the aviation industry, including airlines, regulatory bodies, and safety organizations, make informed decisions that prioritize passenger safety and improve "
            "overall aviation standards."
        ], style={"color": "#FAFAFA", "fontSize": "20px", "textIndent": "20px", "marginTop": "20px"}),
        html.P([html.Strong("As a final point: "), "While aviation today is safer than ever, analyzing its past failures is what ensures a safer future. Data tells the story—if we listen carefully."
            ], style={"color": "#FAFAFA", "fontSize": "20px", "textIndent": "20px", "marginTop": "20px"}),
        html.P([
            "Thank you for exploring the Airplane Crashes Analysis Dashboard! We hope this interactive experience has provided valuable insights into aviation safety and sparked your curiosity about the history of airplane accidents."
        ], style={"color": "#FAFAFA", "fontSize": "20px", "textIndent": "20px", "marginTop": "20px"}),
    ])  
         
def get_data_table():
    return dash_table.DataTable(
        data=airplane_data.head(10).to_dict('records'),
        columns=[{"name": i, "id": i} for i in airplane_data.columns],
        style_table={
            'overflowX': 'auto',
            'border': '1px solid #444'
        },
        style_cell={
            'backgroundColor': "#0E1117",
            'color': 'white',
            'fontSize': '13px',
            'textAlign': 'left',
            'padding': '8px',
            'border': '1px solid #333'
        },
        style_header={
            'backgroundColor': '#FF4B4B',
            'color': 'white',
            'fontWeight': 'bold',
            'border': '1px solid #333'
        },
        page_size=10
    )

def empty_figure_message(message="Please select at least one metric to display."):
    fig = go.Figure()

    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=18, color="white")
    )

    fig.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    return fig

# Main App Layout
app.layout = html.Div([
    html.Div([
        # Header section
        html.Div([
            html.Div([
                html.H1(
                    "Airplane Crashes Analysis",
                    style={
                        "color": "#FFFFFF", "fontSize": "75px",
                        "fontWeight": "500", "margin": 0,
                        "fontFamily": "Caveat, cursive", "lineHeight": "1.2"
                    }
                ),
                html.H1(
                    "Dashboard ✈️",
                    style={
                        "color": "#FF4B4B", "fontSize": "70px",
                        "fontWeight": "500", "margin": 0,
                        "fontFamily": "Caveat, cursive", "lineHeight": "1.2",
                        "alignItems": "center"
                    }
                )
            ], style={"marginRight": "2px"}),

            # Image section
            html.Img(
                src="/assets/—Pngtree—world war ii airplane exploding_21139801.png",
                style={"height": "370px", "marginLeft": "-40px"}
            )
        ], style={
            "display": "flex", "alignItems": "center",
            "justifyContent": "center", "marginBottom": "-80px",
            "paddingTop": "0px"
        }),

        # Tabs section
        dcc.Tabs(
            id="tabs",
            value='tab1',
            children=[
                dcc.Tab(label='Home', value='tab1', style=tab_style, selected_style=selected_tab_style),
                dcc.Tab(label='Exploratory Data Analysis', value='tab2', style=tab_style, selected_style=selected_tab_style),
                dcc.Tab(label='Insights & Recommendations', value='tab3', style=tab_style, selected_style=selected_tab_style),
            ],
            style={
                "backgroundColor": "transparent", "border": "none",
                "borderBottom": "1px solid #333333", "marginBottom": "30px"
            }
        ),

        # Dynamic tab content
        html.Div(id='tabs-content'),

        # Footer section
        html.Footer([
            html.Hr(style={"borderTop": "1px solid #444"}),
            html.P(
                "Built by Khaoula | View source on ",
                style={"color": "#888", "fontSize": "17px", "marginTop": "10px", "display": "inline"}
            ),
            html.A(
                "GitHub",
                href="https://github.com/KhElgoumiri/airplane_analysis",
                target="_blank",
                style={"color": "#FF4B4B", "fontWeight": "bold", "textDecoration": "none","fontSize": "17px"}
            )
        ], style={"textAlign": "center", "marginTop": "60px", "paddingBottom": "20px"})

    ], style={
        "padding": "0 40px 40px 40px",
        "maxWidth": "1200px", "margin": "0 auto"
    })

], style={
    "backgroundColor": "#11181B", "minHeight": "100vh",
    "margin": "0", "padding": "0"
})

##############################################################################################################################
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab1':
        return home_tab()
    elif tab == 'tab2':
        return eda_tab()
    elif tab == 'tab3':
        return recommendations_tab()
    
##############################################################################################################################
@app.callback(
    Output('data-table-container', 'children'),
    Input('tabs', 'value')
)
def update_table(tab_value):
    if tab_value == 'tab1':
        return get_data_table()
    return dash.no_update

##############################################################################################################################
@app.callback(
    Output('accident-time-series', 'figure'),
    Input('metric-selector', 'value')
)
def crash_over_year(selected_metrics):
    # Prepare data: group by year
    summary_by_year = airplane_data_clean.groupby('Year').agg(
                    { 'Date': 'count','Fatalities': 'sum'}).reset_index().rename(columns={'Date': 'Accidents'})
    if not selected_metrics:
        return empty_figure_message("Please select at least one metric to display.")
    
    # Plot normally when something is selected
    fig = px.line(
        summary_by_year,
        x="Year",
        y=selected_metrics,
        labels={"value": "Count", "variable": "Metric"},
        color_discrete_sequence=["#E97451","#800020" ],
        title="Number of accident and Fatalities by Year"  # Custom line colors
    )
   
    fig.update_layout(
            plot_bgcolor="#0E1117",
            paper_bgcolor="#0E1117",
            font_color="white",
            title_font_size=22,  # Increased title font size
            title_x=0.5,
            xaxis = dict(
                    title="Year",
                    tickfont=dict(color="gray"),
                    showline=True,
                    linecolor='gray',  
                    gridcolor='#333'),
            yaxis = dict(
                    title="Count",
                    tickfont=dict(color="gray"),
                    showline=True,
                    linecolor='gray',     
                    gridcolor='#333',
                    range=[0, None] )
            )

    return fig

##############################################################################################################################
@app.callback(
    Output("monthly-crash-bar-chart", "figure"),
    Input("operator-type-selector", "value")
)
def update_bar_chart(selected_types):
    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    airplane_data_clean["Month"] = pd.Categorical(
        airplane_data_clean["Month"], categories=month_order, ordered=True
    )
    # Filter the data
    filtered_df = airplane_data_clean[airplane_data_clean["Operator_Type"].isin(selected_types)]

    # Group and count crashes per month and operator type
    monthly_counts = (
        filtered_df.groupby(["Month", "Operator_Type"])
        .size()
        .reset_index(name="Accident_Count")
    )

    if not selected_types:
        return empty_figure_message("Please select at least one metric to display.")

    # Create the bar chart
    fig = px.bar(
        monthly_counts,
        x="Month",
        y="Accident_Count",
        color="Operator_Type",
        barmode='stack',
        color_discrete_map={
            "Civilian": "#800020",   # Red for Civilian
            "Military": "#E97451"    # Blue for Military
        },
        labels={"Accident_Count": "Number of Crashes", "Month": "Month"},
        category_orders={"Month": month_order},
        title="Crashes by Month and Operator Type",
    )
    # Remove white border from bars
    fig.update_traces(marker_line_width=0)

    fig.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="white",
        title_font_size=22,  # Increased title font size
        title_x=0.45,
        xaxis=dict(
            title="Month",
            tickfont=dict(color="white"),
            showline=True,
            linecolor='gray',
            gridcolor=None
        ),
        yaxis=dict(
            title="Count",
            tickfont=dict(color="white"),
            showline=True,
            linecolor='gray',
            gridcolor='#333',
            range=[0, None]
        )
    )

    return fig

#############################################################################################################################
@app.callback(
    Output("crash-time-pie-chart", "figure"),
    Input("operator-type-selector", "value")
)
def update_pie_chart(selected_types):
    # Categorize Time into periods (e.g., night, morning, afternoon, evening)
    # Handle missing or malformed time values gracefully
    def get_time_period(time_str):
        try:
            hour = int(str(time_str).split(":")[0])
            if 0 <= hour < 6:
                return "Night"
            elif 6 <= hour < 12:
                return "Morning"
            elif 12 <= hour < 18:
                return "Afternoon"
            elif 18 <= hour < 24:
                return "Evening"
        except Exception:
            return "Unknown"
        return "Unknown"

    airplane_data_clean['Time_Period'] = airplane_data_clean['Time'].apply(get_time_period)

    # Filter data
    filtered_data = airplane_data_clean[
        airplane_data_clean["Operator_Type"].isin(selected_types)
    ]

    if not selected_types:
        return empty_figure_message("Please select at least one metric to display.")

    # Create Pie chart
    fig = px.pie(
        filtered_data,
        names="Time_Period",
        title="Crashes by Part of the Day",
        color_discrete_sequence=px.colors.sequential.RdBu
    )

    fig.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="white",
        title_font_size=22,
        title_x=0.45,
            legend=dict(
            font_color="white",
            font=dict(size=16),  
            bgcolor="rgba(0,0,0,0)",
            orientation="v",
            yanchor="bottom",
            y=0.7,
            xanchor="right",
            x=0
        )
    )
      
    fig.update_traces(
        rotation=70,
        hole=0.3,
        marker=dict(line=dict(width=0)),
        domain=dict(x=[1,1], y=[1,1]) 
    )

    return fig
##############################################################################################################################
@app.callback(
    Output('date-search-result', 'children'),
    Input('date-picker', 'date')
)
def display_accidents_per_date(selected_date):
    if not selected_date:
        return html.P("Please select a date to view accident information.", style={"color": "white"})

    df = airplane_data_clean.copy()
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    target_date = pd.to_datetime(selected_date)

    filtered_df = df[df['Date'] == target_date]

    if filtered_df.empty:
        return html.P(f"No accidents found for {target_date.date()}.", style={"color": "white","fontSize": "20px"})
    
    return html.Div([
        html.P(f"Accidents on {target_date.date()}:", style={"color": "#FF4B4B", "fontWeight": "bold", "fontSize": "21px"}),
        html.Ul([
            html.Li([
                html.Span(
                    f"{row['Date'].date()} - {row['Country']} - {row['Operator_Type']} - {row['Type']} - Fatalities: {row['Fatalities']}",
                    style={"color": "#FAFAFA", "fontSize": "20px", "marginBottom": "5px"}
                )
            ]) for _, row in filtered_df.iterrows()
        ], style={"marginLeft": "20px"})
    ])

##############################################################################################################################
@app.callback(
    Output('world-map', 'figure'),
    Input('tabs', 'value')
)
def update_world_map(tab_value):
    country_counts = airplane_data_clean['Country'].value_counts().reset_index()
    country_counts.columns = ['Country', 'Crash_Count']

    # Create choropleth map
    fig = px.choropleth(
        country_counts,
        locations="Country",
        locationmode="country names",
        color="Crash_Count",
        color_continuous_scale="OrRd",
        title="Number of Airplane Crashes by Country"
    )

    fig.update_layout(
        width=1100,
        height=600,
        geo=dict(bgcolor="#0E1117", projection_type="natural earth"),
        paper_bgcolor="#0E1117",
        font_color="white",
        font=dict(size=20),  # Increased font size
        title_font_size=22,  # Increased title font size
        title_x=0.45         # Center the title
    )
    fig.update_geos(
        showcoastlines=True,
        coastlinecolor="white",
        showland=True,
        landcolor="#11181B",
        showlakes=True,
        lakecolor="#444444",
        showocean=True,
        oceancolor="#0E1117"
    )
    fig.update_traces(marker_line_color='white', marker_line_width=0.3)
    return fig
#############################################################################################################################
@app.callback(
    Output("country-search-result", "children"),
    Input("country-input", "value")
)
def search_by_country(country_name):
    if not country_name:
        return html.Div("Please enter a country name.", style={"color": "#FAFAFA", "fontSize": "19px"})

    # Normalize input for comparison
    country = country_name.strip().lower()
    
    # Filter and check matches
    filtered_df = airplane_data_clean[airplane_data_clean["Country"].str.lower() == country]
    
    if filtered_df.empty:
        return html.Div(f"No records found for '{country_name}'.", style={"color": "#FF4B4B"})
    
    num_accidents = len(filtered_df)
    total_fatalities = filtered_df["Fatalities"].sum()

    return html.Div([
        html.P(f"✈️ Total Accidents: {num_accidents}", style={"color": "#FAFAFA", "fontSize": "18px"}),
        html.P(f"💀 Total Fatalities: {total_fatalities}", style={"color": "#FAFAFA", "fontSize": "18px"}),
    ])

############################################################################################################################
@app.callback(
    Output("top-countries-bar-chart", "figure"),
    Input("top-countries-bar-chart", "id") ) 
def update_top_countries_bar_chart(dummy_input):
    # For now, we're not filtering by the country_value, just showing top 10
    top_countries = (
        airplane_data_clean["Country"]
        .value_counts()
        .nlargest(10)
        .rename_axis("Country")
        .reset_index(name="Crash_Count")
    )
    
    fig = px.bar(
        top_countries,
        x="Country",
        y="Crash_Count",
        title="Top 10 Countries by Number of Airplane Crashes",
        color_discrete_sequence=["#800020"],
        template="plotly_dark" 
    )
    
    fig.update_layout(
        plot_bgcolor="#0E1117",
        paper_bgcolor="#0E1117",
        font_color="white",
        title_font_size=22,  # Increased title font size
        title_x=0.45,
        xaxis=dict(
            tickfont=dict(color="white"),
            showline=True,
            linecolor='gray'
        ),
        yaxis=dict(
            title="Count",
            tickfont=dict(color="white"),
            showline=True,
            linecolor='gray',
            gridcolor='#333',
            range=[0, None]
        )
    )
    fig.update_traces(marker_line_width=0)
    
    return fig

##############################################################################################################################
@app.callback(
    Output("cause-pie-chart", "figure"),
    Input("tabs", "value")
)
def update_cause_pie_chart(_):
    # Get cause counts
    cause_counts = airplane_data_clean['Causes'].value_counts().reset_index()
    cause_counts.columns = ['Cause', 'Count']
    
    # Calculate percentages
    total = cause_counts['Count'].sum()
    cause_counts['Percentage'] = (cause_counts['Count'] / total * 100).round(1)
    # Create pie chart
    fig = px.pie(
        cause_counts,
        values='Count',
        names='Cause',
        title='Distribution of Crash Causes',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    fig.update_traces(
        textinfo='percent+label',
        texttemplate='<span style="font-size:16px">%{label}</span><br><span style="font-size:13px">%{percent}</span>',
        rotation=70,
        hole=0.25,
        direction="clockwise",
        sort=False,
        hovertemplate='<b>%{label}</b><br>' +
                      'Percentage: %{percent}<br>' +
                      '<extra></extra>',
        marker=dict(line=dict(width=0)),
        domain=dict(x=[1,1], y=[1,1]) 
    )
    fig.update_layout(
        height=700,
        width=1100,
        margin=dict(t=80, b=10, l=200, r=200),
        paper_bgcolor='#0E1117',
        plot_bgcolor='#0E1117',
        font_color="white",
        title_font_color="white",
        title_font_size=22,  # Increased title font size
        title_x=0.5,
        showlegend=True,
        legend=dict(
            font_color="white",
            font=dict(size=17),  # Updated legend font size
            bgcolor="rgba(0,0,0,0)",
            orientation="v",
            yanchor="bottom",
            y=0.3,
            xanchor="right",
            x=0
        )
    )
    return fig

############################################################################################################################"
@app.callback(
    Output("cause-stats", "children"),
    Input("cause-dropdown", "value")
)
def update_cause_stats(selected_cause):
    filtered = airplane_data_clean[airplane_data_clean['Causes'] == selected_cause]
    crash_count = len(filtered)
    fatality_sum = filtered['Fatalities'].sum()

    return html.Div([
        html.P(f"🛩️ Number of Crashes: {crash_count}", style={"marginBottom": "10px","fontSize": "20px"}),
        html.P(f"☠️ Total Fatalities: {fatality_sum}", style={"marginBottom": "10px","fontSize": "20px"}),
        html.P(f"📊 Fatality Rate: {fatality_sum / crash_count:.2f} per crash" if crash_count > 0 else "No fatality data.")
    ])

#############################################################################################################################

if __name__ == '__main__':
    app.run_server(debug=True)