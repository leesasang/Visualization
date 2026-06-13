import matplotlib.pyplot as plt

# Figure 객체 생성
fig = plt.figure()  # 전체 그림을 위한 Figure 객체를 생성함

# Axes 객체 추가
ax = fig.add_subplot(1, 1, 1)  # 1행 1열의 그리드에 첫 번째 Axes를 추가함

# 데이터 생성
x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 40]

# 데이터를 플롯
ax.plot(x, y)  # Axes 객체의 plot() 메소드를 사용하여 데이터를 플롯함

# 그래프 표시
plt.show()  # 전체 Figure를 화면에 표시함
