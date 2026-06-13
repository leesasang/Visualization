import matplotlib.pyplot as plt

fig, ax = plt.subplots()  # Figure와 Axes 객체를 동시에 생성함

# 데이터 생성
x = [1, 2, 3, 4, 5]
y = [10, 20, 25, 30, 40]

# 산점도 생성
ax.scatter(x, y)  # Axes 객체의 scatter() 메소드를 사용하여 산점도를 생성함

# 제목과 축 레이블 설정
ax.set_title('Scatter Plot')  # 그래프 제목 설정
ax.set_xlabel('X Axis')  # X축 레이블 설정
ax.set_ylabel('Y Axis')  # Y축 레이블 설정

# 그리드 추가
ax.grid(True)  # 그리드를 추가함

# 축 숨기기
ax.spines['top'].set_visible(False)  # 상단 축 숨기기
ax.spines['right'].set_visible(False)  # 우측 축 숨기기

# 그래프 표시
plt.show()  # 전체 Figure를 화면에 표시함
