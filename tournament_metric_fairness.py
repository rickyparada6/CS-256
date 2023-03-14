import numpy as np

GROUP_SIZE = 4
NUM_GROUPS = 8
NUM_TRIALS = 100000


# first metric
def count_envious_teams(groups):
    total = 0
    intra_group_ranks = np.array([np.array(groups[i]).argsort().argsort()+1 for i in range(NUM_GROUPS)])
    for i in range(NUM_GROUPS):
        for j in range(GROUP_SIZE):
            for k in range(NUM_GROUPS):
                for m in range(GROUP_SIZE):
                    if groups[i][j] < groups[k][m] and intra_group_ranks[i][j] > intra_group_ranks[k][m]:
                        total += 1
    return total


# second metric
def intra_group_distance(group):
    dist = 0
    for i in range(GROUP_SIZE-1):
        for j in range(i+1, GROUP_SIZE):
            dist += np.abs(group[i] - group[j])
    return dist


def simulate_draw(pots):
    groups = np.zeros((NUM_GROUPS, GROUP_SIZE))
    for i in range(GROUP_SIZE):
        pot = pots[i]
        if i == 0:
            groups[i][0] = pot[0]  # host country gets group A
            pot = np.delete(pot, 0)
            for j in range(NUM_GROUPS - 1):
                ind = np.random.randint(0, np.size(pot))
                groups[j+1][i] = pot[ind]
                pot = np.delete(pot, ind)
        else:
            for j in range(NUM_GROUPS):
                ind = np.random.randint(0, np.size(pot))
                groups[j][i] = pot[ind]
                pot = np.delete(pot, ind)
    return groups


def main():
    pots = np.array([[51,  1,  2,  3,  4,  5,  7,  8],
                     [9,  10, 11, 12, 13, 14, 15, 16],
                     [20, 21, 23, 24, 25, 26, 29, 35],
                     [37, 38, 46, 49, 60, 18, 31, 42]])
    sorted_pots = np.sort(pots)

    groups = np.array([[51, 46, 20, 10],
                       [5,  21, 15, 18],
                       [4,  49,  9, 26],
                       [3,  42, 11, 35],
                       [7,  31, 12, 23],
                       [2,  38, 24, 16],
                       [1,  25, 14, 37],
                       [8,  60, 13, 29]])
    sorted_groups = np.array([sorted_pots[:, i] for i in range(NUM_GROUPS)])

    group_letters = "ABCDEFGH"
    group_distances = np.zeros(NUM_GROUPS)
    sorted_group_distances = np.zeros(NUM_GROUPS)

    print("Actual envious teams count: " + str(count_envious_teams(groups)))
    print("Sorted envious teams count: " + str(count_envious_teams(sorted_groups)))
    for i, j in enumerate(group_letters):
        group_distances[i] = intra_group_distance(groups[i])
        sorted_group_distances[i] = intra_group_distance(sorted_groups[i])
        print("Actual group " + j + " distance: " + str(intra_group_distance(groups[i])))
        print("Sorted group " + j + " distance: " + str(intra_group_distance(sorted_groups[i])))
    print("Actual average group distance: " + str(np.sum(group_distances)/NUM_GROUPS))
    print("Sorted average group distance: " + str(np.sum(sorted_group_distances)/NUM_GROUPS))

    envious_counts = np.zeros(NUM_TRIALS)
    average_distances = np.zeros(NUM_TRIALS)
    random_group_distances = np.zeros(NUM_GROUPS)
    for k in range(1, NUM_TRIALS+1):
        random_groups = simulate_draw(pots)
        envious_counts[k - 1] = count_envious_teams(random_groups)
        for i, j in enumerate(group_letters):
            random_group_distances[i] = intra_group_distance(random_groups[i])
        average_distances[k-1] = sum(random_group_distances) / NUM_GROUPS
    print("Min envious team count was " + str(np.min(envious_counts)) + " from trial " + str(np.argmin(envious_counts)
                                                                                             + 1))
    print("Max envious team count was " + str(np.max(envious_counts)) + " from trial " + str(np.argmax(envious_counts)
                                                                                             + 1))
    print("Average envious team count was " + str(np.sum(envious_counts) / NUM_TRIALS))
    print("Min group distance was " + str(np.min(average_distances)) + " from trial " + str(np.argmin(average_distances)
                                                                                            + 1))
    print("Max group distance was " + str(np.max(average_distances)) + " from trial " + str(np.argmax(average_distances)
                                                                                            + 1))
    print("Average group distance was " + str(np.sum(average_distances)/NUM_TRIALS))


if __name__ == '__main__':
    main()