import altair as alt
import pandas as pd
import numpy as np

alt.data_transformers.disable_max_rows()


def league_position_chart(df):

    # -----------------------
    # Compute wins
    # -----------------------

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

    # -----------------------
    # Compute ranking
    # -----------------------

    team_summary["Position"] = (
        team_summary
        .groupby("Season")["TotalWins"]
        .rank(method="first", ascending=False)
    )

    # -----------------------
    # Compute rank change
    # -----------------------

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

    # -----------------------
    # Hover highlight
    # -----------------------

    team_select = alt.selection_point(
        fields=["Team"],
        on="mouseover",
        clear="mouseout"
    )

    # -----------------------
    # Base bump chart
    # -----------------------

    base = (
        alt.Chart(team_summary)
        .mark_line(point=True)
        .encode(
            x=alt.X(
                "Season:N",
                sort=["2023-24","2024-25"],
                axis=alt.Axis(title="Season")
            ),
            y=alt.Y(
                "Position:Q",
                scale=alt.Scale(reverse=True),
                axis=alt.Axis(title="League Position (Based on Wins)")
            ),
            detail="Team:N",
            color=alt.Color("Team:N", legend=None),
            strokeWidth=alt.condition(team_select, alt.value(4), alt.value(1)),
            opacity=alt.condition(team_select, alt.value(1), alt.value(0.25)),
            tooltip=["Team","Season","TotalWins","Position","Change"]
        )
        .add_params(team_select)
    )

    # -----------------------
    # Labels for final season
    # -----------------------

    endpoints = team_summary[team_summary["Season"] == "2024-25"]

    labels = (
        alt.Chart(endpoints)
        .mark_text(align="left", dx=8)
        .encode(
            x="Season:N",
            y=alt.Y("Position:Q", scale=alt.Scale(reverse=True)),
            text="Team:N",
            color=alt.Color("Team:N", legend=None)
        )
    )

    bump_chart = (
        base + labels
    ).properties(
        width=650,
        height=650,
        title="League Position Movement Between Seasons (Based on Total Wins)"
    )

    return bump_chart
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


##chart 3

def foul_distribution_dashboard(df):

    import altair as alt
    import pandas as pd

    alt.data_transformers.disable_max_rows()

    # -----------------------
    # Disciplinary metrics
    # -----------------------

    df = df.copy()

    df["Yellows"] = df["HY"] + df["AY"]
    df["Reds"] = df["HR"] + df["AR"]
    df["Fouls"] = df["HF"] + df["AF"]

    # -----------------------
    # Referee summary
    # -----------------------

    ref_summary = (
        df.groupby(["Season", "Referee"])
        .agg(
            Yellows=("Yellows", "mean"),
            Reds=("Reds", "mean"),
            Fouls=("Fouls", "mean")
        )
        .reset_index()
    )

    ref_long = ref_summary.melt(
        id_vars=["Season", "Referee"],
        value_vars=["Yellows", "Reds", "Fouls"],
        var_name="Metric",
        value_name="AveragePerMatch"
    )

    counts = ref_long.groupby(["Referee", "Metric"])["Season"].nunique().reset_index()
    valid_refs = counts[counts["Season"] == 2][["Referee", "Metric"]]
    ref_long = ref_long.merge(valid_refs, on=["Referee", "Metric"])

    # -----------------------
    # Team-level summary
    # -----------------------

    team_ref = df.melt(
        id_vars=["Season", "Referee", "HomeTeam"],
        value_vars=["Yellows", "Reds", "Fouls"],
        var_name="Metric",
        value_name="Value"
    )

    team_summary = (
        team_ref.groupby(["Season", "Referee", "HomeTeam", "Metric"])
        .agg(AvgPerMatch=("Value", "mean"))
        .reset_index()
    )

    team_summary.rename(columns={"HomeTeam": "Team"}, inplace=True)

    # -----------------------
    # Interactions
    # -----------------------

    metric_select = alt.selection_point(
        fields=["Metric"],
        bind=alt.binding_radio(
            options=["Yellows", "Reds", "Fouls"],
            name="Metric"
        ),
        value="Yellows"
    )

    ref_select = alt.selection_point(fields=["Referee"])

    # -----------------------
    # Sorting referees
    # -----------------------

    sort_df = (
        ref_long[
            (ref_long["Season"] == "2024-25") &
            (ref_long["Metric"] == "Yellows")
        ]
        .sort_values("AveragePerMatch", ascending=False)
    )

    sort_order = sort_df["Referee"].tolist()

    # -----------------------
    # Top chart
    # -----------------------

    lines = (
        alt.Chart(ref_long)
        .mark_line(color="lightgray")
        .encode(
            y=alt.Y("Referee:N", sort=sort_order, title="Referee"),
            x="AveragePerMatch:Q",
            detail="Referee:N"
        )
        .transform_filter(metric_select)
    )

    points = (
        alt.Chart(ref_long)
        .mark_circle(size=90)
        .encode(
            y=alt.Y("Referee:N", sort=sort_order),
            x=alt.X("AveragePerMatch:Q",
                    title="Average Cards/Fouls per Match"),
            color=alt.Color("Season:N"),
            opacity=alt.condition(ref_select, alt.value(1), alt.value(0.3)),
            tooltip=["Referee", "Season", "AveragePerMatch"]
        )
        .transform_filter(metric_select)
        .add_params(metric_select, ref_select)
        .properties(
            width=650,
            height=700,
            title="Referee Disciplinary Intensity Across Seasons"
        )
    )

    ranking_chart = lines + points

    # -----------------------
    # Bottom chart
    # -----------------------

    team_chart = (
        alt.Chart(team_summary)
        .mark_bar()
        .encode(
            y=alt.Y("Team:N", sort="-x", title="Team"),
            x=alt.X(
                "AvgPerMatch:Q",
                title="Average Cards/Fouls per Match",
                stack=None
            ),
            color=alt.Color("Season:N"),
            tooltip=["Team", "Season", "AvgPerMatch"]
        )
        .transform_filter(metric_select)
        .transform_filter(ref_select)
        .properties(
            width=650,
            height=350,
            title="Team-Level Disciplinary Intensity Under Selected Referee"
        )
    )

    dashboard = (ranking_chart & team_chart).resolve_scale(
        x="independent"
    )

    return dashboard