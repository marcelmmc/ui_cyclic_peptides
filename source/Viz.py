import pandas as pd
import streamlit as st

import base64
from io import BytesIO

from dash import Dash, dcc, html, Input, Output, no_update, callback
import pandas as pd 
from plotly import express as px
#import plotly.graph_objects as go
from dash import dcc
from dash import html

from rdkit.Chem.Draw import rdMolDraw2D
from rdkit import Chem


def get_2d_structure(smiles: str, svg_height: int, svg_width: int) -> str:

    buffered = BytesIO()

    d2d = rdMolDraw2D.MolDraw2DSVG(svg_width, svg_height)
    opts = d2d.drawOptions()
    opts.clearBackground = False
    d2d.DrawMolecule(Chem.MolFromSmiles(smiles))
    d2d.FinishDrawing()
    img_str = d2d.GetDrawingText()
    buffered.write(str.encode(img_str))
    img_str = base64.b64encode(buffered.getvalue())
    img_str = f"data:image/svg+xml;base64,{repr(img_str)[2:-1]}"

    return img_str

def gen_imgs():
    smiles1 = 'C/C=C/C[C@@H](C)[C@@H](O)[C@H]1C(=O)N[C@@H](CC)C(=O)N(C)CC(=O)N(C)[C@@H](CC(C)C)C(=O)N[C@@H](C(C)C)C(=O)N(C)[C@@H](CC(C)C)C(=O)N[C@@H](C)C(=O)N[C@H](C)C(=O)N(C)[C@@H](CC(C)C)C(=O)N(C)[C@@H](CC(C)C)C(=O)N(C)[C@@H](C(C)C)C(=O)N1C'
    smiles2 = 'CC[C@H](C)[C@H]1C(=O)N(C)[C@@H](Cc2ccccc2)C(=O)NCC(=O)N[C@@H]([C@@H](C)O)C(=O)N[C@@H](Cc2ccccc2)C(=O)N(C)[C@@H](CC(C)C)C(=O)N2CCC[C@H]2C(=O)N[C@H](C(=O)N2CCCCC2)CC(=O)N[C@H](C)C(=O)N[C@@H](CC(C)C)C(=O)N(C)[C@@H](C)C(=O)N[C@@H](CC(C)C)C(=O)N1C'
    smiles3 = 'CCO'
    smiles4 = 'CO'
    
    svg_height, svg_width = 400, 400
    strs = []
    for smiles in [smiles1, smiles2, smiles1, smiles3, smiles4]:
        img_str = get_2d_structure(smiles, svg_height, svg_width)
        strs.append(img_str)
    
    
    return strs

Image_strs = gen_imgs()

@callback(
    Output("graph-tooltip-5", "show"),
    Output("graph-tooltip-5", "bbox"),
    Output("graph-tooltip-5", "children"),
    Input("graph-5", "hoverData"),
)
def display_hover(hoverData):
    if hoverData is None:
        return False, no_update, no_update

    # demo only shows the first point, but other points may also be available
    hover_data = hoverData["points"][0]
    bbox = hover_data["bbox"]
    num = hover_data["pointNumber"]

    im_str = Image_strs[num]
    
    children = [
        html.Div([
            html.Img(
                src=im_str,
                style={"width": "150px", 'display': 'block', 'margin': '0 auto'},
            ),
            html.P("SMILE! " + str(num), style={'font-weight': 'bold'})
        ])
    ]

    return True, bbox, children

st.set_page_config(layout="wide")
st.title("Data Viz")
st.caption("LLM Hackathon for Materials & Chemistry - EPFL Hub")

df = pd.DataFrame(
    {'x': [0,1,2,3,4],
        'y': [0,1,4,9,16],
        'i': [0,1,0,3,1],
        }
)






fig = px.scatter(df, x='x', y='y', color='i')

fig.update_traces(
    hoverinfo="none",
    hovertemplate=None,
)

ttip = dcc.Tooltip(id="graph-tooltip-5", direction='bottom')

layout = html.Div(
    className="container",
    children=[
        dcc.Graph(id="graph-5", figure=fig, clear_on_unhover=False),
        dcc.Tooltip(id="graph-tooltip-5", direction='bottom'),
    ],
)

print(type(fig), type(ttip))
st.plotly_chart(fig, theme="streamlit", use_container_width=True)
#st.plotly_chart(ttip)






def setup_app():
    
    #fig = go.Figure(data=[go.Scatter(x=[0, 1], y=[0, 0.4], mode='markers', marker_opacity=0.5, marker_size=0.5)])
    df = pd.DataFrame(
        {'x': [0,1,2,3,4],
         'y': [0,1,4,9,16],
         'i': [0,1,0,1,1],
         }
    )
    fig = px.scatter(df, x='x', y='y', color='i')
    
    #fig = px.scatter(x=[0, 1, 2, 3, 4], y=[0, 1, 4, 9, 16],)

    fig.update_traces(
        hoverinfo="none",
        hovertemplate=None,
    )
    app = Dash(__name__)

    app.layout = html.Div(
        className="container",
        children=[
            dcc.Graph(id="graph-5", figure=fig, clear_on_unhover=False),
            dcc.Tooltip(id="graph-tooltip-5", direction='bottom'),
        ],
    )
    return app

if __name__ == '__main__':
    app = setup_app()
    app.run(debug=True)