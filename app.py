import streamlit as st
import plotly.graph_objects as go
from data import fetch_data, calc_performance, TICKERS

st.set_page_config(page_title="Ações 2025", layout="wide")
st.title("📈 Cotações 2025 — Santander · Itaú · Vale")

COLORS = {
    "Santander": "#EC0000",
    "Itaú":      "#003087",
    "Vale":      "#009B77",
}


@st.cache_data(ttl=3600)
def load_data():
    return fetch_data()


frames = load_data()
perf = calc_performance(frames)

# ── Métricas resumo ───────────────────────────────────────────────────────────
st.subheader("Resumo")
cols = st.columns(len(TICKERS))
for col, (name, df) in zip(cols, frames.items()):
    close = df["Close"].dropna()
    if len(close) < 2:
        col.metric(name, "N/D")
        continue
    preco_atual = float(close.iloc[-1])
    preco_ontem = float(close.iloc[-2])
    preco_inicial = float(close.iloc[0])
    retorno_acum = (preco_atual / preco_inicial - 1) * 100
    variacao_dia = (preco_atual / preco_ontem - 1) * 100
    col.metric(
        label=f"{name} ({list(TICKERS.values())[list(TICKERS.keys()).index(name)]})",
        value=f"R$ {preco_atual:.2f}",
        delta=f"{variacao_dia:+.2f}% hoje  |  {retorno_acum:+.2f}% em 2025",
    )

st.divider()

# ── Gráfico 1: Preço de Fechamento ───────────────────────────────────────────
st.subheader("Preço de Fechamento (BRL)")
fig1 = go.Figure()
for name, df in frames.items():
    close = df["Close"].dropna()
    fig1.add_trace(go.Scatter(
        x=close.index,
        y=close.values,
        name=name,
        line=dict(color=COLORS[name], width=2),
        hovertemplate="%{x|%d/%m/%Y}<br>R$ %{y:.2f}<extra>" + name + "</extra>",
    ))
fig1.update_layout(
    xaxis_title="Data",
    yaxis_title="Preço (R$)",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=420,
)
st.plotly_chart(fig1, use_container_width=True)

# ── Gráfico 2: Performance Acumulada ─────────────────────────────────────────
st.subheader("Performance Acumulada em 2025 (%)")
fig2 = go.Figure()
for name, series in perf.items():
    fig2.add_trace(go.Scatter(
        x=series.index,
        y=series.values,
        name=name,
        line=dict(color=COLORS[name], width=2),
        hovertemplate="%{x|%d/%m/%Y}<br>%{y:+.2f}%<extra>" + name + "</extra>",
    ))
fig2.add_hline(y=0, line_dash="dot", line_color="gray", line_width=1)
fig2.update_layout(
    xaxis_title="Data",
    yaxis_title="Retorno acumulado (%)",
    hovermode="x unified",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=420,
)
st.plotly_chart(fig2, use_container_width=True)

# ── Gráfico 3: Volume Negociado (média semanal) ───────────────────────────────
st.subheader("Volume Negociado — Média Semanal")
fig3 = go.Figure()
for name, df in frames.items():
    vol = df["Volume"].dropna()
    vol_weekly = vol.resample("W").mean()
    fig3.add_trace(go.Bar(
        x=vol_weekly.index,
        y=vol_weekly.values,
        name=name,
        marker_color=COLORS[name],
        opacity=0.8,
        hovertemplate="%{x|%d/%m/%Y}<br>%{y:,.0f}<extra>" + name + "</extra>",
    ))
fig3.update_layout(
    barmode="group",
    xaxis_title="Semana",
    yaxis_title="Volume médio",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    height=420,
)
st.plotly_chart(fig3, use_container_width=True)

st.caption("Dados: Yahoo Finance via yfinance · Atualização a cada hora")
