import altair as alt
import pandas as pd
import numpy as np

alt.data_transformers.disable_max_rows()


# --------------------------------------------------
# Chart 1: League position bump chart
# --------------------------------------------------

def attacking_consistency_chart(df):

    import pandas as pd
    import altair as alt

    # -----------------------
    # Build long match-level dataset
    # -----------------------

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

    # -----------------------
    # IMPORTANT: sort properly
    # -----------------------

    long_df = long_df.sort_values(["Season","Team","Date"])

    long_df["Matchweek"] = (
        long_df.groupby(["Season","Team"]).cumcount() + 1
    )

    # -----------------------
    # Reshape for metric toggle
    # -----------------------

    metric_df = long_df.melt(
        id_vars=["Season","Team","Date","Matchweek"],
        value_vars=["Goals","Shots","ShotsOnTarget","Corners"],
        var_name="Metric",
        value_name="Value"
    )

    # -----------------------
    # Rolling average
    # -----------------------

    metric_df["RollingValue"] = (
        metric_df
        .groupby(["Season","Team","Metric"])["Value"]
        .transform(lambda x: x.rolling(5, min_periods=1).mean())
    )

    # -----------------------
    # Selections
    # -----------------------

    team_select = alt.selection_point(
        fields=["Team"],
        bind=alt.binding_select(options=sorted(metric_df["Team"].unique()))
    )

    season_select = alt.selection_point(
        fields=["Season"],
        bind=alt.binding_radio(options=["2023-24","2024-25"])
    )

    metric_select = alt.selection_point(
        fields=["Metric"],
        bind=alt.binding_radio(
            options=["Goals","Shots","ShotsOnTarget","Corners"]
        )
    )

    # -----------------------
    # Chart
    # -----------------------

    chart = (
        alt.Chart(metric_df)
        .mark_line(size=3)
        .encode(
            x=alt.X("Matchweek:Q", title="Matchweek"),
            y=alt.Y("RollingValue:Q", title="5-Match Rolling Average"),
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
def home_advantage_dashboard(df, season):

    import altair as alt
    import numpy as np

    alt.data_transformers.disable_max_rows()

    # -----------------------
    # Compute points
    # -----------------------

    df["HomePoints"] = np.where(
        df["FTHG"] > df["FTAG"], 3,
        np.where(df["FTHG"] == df["FTAG"], 1, 0)
    )

    df["AwayPoints"] = np.where(
        df["FTAG"] > df["FTHG"], 3,
        np.where(df["FTAG"] == df["FTHG"], 1, 0)
    )

    # -----------------------
    # Team aggregation
    # -----------------------

    home = df.groupby(["Season","HomeTeam"])["HomePoints"].sum().reset_index()
    home.columns = ["Season","Team","HomePoints"]

    away = df.groupby(["Season","AwayTeam"])["AwayPoints"].sum().reset_index()
    away.columns = ["Season","Team","AwayPoints"]

    team_perf = home.merge(away, on=["Season","Team"])

    team_perf["HomeAdvantage"] = (
        team_perf["HomePoints"] - team_perf["AwayPoints"]
    )

    team_perf = team_perf[team_perf["Season"] == season]

    # -----------------------
    # Brush interaction
    # -----------------------

    brush = alt.selection_interval(encodings=["y"])

    # -----------------------
    # Top chart
    # -----------------------

    top_chart = (
        alt.Chart(team_perf)
        .mark_bar()
        .encode(
            y=alt.Y("Team:N", sort="-x", title="Team"),
            x=alt.X(
                "HomeAdvantage:Q",
                title="Home Advantage (Home Points − Away Points)"
            ),
            color=alt.condition(
                alt.datum.HomeAdvantage > 0,
                alt.value("steelblue"),
                alt.value("orange")
            ),
            opacity=alt.condition(brush, alt.value(1), alt.value(0.3)),
            tooltip=["Team","HomePoints","AwayPoints","HomeAdvantage"]
        )
        .add_params(brush)
        .properties(width=650, height=350)
    )

    # -----------------------
    # Bottom chart
    # -----------------------

    melted = team_perf.melt(
        id_vars=["Team"],
        value_vars=["HomePoints","AwayPoints"],
        var_name="Venue",
        value_name="Points"
    )

    bottom_chart = (
        alt.Chart(melted)
        .mark_bar()
        .encode(
            x=alt.X("Venue:N", title="Venue"),
            y=alt.Y("Points:Q", title="Total Points"),
            column=alt.Column("Team:N", title="Team"),
            color=alt.Color("Venue:N", legend=None),
            tooltip=["Team","Venue","Points"]
        )
        .transform_filter(brush)
        .properties(width=120, height=250)
    )

    # -----------------------
    # Combine charts
    # -----------------------

    dashboard = top_chart

    return dashboard