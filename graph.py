import subprocess
import matplotlib.pyplot as plt
import json
import numpy as np

executable_1 = "pupeler.exe"
executable_2 = "pupoina.exe"
executable_3 = "Runge.exe"

with open("config.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Параметры из config.json
dt = data['dt']
x0 = data['x0']
v0 = data['v0']
omega = data['omega']
k = data['decr']


def run_simulation(exe_path):
    result = subprocess.run(
        [exe_path, "config.json"],
        capture_output=True,
        text=True,
        check=True
    )

    dat_x, dat_v, dat_E, dat_t = [], [], [], []

    lines = result.stdout.splitlines()

    for i, line in enumerate(lines):
        part = line.split()

        if len(part) < 3:
            continue

        dat_x.append(float(part[0]))
        dat_v.append(float(part[1]))
        dat_E.append(float(part[2]))
        dat_t.append(dt * i)

    return dat_t, dat_x, dat_v, dat_E


# Численные методы
t1, x1, v1, E1 = run_simulation(executable_1)
t2, x2, v2, E2 = run_simulation(executable_2)
t3, x3, v3, E3 = run_simulation(executable_3)


# ==========================================
# АНАЛИТИЧЕСКОЕ РЕШЕНИЕ
# ==========================================

# Временная сетка совпадает с RK4
t_analytical = np.array(t3)

alpha = k / 2
D = alpha**2 - omega**2

if D < -1e-14:
    # Колебательный режим
    Omega = np.sqrt(-D)

    C1 = x0
    C2 = (v0 + alpha * x0) / Omega

    x_analytical = np.exp(-alpha * t_analytical) * (
        C1 * np.cos(Omega * t_analytical)
        + C2 * np.sin(Omega * t_analytical)
    )

    v_analytical = np.exp(-alpha * t_analytical) * (
        v0 * np.cos(Omega * t_analytical)
        - ((alpha * v0 + omega**2 * x0) / Omega)
        * np.sin(Omega * t_analytical)
    )

elif abs(D) <= 1e-14:
    # Критическое затухание
    C1 = x0
    C2 = v0 + alpha * x0

    x_analytical = np.exp(-alpha * t_analytical) * (
        C1 + C2 * t_analytical
    )

    v_analytical = np.exp(-alpha * t_analytical) * (
        v0 - alpha * C2 * t_analytical
    )

else:
    # Апериодический режим
    Lambda = np.sqrt(D)

    C1 = x0
    C2 = (v0 + alpha * x0) / Lambda

    x_analytical = np.exp(-alpha * t_analytical) * (
        C1 * np.cosh(Lambda * t_analytical)
        + C2 * np.sinh(Lambda * t_analytical)
    )

    v_analytical = np.exp(-alpha * t_analytical) * (
        v0 * np.cosh(Lambda * t_analytical)
        - ((alpha * v0 + omega**2 * x0) / Lambda)
        * np.sinh(Lambda * t_analytical)
    )


# Аналитическая энергия (масса m = 1)
E_analytical = 0.5 * (
    v_analytical**2
    + omega**2 * x_analytical**2
)


# ==========================================
# ВЫБОР МЕТОДОВ
# ==========================================

show_methods = {
    # "euler",
    "heun",
    "rk4",
    "analytical"
}


fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(10, 13))


methods = {
    "euler": {
        "name": "Эйлер",
        "t": t1,
        "x": x1,
        "v": v1,
        "E": E1,
        "color": "blue",
        "linestyle": "-"
    },

    "heun": {
        "name": "Хойн",
        "t": t2,
        "x": x2,
        "v": v2,
        "E": E2,
        "color": "orange",
        "linestyle": "--"
    },

    "rk4": {
        "name": "Рунге — Кутта",
        "t": t3,
        "x": x3,
        "v": v3,
        "E": E3,
        "color": "green",
        "linestyle": "-"
    },

    "analytical": {
        "name": "Аналитическое решение",
        "t": t_analytical,
        "x": x_analytical,
        "v": v_analytical,
        "E": E_analytical,
        "color": "red",
        "linestyle": ":"
    }
}


# Какие данные отображать на каждом графике
plots = [
    (ax[0], "t", "x", "X"),
    (ax[1], "t", "v", "V"),
    (ax[2], "t", "E", "E"),
    (ax[3], "x", "v", None)
]


for axis, x_key, y_key, suffix in plots:

    for key, method in methods.items():

        if key not in show_methods:
            continue

        label = method["name"]

        if suffix is not None:
            label += f" ({suffix})"

        axis.plot(
            method[x_key],
            method[y_key],
            label=label,
            color=method["color"],
            linestyle=method["linestyle"],
            linewidth=1.5 if key != "analytical" else 2
        )

    axis.legend()
    axis.grid(True)


# ==========================================
# НАСТРОЙКА ГРАФИКОВ
# ==========================================

ax[0].set_title("Сравнение координаты X(t)")
ax[0].set_xlabel("t, с")
ax[0].set_ylabel("x, м")

ax[1].set_title("Сравнение скорости V(t)")
ax[1].set_xlabel("t, с")
ax[1].set_ylabel("v, м/с")

ax[2].set_title("Сравнение энергии E(t)")
ax[2].set_xlabel("t, с")
ax[2].set_ylabel("E, Дж")

ax[3].set_title("Фазовая диаграмма")
ax[3].set_xlabel("x, м")
ax[3].set_ylabel("v, м/с")


plt.tight_layout()
plt.show()