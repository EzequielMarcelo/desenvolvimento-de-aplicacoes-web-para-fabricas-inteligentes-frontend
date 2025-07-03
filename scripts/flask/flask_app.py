from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
import os

app = Flask(__name__)

# --- Dados de Exemplo ---
dados_temp = {
    'Mês': ['8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19'],
    'Valor': [25, 30, 32, 36, 40, 46, 47, 50, 49, 51, 55, 60]
}
df_temp = pd.DataFrame(dados_temp)

progresso_total = {'Temp': 70, 'Faltante': 30}
porcentagem_concluida = progresso_total['Faltante']

# --- Rota principal ---
@app.route('/')
def dashboard():
    # Métricas
    temp_min = df_temp['Valor'].min()
    temp_max = df_temp['Valor'].max()
    temp_media = df_temp['Valor'].mean()

    # Gráfico de Linha
    fig_linha = go.Figure(data=go.Scatter(
        x=df_temp['Mês'], y=df_temp['Valor'], mode='lines+markers',
        line=dict(color='#6a1b9a', width=3),
        marker=dict(size=8, color='#c85dd1')
    ))
    fig_linha.update_layout(
        xaxis_title="Hora",
        yaxis_title="Temperatura",
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0')
    )
    graph_linha_html = pio.to_html(fig_linha, full_html=False)

    # Gráfico Circular
    fig_circular = go.Figure(data=[go.Pie(
        labels=list(progresso_total.keys()),
        values=list(progresso_total.values()),
        hole=.7,
        marker_colors=['#6a1b9a', '#4a4a8a'],
        textinfo='none'
    )])
    fig_circular.update_layout(
        height=300,
        paper_bgcolor='rgba(0,0,0,0)',
        annotations=[dict(text=f'{porcentagem_concluida} ºC', x=0.5, y=0.5, font_size=30, showarrow=False, font_color="#e0e0e0")]
    )
    graph_circular_html = pio.to_html(fig_circular, full_html=False)

    return render_template("dashboard.html",
        temp_min=temp_min,
        temp_max=temp_max,
        temp_media=temp_media,
        tempo_operacao="8.5",
        graph_linha=graph_linha_html,
        graph_circular=graph_circular_html
    )

@app.route('/settings', methods=['GET', 'POST'])
def configuracoes():
    if request.method == 'POST':
        nome_usuario = request.form.get('nome_usuario', 'Usuário Padrão')
        tema = request.form.get('tema', 'Escuro')
        notificacoes = request.form.get('notificacoes') == 'on'
        return redirect(url_for('dashboard'))

    return render_template("settings.html")

if __name__ == '__main__':
    app.run(debug=True)
