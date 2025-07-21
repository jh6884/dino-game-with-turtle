import turtle
import time
import random

# 윈도우 설정
wn = turtle.Screen()
wn.setup(width=640, height=320)
wn.bgcolor("lightgray")
wn.tracer(0) # 화면 업데이트를 수동으로 제어

# 플레이어 (터틀) 설정
player = turtle.Turtle()
player.shape("square")
player.color("green")
player.penup()
player.goto(-150, -100) # 초기 위치 (바닥)

# 장애물 설정
def create_obstacle():
    obstacle = turtle.Turtle()
    obstacle.shape("square")
    obstacle.color("red")
    obstacle.penup()
    obstacle.goto(320, random.randint(-100, 0))
    obstacles.append(obstacle)
    
# 장애물 관련 변수
obstacle_speed = 10
obstacles = []
min_obstacle_distance = 20
score = 0

def schedule_next_turtle_creation():
    # 다음 터틀이 생성될 시간을 무작위로 결정
    delay = random.randint(800, 4000) 
    # create_obstacle 함수를 호출하도록 예약
    wn.ontimer(create_obstacle, delay)
    # 다시 다음 생성 시간을 스케줄링
    wn.ontimer(schedule_next_turtle_creation, delay)
    
# 점프 관련 변수
is_jumping = False
jump_height = 100 # 최대 점프 높이
jump_speed = 15   # 점프 상승 속도
gravity = 2       # 중력 값 (하강 속도)
vertical_velocity = 0 # 현재 수직 속도 (점프/하강 방향과 속도를 조절)
initial_jump_velocity = 20 # 초기 점프 시작 시 부여되는 속도

# 점프 함수
def jump():
    global is_jumping, vertical_velocity
    if not is_jumping: # 현재 점프 중이 아니라면
        is_jumping = True
        vertical_velocity = initial_jump_velocity # 점프 시작 시 초기 속도 설정

def check_collision(t1, t2, threshold):
    # 두 터틀 객체 t1과 t2 사이의 거리가 threshold보다 작으면 충돌
    if t1.distance(t2) < threshold:
        return True
    return False

def animate_jump():
    global is_jumping, vertical_velocity

    if is_jumping:
        current_y = player.ycor()
        # 현재 수직 속도만큼 터틀의 y 좌표 변경
        player.sety(current_y + vertical_velocity)
        # 중력 적용: 매 프레임마다 속도를 줄임
        vertical_velocity -= gravity
        # 바닥에 닿았는지 확인 (하강 중일 때만)
        if player.ycor() <= -100:
            player.sety(-100) # 바닥에 정확히 위치
            is_jumping = False
            vertical_velocity = 0 # 속도 초기화
            
    wn.update() # 화면 업데이트
    wn.ontimer(animate_jump, 20) # 20ms마다 animate_jump 함수를 다시 호출

def game_loop():
    global score
    for obstacle in list(obstacles): # 리스트 순회 중 삭제를 위해 copy() 사용
        obstacle.setx(obstacle.xcor() - obstacle_speed) # 왼쪽으로 이동
        
        if check_collision(player, obstacle, min_obstacle_distance):
            print("Game Over! score = {}".format(score))
            game_over_pen = turtle.Turtle()
            game_over_pen.hideturtle()
            game_over_pen.penup()
            game_over_pen.goto(0, 0)
            game_over_pen.write("GAME OVER!", align="center", font=("Arial", 30, "normal"))
            return # 게임 오버 시 루프 중단

        if obstacle.xcor() < -340:
            obstacle.clear()
            obstacle.hideturtle()
            obstacles.remove(obstacle)
            score += 1
    wn.update()
    wn.ontimer(game_loop, 20)
    

# 키보드 이벤트
wn.listen()
wn.onkey(jump, "space")

animate_jump()
schedule_next_turtle_creation()
game_loop()
wn.mainloop() # 윈도우를 열린 상태로 유지