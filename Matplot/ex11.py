import matplotlib.pyplot as plt

fig, ax = plt.subplots()  # Figure와 Axes 객체를 동시에 생성함

# 데이터 생성
categories = ['A', 'B', 'C', 'D']
values = [10, 20, 15, 25]

# 막대 그래프 생성
ax.bar(categories, values)  # Axes 객체의 bar() 메소드를 사용하여 막대 그래프를 생성함

# 제목과 축 레이블 설정
ax.set_title('Bar Chart')  # 그래프 제목 설정
ax.set_xlabel('Categories')  # X축 레이블 설정
ax.set_ylabel('Values')  # Y축 레이블 설정

# 그리드 추가
ax.grid(True, axis='y')  # Y축에 그리드를 추가함

# 축 숨기기
ax.spines['top'].set_visible(False)  # 상단 축 숨기기
ax.spines['right'].set_visible(False)  # 우측 축 숨기기

# 그래프 표시
plt.show()  # 전체 Figure를 화면에 표시함
