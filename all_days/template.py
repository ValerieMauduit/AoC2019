# --- Day  ---

# First star:

# Second star:

def run(data_dir, star):
    with open(f'{data_dir}/input-day.txt', 'r') as fic:
        tempo = [x.split(',') for x in fic.read().strip('\n').split('\n')]
    if star == 1:
        print(f'Star {star} - ')
        return
    elif star == 2:
        print(f'Star {star} - ')
        return
    else:
        raise Exception('Star number must be either 1 or 2.')
