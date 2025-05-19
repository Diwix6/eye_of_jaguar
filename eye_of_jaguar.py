import pygame
import sys
import math
import random

# Инициализация Pygame
pygame.init()

# --- Параметры экрана и Pixel Art ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
PIXEL_SCALE_FACTOR = 5

BUFFER_WIDTH = SCREEN_WIDTH // PIXEL_SCALE_FACTOR
BUFFER_HEIGHT = SCREEN_HEIGHT // PIXEL_SCALE_FACTOR

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pixel_buffer = pygame.Surface((BUFFER_WIDTH, BUFFER_HEIGHT))
pygame.display.set_caption("Pixel Face Animation (Droopy Ears)")

# --- Цвета ---
BACKGROUND_COLOR = (0, 0, 0)
FACE_BLUE_COLOR = (60, 150, 240)
EYE_INNER_COLOR = (0, 0, 0)

# --- Параметры для пиксельного буфера ---

# Добавьте эту константу в раздел параметров (после других параметров)
FACE_OFFSET_Y_BUFF = -10  # Отрицательное значение поднимает лицо вверх



EYE_OUTER_DIAMETER_BUFF = 32
EYE_OUTER_RADIUS_BUFF = EYE_OUTER_DIAMETER_BUFF // 2
EYE_OUTLINE_THICKNESS_BUFF = 3
EYE_INNER_RADIUS_BUFF = EYE_OUTER_RADIUS_BUFF - EYE_OUTLINE_THICKNESS_BUFF

BROW_PUFF_WIDTH_BUFF = EYE_OUTER_RADIUS_BUFF * 0.8
BROW_PUFF_HEIGHT_BUFF = EYE_OUTER_RADIUS_BUFF * 0.4
BROW_PUFF_OFFSET_Y_FROM_EYE_CENTER_BUFF = -EYE_OUTER_RADIUS_BUFF * 1.4
BROW_PUFF_WINK_RAISE_BUFF = -BROW_PUFF_HEIGHT_BUFF * 0.6
current_left_brow_puff_y_offset_buff = 0; current_right_brow_puff_y_offset_buff = 0
current_left_brow_puff_x_offset_buff = 0; current_right_brow_puff_x_offset_buff = 0
target_left_brow_puff_y_offset = 0; target_right_brow_puff_y_offset = 0
target_left_brow_puff_x_offset = 0; target_right_brow_puff_x_offset = 0

# Кошачьи УШИ (перевернутые/обвислые, меньше, правее, ниже)
EAR_SIDE_LENGTH_BUFF = EYE_OUTER_DIAMETER_BUFF * 0.65 # Уменьшаем еще (было 0.75)
EAR_OPENING_ANGLE_DEG = 70 # Угол между двумя линиями уха (для обвислых может быть шире)
EAR_LINE_THICKNESS_BUFF = max(1, PIXEL_SCALE_FACTOR // 3)
EAR_TILT_ANGLE_DEG = 30 # Небольшой наклон "складки" уха
# Позиция "основания" (верхней точки соединения) ушей - теперь это точка, откуда они "свисают"

EAR_BASE_OFFSET_Y_FROM_TOP_BUFF = BUFFER_HEIGHT * 0.22 + FACE_OFFSET_Y_BUFF

EAR_BASE_SPACING_FROM_CENTER_X_BUFF = EYE_OUTER_DIAMETER_BUFF * 1.5
EAR_GENERAL_X_SHIFT_BUFF = 1 # Смещаем группу ушей вправо (было 6)

# Позиции элементов
EYE_SPACING_BUFF = EYE_OUTER_DIAMETER_BUFF * 1.6

EYE_CENTER_Y_BUFF = BUFFER_HEIGHT // 2 + 10 + FACE_OFFSET_Y_BUFF

LEFT_EYE_BASE_CX_BUFF = BUFFER_WIDTH // 2 - int(EYE_SPACING_BUFF / 2)
RIGHT_EYE_BASE_CX_BUFF = BUFFER_WIDTH // 2 + int(EYE_SPACING_BUFF / 2)

NOSE_DOT_RADIUS_BUFF = max(1, EYE_OUTER_DIAMETER_BUFF // 12)
NOSE_CENTER_Y_BUFF = EYE_CENTER_Y_BUFF + EYE_OUTER_RADIUS_BUFF + NOSE_DOT_RADIUS_BUFF * 3
MOUTH_DOT_RADIUS_BUFF = NOSE_DOT_RADIUS_BUFF
MOUTH_CENTER_Y_BUFF = NOSE_CENTER_Y_BUFF + MOUTH_DOT_RADIUS_BUFF * 4
MOUTH_HORIZONTAL_SPACING_SCALE = 3.5
WHISKER_LENGTH_BUFF = EYE_OUTER_RADIUS_BUFF * 0.8
WHISKER_Y_OFFSET_FROM_EYE_CENTER_BUFF = EYE_OUTER_RADIUS_BUFF * 0.5
WHISKER_X_START_OFFSET_FROM_EYE_EDGE_BUFF = EYE_OUTER_RADIUS_BUFF * 0.2

# --- Анимационные параметры ---
face_state = "idle"; wink_eye = None; wink_progress = 0.0
WINK_TOTAL_DURATION = 3500; WINK_CLOSE_PHASE_RATIO = 0.05
WINK_HOLD_PHASE_RATIO = 0.80; WINK_OPEN_PHASE_RATIO = 0.15
WINK_HALF_CLOSE_AMOUNT = 0.65; NEXT_WINK_CHANCE = 0.0025
last_wink_time = 0; wink_start_time = 0
blink_progress_val = 0.0; BLINK_SPEED_CLOSING = 0.20; BLINK_SPEED_OPENING = 0.25
NEXT_BLINK_MIN_DELAY = 2500; NEXT_BLINK_MAX_DELAY = 7000; next_blink_time = 0
CLOSED_EYE_DURATION = random.randint(80, 150); blink_phase = "closing"
target_eye_offset_x_buff = 0; target_eye_offset_y_buff = 0
current_eye_offset_x_buff = 0; current_eye_offset_y_buff = 0
NEXT_LOOK_CHANGE_MIN_DELAY = 2000; NEXT_LOOK_CHANGE_MAX_DELAY = 4500; look_change_time = 0
MAX_EYE_SHIFT_BUFF = EYE_INNER_RADIUS_BUFF * 0.30; LOOK_TRANSITION_SPEED = 0.09

clock = pygame.time.Clock(); FPS = 30

# --- Функции рисования ---
def draw_eye_on_buffer(surface, base_center_x, base_center_y, eye_shift_x, eye_shift_y, eyelid_closure_amount):
    current_center_x = base_center_x + int(eye_shift_x)
    current_center_y = base_center_y + int(eye_shift_y)
    pygame.draw.circle(surface, FACE_BLUE_COLOR, (current_center_x, current_center_y), EYE_OUTER_RADIUS_BUFF)
    pygame.draw.circle(surface, EYE_INNER_COLOR, (current_center_x, current_center_y), EYE_INNER_RADIUS_BUFF)
    if eyelid_closure_amount > 0.001:
        rect_height = int(EYE_OUTER_DIAMETER_BUFF * eyelid_closure_amount)
        if rect_height > 0:
            pygame.draw.rect(surface, BACKGROUND_COLOR,
                             (current_center_x - EYE_OUTER_RADIUS_BUFF, current_center_y - EYE_OUTER_RADIUS_BUFF,
                              EYE_OUTER_DIAMETER_BUFF, rect_height))

def draw_brow_puff_on_buffer(surface, eye_base_cx, eye_base_cy, anim_x_offset, anim_y_offset):
    puff_center_x = eye_base_cx + int(anim_x_offset)
    puff_center_y = eye_base_cy + int(BROW_PUFF_OFFSET_Y_FROM_EYE_CENTER_BUFF + anim_y_offset)
    puff_rect = pygame.Rect(0,0, int(BROW_PUFF_WIDTH_BUFF), int(BROW_PUFF_HEIGHT_BUFF))
    puff_rect.center = (puff_center_x, puff_center_y)
    pygame.draw.ellipse(surface, FACE_BLUE_COLOR, puff_rect)

def draw_cat_ear_on_buffer(surface, side, buffer_center_x, base_y_offset,
                           side_len, opening_angle_deg, tilt_angle_deg,
                           spacing_from_center_x, general_x_shift, line_thickness):
    # "base_pivot" - это точка на голове, откуда ухо "растет" или "крепится"
    base_pivot_y = base_y_offset
    if side == "left":
        base_pivot_x = buffer_center_x - spacing_from_center_x + general_x_shift
        # Для обвислых ушей, наклон может быть интерпретирован как поворот "складки"
        effective_tilt_deg = -tilt_angle_deg 
    else: # right
        base_pivot_x = buffer_center_x + spacing_from_center_x + general_x_shift
        effective_tilt_deg = tilt_angle_deg

    half_opening_rad = math.radians(opening_angle_deg / 2)
    tilt_rad = math.radians(effective_tilt_deg)

    # Базовые углы для обвислых ушей: смотрят вниз и в стороны.
    # Например, 0 радиан - вправо. math.pi / 2 - вниз.
    # Левое ухо: линии идут влево-вниз и вправо-вниз от точки крепления (относительно вертикали)
    # Правое ухо: симметрично.

    # Угол первой линии (например, "внутренней", ближе к центру головы, но свисающей)
    # Пусть 0 градусов (вдоль оси X) будет базой, и оттуда откладываем углы
    # Для левого уха: одна линия идет больше вниз, другая больше вбок-вниз.
    # Для правого уха: симметрично.
    
    # Угол от вертикали вниз (math.pi/2)
    # Первая линия: (math.pi/2) - half_opening_rad + tilt_rad (если tilt_rad отклоняет наружу)
    # Вторая линия: (math.pi/2) + half_opening_rad + tilt_rad
    
    # Изменим базовое направление "взгляда" ушей, чтобы они свисали
    # Пусть базовая линия для углов будет горизонтальная, идущая вправо (0 радиан)
    # Тогда для левого уха, свисающего влево и вниз:
    #   - одна линия около 3*math.pi/4 (вниз и влево)
    #   - другая линия около 5*math.pi/4 (вниз и влево, но другой край) - это не то.

    # Проще: задаем два угла от точки крепления
    if side == "left":
        # Левое ухо должно свисать влево и вниз
        angle1_base_deg = 180 - 45 # Влево-вверх (если бы ухо стояло)
        angle2_base_deg = 180 + 45 # Влево-вниз
        # Переворачиваем:
        angle1_base_deg = 90 + opening_angle_deg/2 - tilt_angle_deg # Вниз и влево
        angle2_base_deg = 90 - opening_angle_deg/2 - tilt_angle_deg # Вниз и ближе к центру (если tilt наружу)
    else: # right
        angle1_base_deg = 90 - opening_angle_deg/2 + tilt_angle_deg # Вниз и вправо
        angle2_base_deg = 90 + opening_angle_deg/2 + tilt_angle_deg # Вниз и ближе к центру

    angle1 = math.radians(angle1_base_deg)
    angle2 = math.radians(angle2_base_deg)


    tip1_x = base_pivot_x + side_len * math.cos(angle1)
    tip1_y = base_pivot_y + side_len * math.sin(angle1)
    tip2_x = base_pivot_x + side_len * math.cos(angle2)
    tip2_y = base_pivot_y + side_len * math.sin(angle2)
    
    pygame.draw.line(surface, FACE_BLUE_COLOR, (int(base_pivot_x), int(base_pivot_y)), (int(tip1_x), int(tip1_y)), line_thickness)
    pygame.draw.line(surface, FACE_BLUE_COLOR, (int(base_pivot_x), int(base_pivot_y)), (int(tip2_x), int(tip2_y)), line_thickness)


def draw_nose_on_buffer(surface, base_cx, base_cy, dot_radius):
    offset_x = int(dot_radius * 2.5); offset_y = int(dot_radius * 1.5)
    pygame.draw.circle(surface, FACE_BLUE_COLOR, (base_cx - offset_x // 2, base_cy), dot_radius)
    pygame.draw.circle(surface, FACE_BLUE_COLOR, (base_cx + offset_x // 2, base_cy), dot_radius)
    pygame.draw.circle(surface, FACE_BLUE_COLOR, (base_cx, base_cy - offset_y), dot_radius)

def draw_mouth_on_buffer(surface, base_cx, base_cy, dot_radius, horizontal_spacing_scale):
    offset_x = int(dot_radius * horizontal_spacing_scale)
    pygame.draw.circle(surface, FACE_BLUE_COLOR, (base_cx - offset_x // 2, base_cy), dot_radius)
    pygame.draw.circle(surface, FACE_BLUE_COLOR, (base_cx + offset_x // 2, base_cy), dot_radius)
    pygame.draw.circle(surface, FACE_BLUE_COLOR, (base_cx, base_cy + dot_radius // 2), max(1, dot_radius -1 if dot_radius > 1 else 1 ))

def draw_whiskers_on_buffer(surface, eye_center_x, eye_center_y, is_left_side, length, y_offset_from_eye_center):
    start_y = eye_center_y + y_offset_from_eye_center
    line_thickness = max(1, EYE_OUTER_DIAMETER_BUFF // 20)
    if is_left_side:
        start_x = eye_center_x - EYE_OUTER_RADIUS_BUFF - WHISKER_X_START_OFFSET_FROM_EYE_EDGE_BUFF; end_x = start_x - length
    else:
        start_x = eye_center_x + EYE_OUTER_RADIUS_BUFF + WHISKER_X_START_OFFSET_FROM_EYE_EDGE_BUFF; end_x = start_x + length
    pygame.draw.line(surface, FACE_BLUE_COLOR, (start_x, start_y - line_thickness*2), (end_x, start_y - line_thickness*2), line_thickness)
    pygame.draw.line(surface, FACE_BLUE_COLOR, (start_x, start_y + line_thickness*2), (end_x, start_y + line_thickness*2), line_thickness)

next_brow_puff_anim_time = 0
# ... (rest of the animation logic and main loop - no changes needed there from previous version)

running = True
while running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE: running = False

    left_eye_closure = 0.0; right_eye_closure = 0.0
    actual_left_brow_puff_y_offset = current_left_brow_puff_y_offset_buff
    actual_right_brow_puff_y_offset = current_right_brow_puff_y_offset_buff

    # --- Логика состояний лица ---
    if face_state == "idle":
        if current_time >= next_blink_time:
            face_state = "blinking"; blink_progress_val = 0.0; blink_phase = "closing"; CLOSED_EYE_DURATION = random.randint(80, 180)
        elif random.random() < NEXT_WINK_CHANCE and current_time > last_wink_time + 3000:
            face_state = "winking"; wink_eye = random.choice(["left", "right"]); wink_start_time = current_time; last_wink_time = current_time; wink_progress = 0.0
    if face_state == "blinking":
        if blink_phase == "closing":
            blink_progress_val += BLINK_SPEED_CLOSING
            if blink_progress_val >= 1.0: blink_progress_val = 1.0; blink_phase = "closed"; blink_closed_start_time = current_time
        elif blink_phase == "closed":
            if current_time >= blink_closed_start_time + CLOSED_EYE_DURATION: blink_phase = "opening"
        elif blink_phase == "opening":
            blink_progress_val -= BLINK_SPEED_OPENING
            if blink_progress_val <= 0.0: blink_progress_val = 0.0; blink_phase = "closing"; face_state = "idle"; next_blink_time = current_time + random.randint(NEXT_BLINK_MIN_DELAY, NEXT_BLINK_MAX_DELAY)
        left_eye_closure = blink_progress_val; right_eye_closure = blink_progress_val
    elif face_state == "winking":
        elapsed_wink_time = current_time - wink_start_time
        close_phase_end_time = WINK_TOTAL_DURATION*WINK_CLOSE_PHASE_RATIO; hold_phase_end_time = close_phase_end_time + WINK_TOTAL_DURATION*WINK_HOLD_PHASE_RATIO
        current_wink_eye_closure = 0.0; current_tuft_raise_factor = 0.0
        if elapsed_wink_time <= close_phase_end_time: 
            pr = elapsed_wink_time/close_phase_end_time if close_phase_end_time > 0 else 1; current_wink_eye_closure=pr*WINK_HALF_CLOSE_AMOUNT; current_tuft_raise_factor=pr
        elif elapsed_wink_time <= hold_phase_end_time: current_wink_eye_closure=WINK_HALF_CLOSE_AMOUNT; current_tuft_raise_factor=1.0
        elif elapsed_wink_time < WINK_TOTAL_DURATION: 
            pr = (elapsed_wink_time-hold_phase_end_time)/(WINK_TOTAL_DURATION*WINK_OPEN_PHASE_RATIO) if (WINK_TOTAL_DURATION*WINK_OPEN_PHASE_RATIO)>0 else 1
            current_wink_eye_closure=(1.0-pr)*WINK_HALF_CLOSE_AMOUNT; current_tuft_raise_factor=(1.0-pr)
        else: face_state="idle"; current_wink_eye_closure=0.0; current_tuft_raise_factor=0.0
        if wink_eye=="left": left_eye_closure=current_wink_eye_closure; actual_right_brow_puff_y_offset+=BROW_PUFF_WINK_RAISE_BUFF*current_tuft_raise_factor
        else: right_eye_closure=current_wink_eye_closure; actual_left_brow_puff_y_offset+=BROW_PUFF_WINK_RAISE_BUFF*current_tuft_raise_factor
    
    if face_state == "idle" or face_state == "winking":
        if current_time >= look_change_time:
            if random.random() < 0.4: target_eye_offset_x_buff=0; target_eye_offset_y_buff=0
            else: target_eye_offset_x_buff=random.uniform(-MAX_EYE_SHIFT_BUFF,MAX_EYE_SHIFT_BUFF); target_eye_offset_y_buff=random.uniform(-MAX_EYE_SHIFT_BUFF*0.7,MAX_EYE_SHIFT_BUFF*0.7)
            look_change_time = current_time + random.randint(NEXT_LOOK_CHANGE_MIN_DELAY, NEXT_LOOK_CHANGE_MAX_DELAY)
    current_eye_offset_x_buff+=(target_eye_offset_x_buff-current_eye_offset_x_buff)*LOOK_TRANSITION_SPEED
    current_eye_offset_y_buff+=(target_eye_offset_y_buff-current_eye_offset_y_buff)*LOOK_TRANSITION_SPEED

    if face_state != "winking":
        if current_time >= next_brow_puff_anim_time:
            next_brow_puff_anim_time=current_time+random.randint(1000,3000)
            target_left_brow_puff_y_offset=random.uniform(-BROW_PUFF_HEIGHT_BUFF*0.2,BROW_PUFF_HEIGHT_BUFF*0.1); target_right_brow_puff_y_offset=random.uniform(-BROW_PUFF_HEIGHT_BUFF*0.2,BROW_PUFF_HEIGHT_BUFF*0.1)
            target_left_brow_puff_x_offset=random.uniform(-BROW_PUFF_WIDTH_BUFF*0.1,BROW_PUFF_WIDTH_BUFF*0.1); target_right_brow_puff_x_offset=random.uniform(-BROW_PUFF_WIDTH_BUFF*0.1,BROW_PUFF_WIDTH_BUFF*0.1)
            sync_y = random.uniform(-BROW_PUFF_HEIGHT_BUFF * 0.2, BROW_PUFF_HEIGHT_BUFF * 0.1)
            sync_x = random.uniform(-BROW_PUFF_WIDTH_BUFF * 0.1, BROW_PUFF_WIDTH_BUFF * 0.1)
            if random.random()<0.6: sync_y=random.uniform(-BROW_PUFF_HEIGHT_BUFF*0.2,BROW_PUFF_HEIGHT_BUFF*0.1); sync_x=random.uniform(-BROW_PUFF_WIDTH_BUFF*0.1,BROW_PUFF_WIDTH_BUFF*0.1)
            target_left_brow_puff_y_offset=sync_y; target_right_brow_puff_y_offset=sync_y; target_left_brow_puff_x_offset=sync_x; target_right_brow_puff_x_offset=sync_x
        bps=0.05 
        current_left_brow_puff_y_offset_buff+=(target_left_brow_puff_y_offset-current_left_brow_puff_y_offset_buff)*bps; current_right_brow_puff_y_offset_buff+=(target_right_brow_puff_y_offset-current_right_brow_puff_y_offset_buff)*bps
        current_left_brow_puff_x_offset_buff+=(target_left_brow_puff_x_offset-current_left_brow_puff_x_offset_buff)*bps; current_right_brow_puff_x_offset_buff+=(target_right_brow_puff_x_offset-current_right_brow_puff_x_offset_buff)*bps
        actual_left_brow_puff_y_offset=current_left_brow_puff_y_offset_buff; actual_right_brow_puff_y_offset=current_right_brow_puff_y_offset_buff
    if face_state=="blinking": bbd=BROW_PUFF_HEIGHT_BUFF*0.2*blink_progress_val; actual_left_brow_puff_y_offset+=bbd; actual_right_brow_puff_y_offset+=bbd

    pixel_buffer.fill(BACKGROUND_COLOR)
    ncx=BUFFER_WIDTH//2; draw_nose_on_buffer(pixel_buffer,ncx,int(NOSE_CENTER_Y_BUFF),NOSE_DOT_RADIUS_BUFF)
    mcx=BUFFER_WIDTH//2; draw_mouth_on_buffer(pixel_buffer,mcx,int(MOUTH_CENTER_Y_BUFF),MOUTH_DOT_RADIUS_BUFF,MOUTH_HORIZONTAL_SPACING_SCALE)
    aecy=EYE_CENTER_Y_BUFF
    draw_whiskers_on_buffer(pixel_buffer,LEFT_EYE_BASE_CX_BUFF,aecy,True,int(WHISKER_LENGTH_BUFF),int(WHISKER_Y_OFFSET_FROM_EYE_CENTER_BUFF))
    draw_whiskers_on_buffer(pixel_buffer,RIGHT_EYE_BASE_CX_BUFF,aecy,False,int(WHISKER_LENGTH_BUFF),int(WHISKER_Y_OFFSET_FROM_EYE_CENTER_BUFF))
    draw_eye_on_buffer(pixel_buffer,LEFT_EYE_BASE_CX_BUFF,EYE_CENTER_Y_BUFF,current_eye_offset_x_buff,current_eye_offset_y_buff,left_eye_closure)
    draw_eye_on_buffer(pixel_buffer,RIGHT_EYE_BASE_CX_BUFF,EYE_CENTER_Y_BUFF,current_eye_offset_x_buff,current_eye_offset_y_buff,right_eye_closure)
    draw_brow_puff_on_buffer(pixel_buffer,LEFT_EYE_BASE_CX_BUFF,EYE_CENTER_Y_BUFF,current_left_brow_puff_x_offset_buff,actual_left_brow_puff_y_offset)
    draw_brow_puff_on_buffer(pixel_buffer,RIGHT_EYE_BASE_CX_BUFF,EYE_CENTER_Y_BUFF,current_right_brow_puff_x_offset_buff,actual_right_brow_puff_y_offset)
    
    draw_cat_ear_on_buffer(pixel_buffer, "left", BUFFER_WIDTH // 2, int(EAR_BASE_OFFSET_Y_FROM_TOP_BUFF),
                           int(EAR_SIDE_LENGTH_BUFF), int(EAR_OPENING_ANGLE_DEG), int(EAR_TILT_ANGLE_DEG),
                           int(EAR_BASE_SPACING_FROM_CENTER_X_BUFF), int(EAR_GENERAL_X_SHIFT_BUFF), EAR_LINE_THICKNESS_BUFF)
    draw_cat_ear_on_buffer(pixel_buffer, "right", BUFFER_WIDTH // 2, int(EAR_BASE_OFFSET_Y_FROM_TOP_BUFF),
                           int(EAR_SIDE_LENGTH_BUFF), int(EAR_OPENING_ANGLE_DEG), int(EAR_TILT_ANGLE_DEG),
                           int(EAR_BASE_SPACING_FROM_CENTER_X_BUFF), int(EAR_GENERAL_X_SHIFT_BUFF), EAR_LINE_THICKNESS_BUFF)

    scaled_surface = pygame.transform.scale(pixel_buffer, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_surface, (0,0))
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()