def get_num_ending(num, cases):
    """Склоняет существительное,в зависимости от числительного,
    стоящего перед ним.
    """
    num = num % 100
    if num in [11, 19]:
        return cases[2]
    else:
        i = num % 10
        if i == 1:
            return cases[0]
        elif 2 <= i <= 4:
            return cases[1]
        else:
            return cases[2]