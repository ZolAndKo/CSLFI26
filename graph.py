import subprocess
import matplotlib.pyplot as plt

executable_1 = "C:\\Users\\ilyaz\\OneDrive\\Desktop\\факульт ААА и БББ\\Wk 4+5\\pupeler.exe"
executable_2 = "C:\\Users\\ilyaz\\OneDrive\\Desktop\\факульт ААА и БББ\\Wk 4+5\\pupoina.exe"
executable_3 = "C:\\Users\\ilyaz\\OneDrive\\Desktop\\факульт ААА и БББ\\Wk 4+5\\Runge.exe"

dt=0.01

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
        dat_t.append(dt*i)
    return dat_t, dat_x, dat_v, dat_E

t1, x1, v1, E1 = run_simulation(executable_1)


t2, x2, v2, E2 = run_simulation(executable_2)

t3, x3, v3, E3 = run_simulation(executable_3)

show_methods = {"rk4"}


fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(8, 10))

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
            linestyle=method["linestyle"]
        )

    axis.legend()
    axis.grid(True)


# Настройки координаты
ax[0].set_title("Сравнение координаты X(t)")
ax[0].set_xlabel("t, с")
ax[0].set_ylabel("x, м")

# Настройки скорости
ax[1].set_title("Сравнение скорости V(t)")
ax[1].set_xlabel("t, с")
ax[1].set_ylabel("v, м/с")

# Настройки энергии
ax[2].set_title("Сравнение энергии E(t)")
ax[2].set_xlabel("t, с")
ax[2].set_ylabel("E, Дж")

# Настройки фазовой диаграммы
ax[3].set_title("Фазовая диаграмма")
ax[3].set_xlabel("x, м")
ax[3].set_ylabel("v, м/с")

plt.tight_layout()
plt.show()