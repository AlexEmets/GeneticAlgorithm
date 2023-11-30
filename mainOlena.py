import random

def evaluate_schedule_conflicts(schedule):
    conflicts_count = sum(
        schedule[i]['time'] == schedule[j]['time'] or
        schedule[i]['teacher'] == schedule[j]['teacher'] or
        schedule[i]['group'] == schedule[j]['group'] 
        for i in range(len(schedule)) for j in range(i + 1, len(schedule))
    )
    return 1.0 / (1.0 + conflicts_count)

def mutate_schedule(schedule, rate_of_mutation, available_teachers, group_list, num_classes_per_day):
    return [
        {
            "subject": lesson["subject"],
            "teacher": random.choice(available_teachers) if random.random() < rate_of_mutation else lesson["teacher"],
            "group": random.choice(group_list) if random.random() < rate_of_mutation else lesson["group"],
            "time": random.randint(1, num_classes_per_day) if random.random() < rate_of_mutation else lesson["time"]
        }
        for lesson in schedule
    ]

def combine_schedules(schedule_a, schedule_b):
    point_of_crossover = random.randint(1, len(schedule_a) - 1)
    return schedule_a[:point_of_crossover] + schedule_b[point_of_crossover:], \
           schedule_b[:point_of_crossover] + schedule_a[point_of_crossover:]

def extract_optimal_schedule_from_population(current_population, fitness_values):
    return max(zip(current_population, fitness_values), key=lambda item: item[1])[0]

def generate_schedule_population(size, subjects_list, teachers_list, groups_list, classes_daily):
    return [
        [
            {
                "subject": subj,
                "teacher": random.choice(teachers_list),
                "group": random.choice(groups_list),
                "time": random.randint(1, classes_daily)
            }
            for subj in subjects_list
        ] for _ in range(size)
    ]

def optimize_schedule(population_size, mutation_rate, num_generations, subjects, teachers, groups, classes_per_day):
    current_population = generate_schedule_population(population_size, subjects, teachers, groups, classes_per_day)
    optimal_schedule = []

    for generation_num in range(num_generations):
        fitness_scores = [evaluate_schedule_conflicts(schedule) for schedule in current_population]
        optimal_schedule = extract_optimal_schedule_from_population(current_population, fitness_scores)

        print(f'Generation {generation_num + 1}: Top Fitness Score = {max(fitness_scores)}')

        new_population = [
            mutate_schedule(
                combine_schedules(*random.choices(current_population, weights=fitness_scores, k=2))[index], 
                mutation_rate, 
                teachers, 
                groups, 
                classes_per_day
            ) 
            for index in range(2) 
            for _ in range(population_size // 2)
        ]
        current_population = new_population

    return optimal_schedule, max(fitness_scores)

NUM_GENERATIONS = 200
SIZE_OF_POPULATION = 1000
RATE_OF_MUTATION = 0.2

if __name__ == '__main__':
    groups = ['Group_1', 'Group_2', 'Group_3', 'Group_4', 'Group_5', 'Group_6']
    subjects = ['Subject_1', 'Subject_2', 'Subject_3', 'Subject_4', 'Subject_5', 'Subject_6']
    teachers = ['Федорус', 'Криволап', 'Свистунов', 'Омельчук', 'Шишацька', 'Поліщук']
    lectures_per_day = 4

    final_schedule, final_fitness = optimize_schedule(SIZE_OF_POPULATION, RATE_OF_MUTATION, NUM_GENERATIONS, subjects, teachers, groups, lectures_per_day)
    print('Optimal Schedule Obtained:')
    for lesson in final_schedule:
        print(lesson)
    print(f'Fitness Score: {final_fitness}')