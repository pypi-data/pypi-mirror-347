import marimo

__generated_with = "0.13.8"
app = marimo.App(width="full")


@app.cell
def _():
    import multi_mst
    import pandas as pd
    return multi_mst, pd


@app.cell
def _(pd):
    df = pd.read_csv("http://aida-lab.be/assets/horse.csv").sample(n=200, random_state=42)
    return (df,)


@app.cell
def _(df, multi_mst):
    m_mst = multi_mst.MultiMST(df, metric="euclidean", iterations=100)
    return (m_mst,)


@app.cell
def _(m_mst):
    graph = m_mst.run()
    return


@app.cell
def _(m_mst):
    m_mst.export()
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
