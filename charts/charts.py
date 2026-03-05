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