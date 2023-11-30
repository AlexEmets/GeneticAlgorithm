import random

def get_fitness_score(schedule):
    conflicts = sum(schedule[i]['time'] == schedule[j]['time'] or
                    schedule[i]['teacher'] == schedule[j]['teacher'] or
                    schedule[i]['group'] == schedule[j]['group'] 
                    for i in range(len(schedule)) for j in range(i + 1, len(schedule)))
    return 1.0 / (1.0 + conflicts)

def schedule_mutate(schedule, mutation_rate, teachers, groups, classes_per_day):
    return [
        {
            "subject": class_instance["subject"],
            "teacher": random.choice(teachers) if random.random() < mutation_rate else class_instance["teacher"],
            "group": random.choice(groups) if random.random() < mutation_rate else class_instance["group"],
            "time": random.randint(1, classes_per_day) if random.random() < mutation_rate else class_instance["time"]
        } for class_instance in schedule
    ]

def schedules_crossover(schedule1, schedule2):
    crossover_point = random.randint(1, len(schedule1) - 1)
    return schedule1[:crossover_point] + schedule2[crossover_point:], \
           schedule2[:crossover_point] + schedule1[crossover_point:]

def get_best_element_in_population(population, fitness_scores):
    return max(zip(population, fitness_scores), key=lambda x: x[1])[0]

def find_best_schedule(population_size, mutation_rate, generations, subjects, teachers, groups, classes_per_day):
    population = generate_random_population(population_size, subjects, teachers, groups, classes_per_day)
    best_schedule = []

    for generation in range(generations):
        fitness_scores = [get_fitness_score(schedule) for schedule in population]
        best_schedule = get_best_element_in_population(population, fitness_scores)

        print(f'Покоління {generation + 1}: Найкращий показник функції пристосування = {max(fitness_scores)}')

        new_population = [schedule_mutate(schedules_crossover(*random.choices(population, weights=fitness_scores, k=2))[i], mutation_rate, teachers, groups, classes_per_day)
                          for i in range(2) for _ in range(population_size // 2)]
        population = new_population

    return best_schedule, max(fitness_scores)

def generate_random_population(population_size, subjects, teachers, groups, classes_per_day):
    population = []
    for _ in range(population_size):
        schedule = []
        for subject in subjects:
            schedule.append({
                "subject": subject,
                "teacher": random.choice(teachers),
                "group": random.choice(groups),
                "time": random.randint(1, classes_per_day)
            })
        population.append(schedule)
    return population

k_generations_amount = 200
k_population_size = 1000
k_mutation_rate = 0.2

if __name__ == '__main__':
    k_groups = ['Group_1', 'Group_2', 'Group_3', 'Group_4', 'Group_5', 'Group_6']
    k_subjects = ['Subject_1', 'Subject_2', 'Subject_3', 'Subject_4', 'Subject_5', 'Subject_6']
    k_teachers = ['Федорус', 'Криволап', 'Свистунов', 'Омельчук', 'Шишацька', 'Поліщук']
    k_lecturesPerDay = 5

    best_schedule, fitness = find_best_schedule(k_population_size, k_mutation_rate, k_generations_amount, k_subjects, k_teachers, k_groups, k_lecturesPerDay)
    print('Отримано найоптимальніший розклад:')
    for lesson in best_schedule:
        print(lesson)
    print(f'Фітнес показник: {fitness}')
