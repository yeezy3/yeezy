import pygame as pg
import math
import random

def genSprite(image, pos, status=None):
    Sprite = pg.sprite.Sprite()
    Sprite.image = image
    Sprite.rect = Sprite.image.get_rect()
    Sprite.rect.x, Sprite.rect.y = pos[0], pos[1]
    if status != None:
        Sprite.status = status
    return Sprite

# 게임기본설정
실행여부 = True
화면가로길이, 화면세로길이 = 1200, 800
전체시간 = 0
화면 = pg.display.set_mode([화면가로길이, 화면세로길이])
## 화면 크기 정하기
pg.display.set_caption('무단횡단 잘하기 !')
배경이미지 = pg.image.load('img/제목 없음.jpg')
배경이미지 = pg.transform.scale(배경이미지, (화면가로길이, 화면세로길이))
## 이미지를 정해진 사이즈로 변경

캐릭터위치 = [화면가로길이 // 2, 화면세로길이 // 2]
캐릭터속도 = 10
게임요소크기 = (120, 120)
캐릭터이미지딕셔너리 = {"뒤로뛰기": [], "뛰기" : []}
캐릭터멈춤이미지 = pg.image.load(f'img/멈춤.gif')
캐릭터멈춤이미지 = pg.transform.scale(캐릭터멈춤이미지, 게임요소크기)
캐릭터이미지딕셔너리["멈춤"] = 캐릭터멈춤이미지

자동차자동생성시간 = 2
자동차자동생성남은시간 = 1

for 인덱스 in range(3):
    캐릭터뛰는모습이미지 = pg.image.load(f'img/뛰기{인덱스 + 1}.gif')
    캐릭터뛰는모습이미지 = pg.transform.scale(캐릭터뛰는모습이미지, 게임요소크기)
    캐릭터이미지딕셔너리["뛰기"].append(캐릭터뛰는모습이미지)

    캐릭터뛰는모습반전이미지 = pg.image.load(f'img/뛰기{인덱스 + 1}.gif')
    캐릭터뛰는모습반전이미지 = pg.transform.scale(캐릭터뛰는모습반전이미지, 게임요소크기)
    캐릭터이미지딕셔너리["뒤로뛰기"].append(캐릭터뛰는모습반전이미지)

캐릭터이미지상태 = "멈춤"
캐릭터이미지인덱스 = 0
캐릭터이미지흐름 = 1
캐릭터스프라이트 = genSprite(캐릭터이미지딕셔너리[캐릭터이미지상태], 캐릭터위치)

자동차이미지리스트 = []
for 인덱스 in range(4):
    자동차이미지 = pg.image.load(f'img/{인덱스 + 1}.gif')
    자동차이미지 = pg.transform.scale(자동차이미지, 게임요소크기)
    자동차이미지리스트.append(자동차이미지)
자동차스프라이트리스트 = []
자동차스프라이트리스트.append(genSprite(자동차이미지리스트[-1], (200, 200)))

이미지움직임최대시간 = 0.3
이미지움직임시간 = 0

시계 = pg.time.Clock()

state = 0 # 0 게임 중 1 게임 종료

while 실행여부:
    화면.blit(배경이미지, (0, 0))
    if state == 0:
        흐른시간 = 시계.tick(60) / 1000
        전체시간 += 흐른시간
        캐릭터스프라이트.rect.x, 캐릭터스프라이트.rect.y = 캐릭터위치[0], 캐릭터위치[1]
        화면.blit(캐릭터스프라이트.image, 캐릭터스프라이트.rect)

        idx = 0

        for 자동차_스프라이트 in 자동차스프라이트리스트:
            if idx %4 == 0:
                자동차_스프라이트.rect.x -= 4
                자동차_스프라이트.rect.y += 0
            elif idx %4 ==1:
                자동차_스프라이트.rect.x += 0
                자동차_스프라이트.rect.y += 3
            elif idx %4 == 2:
                자동차_스프라이트.rect.y += 1
            else:
                자동차_스프라이트.rect.y -= 1
            idx += 1
            화면.blit(자동차_스프라이트.image, 자동차_스프라이트.rect)

        pg.event.get()
        keys = pg.key.get_pressed()
        이미지움직임시간 -= 흐른시간
        if keys[pg.K_LEFT] or keys[pg.K_RIGHT] or keys[pg.K_UP] or keys[pg.K_DOWN]:

            if keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
                if keys[pg.K_LEFT]:
                    if 캐릭터이미지상태 != '뛰기':
                        캐릭터이미지상태 = '뛰기'
                    if 캐릭터위치[0] >= 0:
                        캐릭터위치[0] -= 캐릭터속도 * 1  # 원하는 속도
                if keys[pg.K_RIGHT]:
                    if 캐릭터이미지상태 != "뒤로뛰기":
                        캐릭터이미지상태 = "뒤로뛰기"
                    if 캐릭터위치[0] < 화면가로길이 - 게임요소크기[0] + 20:
                        캐릭터위치[0] += 캐릭터속도 * 1
            if keys[pg.K_UP] or keys[pg.K_DOWN]:
                if 캐릭터이미지상태 != '뛰기' and 캐릭터이미지상태 != '뒤로뛰기':
                    캐릭터이미지상태 = '뛰기'
                if keys[pg.K_UP] :
                    캐릭터위치[1] -= 캐릭터속도 * 1
                elif keys[pg.K_DOWN] :
                    캐릭터위치[1] += 캐릭터속도 * 1
                else:
                    이미지움직임시간 = 0
            if 이미지움직임시간 <= 0:
                이미지움직임시간 = 이미지움직임최대시간
                캐릭터이미지인덱스 += 캐릭터이미지흐름
                캐릭터스프라이트.image = 캐릭터이미지딕셔너리[캐릭터이미지상태][캐릭터이미지인덱스]
                if 캐릭터이미지인덱스 == 0 or 캐릭터이미지인덱스 == len(캐릭터이미지딕셔너리[캐릭터이미지상태]) - 1:
                    캐릭터이미지흐름 *= -1
        else:
            캐릭터이미지상태 = '멈춤'
            캐릭터스프라이트.image = 캐릭터이미지딕셔너리[캐릭터이미지상태]
                # 캐릭터스프라이트.image = 캐릭터이미지딕셔너리[캐릭터이미지상태]

        자동차자동생성남은시간 -= 흐른시간
        if 자동차자동생성남은시간 <= 0:
            생성위치 = [random.random() * (화면가로길이 - 게임요소크기[0]),
            random.random() * (화면세로길이 - 게임요소크기[1])]
            자동차스프라이트리스트.append(genSprite(자동차이미지리스트[-1], 생성위치))
            자동차자동생성남은시간 = 자동차자동생성시간
        for 자동차스프라이트 in 자동차스프라이트리스트:
            if pg.sprite.collide_mask(캐릭터스프라이트, 자동차스프라이트):
                state = 1

    elif state == 1:
        print("끝")
        break

    pg.display.update()

pg.display.quit()