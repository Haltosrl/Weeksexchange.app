import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import pandas as pd
import os

# Avvio dell'app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Definizione delle opzioni per la personalizzazione
customization_options = [
    {"label": "Vacanza con famiglia e minori", "value": "Vacanza con famiglia e minori"},
    {"label": "Sport", "value": "Sport"},
    {"label": "Gioco di carte", "value": "Gioco di carte"},
    {"label": "Relax totale", "value": "Relax totale"},
    {"label": "Vacanza per coppie senza figli", "value": "Vacanza per coppie senza figli"},
    {"label": "Avventura", "value": "Avventura"},
    {"label": "Cultura e visite guidate", "value": "Cultura e visite guidate"},
    {"label": "Gastronomia", "value": "Gastronomia"},
    {"label": "Benessere e spa", "value": "Benessere e spa"},
    {"label": "Naturismo", "value": "Naturismo"}
]

# Sottocategorie per ciascuna opzione
subcategories = {
    "Sport": [
        {"label": "Padel", "value": "Padel"},
        {"label": "Bicicletta", "value": "Bicicletta"},
        {"label": "Tennis", "value": "Tennis"},
        {"label": "Gym", "value": "Gym"},
        {"label": "Beach Volley", "value": "Beach Volley"}
    ],
    "Gioco di carte": [
        {"label": "Burraco", "value": "Burraco"},
        {"label": "Bridge", "value": "Bridge"},
        {"label": "Scopa", "value": "Scopa"},
        {"label": "Briscola", "value": "Briscola"},
        {"label": "Tresette", "value": "Tresette"},
        {"label": "Scala 40", "value": "Scala 40"}
    ],
    "Vacanza con famiglia e minori": [
        {"label": "Attività per bambini", "value": "Attività per bambini"},
        {"label": "Servizi di babysitting", "value": "Servizi di babysitting"}
    ],
    "Gastronomia": [
        {"label": "Tour enogastronomici", "value": "Tour enogastronomici"},
        {"label": "Degustazioni", "value": "Degustazioni"}
    ]
}

# Variabile codice per il numero identificativo del cliente
cliente_id = "12345"


app.layout = html.Div(
    style={"backgroundColor": "#f8f9fa", "padding": "20px"},
    children=[
        dbc.Container([
            html.H1("Personalizzazione della Vacanza Holibuy", className="text-center my-4", style={"color": "#007bff"}),
            html.P("Seleziona le opzioni che preferisci per rendere la tua vacanza perfetta:", className="lead text-center mb-5"),

            dbc.Row([
                dbc.Col([
                    dbc.Label("Codice Identificativo Cliente", className="fw-bold"),
                    dbc.Input(id="cliente-id", type="text", value=cliente_id, readonly=True, className="mb-4")
                ], width=6, className="mx-auto")
            ], className="my-4"),

            dbc.Row([
                dbc.Col([
                    html.Div([
                        dcc.Checklist(
                            options=[customization_options[i]],
                            value=[],
                            id=f"customization-checklist-{i}",
                            inline=False,
                            className="mb-3",
                            labelStyle={"margin-left": "5px"}
                        ),
                        html.Div(
                            [
                                dcc.Checklist(
                                    options=subcategories.get(customization_options[i]['value'], []),
                                    value=[],
                                    id=f"{customization_options[i]['value'].lower().replace(' ', '-')}-subcategories",
                                    inline=False,
                                    className="ms-4",
                                    labelStyle={"margin-left": "5px"}
                                ),
                                dbc.Label("Altro", className="fw-bold mt-3"),
                                dbc.Input(id=f"{customization_options[i]['value'].lower().replace(' ', '-')}-altro", type="text", placeholder="Specifica altro...", className="mb-4")
                            ],
                            id=f"{customization_options[i]['value'].lower().replace(' ', '-')}-subcategories-div",
                            style={"display": "none"}
                        )
                    ]) for i in range(len(customization_options))
                ], width=12),
            ], className="my-4"),

            dbc.Row([
                dbc.Col([
                    dbc.Button("Invia Preferenze", id="submit-button", color="primary", className="mt-4", n_clicks=0)
                ], width=4, className="text-center mx-auto")
            ])
        ])
    ]
)

# Callback per mostrare/nascondere le sottocategorie
@app.callback(
    [Output(f"{customization_options[i]['value'].lower().replace(' ', '-')}-subcategories-div", 'style') for i in range(len(customization_options))],
    [Input(f"customization-checklist-{i}", 'value') for i in range(len(customization_options))]
)
def toggle_subcategories(*checklist_values):
    styles = []
    for i, value in enumerate(checklist_values):
        if customization_options[i]['value'] in value:
            styles.append({"margin-left": "20px", "margin-top": "10px", "display": "block"})
        else:
            styles.append({"margin-left": "20px", "margin-top": "10px", "display": "none"})
    return styles

# Callback per gestire l'invio delle preferenze e salvare in CSV
@app.callback(
    Output('submit-button', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State(f"customization-checklist-{i}", 'value') for i in range(len(customization_options))] +
    [State(f"{customization_options[i]['value'].lower().replace(' ', '-')}-altro", 'value') for i in range(len(customization_options))]
)
def update_button_text(n_clicks, *selected_options):
    if n_clicks > 0:
        checklist_values = selected_options[:len(customization_options)]
        altro_values = selected_options[len(customization_options):]
        all_selected = [item for sublist in checklist_values for item in sublist]
        for i, value in enumerate(altro_values):
            if value:
                all_selected.append(f"Altro ({customization_options[i]['label']}): {value}")
        # Creazione del DataFrame per salvare le preferenze
        data = {
            'Cliente ID': [cliente_id],
            'Preferenze': [', '.join(all_selected)]
        }
        df = pd.DataFrame(data)
        # Percorso di salvataggio del file CSV basato sul codice identificativo cliente
        save_path = f'/Users/gp/Library/CloudStorage/OneDrive-Personale/Holibuy/Custom/Custom Clienti/{cliente_id}.csv'
        # Salva il file CSV
        df.to_csv(save_path, index=False)
        return f"Preferenze inviate: {', '.join(all_selected)}"
    return "Invia Preferenze"

# Esecuzione dell'app
if __name__ == "__main__":
    app.run_server(debug=True, host="127.0.0.1", port=8051)
