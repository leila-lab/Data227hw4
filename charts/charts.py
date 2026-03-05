import altair as alt
import pandas as pd

alt.data_transformers.disable_max_rows()

def league_position_bump_chart(df):

    df["HomeWin"] = (df["FTHG"] > df["FTAG"]).astype(int)
    df["AwayWin"] = (df["FTAG"] > df["FTHG"]).astype(int)

    home_wins = df.groupby(["Season", "HomeTeam"])["HomeWin"].sum().reset_index()
    home_wins.columns = ["Season", "Team", "HomeWins"]

    away_wins = df.groupby(["Season", "AwayTeam"])["AwayWin"].sum().reset_index()
    away_wins.columns = ["Season", "Team", "AwayWins"]

    team_summary = home_wins.merge(away_wins, on=["Season", "Team"])
    team_summary["TotalWins"] = team_summary["HomeWins"] + team_summary["AwayWins"]

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
        rank_change[["Team", "Change"]],
        on="Team"
    )

    team_summary["ChangeLabel"] = team_summary["Change"].apply(
        lambda x: f"+{int(x)}" if x > 0 else
                  f"{int(x)}" if x < 0 else "0"
    )

    team_select = alt.selection_point(
        fields=["Team"],
        on="mouseover",
        clear="mouseout"
    )

    base = (
        alt.Chart(team_summary)
        .mark_line(point=True)
        .encode(
            x=alt.X("Season:N", sort=["2023-24","2024-25"]),
            y=alt.Y("Position:Q", scale=alt.Scale(reverse=True)),
            detail="Team:N",
            color=alt.Color("Team:N", legend=None),
            strokeWidth=alt.condition(team_select, alt.value(4), alt.value(1)),
            opacity=alt.condition(team_select, alt.value(1), alt.value(0.25)),
            tooltip=["Team","Season","TotalWins","Position","Change"]
        )
        .add_params(team_select)
    )

    endpoints = team_summary[team_summary["Season"] == "2024-25"]

    team_labels = (
        alt.Chart(endpoints)
        .mark_text(align="left", dx=10)
        .encode(
            x="Season:N",
            y=alt.Y("Position:Q", scale=alt.Scale(reverse=True)),
            text="Team:N",
            color=alt.Color("Team:N", legend=None)
        )
    )

    change_labels = (
        alt.Chart(endpoints)
        .mark_text(align="left", dx=65)
        .encode(
            x="Season:N",
            y=alt.Y("Position:Q", scale=alt.Scale(reverse=True)),
            text="ChangeLabel:N",
            color=alt.Color("Team:N", legend=None)
        )
    )

    bump_chart = (
        (base + team_labels + change_labels)
        .properties(
            width=650,
            height=650,
            title="League Position Movement Between Seasons"
        )
    )

    return bump_chart

import altair as alt
import pandas as pd
import numpy as np

alt.data_transformers.disable_max_rows()

def team_consistency_chart(df):

    home_long = df[[
        "Season","Date","HomeTeam",
        "FTHG","HS","HST","HC"
    ]].copy()

    home_long.columns = [
        "Season","Date","Team",
        "Goals","Shots","ShotsOnTarget","Corners"
    ]

    away_long = df[[
        "Season","Date","AwayTeam",
        "FTAG","AS","AST","AC"
    ]].copy()

    away_long.columns = [
        "Season","Date","Team",
        "Goals","Shots","ShotsOnTarget","Corners"
    ]

    long_df = pd.concat([home_long, away_long])

    long_df = long_df.sort_values(["Season","Team","Date"])

    long_df["Matchweek"] = (
        long_df
        .groupby(["Season","Team"])
        .cumcount() + 1
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

    team_select = alt.selection_point(
        fields=["Team"],
        bind=alt.binding_select(options=sorted(metric_df["Team"].unique())),
        name="Team"
    )

    season_select = alt.selection_point(
        fields=["Season"],
        bind=alt.binding_radio(options=["2023-24","2024-25"]),
        name="Season"
    )

    metric_select = alt.selection_point(
        fields=["Metric"],
        bind=alt.binding_radio(
            options=["Goals","Shots","ShotsOnTarget","Corners"]
        ),
        name="Metric"
    )

    chart = (
        alt.Chart(metric_df)
        .mark_line(size=3)
        .encode(
            x="Matchweek:Q",
            y="RollingValue:Q",
            tooltip=["Team","Season","Matchweek","Metric","RollingValue"]
        )
        .transform_filter(team_select)
        .transform_filter(season_select)
        .transform_filter(metric_select)
        .add_params(team_select, season_select, metric_select)
        .properties(
            width=750,
            height=450,
            title="Attacking Consistency Across Matchweeks"
        )
    )

    return chart

def home_advantage_dashboard(df):

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

    season_select = alt.selection_point(
        fields=["Season"],
        bind=alt.binding_radio(options=["2023-24","2024-25"]),
        name="Season"
    )

    brush = alt.selection_interval(encodings=["y"])

    top_chart = (
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
            opacity=alt.condition(brush, alt.value(1), alt.value(0.3)),
            tooltip=["Team","HomePoints","AwayPoints","HomeAdvantage"]
        )
        .transform_filter(season_select)
        .add_params(season_select, brush)
    )

    melted = team_perf.melt(
        id_vars=["Season","Team"],
        value_vars=["HomePoints","AwayPoints"],
        var_name="Venue",
        value_name="Points"
    )

    bottom_chart = (
        alt.Chart(melted)
        .mark_bar()
        .encode(
            x="Venue:N",
            y="Points:Q",
            column="Team:N",
            color="Venue:N"
        )
        .transform_filter(season_select)
        .transform_filter(brush)
    )

    return top_chart & bottom_chart