import matplotlib.pyplot as plt

fig, ax = plt.subplots()  # Figure와 Axes 객체를 동시에 생성함

# 데이터 생성
labels = ['A', 'B', 'C', 'D']
sizes = [20, 30, 25, 25]

# 원형 차트 생성
ax.pie(sizes, labels=labels, autopct='%1.1f%%')  # Axes 객체의 pie() 메소드를 사용하여 원형 차트를 생성함

# 제목 설정
ax.set_title('Pie Chart')  # 그래프 제목 설정

# 축 숨기기 (원형 차트는 축을 숨기는 것이 일반적임)
ax.axis('equal')  # 원형 차트가 원형으로 보이도록 함

# 그래프 표시
plt.show()  # 전체 Figure를 화면에 표시함
