def calculate_elo_rating(rating_a, rating_b):
    k_factor = 32
    expected_score_a = 1 / (1 + 10 ** ((rating_b - rating_a) / 400))
    new_rating_a = rating_a + k_factor * (1 - expected_score_a)
    return int(new_rating_a)


def update_teams_points(winner, loser):
    won_points = calculate_elo_rating(winner.points, loser.points)
    lose_points = loser.points - (won_points - winner.points)
    winner.points = won_points
    loser.points = lose_points
    winner.save()
    loser.save()

# def multiply(): multiply_numbers = [i for i in range(1, 11)] for i in range(1, len(multiply_numbers) + 1): print(
# "|" + '-' * 39 + "|") print('|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|{:^3}|'.format((i * 1),
# (i * 2), (i * 3), (i * 4), (i * 5), (i * 6), (i * 7), (i * 8), (i * 9), (i * 10))) print("|" + '-' * 39 + "|")
