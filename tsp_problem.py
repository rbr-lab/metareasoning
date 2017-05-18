import random
import numpy as np
import tsp
import matplotlib.pyplot as plt
import randomized_tour_improver
import experiments


def pop(queue):
    minimum_value = float('inf')
    minimum_key = None

    for key in queue:
        if queue[key] < minimum_value:
            minimum_value = queue[key]
            minimum_key = key

    del queue[minimum_key]

    return minimum_key


def get_heuristic(current_node, start_city, cities):
    if is_goal(current_node.state, cities):
        return 0

    # TODO: Add the start city
    subset = cities - set(current_node.state)

    predecessors = {}
    key = {}
    queue = {}

    for state in subset:
        predecessors[state] = -1
        key[state] = float('inf')
        queue[state] = float('inf')

    current_city = current_node.state[-1]
    queue[current_city] = 0

    while queue:
        current_city = pop(queue)

        for successor in get_successors(current_node.state, subset):
            next_city = successor['state'][-1]

            # TODO: Fix this
            cost = np.linalg.norm(np.subtract(current_city, next_city))

            if next_city in queue and cost < key[next_city]:
                predecessors[next_city] = current_city
                key[next_city] = cost
                queue[next_city] = cost

    cost = 0
    for parent_city, child_city in predecessors.iteritems():
        if child_city != -1:
            # TODO: Fix this
            cost += np.linalg.norm(np.subtract(parent_city, child_city))

    return cost


def is_goal(state, cities):
    return len(cities) == len(state)


def get_successors(state, cities):
    return [{'action': city, 'state': list(state) + [city]} for city in cities - set(state)]


def get_cost(state, action, next_state):
    return np.linalg.norm(np.subtract(state[-1], next_state))


def get_tour_distance(start_city, actions):
    distance = get_cost(start_city, actions[0], actions[0])

    for i in range(len(actions)):
        if i + 1 == len(actions):
            break

        distance += get_cost(actions[i], actions[i + 1], actions[i + 1])

    return distance


def show_plot(filename, optimal_distance):
    print('Saving file:', filename)

    cities = tsp.load_instance(filename)
    start_city = list(cities)[0]

    statistics = {'time': [], 'distances': []}
    randomized_tour_improver.k_opt_solve(cities, start_city, statistics)

    solution_qualities = [1 - ((distance - optimal_distance) / optimal_distance) for distance in statistics['distances']]

    plt.title('Performance Profile')
    plt.xlabel('Time')
    plt.ylabel('Solution Quality')
    plt.scatter(statistics['time'], solution_qualities, color='r')
    plt.savefig('test.png')


def save_all_plots(filename, directory='plots'):
    with open(filename) as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            filename, optimal_distance = experiments.parse_line(line)

            print 'Saving file:', filename

            cities = tsp.load_instance(filename)
            start_city = list(cities)[0]

            statistics = {'time': [], 'distances': []}
            randomized_tour_improver.k_opt_solve(cities, start_city, statistics)

            # solution_qualities = [1 - ((distance - optimal_distance) / optimal_distance) for distance in statistics['distances']]
            solution_qualities = [optimal_distance / distance for distance in statistics['distances']]

            plt.figure()
            plt.title('Performance Profile')
            plt.xlabel('Time')
            plt.ylabel('Solution Quality')
            plt.scatter(statistics['time'], solution_qualities, color='r')
            plt.savefig(directory + '/plot-%i.png' % i)


def main():
    save_all_plots('instances/instances.csv')


if __name__ == '__main__':
    main()
