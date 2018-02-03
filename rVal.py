def calculate_rsqd(POP_SIZE, fitness, points):
    sqd_error = POP_SIZE * fitness

    total_y = 0
    for point in points:
        total_y += point[1]

    mean_y = total_y - len(points)

    total_sqd = 0
    for point in points:
        total_sqd += (point[1] - mean_y)**2

    return (1 - (sqd_error / total_sqd))