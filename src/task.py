import pygame 
import datetime
import time
import csv


def mbti_task(
    screen_width: int,
    screen_height: int,
    isi: int,
    image_folder: str,
    num_trials: int,
    num_images: int,
    event_save_path: str
):
    pygame.init()


    screen = pygame.display.set_mode((screen_width, screen_height))
    current_time = datetime.datetime.now()
    hour = str(current_time).split(" ")[1].split(":")[0]
    min = str(current_time).split(" ")[1].split(":")[1]
    sec = str(current_time).split(" ")[1].split(":")[2]

    filename = f"{event_save_path}/combination_event_{hour}.{min}.{sec}.csv"
    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ISI", "RT", "Response", "Stimulus"])


    for _ in range(num_trials):
        for num_image in range(num_images):
            start_time = pygame.time.get_ticks()
            
            task_image = pygame.image.load(f"{image_folder}/tasks/M{num_image+1}.jpg")
            
            screen.blit( #스크린에 이미지 가운데 정렬
                task_image,
                (
                    screen_width // 2 - task_image.get_width() // 2,
                    screen_height // 2 - task_image.get_height() // 2,
                ),
            )
            pygame.display.flip()

            response = "CR" #active 하려면 함 go- 누르기(Hit) nogo일때 - 안누름(CR-correction)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        response = "HIT"
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            end_time = pygame.time.get_ticks()

            time.sleep(isi / 1000.0)

            if response == "HIT":
                rt = end_time - start_time
            else:
                rt = 1000

            # CSV 파일에 결과 기록
            with open(filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        isi,
                        rt,
                        response,
                        num_image + 1,
                    ]
                )
    time.sleep(30) 
    pygame.quit()
