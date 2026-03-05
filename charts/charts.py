import altair as alt
import pandas as pd
import numpy as np

alt.data_transformers.disable_max_rows()


# --------------------------------------------------
# Chart 1: League position bump chart
# --------------------------------------------------

def league_position_chart(df):

    df["HomeWin"] = (df["FTHG"] > df["FTAG"]).astype(int)
    df["AwayWin"] = (df["FTAG"] > df["FTHG"]).astype(int)

    home = df.groupby(["Season","HomeTeam"])["HomeWin"].sum().reset_index()
    home.columns = ["Season","Team","HomeWins"]

    away = df.groupby(["Season","AwayTeam"])["AwayWin"].sum().reset_index()
    away.columns = ["Season","Team","AwayWins"]

    team_summary = home.merge(away, on=["Season","Team"])

    team_summary["TotalWins"] = (
        team_summary["HomeWins"] + team_summary["AwayWins"]
    )

    team_summary["Position"] = (
        team_summary
        .groupby("Season")["TotalWins"]
        .rank(method="first", ascending=False)
    )

    rank_change = (
        team_summary
        .pivot(index="Team", columns="Season", values="Position")
        .reset_index()
    )

    rank_change["Change"] = (
        rank_change["2023-24"] - rank_change["2024-25"]
    )

    team_summary = team_summary.merge(
        rank_change[["Team","Change"]],
        on="Team"
    )

    base = alt.Chart(team_summary).mark_line(point=True).encode(
        x=alt.X("Season:N", sort=["2023-24","2024-25"]),
        y=alt.Y("Position:Q", scale=alt.Scale(reverse=True)),
        detail="Team:N",
        color="Team:N",
        tooltip=["Team","Season","TotalWins","Position","Change"]
    )

    return base.properties(
        width=650,
        height=600,
        title="League Position Movement Between Seasons"
    )


# --------------------------------------------------
# Chart 2: Attacking consistency
# --------------------------------------------------

def attacking_consistency_chart(df):

    home = df[[
        "Season","Date","HomeTeam","FTHG","HS","HST","HC"
    ]].copy()

    home.columns = [
        "Season","Date","Team","Goals","Shots","ShotsOnTarget","Corners"
    ]

    away = df[[
        "Season","Date","AwayTeam","FTAG","AS","AST","AC"
    ]].copy()

    away.columns = [
        "Season","Date","Team","Goals","Shots","ShotsOnTarget","Corners"
    ]

    long_df = pd.concat([home, away])

    long_df = long_df.sort_values(["Season","Team","Date"])

    long_df["Matchweek"] = (
        long_df.groupby(["Season","Team"]).cumcount() + 1
    )

    metric_df = long_df.melt(
        id_vars=["Season","Team","Date","Matchweek"],
        value_vars=["Goals","Shots","ShotsOnTarget","Corners"],
        var_name="Metric",
        value_name="Value"
    )

    metric_df["RollingValue"] = (
        metric_df
        .groupby(["Season","Team","Metric"])["Value"]
        .transform(lambda x: x.rolling(5, min_periods=1).mean())
    )

    team = alt.selection_point(
        fields=["Team"],
        bind=alt.binding_select(
            options=sorted(metric_df["Team"].unique())
        )
    )

    season = alt.selection_point(
        fields=["Season"],
        bind=alt.binding_radio(
            options=["2023-24","2024-25"]
        )
    )

    metric = alt.selection_point(
        fields=["Metric"],
        bind=alt.binding_radio(
            options=["Goals","Shots","ShotsOnTarget","Corners"]
        )
    )

    chart = (
        alt.Chart(metric_df)
        .mark_line(size=3)
        .encode(
            x="Matchweek:Q",
            y="RollingValue:Q",
            tooltip=["Team","Season","Matchweek","Metric","RollingValue"]
        )
        .transform_filter(team)
        .transform_filter(season)
        .transform_filter(metric)
        .add_params(team, season, metric)
    )

    return chart.properties(
        width=750,
        height=450,
        title="Attacking Consistency Across Matchweeks"
    )


# --------------------------------------------------
# Chart 3: Home advantage
# --------------------------------------------------

def home_advantage_chart(df):

    df["HomePoints"] = np.where(
        df["FTHG"] > df["FTAG"],3,
        np.where(df["FTHG"] == df["FTAG"],1,0)
    )

    df["AwayPoints"] = np.where(
        df["FTAG"] > df["FTHG"],3,
        np.where(df["FTAG"] == df["FTHG"],1,0)
    )

    home = df.groupby(["Season","HomeTeam"])["HomePoints"].sum().reset_index()
    home.columns = ["Season","Team","HomePoints"]

    away = df.groupby(["Season","AwayTeam"])["AwayPoints"].sum().reset_index()
    away.columns = ["Season","Team","AwayPoints"]

    team_perf = home.merge(away, on=["Season","Team"])

    team_perf["HomeAdvantage"] = (
        team_perf["HomePoints"] - team_perf["AwayPoints"]
    )

    season = alt.selection_point(
        fields=["Season"],
        bind=alt.binding_radio(
            options=["2023-24","2024-25"]
        )
    )

    chart = (
        alt.Chart(team_perf)
        .mark_bar()
        .encode(
            y=alt.Y("Team:N", sort="-x"),
            x="HomeAdvantage:Q",
            color=alt.condition(
                alt.datum.HomeAdvantage > 0,
                alt.value("steelblue"),
                alt.value("orange")
            ),
            tooltip=["Team","HomePoints","AwayPoints","HomeAdvantage"]
        )
        .transform_filter(season)
        .add_params(season)
    )

    return chart.properties(
        width=650,
        height=400,
        title="Home Advantage by Team"
    )