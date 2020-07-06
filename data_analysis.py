import numpy as np
import pandas as pd
import plotly.graph_objects as go


def calc_winning_percentage(ser):
    return np.sum(ser) / ser.count()


def is_hit_once_better(row):
    if (
            row['num_games_hitonce'] >= 10
        and row['num_games_nohit'] >= 10
        and row['winning_percentage_hitonce'] >= row['winning_percentage_nohit']
    ):
        return 1
    elif (
            row['num_games_hitonce'] >= 10
        and row['num_games_nohit'] >= 10
        and row['winning_percentage_hitonce'] < row['winning_percentage_nohit']
    ):
        return -1
    else:
        return 0


def main():
    df = pd.read_csv(
        'game_data.csv',
        index_col='game_nums'
    )
    stats = df.groupby(['human_starting_score', 'human_hit_once', 'dealer_first_card_score']).agg({
        'human_won': calc_winning_percentage,
        'human_hit_once': 'count'
    }).rename(columns={
        'human_won': 'winning_percentage',
        'human_hit_once': 'num_games'
    }).reset_index()

    for human_hit_once in [False, True]:
        tempdf = stats.loc[stats['human_hit_once'] == human_hit_once]
        fig = go.Figure()
        fig.add_trace(
            go.Heatmap(
                z=tempdf['winning_percentage'],
                x=tempdf['human_starting_score'],
                y=tempdf['dealer_first_card_score'],
                # hovertext=hovertext,
                # hoverinfo='text',
                hoverongaps=False,
                colorscale='Reds'
            )
        )

        fig.update_xaxes(showgrid=True)
        fig.update_yaxes(showgrid=True)

        fig.update_layout(
            title='human_hit_once=' + str(human_hit_once),
            xaxis_title='human_starting_score',
            yaxis_title='dealer_first_card_score'
            # xaxis_type='category',
            # yaxis_type='category'
        )

        fig.show()

    hit_once = stats.loc[stats['human_hit_once'] == True]
    no_hit = stats.loc[stats['human_hit_once'] == False]
    joined = hit_once.merge(
        right=no_hit,
        on=['human_starting_score', 'dealer_first_card_score'],
        suffixes=['_hitonce', '_nohit']
    )
    joined['is_hit_once_better'] = joined.apply(
        is_hit_once_better,
        axis=1
    )

    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            z=joined['is_hit_once_better'],
            x=joined['human_starting_score'],
            y=joined['dealer_first_card_score'],
            # hovertext=hovertext,
            # hoverinfo='text',
            hoverongaps=False,
            colorscale='Reds'
        )
    )

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    fig.update_layout(
        title='Is Hit Once Better?',
        xaxis_title='human_starting_score',
        yaxis_title='dealer_first_card_score'
        # xaxis_type='category',
        # yaxis_type='category'
    )

    fig.show()


main()
