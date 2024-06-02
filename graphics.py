from math import sqrt


def apply_phong_lighting(material, light_source, point, normal):
    # Нормализация векторов
    light_vec = [light_source.position[i] - point[i] for i in range(3)]
    dist = sqrt(sum(lv**2 for lv in light_vec))
    light_vec = [lv / dist for lv in light_vec]

    norm_len = sqrt(sum(n**2 for n in normal))
    normal = [n / norm_len for n in normal]

    # Диффузное освещение
    dot = max(0, sum(normal[i] * light_vec[i] for i in range(3)))
    diffuse = [int(material.diffuse[i] * light_source.intensity * dot) for i in range(3)]

    # Зеркальное освещение
    reflect = [2 * dot * normal[i] - light_vec[i] for i in range(3)]
    view = [0, 0, 1]  # предполагается, что наблюдатель в бесконечности
    spec = pow(max(0, sum(reflect[i] * view[i] for i in range(3))), material.shininess)
    specular = [int(material.specular[i] * light_source.intensity * spec) for i in range(3)]

    # Результирующий цвет
    color = [min(255, material.ambient[i] + diffuse[i] + specular[i]) for i in range(3)]
    return color
