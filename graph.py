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


fig, ax = plt.subplots(nrows=4, ncols=1, figsize=(8, 10))


ax[0].plot(t1, x1, label='Эйлер (X)', color='blue')
ax[0].plot(t2, x2, label='Хойн (X)', color='orange', linestyle='--')
ax[0].plot(t3, x3, label='Рунге (X)', color='green')
ax[0].set_title('Сравнение координаты X(t)', fontsize=12)
ax[0].set_xlabel('t, c')
ax[0].set_ylabel('x, м')
ax[0].legend()
ax[0].grid(True)

ax[1].plot(t1, v1, label='Эйлер (V)', color='blue')
ax[1].plot(t2, v2, label='Хойн (V)', color='orange', linestyle='--')
ax[1].plot(t3, v3, label='Рунге (X)', color='green')
ax[1].set_title('Сравнение скорости V(t)', fontsize=12)
ax[1].set_xlabel('t, c')
ax[1].set_ylabel('v, м/с')
ax[1].legend()
ax[1].grid(True)

'''
ax[2].plot(t1, E1, label='Эйлер (E)', color='blue')
ax[2].plot(t2, E2, label='Хойн (E)', color='orange', linestyle='--')
'''
ax[2].plot(t3, E3, label='Рунге (X)', color='green')
ax[2].set_title('Сравнение энергии E(t)', fontsize=12)
ax[2].set_xlabel('t, c')
ax[2].set_ylabel('E, Дж')
ax[2].legend()
ax[2].grid(True)

ax[3].plot(x1, v1, label='Эйлер', color='blue')
ax[3].plot(x2, v2, label='Хойн', color='orange', linestyle='--')
ax[3].plot(x3, v3, label='Рунге (X)', color='green')
ax[3].set_title('Фаз диограммы', fontsize=12)
ax[3].legend()
ax[3].grid(True)

plt.tight_layout()
plt.show()