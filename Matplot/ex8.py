import matplotlib.pyplot as plt

fig, ax = plt.subplots()  # Figure와 Axes 객체를 동시에 생성함

# 데이터 생성
x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 40]

# 데이터를 플롯
ax.plot(x, y)  # 데이터를 플롯

# 그래프 표시
plt.show()  # 전체 Figure를 화면에 표시함
