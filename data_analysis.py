import numpy as np
import pandas as pd
import plotly.graph_objects as go


def calc_winning_percentage(ser):
    return np.sum(ser) / ser.count()


def main():
    df = pd.read_csv(
        'game_data.csv',
        index_col='game_nums'
    )
    winning_percentage_by_threshold = df.groupby('human_stay_threshold').agg({
        'human_won': calc_winning_percentage
    }).rename(
        columns={'human_won': 'winning_percentage'}
    ).reset_index()

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=winning_percentage_by_threshold['human_stay_threshold'],
            y=winning_percentage_by_threshold['winning_percentage']
        )
    )

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    fig.update_layout(
        # title='human_hit_once=' + str(human_hit_once),
        xaxis_title='human_stay_threshold',
        yaxis_title='winning_percentage'
        # xaxis_type='category',
        # yaxis_type='category'
    )

    fig.show()

    stats = df.groupby(['human_stay_threshold', 'dealer_first_card_score']).agg({
        'human_won': calc_winning_percentage,
        'dealer_final_score': 'count'
    }).rename(columns={
        'human_won': 'winning_percentage',
        'dealer_final_score': 'num_games'
    }).reset_index()
    stats = stats.loc[stats['num_games'] >= 10]

    fig = go.Figure()
    fig.add_trace(
        go.Heatmap(
            z=stats['winning_percentage'],
            x=stats['human_stay_threshold'],
            y=stats['dealer_first_card_score'],
            # hovertext=hovertext,
            # hoverinfo='text',
            hoverongaps=False,
            colorscale='Reds'
        )
    )

    fig.update_xaxes(showgrid=True)
    fig.update_yaxes(showgrid=True)

    fig.update_layout(
        # title='human_hit_once=' + str(human_hit_once),
        xaxis_title='human_stay_threshold',
        yaxis_title='dealer_first_card_score'
        # xaxis_type='category',
        # yaxis_type='category'
    )

    fig.show()

main()
