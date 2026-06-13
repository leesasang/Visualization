import matplotlib.pyplot as plt

fig, axs = plt.subplots(2, 2)  # 2행 2열의 그리드에 4개의 Axes 객체를 생성함

# 데이터 생성
x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 40]

# 각 Axes에 데이터를 플롯
for ax in axs.flat:
    ax.plot(x, y)  # 각 Axes 객체에 데이터를 플롯함

# 그래프 표시
plt.show()  # 전체 Figure를 화면에 표시함
