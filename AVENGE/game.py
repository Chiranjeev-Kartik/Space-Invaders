"""
Author: Kartikay Chiranjeev Gupta
Last Modified: 8/16/2021
"""
from main import *


# Miscellaneous function................................................................................................
def generate_levels(n):
    """
    Generates n number of random levels ( with no boss ).
    :param n: Number of levels to be generated.
    :return: None
    """
    level = 1
    while level <= n:
        stage = [[random.choice([1, 0]) for _ in range(11)], [random.choice([1, 0]) for _ in range(11)],
                 [random.choice([1, 0]) for _ in range(11)]]
        no_villain = []
        no_moves = cycle([0])
        if level_maker(stage, no_villain, [0], SHOOT_OFFSET, no_moves, VILLAIN1_SHOOT_SOUND, 1, 'Level.mp3') \
                is None:
            print(f'LEVEL {level} COMPLETED.')
        level += 1
        player.health += HEALTH_REWARD  # Winning Reward.
    return None


# LEVELS CONSTRUCTION...................................................................................................


def level_10():
    stage1 = [[1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    villain_1 = [Villain(440, -240, VILLAIN_HEALTH, VILLAIN_1, LASER_VILLAIN, VILLAIN_DAMAGE)]
    villain_moves = cycle([440, 440, 440])
    if level_maker(stage1, villain_1, [0], 3 * SHOOT_OFFSET, villain_moves, VILLAIN1_SHOOT_SOUND, 1, 'Traversing.mp3') \
            is None:
        print('LEVEL 10 COMPLETED.')
    player.health += HEALTH_REWARD
    return None


def level_20():

    stage2 = [[1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1], [1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1]]
    villain_2 = [Villain(440, -140, VILLAIN_HEALTH * 2, VILLAIN_2, LASER_VILLAIN, VILLAIN_DAMAGE)]
    villain_moves = cycle([440, 440, 440])
    if level_maker(stage2, villain_2, [-100, 0, 100], 3 * SHOOT_OFFSET, villain_moves, VILLAIN2_SHOOT_SOUND, 1,
                   'Ten Inch Spikes.mp3') is None:
        print('LEVEL 20 COMPLETED.')
    player.health += HEALTH_REWARD
    return None


def level_30():
    stage3 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
    villain_3 = [Villain(440, -100, VILLAIN_HEALTH * 3, VILLAIN_3, LASER_VILLAIN, VILLAIN_DAMAGE)]
    villain_moves = cycle(generate_move(50, WIDTH - 350, 500, 20))
    if level_maker(stage3, villain_3, [0], 3 * SHOOT_OFFSET, villain_moves, VILLAIN2_SHOOT_SOUND, 3,
                   'Emergency On Level 3.mp3') is None:
        print('LEVEL 30 COMPLETED.')
    return None


# ......................................................................................................................

generate_levels(9)  # 9 randomly generated levels.
level_10()  # Boss level.
generate_levels(9)  # 9 randomly generated levels.
level_20()  # Boss level.
generate_levels(9)  # 9 randomly generated levels.
level_30()  # Boss level.
the_end()  # The End.
