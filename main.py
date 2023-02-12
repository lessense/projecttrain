''' Импортирование библиотек '''
import os
import sys
import random
import pygame
import time
import math
import copy
from PIL import Image
import webbrowser

IMAGES = {}

def load_image(name, remove_bg = False):
    if (name, remove_bg) in IMAGES:
        return IMAGES[(name, remove_bg)]
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)

    if remove_bg:
        image = image.convert()
        colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    IMAGES[(name, remove_bg)] = image
    return IMAGES[(name, remove_bg)]

def draw_text(_window, text, font, aa, fg, bg, x, y, centered_x=0, centered_y=0):

    '''
    :param centered_x:
        -1 -> left
        0 -> center
        1 -> right
    :param centered_y:
        -1 -> bottom
        0 -> center
        1 -> top
    '''
    text = font.render(text, aa, fg, bg)
    rect = text.get_rect()
    w, h = rect.width, rect.height
    x -= (w//2) * centered_x
    y -= (h//2) * centered_y
    place = text.get_rect(center=(x,y))
    _window.blit(text, place)

class Rail:
    '''
        rotation = 0..3

        При rotation == 0 следующие состояния:
            type 0 - прямой рельс
            type 1 - поворот
            type 2 - буква T
                state 0 - левый поворот
                state 1 - правый поворот
                state 2 - прямая
            type 3 - перекрёсток
                state 0 - проезд прямо
                state 1 - проезд поперёк
    '''

    def __init__(self, pos=(0, 0), type=0, rotation=0, state=0):
        self.pos = pos
        self.type = type
        self.rotation = rotation
        self.state = state

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def change_state(self):
        C = 0
        if self.type == 0:
            C = 1
        elif self.type == 1:
            C = 1
        elif self.type == 2:
            C = 3
        elif self.type == 3:
            C = 2
        self.state = (self.state + 1) % C

    def rotate_train(self, rot):
        '''
            rot = 0 - вправо
            rot = 1 - вниз
            rot = 2 - влево
            rot = 3 - вверх
        '''
        if rot == 0:
            if self.type == 0:
                if self.state == 0:
                    if self.rotation == 0:
                        return 0
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return 0
                    if self.rotation == 3:
                        return -1
            if self.type == 1:
                if self.state == 0:
                    if self.rotation == 0:
                        return 1
                    if self.rotation == 1:
                        return 3
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return -1
            if self.type == 2:
                if self.state == 0:
                    if self.rotation == 0:
                        return 1
                    if self.rotation == 1:
                        return 3
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return -1
                if self.state == 1:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return 1
                    if self.rotation == 2:
                        return 3
                    if self.rotation == 3:
                        return -1
                if self.state == 2:
                    if self.rotation == 0:
                        return 0
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return 0
                    if self.rotation == 3:
                        return -1
            if self.type == 3:
                if self.state == 0:
                    if self.rotation == 0:
                        return 0
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return 0
                    if self.rotation == 3:
                        return -1
                if self.state == 1:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return 0
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return 0
        if rot == 1:
            if self.type == 0:
                if self.state == 0:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return 1
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return 1
            if self.type == 1:
                if self.state == 0:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return 2
                    if self.rotation == 2:
                        return 0
                    if self.rotation == 3:
                        return -1
            if self.type == 2:
                if self.state == 0:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return 2
                    if self.rotation == 2:
                        return 0
                    if self.rotation == 3:
                        return -1
                if self.state == 1:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return 2
                    if self.rotation == 3:
                        return 0
                if self.state == 2:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return 1
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return 1
            if self.type == 3:
                if self.state == 0:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return 1
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return 1
                if self.state == 1:
                    if self.rotation == 0:
                        return 1
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return 1
                    if self.rotation == 3:
                        return -1
        if rot == 2:
            if self.type == 0:
                if self.state == 0:
                    if self.rotation == 0:
                        return 2
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return 2
                    if self.rotation == 3:
                        return -1
            if self.type == 1:
                if self.state == 0:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return 3
                    if self.rotation == 3:
                        return 1
            if self.type == 2:
                if self.state == 0:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return 3
                    if self.rotation == 3:
                        return 1
                if self.state == 1:
                    if self.rotation == 0:
                        return 1
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return 3
                if self.state == 2:
                    if self.rotation == 0:
                        return 2
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return 2
                    if self.rotation == 3:
                        return -1
            if self.type == 3:
                if self.state == 0:
                    if self.rotation == 0:
                        return 2
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return 2
                    if self.rotation == 3:
                        return -1
                if self.state == 1:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return 2
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return 2
        if rot == 3:
            if self.type == 0:
                if self.state == 0:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return 3
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return 3
            if self.type == 1:
                if self.state == 0:
                    if self.rotation == 0:
                        return 2
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return 0
            if self.type == 2:
                if self.state == 0:
                    if self.rotation == 0:
                        return 2
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return 0
                if self.state == 1:
                    if self.rotation == 0:
                        return 0
                    if self.rotation == 1:
                        return 2
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return -1
                if self.state == 2:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return 3
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return 3
            if self.type == 3:
                if self.state == 0:
                    if self.rotation == 0:
                        return -1
                    if self.rotation == 1:
                        return 3
                    if self.rotation == 2:
                        return -1
                    if self.rotation == 3:
                        return 3
                if self.state == 1:
                    if self.rotation == 0:
                        return 3
                    if self.rotation == 1:
                        return -1
                    if self.rotation == 2:
                        return 3
                    if self.rotation == 3:
                        return -1


class Carriage:
    '''
    type 0 - пассажирский
    type 1 - самосвал (iron)
    type 2 - полувагон (coal)
    type 3 - платформа (wood)
    type 4 - хоппер (crops)
    type 5 - локомотив
    '''

    def __init__(self, type=5, pos=(0, 0), rot=0, loading=False, loading_start = 0, loading_duration = 500):
        self.type = type
        self.capacity = 10
        self.full = 0
        self.pos = pos
        self.rot = rot
        self.loading = loading
        self.loading_start = loading_start
        self.loading_duration = loading_duration
        if (self.type == 0):
            self.passengers = []
            self.food = 0
            self.food_capacity = 42

    def load(self):
        if (self.loading and TIMER - self.loading_start >= self.loading_duration):
            self.loading = False
        if self.loading:
            return
        for b in game.buildings:
            if type(game.buildings[b]) == Coal_Mine and self.type == 2 and abs(b[0] - self.pos[0]) + abs(b[1] - self.pos[1]) == 1 and self.full < self.capacity:
                self.full += 1
                self.loading = True
                self.loading_start = TIMER
                game.stats.params['coal_earned'] += 1
                return
            if type(game.buildings[b]) == Iron_Mine and self.type == 1 and abs(b[0] - self.pos[0]) + abs(b[1] - self.pos[1]) == 1 and self.full < self.capacity:
                self.full += 1
                self.loading = True
                self.loading_start = TIMER
                game.stats.params['iron_earned'] += 1
                return
            if type(game.buildings[b]) == Sawmill and self.type == 3 and abs(b[0]-self.pos[0]) + abs(b[1]-self.pos[1]) == 1 and self.full < self.capacity:
                self.full += 1
                self.loading = True
                self.loading_start = TIMER
                game.stats.params['wood_earned'] += 1
                return
            if type(game.buildings[b]) == Seaport and self.type == 4 and abs(b[0]-self.pos[0]) + abs(b[1]-self.pos[1]) == 1 and self.full < self.capacity:
                self.full += 1
                self.loading = True
                self.loading_start = TIMER
                game.stats.params['crops_earned'] += 1
                return
            if type(game.buildings[b]) == Station and self.type == 0 and abs(b[0] - self.pos[0]) + abs(b[1] - self.pos[1]) == 1:
                leaving_passenger = -1
                for i in range(len(self.passengers)):
                    if self.passengers[i].destination == game.buildings[b].name:
                        leaving_passenger = i
                if (leaving_passenger != -1):
                    game.resources['money'] += self.passengers[leaving_passenger].ticket_cost
                    self.passengers.pop(leaving_passenger)
                    self.full -= 1
                    self.loading = True
                    self.loading_start = TIMER
                    game.exp += 1
                    game.stats.params['passengers_collected'] += 1
                    return
            if type(game.buildings[b]) == Station and self.type == 0 and abs(b[0]-self.pos[0]) + abs(b[1]-self.pos[1]) == 1 and self.full < self.capacity:
                passenger = game.buildings[b].collect_passenger()
                if (passenger is not None) and (self.food > 0):
                    self.food -= 1
                    self.passengers.append(passenger)
                    self.full += 1
                    self.loading = True
                    self.loading_start = TIMER
                    return
            if type(game.buildings[b]) == Storage and self.type != 0 and abs(b[0]-self.pos[0]) + abs(b[1]-self.pos[1]) == 1 and self.full > 0:
                if (self.type == 1):
                    self.full -= 1
                    game.resources['iron'] += 1
                    game.exp += 1
                if (self.type == 2):
                    self.full -= 1
                    game.resources['coal'] += 1
                    game.exp += 1
                if (self.type == 3):
                    self.full -= 1
                    game.resources['wood'] += 1
                    game.exp += 1
                if (self.type == 4):
                    self.full -= 1
                    game.resources['crops'] += 1
                    game.exp += 1
                if (self.type == 0):
                    pass
                self.loading = True
                self.loading_start = TIMER
                return




class Train:
    global game

    def __init__(self,
                 carriages=None, name=None,
                 coal = 0, coal_capacity = 99,
                 engine=False, bps = 2, previous_move = 0,
                 coalps = 0.6, previous_coal = 0):
        if carriages is None:
            carriages = []
        if name is None:
            name = random.choice(["Томас", "Джеймс", "Гордон", "Эдвард", "Эмили", "Перси", "Генри", "Тоби"])
        self.carriages = carriages
        self.name = name
        self.coal = coal
        self.coal_capacity = coal_capacity
        self.engine = engine
        self.bps = bps
        self.previous_move = previous_move
        self.coalps = coalps
        self.previous_coal = previous_coal

    def load(self):
        for carriage in self.carriages:
            carriage.load()

    def process(self):
        if (self.coal == 0):
            self.engine = False
        if (self.engine):
            if (TIMER - self.previous_coal) * (self.coalps / 1000) >= 1:
                self.previous_coal = TIMER
                self.coal -= 1
        self.load()
        if any(carriage.loading for carriage in self.carriages):
            #print("CARRIAGE BEING LOADED")
            return
        if (not self.engine):
            #print("ENGINE IS OFF")
            return
        if any(carriage.pos not in game.rails for carriage in self.carriages):
            #print("CARRIAGE NOT ON RAILS")
            return
        for i in range(len(self.carriages)):
            carriage = self.carriages[i]
            rot = game.rails[carriage.pos].rotate_train(carriage.rot)
            X = carriage.pos[0]
            Y = carriage.pos[1]
            if rot == 0:
                X += 1
            if rot == 1:
                Y += 1
            if rot == 2:
                X -= 1
            if rot == 3:
                Y -= 1
            if rot == -1:
                #print("ROT -1")
                return
            if (X, Y) not in game.rails:
                #print("(X,Y) not in game.rails")
                return
            if game.rails[(X, Y)].rotate_train(rot) == -1:
                #print("CANT ROTATE CAR")
                return
            if (i == 0 and any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains)):
                #print("SOMETHING ON TRAIN'S WAY")
                return
        for i in range(1, len(self.carriages)):
            rot = game.rails[self.carriages[i].pos].rotate_train(self.carriages[i].rot)
            X = self.carriages[i].pos[0]
            Y = self.carriages[i].pos[1]
            if rot == 0:
                X += 1
            if rot == 1:
                Y += 1
            if rot == 2:
                X -= 1
            if rot == 3:
                Y -= 1
            if (X, Y) != self.carriages[i - 1].pos:
                #print("CARRIAGE GAP")
                return
        if TIMER - self.previous_move < (1 / self.bps) * 1000:
            return
        ''' Now we can move '''

        self.previous_move = TIMER

        for i in range(len(self.carriages)):
            rot = game.rails[self.carriages[i].pos].rotate_train(self.carriages[i].rot)
            X = self.carriages[i].pos[0]
            Y = self.carriages[i].pos[1]
            if rot == 0:
                X += 1
            if rot == 1:
                Y += 1
            if rot == 2:
                X -= 1
            if rot == 3:
                Y -= 1
            self.carriages[i].pos = (X, Y)
            self.carriages[i].rot = rot

        game.stats.params['trains_travelled'] += 1

        return

class Shop_Helper:
    def __init__(self, shop_mode = False, section=0, pos=0, products=None, description=None):
        '''
        sections:
            0 -> rails
                pos = 0 -> straight
                pos = 1 -> turn
                pos = 2 -> T
                pos = 3 -> cross
            1 -> buildings
                pos = 0 -> coal mine
                pos = 1 -> iron mine
                pos = 2 -> sawmill
                pos = 3 -> seaport
                pos = 4 -> station
                pos = 5 -> storage
            2 -> carriages
                pos = 0 -> пассажирский
                pos = 1 -> самосвал (iron)
                pos = 2 -> полувагон (coal)
                pos = 3 -> платформа (wood)
                pos = 4 -> хоппер (crops)
                pos = 5 -> локомотив
            3 -> resources
                pos = 0 -> coal
                pos = 1 -> iron
                pos = 2 -> wood
                pos = 3 -> crops
        '''
        if products is None:
            products = [['rail_0', 'rail_1', 'rail_2', 'rail_3'],
                        ['coal_mine', 'iron_mine', 'sawmill', 'seaport', 'station', 'storage'],
                        ['car_0', 'car_1', 'car_2', 'car_3', 'car_4', 'car_5'],
                        ['coal', 'iron', 'wood', 'crops']]
        if description is None:
            description = {'rail_0' : "Прямой рельс перемещает поезда в том же направлении.",
                           'rail_1' : "Поворотный рельс позволяет повернуть поезд на 90 градусов.",
                           'rail_2' : "Т-образная развилка работает как прямой или как поворотный рельс.",
                           'rail_3' : "Перекрёсток пропускает поезда в одном из двух направлений.",
                           'coal_mine' : "Угольная шахта приносит уголь.",
                           'iron_mine' : "Железная шахта приносит железо.",
                           'sawmill' : "Лесопилка приносит доски.",
                           'seaport' : "Морской порт приносит еду.",
                           'station' : "На станции происходит посадка и выход пассажиров.",
                           'storage' : "На складе разгружаются вагоны с ресурсами.",
                           'car_0' : "Пассажирский вагон перевозит пассажиров.",
                           'car_1' : "Вагон-самосвал перевозит железо.",
                           'car_2' : "Полувагон перевозит уголь.",
                           'car_3' : "Вагон-платформа перевозит доски.",
                           'car_4' : "Вагон-хоппер перевозит еду.",
                           'car_5' : "Локомотив тянет за собой остальные вагоны.",
                           'coal' : "Уголь нужен для движения поездов.",
                           'iron' : "Железо используется при строительстве.",
                           'wood' : "Доски используются при строительстве.",
                           'crops' : "Еда нужна для перевозки пассажиров."}
        self.shop_mode = shop_mode
        self.section = section
        self.pos = pos
        self.products = products
        self.description = description

    def process_event(self, event):
        if game.build.build_mode or game.stats.stats_mode:
            return
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if not self.shop_mode:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.shop_mode = True
                self.section = 0
                self.pos = 0
                game.manager.state = -1
                game.manager.params['pos'] = (-100, -100)
                return
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                self.shop_mode = False
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.section = 0
                self.pos = 0
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                self.section = 1
                self.pos = 0
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                self.section = 2
                self.pos = 0
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                self.section = 3
                self.pos = 0
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.pos = (self.pos - 1) % len(self.products[self.section])
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.pos = (self.pos + 1) % len(self.products[self.section])
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                product_name = self.products[self.section][self.pos]
                IT = 1
                if keys[pygame.K_LSHIFT]:
                    IT = 10
                for _ in range(IT):
                    need_resources = game.resources_for_buildings[product_name]
                    accept = False
                    if game.lvl >= game.lvl_for_building[product_name] and all(game.resources[resource] >= need_resources[resource] for resource in need_resources):
                        accept = True
                    if accept:
                        for resource in need_resources:
                            game.resources[resource] -= need_resources[resource]
                        if product_name == 'coal_mine':
                            game.storage_buildings['coal_mine'] += 1
                            game.exp += 30
                        if product_name == 'iron_mine':
                            game.storage_buildings['iron_mine'] += 1
                            game.exp += 50
                        if product_name == 'sawmill':
                            game.storage_buildings['sawmill'] += 1
                            game.exp += 20
                        if product_name == 'seaport':
                            game.storage_buildings['seaport'] += 1
                            game.exp += 100
                        if product_name == 'station':
                            game.storage_buildings['station'] += 1
                            game.exp += 10
                        if product_name == 'storage':
                            game.storage_buildings['storage'] += 1
                            game.exp += 40
                        if product_name == 'rail_0':
                            game.storage_rails[0] += 1
                            game.exp += 2
                        if product_name == 'rail_1':
                            game.storage_rails[1] += 1
                            game.exp += 2
                        if product_name == 'rail_2':
                            game.storage_rails[2] += 1
                            game.exp += 2
                        if product_name == 'rail_3':
                            game.storage_rails[3] += 1
                            game.exp += 2
                        if product_name == 'car_0':
                            game.storage_carriages[0] += 1
                            game.exp += 5
                        if product_name == 'car_1':
                            game.storage_carriages[1] += 1
                            game.exp += 5
                        if product_name == 'car_2':
                            game.storage_carriages[2] += 1
                            game.exp += 5
                        if product_name == 'car_3':
                            game.storage_carriages[3] += 1
                            game.exp += 5
                        if product_name == 'car_4':
                            game.storage_carriages[4] += 1
                            game.exp += 5
                        if product_name == 'car_5':
                            game.storage_carriages[5] += 1
                            game.exp += 5
                        if product_name == 'coal':
                            game.resources['coal'] += 1
                        if product_name == 'iron':
                            game.resources['iron'] += 1
                        if product_name == 'wood':
                            game.resources['wood'] += 1
                        if product_name == 'crops':
                            game.resources['crops'] += 1
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                product_name = self.products[self.section][self.pos]
                IT = 1
                if keys[pygame.K_LSHIFT]:
                    IT = 10
                for _ in range(IT):
                    if product_name == 'coal_mine':
                        if game.storage_buildings['coal_mine'] >= 1:
                            game.storage_buildings['coal_mine'] -= 1
                            game.resources['money'] += 10
                    if product_name == 'iron_mine':
                        if game.storage_buildings['iron_mine'] >= 1:
                            game.storage_buildings['iron_mine'] -= 1
                            game.resources['money'] += 10
                    if product_name == 'sawmill':
                        if game.storage_buildings['sawmill'] >= 1:
                            game.storage_buildings['sawmill'] -= 1
                            game.resources['money'] += 5
                    if product_name == 'seaport':
                        if game.storage_buildings['seaport'] >= 1:
                            game.storage_buildings['seaport'] -= 1
                            game.resources['money'] += 25
                    if product_name == 'station':
                        if game.storage_buildings['station'] >= 1:
                            game.storage_buildings['station'] -= 1
                            game.resources['money'] += 20
                    if product_name == 'storage':
                        if game.storage_buildings['storage'] >= 1:
                            game.storage_buildings['storage'] -= 1
                            game.resources['money'] += 25
                    if product_name == 'rail_0':
                        if game.storage_rails[0] >= 1:
                            game.storage_rails[0] -= 1
                            game.resources['money'] += 2
                    if product_name == 'rail_1':
                        if game.storage_rails[1] >= 1:
                            game.storage_rails[1] -= 1
                            game.resources['money'] += 3
                    if product_name == 'rail_2':
                        if game.storage_rails[2] >= 1:
                            game.storage_rails[2] -= 1
                            game.resources['money'] += 5
                    if product_name == 'rail_3':
                        if game.storage_rails[3] >= 1:
                            game.storage_rails[3] -= 1
                            game.resources['money'] += 6
                    if product_name == 'car_0':
                        if game.storage_carriages[0] >= 1:
                            game.storage_carriages[0] -= 1
                            game.resources['money'] += 15
                    if product_name == 'car_1':
                        if game.storage_carriages[1] >= 1:
                            game.storage_carriages[1] -= 1
                            game.resources['money'] += 7
                    if product_name == 'car_2':
                        if game.storage_carriages[2] >= 1:
                            game.storage_carriages[2] -= 1
                            game.resources['money'] += 5
                    if product_name == 'car_3':
                        if game.storage_carriages[3] >= 1:
                            game.storage_carriages[3] -= 1
                            game.resources['money'] += 5
                    if product_name == 'car_4':
                        if game.storage_carriages[4] >= 1:
                            game.storage_carriages[4] -= 1
                            game.resources['money'] += 10
                    if product_name == 'car_5':
                        if game.storage_carriages[5] >= 1:
                            game.storage_carriages[5] -= 1
                            game.resources['money'] += 25
                    if product_name == 'coal':
                        if game.resources['coal'] >= 1:
                            game.resources['coal'] -= 1
                            game.resources['money'] += 1
                    if product_name == 'iron':
                        if game.resources['iron'] >= 1:
                            game.resources['iron'] -= 1
                            game.resources['money'] += 1
                    if product_name == 'wood':
                        if game.resources['wood'] >= 1:
                            game.resources['wood'] -= 1
                            game.resources['money'] += 1
                    if product_name == 'crops':
                        if game.resources['crops'] >= 1:
                            game.resources['crops'] -= 1
                            game.resources['money'] += 2
                return
    def get_source(self):
        source = ""
        if self.section == 0:
            source = f"rail_{self.pos}_0.png"
        if self.section == 1:
            source = f"building_{self.products[self.section][self.pos]}.png"
        if self.section == 2:
            source = f"carriage_{self.pos}.png"
        if self.section == 3:
            source = f"icon_{self.products[self.section][self.pos]}.png"
        return source

    def draw(self, screen):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if not self.shop_mode:
            return

        img = load_image("shop_bg.png")
        img = pygame.transform.scale(img, (1300, 900))
        img_rect = img.get_rect(topleft=(0,0))
        screen.blit(img, img_rect)

        for i in range(4):
            pygame.draw.rect(screen, (193,147,117), (60+310*i, 80, 250,100))
            pygame.draw.rect(screen, (90,54,39), (60+310*i, 80, 250, 100), 6)
            color = (0,0,0)
            if i == self.section:
                color = (100, 255, 100)
            draw_text(screen, ["РЕЛЬСЫ", "ЗДАНИЯ", "ВАГОНЫ", "РЕСУРСЫ"][i], pygame.font.SysFont('malgungothic', 40), True, color, None, 185+310*i, 130, 0, 0)


            flag = False
            if (i == 0 and keys[pygame.K_1]):
                flag = True
            if (i == 1 and keys[pygame.K_2]):
                flag = True
            if (i == 2 and keys[pygame.K_3]):
                flag = True
            if (i == 3 and keys[pygame.K_4]):
                flag = True
            if not flag:
                pygame.draw.circle(screen, (193, 147, 117), (185+310*i, 40), 25)
            else:
                pygame.draw.circle(screen, (100, 255, 100), (185 + 310 * i, 40), 25)
            pygame.draw.circle(screen, (90, 54, 39), (185 + 310 * i, 40), 25, 6)
            draw_text(screen, f"{i + 1}", pygame.font.SysFont('malgungothic', 25), True, (0, 0, 0), None, 185 + 310 * i, 37, 0, 0)

        self.pos = (self.pos - 1) % len(self.products[self.section])
        source1 = self.get_source()
        self.pos = (self.pos + 1) % len(self.products[self.section])
        source2 = self.get_source()
        self.pos = (self.pos + 1) % len(self.products[self.section])
        source3 = self.get_source()
        self.pos = (self.pos - 1) % len(self.products[self.section])

        img = load_image(source1)
        img = pygame.transform.scale(img, (200, 200))
        img_rect = img.get_rect(topleft=(240,280))
        screen.blit(img, img_rect)
        pygame.draw.rect(screen, (90,54,39), (240,280,200,200), 6)
        if keys[pygame.K_a]:
            pygame.draw.circle(screen, (100, 255, 100), (340, 240), 25)
        else:
            pygame.draw.circle(screen, (193, 147, 117), (340, 240), 25)
        pygame.draw.circle(screen, (90, 54, 39), (340, 240), 25, 6)
        draw_text(screen, f"A", pygame.font.SysFont('malgungothic', 25), True, (0, 0, 0), None, 340, 237, 0, 0)

        need_lvl = game.lvl_for_building[self.products[self.section][(self.pos - 1) % len(self.products[self.section])]]
        if game.lvl < need_lvl:
            img = load_image('lock.png', -1)
            img = pygame.transform.scale(img, (100, 100))
            img_rect = img.get_rect(center=(340, 380))
            screen.blit(img, img_rect)
            draw_text(screen, f"{need_lvl}", pygame.font.SysFont('malgungothic', 25), True, (0, 0, 0), None, 340, 390, 0, 0)

        img = load_image(source2)
        img = pygame.transform.scale(img, (200, 200))
        img_rect = img.get_rect(topleft=(550, 280))
        screen.blit(img, img_rect)
        pygame.draw.rect(screen, (90, 54, 39), (550, 280, 200, 200), 6)

        need_lvl = game.lvl_for_building[self.products[self.section][(self.pos) % len(self.products[self.section])]]
        if game.lvl < need_lvl:
            img = load_image('lock.png', -1)
            img = pygame.transform.scale(img, (100, 100))
            img_rect = img.get_rect(center=(650, 380))
            screen.blit(img, img_rect)
            draw_text(screen, f"{need_lvl}", pygame.font.SysFont('malgungothic', 25), True, (0, 0, 0), None, 650, 390, 0, 0)

        img = load_image(source3)
        img = pygame.transform.scale(img, (200, 200))
        img_rect = img.get_rect(topleft=(860, 280))
        screen.blit(img, img_rect)
        pygame.draw.rect(screen, (90, 54, 39), (860, 280, 200, 200), 6)
        if keys[pygame.K_d]:
            pygame.draw.circle(screen, (100, 255, 100), (960, 240), 25)
        else:
            pygame.draw.circle(screen, (193, 147, 117), (960, 240), 25)
        pygame.draw.circle(screen, (90, 54, 39), (960, 240), 25, 6)
        draw_text(screen, f"D", pygame.font.SysFont('malgungothic', 25), True, (0, 0, 0), None, 960, 237, 0, 0)

        need_lvl = game.lvl_for_building[self.products[self.section][(self.pos + 1) % len(self.products[self.section])]]
        if game.lvl < need_lvl:
            img = load_image('lock.png', -1)
            img = pygame.transform.scale(img, (100, 100))
            img_rect = img.get_rect(center=(960, 380))
            screen.blit(img, img_rect)
            draw_text(screen, f"{need_lvl}", pygame.font.SysFont('malgungothic', 25), True, (0, 0, 0), None, 960, 390, 0, 0)

        product_name = self.products[self.section][self.pos]
        need_resources = list(game.resources_for_buildings[product_name].items())

        pygame.draw.rect(screen, (193, 147, 117), (60, 500, 1180, 80))
        pygame.draw.rect(screen, (90, 54, 39), (60, 500, 1180, 80), 6)

        draw_text(screen, f"{self.description[product_name]}", pygame.font.SysFont('malgungothic', 25), True, (0, 0, 0), None, 650, 537, 0, 0)

        pygame.draw.rect(screen, (193, 147, 117), (60, 600, 560, 290))
        pygame.draw.rect(screen, (90, 54, 39), (60, 600, 560, 290), 6)
        draw_text(screen, f"Купить (ENTER), x10 - SHIFT", pygame.font.SysFont('malgungothic', 25), True, (0,0,0), None, 340, 620, 0, 0)

        pygame.draw.line(screen, (90, 54, 30), (340, 650), (340, 840), 6)

        for i in range(len(need_resources)):
            res = need_resources[i]
            img = load_image(f"icon_{res[0]}.png")
            img = pygame.transform.scale(img, (60, 60))
            img_rect = img.get_rect(topleft=(80, 650+70*i))
            screen.blit(img, img_rect)

            color = (255, 0, 0)
            if game.resources[res[0]] >= res[1]:
                color = (100, 255, 100)
            draw_text(screen, f"{game.resources[res[0]]}/{res[1]}", pygame.font.SysFont('malgungothic', 30), True, color, None, 150, 677+70*i, -1, 0)

        img = load_image(source2)
        img = pygame.transform.scale(img, (60, 60))
        img_rect = img.get_rect(topleft=(360, 650))
        screen.blit(img, img_rect)
        draw_text(screen, f"x1", pygame.font.SysFont('malgungothic', 30), True, (0,0,0), None, 430, 677, -1, 0)

        pygame.draw.rect(screen, (193, 147, 117), (680, 600, 560, 290))
        pygame.draw.rect(screen, (90, 54, 39), (680, 600, 560, 290), 6)
        draw_text(screen, f"Продать (BACKSPACE), x10 - SHIFT", pygame.font.SysFont('malgungothic', 25), True, (0, 0, 0), None, 960, 620, 0, 0)

        pygame.draw.line(screen, (90, 54, 30), (960, 650), (960, 840), 6)

        img = load_image(source2)
        img = pygame.transform.scale(img, (60, 60))
        img_rect = img.get_rect(topleft=(700, 650))
        screen.blit(img, img_rect)
        N = 0
        if product_name in ['coal_mine', 'iron_mine', 'sawmill', 'seaport', 'station', 'storage']:
            N = game.storage_buildings[product_name]
        if product_name in ['rail_0', 'rail_1', 'rail_2', 'rail_3']:
            N = game.storage_rails[int(product_name[-1])]
        if product_name in ['car_0', 'car_1', 'car_2', 'car_3', 'car_4', 'car_5']:
            N = game.storage_carriages[int(product_name[-1])]
        if product_name in ['coal', 'iron', 'wood', 'crops']:
            N = game.resources[product_name]
        color = (255, 0, 0)
        if N >= 1:
            color = (100, 255, 100)
        draw_text(screen, f"{N}/1", pygame.font.SysFont('malgungothic', 30), True, color, None, 770, 677, -1, 0)

        img = load_image('icon_money.png')
        img = pygame.transform.scale(img, (60, 60))
        img_rect = img.get_rect(topleft=(980, 650))
        screen.blit(img, img_rect)

        draw_text(screen, f"x{game.resources_for_buildings[product_name]['money']//2}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 1050, 677, -1, 0)

        return

class Stats_Helper:
    def __init__(self, stats_mode=False, params=None):
        if params is None:
            params = {'rails_placed' : 0,
                      'coal_earned' : 0,
                      'iron_earned' : 0,
                      'wood_earned' : 0,
                      'crops_earned' : 0,
                      'passengers_collected' : 0,
                      'game_completed_time' : '--:--',
                      'trains_travelled' : 0}
        self.stats_mode = stats_mode
        self.params = params
    def process_event(self, event):
        if game.build.build_mode or game.shop.shop_mode:
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_m:
            self.stats_mode = not self.stats_mode
            if self.stats_mode:
                game.manager.state = -1
                game.manager.params['pos'] = (-100, -100)
            return
    def draw(self, screen):
        if not self.stats_mode:
            return
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        img = load_image("load_bg.png")
        img = pygame.transform.scale(img, (1300, 900))
        img_rect = img.get_rect(topleft=(0, 0))
        screen.blit(img, img_rect)

        pygame.draw.rect(screen, (193, 147, 117), (50, 50, 1200, 500))
        pygame.draw.rect(screen, (90, 54, 39), (50, 50, 1200, 500), 6)

        draw_text(screen, f"Статистика", pygame.font.SysFont('malgungothic', 70), True, (0, 0, 0), None, 650, 100, 0, 0)
        draw_text(screen, f"Рельсов поставлено: {self.params['rails_placed']}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 170, -1, 0)
        draw_text(screen, f"Блоков пройдено поездами: {self.params['trains_travelled']}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 210, -1, 0)
        draw_text(screen, f"Перевезено пассажиров: {self.params['passengers_collected']}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 250, -1, 0)
        draw_text(screen, f"Загружено угля: {self.params['coal_earned']}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 290, -1, 0)
        draw_text(screen, f"Загружено железа: {self.params['iron_earned']}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 330, -1, 0)
        draw_text(screen, f"Загружено досок: {self.params['wood_earned']}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 370, -1, 0)
        draw_text(screen, f"Загружено еды: {self.params['crops_earned']}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 410, -1, 0)

        draw_text(screen, f"Игра пройдена за {self.params['game_completed_time']}", pygame.font.SysFont('malgungothic', 50), True, (0, 0, 0), None, 70, 490, -1, 0)

class Build_Helper:
    def __init__(self, build_mode=False, section=0, pos=0):
        self.build_mode = build_mode
        self.section = section
        self.pos = pos
    def process_event(self, event):
        if game.shop.shop_mode or game.stats.stats_mode:
            return
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if not self.build_mode:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.build_mode = True
                self.section = 0
                self.pos = 0
                game.manager.state = -1
                game.manager.params['pos'] = (-100, -100)
                return
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_b:
                self.build_mode = False
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                self.section = 0
                self.pos = 0
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                self.section = 1
                self.pos = 0
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                self.section = 2
                self.pos = 0
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                self.pos = (self.pos - 1) % len(game.shop.products[self.section])
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                self.pos = (self.pos + 1) % len(game.shop.products[self.section])
                return
            if event.type == pygame.MOUSEBUTTONDOWN:
                X, Y = mouse_pos[0]//100+game.dx, mouse_pos[1]//100+game.dy
                if self.section == 0:
                    if self.pos == 0:
                        if game.get_biome((X,Y)) == 'plain' and game.storage_rails[0]>=1 and (X,Y) not in game.rails and (X,Y) not in game.buildings and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            game.rails[(X,Y)] = Rail(pos=(X,Y), type=0, rotation=0)
                            game.storage_rails[0] -= 1
                            game.stats.params['rails_placed'] += 1
                    if self.pos == 1:
                        if game.get_biome((X,Y)) == 'plain' and game.storage_rails[1]>=1 and (X,Y) not in game.rails and (X,Y) not in game.buildings and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            game.rails[(X,Y)] = Rail(pos=(X,Y), type=1, rotation=0)
                            game.storage_rails[1] -= 1
                            game.stats.params['rails_placed'] += 1
                    if self.pos == 2:
                        if game.get_biome((X,Y)) == 'plain' and game.storage_rails[2]>=1 and (X,Y) not in game.rails and (X,Y) not in game.buildings and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            game.rails[(X,Y)] = Rail(pos=(X,Y), type=2, rotation=0)
                            game.storage_rails[2] -= 1
                            game.stats.params['rails_placed'] += 1
                    if self.pos == 3:
                        if game.get_biome((X,Y)) == 'plain' and game.storage_rails[3]>=1 and (X,Y) not in game.rails and (X,Y) not in game.buildings and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            game.rails[(X,Y)] = Rail(pos=(X,Y), type=3, rotation=0)
                            game.storage_rails[3] -= 1
                            game.stats.params['rails_placed'] += 1
                if self.section == 1:
                    if self.pos == 0:
                        if game.get_biome((X,Y)) == 'mountains' and game.storage_buildings['coal_mine']>=1 and (X,Y) not in game.rails and (X,Y) not in game.buildings and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            game.buildings[(X,Y)] = Coal_Mine()
                            game.storage_buildings['coal_mine'] -= 1
                    if self.pos == 1:
                        if game.get_biome((X,Y)) == 'mountains' and game.storage_buildings['iron_mine']>=1 and (X,Y) not in game.rails and (X,Y) not in game.buildings and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            game.buildings[(X,Y)] = Iron_Mine()
                            game.storage_buildings['iron_mine'] -= 1
                    if self.pos == 2:
                        if game.get_biome((X,Y)) == 'forest' and game.storage_buildings['sawmill']>=1 and (X,Y) not in game.rails and (X,Y) not in game.buildings and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            game.buildings[(X,Y)] = Sawmill()
                            game.storage_buildings['sawmill'] -= 1
                    if self.pos == 3:
                        if game.get_biome((X,Y)) == 'sea' and game.storage_buildings['seaport']>=1 and (X,Y) not in game.rails and (X,Y) not in game.buildings and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            game.buildings[(X,Y)] = Seaport()
                            game.storage_buildings['seaport'] -= 1
                    if self.pos == 4:
                        if game.get_biome((X,Y)) == 'plain' and game.storage_buildings['station']>=1 and (X,Y) not in game.rails and (X,Y) not in game.buildings and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            game.buildings[(X,Y)] = Station()
                            game.storage_buildings['station'] -= 1
                    if self.pos == 5:
                        if game.get_biome((X,Y)) == 'plain' and game.storage_buildings['storage']>=1 and (X,Y) not in game.rails and (X,Y) not in game.buildings and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            game.buildings[(X,Y)] = Storage()
                            game.storage_buildings['storage'] -= 1
                if self.section == 2:
                    if self.pos == 0:
                        if (X,Y) in game.rails and game.storage_carriages[0]>=1 and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            ok = False
                            for rot in range(4):
                                rot2 = game.rails[(X,Y)].rotate_train(rot)
                                X1 = X
                                Y1 = Y
                                if rot2 == 0:
                                    X1 += 1
                                if rot2 == 1:
                                    Y1 += 1
                                if rot2 == 2:
                                    X1 -= 1
                                if rot2 == 3:
                                    Y1 -= 1
                                for train in game.trains:
                                    if train.carriages[-1].pos == (X1, Y1) and train.carriages[-1].rot == rot2:
                                        train.carriages.append(Carriage(type=0,pos=(X,Y),rot=rot))
                                        game.storage_carriages[0] -= 1
                                        ok = True
                                        break
                                if ok:
                                    break
                    if self.pos == 1:
                        if (X,Y) in game.rails and game.storage_carriages[1]>=1 and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            ok = False
                            for rot in range(4):
                                rot2 = game.rails[(X,Y)].rotate_train(rot)
                                X1 = X
                                Y1 = Y
                                if rot2 == 0:
                                    X1 += 1
                                if rot2 == 1:
                                    Y1 += 1
                                if rot2 == 2:
                                    X1 -= 1
                                if rot2 == 3:
                                    Y1 -= 1
                                for train in game.trains:
                                    if train.carriages[-1].pos == (X1, Y1) and train.carriages[-1].rot == rot2:
                                        train.carriages.append(Carriage(type=1,pos=(X,Y),rot=rot))
                                        game.storage_carriages[1] -= 1
                                        ok = True
                                        break
                                if ok:
                                    break
                    if self.pos == 2:
                        if (X,Y) in game.rails and game.storage_carriages[2]>=1 and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            ok = False
                            for rot in range(4):
                                rot2 = game.rails[(X,Y)].rotate_train(rot)
                                X1 = X
                                Y1 = Y
                                if rot2 == 0:
                                    X1 += 1
                                if rot2 == 1:
                                    Y1 += 1
                                if rot2 == 2:
                                    X1 -= 1
                                if rot2 == 3:
                                    Y1 -= 1
                                for train in game.trains:
                                    if train.carriages[-1].pos == (X1, Y1) and train.carriages[-1].rot == rot2:
                                        train.carriages.append(Carriage(type=2,pos=(X,Y),rot=rot))
                                        game.storage_carriages[2] -= 1
                                        ok = True
                                        break
                                if ok:
                                    break
                    if self.pos == 3:
                        if (X,Y) in game.rails and game.storage_carriages[3]>=1 and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            ok = False
                            for rot in range(4):
                                rot2 = game.rails[(X,Y)].rotate_train(rot)
                                X1 = X
                                Y1 = Y
                                if rot2 == 0:
                                    X1 += 1
                                if rot2 == 1:
                                    Y1 += 1
                                if rot2 == 2:
                                    X1 -= 1
                                if rot2 == 3:
                                    Y1 -= 1
                                for train in game.trains:
                                    if train.carriages[-1].pos == (X1, Y1) and train.carriages[-1].rot == rot2:
                                        train.carriages.append(Carriage(type=3,pos=(X,Y),rot=rot))
                                        game.storage_carriages[3] -= 1
                                        ok = True
                                        break
                                if ok:
                                    break
                    if self.pos == 4:
                        if (X,Y) in game.rails and game.storage_carriages[4]>=1 and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            ok = False
                            for rot in range(4):
                                rot2 = game.rails[(X,Y)].rotate_train(rot)
                                X1 = X
                                Y1 = Y
                                if rot2 == 0:
                                    X1 += 1
                                if rot2 == 1:
                                    Y1 += 1
                                if rot2 == 2:
                                    X1 -= 1
                                if rot2 == 3:
                                    Y1 -= 1
                                for train in game.trains:
                                    if train.carriages[-1].pos == (X1, Y1) and train.carriages[-1].rot == rot2:
                                        train.carriages.append(Carriage(type=4,pos=(X,Y),rot=rot))
                                        game.storage_carriages[4] -= 1
                                        ok = True
                                        break
                                if ok:
                                    break
                    if self.pos == 5:
                        if (X,Y) in game.rails and game.storage_carriages[5]>=1 and not any(any(car.pos == (X,Y) for car in train.carriages) for train in game.trains):
                            for rot in [0, 3, 2, 1]:
                                if game.rails[(X,Y)].rotate_train(rot) != -1:
                                    game.trains.append(Train(carriages=[Carriage(type=5, pos=(X,Y), rot=rot)]))
                                    game.storage_carriages[5] -= 1
                                    break


    def get_source(self, i, j):
        source = ""
        if i == 0:
            source = f"rail_{j}_0.png"
        if i == 1:
            source = f"building_{game.shop.products[i][j]}.png"
        if i == 2:
            source = f"carriage_{j}.png"
        if i == 3:
            source = f"icon_{game.shop.products[i][j]}.png"
        return source

    def draw(self, screen):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if not self.build_mode:
            return
        pygame.draw.rect(screen, (193, 147, 117), (15, 730, len(game.shop.products[self.section])*130, 160))
        pygame.draw.rect(screen, (90,54,39), (15, 730, len(game.shop.products[self.section]) * 130, 160), 6)
        for i in range(len(game.shop.products[self.section])):
            img = load_image(self.get_source(self.section, i))
            img = pygame.transform.scale(img, (100, 100))
            img_rect = img.get_rect(topleft=(30+130*i, 750))
            screen.blit(img, img_rect)
            #draw_text(screen, f"x1", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 430, 677, -1, 0)

            #pygame.draw.rect(screen, (193, 147, 117), (680, 600, 560, 290))
            if i == self.pos:
                color = (100, 255, 100)
                pygame.draw.rect(screen, color, (30 + 130 * i, 750, 100, 100), 6)
            N = 0
            if self.section == 0:
                N = game.storage_rails[i]
            if self.section == 1:
                N = game.storage_buildings[game.shop.products[self.section][i]]
            if self.section == 2:
                N = game.storage_carriages[i]
            color = (255, 0, 0)
            if N > 0:
                color = (100, 255, 100)

            draw_text(screen, f"x{N}", pygame.font.SysFont('malgungothic', 25), True, color, None, 125+130*i, 865, 1, 0)
        X = mouse_pos[0]//100
        Y = mouse_pos[1]//100
        img = load_image(self.get_source(self.section, self.pos))
        img = pygame.transform.scale(img, (100, 100))
        img_rect = img.get_rect(topleft=(X*100,Y*100))
        screen.blit(img, img_rect)

class Manager:
    def __init__(self, state=-1, params=None):
        if params is None:
            params = {}
        self.state = state
        self.params = params
        '''
        states:
            -1 -> manager is off
            0 -> empty cell picked
            1 -> building picked
            2 -> rail picked
            3 -> train picked
        '''
    def process_event(self, event):
        if game.build.build_mode or game.shop.shop_mode or game.stats.stats_mode:
            return
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        X, Y = mouse_pos[0]//100 + game.dx, mouse_pos[1]//100 + game.dy
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.state = -1
            self.params['pos'] = (-100, -100)
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if ('pos' in self.params) and (X, Y) == self.params['pos']:
                self.state = -1
                self.params['pos'] = (-100, -100)
                return
            else:
                for t in range(len(game.trains)):
                    for c in range(len(game.trains[t].carriages)):
                        if game.trains[t].carriages[c].pos == (X, Y):
                            self.state = 3
                            self.params = {'train': t, 'carriage': c}
                            return
                if (X, Y) in game.buildings:
                    self.state = 1
                    self.params = {'pos': (X, Y)}
                    return
                if (X, Y) in game.rails:
                    self.state = 2
                    self.params = {'pos': (X, Y)}
                    return
                self.state = 0
                self.params = {'pos': (X, Y)}
                return
        if self.state == -1:
            return
        if self.state == 0:
            return
        if self.state == 1:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                b = game.buildings.pop(self.params['pos'])
                if type(b) == Coal_Mine:
                    game.storage_buildings['coal_mine'] += 1
                if type(b) == Iron_Mine:
                    game.storage_buildings['iron_mine'] += 1
                if type(b) == Sawmill:
                    game.storage_buildings['sawmill'] += 1
                if type(b) == Seaport:
                    game.storage_buildings['seaport'] += 1
                if type(b) == Station:
                    game.storage_buildings['station'] += 1
                if type(b) == Storage:
                    game.storage_buildings['storage'] += 1
                self.state = -1
                self.params['pos'] = (-100, -100)
            return
        if self.state == 2:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                if not any(any(c.pos == self.params['pos'] for c in t.carriages) for t in game.trains):
                    game.rails[self.params['pos']].rotate()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LSHIFT:
                if not any(any(c.pos == self.params['pos'] for c in t.carriages) for t in game.trains):
                    game.rails[self.params['pos']].change_state()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                if not any(any(c.pos == self.params['pos'] for c in t.carriages) for t in game.trains):
                    r = game.rails.pop(self.params['pos'])
                    game.storage_rails[r.type] += 1
                    self.state = -1
                    self.params['pos'] = (-100, -100)
            return
        if self.state == 3:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                if self.params['carriage'] < len(game.trains[self.params['train']].carriages) - 1:
                    self.params['carriage'] += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                if self.params['carriage'] > 0:
                    self.params['carriage'] -= 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                IT = 1
                if keys[pygame.K_LSHIFT]:
                    IT = 10
                for i in range(IT):
                    t = game.trains[self.params['train']]
                    c = t.carriages[self.params['carriage']]
                    if c.type == 0:
                        if game.resources['crops'] >= 1 and c.food < c.food_capacity:
                            game.resources['crops'] -= 1
                            c.food += 1
                    if c.type == 5:
                        if game.resources['coal'] >= 1 and t.coal < t.coal_capacity:
                            game.resources['coal'] -= 1
                            t.coal += 1
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                t = game.trains[self.params['train']]
                c = t.carriages[self.params['carriage']]
                if c.type == 5:
                    t.engine = not t.engine
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                t = game.trains[self.params['train']]
                c_num = self.params['carriage']
                while len(t.carriages) > c_num:
                    c = t.carriages.pop()
                    game.storage_carriages[c.type] += 1
                if len(t.carriages) == 0:
                    game.trains.pop(self.params['train'])
                self.state = -1
                self.params['pos'] = (-100, -100)
            return

    def draw(self, screen):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if self.state == -1:
            return
        pygame.draw.rect(screen, (193, 147, 117), (890, 10, 390, 300))
        pygame.draw.rect(screen, (90, 54, 39), (890, 10, 390, 300), 6)
        draw_text(screen, f"INFO", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 30, -1, 0)
        if self.state == 0:
            pygame.draw.rect(screen, (100,255,100), ((self.params['pos'][0]-game.dx)*100, (self.params['pos'][1]-game.dy)*100, 100, 100), 3)
            draw_text(screen, f"Биом: {game.get_biome(self.params['pos'])}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 70, -1, 0)
            return
        if self.state == 2:
            pygame.draw.rect(screen, (100, 255, 100), ((self.params['pos'][0] - game.dx) * 100, (self.params['pos'][1] - game.dy) * 100, 100, 100), 3)
            draw_text(screen, f"Биом: {game.get_biome(self.params['pos'])}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 70, -1, 0)
            rail = ["прямой", "поворотный", "развилка", "перекрёсток"][game.rails[self.params['pos']].type]
            draw_text(screen, f"Рельс: {rail}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 110, -1, 0)
            draw_text(screen, f"Направление (R): {game.rails[self.params['pos']].rotation}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 150, -1, 0)
            if game.rails[self.params['pos']].type in [2, 3]:
                draw_text(screen, f"Состояние (SHIFT): {game.rails[self.params['pos']].state}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 190, -1, 0)
            return
        if self.state == 1:
            pygame.draw.rect(screen, (100, 255, 100), ((self.params['pos'][0] - game.dx) * 100, (self.params['pos'][1] - game.dy) * 100, 100, 100), 3)
            draw_text(screen, f"Биом: {game.get_biome(self.params['pos'])}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 70, -1, 0)
            b = game.buildings[self.params['pos']]
            b_name = ""
            if type(b) == Coal_Mine:
                b_name = "Угольная шахта"
            if type(b) == Iron_Mine:
                b_name = "Железная шахта"
            if type(b) == Sawmill:
                b_name = "Лесопилка"
            if type(b) == Seaport:
                b_name = "Морской порт"
            if type(b) == Station:
                b_name = "Станция"
            if type(b) == Storage:
                b_name = "Склад"
            draw_text(screen, f"Здание: {b_name}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 110, -1, 0)
            if type(b) == Station:
                draw_text(screen, f"Название:", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 190, -1, 0)
                draw_text(screen, f"{b.name}", pygame.font.SysFont('malgungothic', 30, bold=True), True, (0, 0, 0), None, 900, 230, -1, 0)
            return
        if self.state == 3:
            t = game.trains[self.params['train']]
            c = t.carriages[self.params['carriage']]
            pygame.draw.rect(screen, (100, 255, 100), ((c.pos[0] - game.dx) * 100, (c.pos[1] - game.dy) * 100, 100, 100), 3)
            draw_text(screen, f"Паровоз: {t.name}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 70, -1, 0)
            draw_text(screen, f"Вагон: {self.params['carriage']} ({['пассажирский', 'самосвал', 'полувагон', 'платформа', 'хоппер', 'локомотив'][c.type]})", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 110, -1, 0)
            if c.type == 0:
                draw_text(screen, f"Пассажиры: {c.full} / {c.capacity}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 150, -1, 0)
                draw_text(screen, f"Еда (ENTER): {c.food} / {c.food_capacity}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 190, -1, 0)
            if c.type == 5:
                draw_text(screen, f"Уголь (ENTER): {t.coal} / {t.coal_capacity}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 150, -1, 0)
                draw_text(screen, f"Двигатель (E): {'ВКЛ' if t.engine else 'ВЫКЛ'}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 190, -1, 0)
            if c.type in [1, 2, 3, 4]:
                draw_text(screen, f"Наполнение: {c.full} / {c.capacity}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 900, 150, -1, 0)

class Game_Controller:
    def __init__(self, mp=(650, 450), pos=(0,0)):
        self.mp = mp
        self.pos = pos
    def process_event(self, TICK_SPEED):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if game.shop.shop_mode:
            return
        if keys[pygame.K_LCTRL]:
            dx = mouse_pos[0] - self.mp[0]
            dy = mouse_pos[1] - self.mp[1]
            d = (dx**2 + dy**2)**0.5
            X = self.pos[0] + dx * 0.01 * TICK_SPEED / 1000
            Y = self.pos[1] + dy * 0.01 * TICK_SPEED / 1000
            self.pos = (X,Y)
            game.dx = int(self.pos[0])
            game.dy = int(self.pos[1])

    def draw(self, screen):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if not keys[pygame.K_LCTRL]:
            return
        pygame.draw.circle(screen, (255, 0, 0), self.mp, 10)
        pygame.draw.line(screen, (255, 0, 0), self.mp, mouse_pos, 2)

class Loading_Screen:
    def __init__(self, state=0, params=None, cd=100, pr=0):
        if params is None:
            params = {'perc': 0, 'tomas' : 0}
        self.state = state
        self.params = params
        self.cd = cd
        self.pr = pr
    def process_event(self, event):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if self.state == 0:
            if event.type == TICK:
                if TIMER - self.pr >= self.cd:
                    self.pr = TIMER
                    self.params['perc'] += random.random() * 1.5
                    self.params['tomas'] = (self.params['tomas'] + 1) % 8
                    if self.params['perc'] >= 100:
                        self.state = 1
            return
        if self.state == 1:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 350 <= mouse_pos[0] <= 950 and 230 <= mouse_pos[1] <= 350:
                    self.state = 4
                if 350 <= mouse_pos[0] <= 950 and 390 <= mouse_pos[1] <= 510:
                    self.state = 2
                if 350 <= mouse_pos[0] <= 950 and 550 <= mouse_pos[1] <= 670:
                    self.state = 3
                return
        if self.state == 3:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 570 <= mouse_pos[0] <= 730 and 205 <= mouse_pos[1] <= 255:
                    self.state = 1
                if 50 <= mouse_pos[0] <= 1250 and 95 <= mouse_pos[1] <= 125:
                    webbrowser.open('https://vk.com/id309167010', new=2)
                if 50 <= mouse_pos[0] <= 1250 and 135 <= mouse_pos[1] <= 165:
                    webbrowser.open('https://vk.com/lesssense', new=2)
                return
        if self.state == 2:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 570 <= mouse_pos[0] <= 730 and 445 <= mouse_pos[1] <= 495:
                    self.state = 1
                return

    def cut_sheet(self, sheet, columns, rows):
        rect = pygame.Rect(0, 0, sheet.get_width() // columns, sheet.get_height() // rows)
        i = 0
        j = self.params['tomas']
        return sheet.subsurface(pygame.Rect((rect.w * i, rect.h * j + 1), rect.size))

    def draw(self, screen):
        keys = pygame.key.get_pressed()
        mouse_pos = pygame.mouse.get_pos()
        if self.state == 0:
            img = load_image("load_bg.png")
            img = pygame.transform.scale(img, (1300, 900))
            img_rect = img.get_rect(topleft=(0, 0))
            screen.blit(img, img_rect)
            tomas = load_image("tomas.png", -1)
            img = self.cut_sheet(tomas, 1, 8)
            img_rect = img.get_rect(bottomleft=(int(50+(954-50)*self.params['perc']/100), 281))
            screen.blit(img, img_rect)

            pygame.draw.rect(screen, (193,147,117), (350,650,600,180))
            pygame.draw.rect(screen, (90,54,39), (350, 650, 600, 180), 6)
            draw_text(screen, f"Ж/Д ИМПЕРИЯ", pygame.font.SysFont('malgungothic', 70, bold=True), True, (0,0,0), None, 650, 700, 0, 0)
            draw_text(screen, f"{int(self.params['perc'])}%", pygame.font.SysFont('malgungothic', 50, bold=True), True, (0,0,0), None, 650, 780, 0, 0)
        if self.state == 1:
            img = load_image("load_bg.png")
            img = pygame.transform.scale(img, (1300, 900))
            img_rect = img.get_rect(topleft=(0, 0))
            screen.blit(img, img_rect)

            pygame.draw.rect(screen, (193, 147, 117), (350, 230, 600, 120))
            pygame.draw.rect(screen, (90, 54, 39), (350, 230, 600, 120), 6)
            color = (0,0,0)
            if 350 <= mouse_pos[0] <= 950 and 230 <= mouse_pos[1] <= 350:
                color = (100, 255, 100)
            draw_text(screen, f"Новая игра", pygame.font.SysFont('malgungothic', 70, bold=True), True, color, None, 650, 287, 0, 0)

            pygame.draw.rect(screen, (193, 147, 117), (350, 390, 600, 120))
            pygame.draw.rect(screen, (90, 54, 39), (350, 390, 600, 120), 6)
            color = (0, 0, 0)
            if 350 <= mouse_pos[0] <= 950 and 390 <= mouse_pos[1] <= 510:
                color = (100, 255, 100)
            draw_text(screen, f"Об игре", pygame.font.SysFont('malgungothic', 70, bold=True), True, color, None, 650, 447, 0, 0)

            pygame.draw.rect(screen, (193, 147, 117), (350, 550, 600, 120))
            pygame.draw.rect(screen, (90, 54, 39), (350, 550, 600, 120), 6)
            color = (0, 0, 0)
            if 350 <= mouse_pos[0] <= 950 and 550 <= mouse_pos[1] <= 670:
                color = (100, 255, 100)
            draw_text(screen, f"Ссылки", pygame.font.SysFont('malgungothic', 70, bold=True), True, color, None, 650, 607, 0, 0)
        if self.state == 3:
            img = load_image("load_bg.png")
            img = pygame.transform.scale(img, (1300, 900))
            img_rect = img.get_rect(topleft=(0, 0))
            screen.blit(img, img_rect)

            pygame.draw.rect(screen, (193, 147, 117), (50, 50, 1200, 210))
            pygame.draw.rect(screen, (90, 54, 39), (50, 50, 1200, 210), 6)

            draw_text(screen, f"Игра 'Ж/Д Империя' создана в рамках обучения в Яндекс.Лицее", pygame.font.SysFont('malgungothic', 30), True, (0,0,0), None, 70, 70, -1, 0)
            color = (0,0,0)
            if 50 <= mouse_pos[0] <= 1250 and 95 <= mouse_pos[1] <= 125:
                color = (100, 255, 100)
            draw_text(screen, f"Код: Евгений Уткин", pygame.font.SysFont('malgungothic', 30), True, color, None, 70, 110, -1, 0)
            color = (0, 0, 0)
            if 50 <= mouse_pos[0] <= 1250 and 135 <= mouse_pos[1] <= 165:
                color = (100, 255, 100)
            draw_text(screen, f"Дизайн: Елисавета Шелестова", pygame.font.SysFont('malgungothic', 30), True, color, None, 70, 150, -1, 0)
            draw_text(screen, f"© 2023", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 190, -1, 0)
            color = (0,0,0)
            if 570 <= mouse_pos[0] <= 730 and 205 <= mouse_pos[1] <= 255:
                color = (100, 255, 100)
            draw_text(screen, f"← назад", pygame.font.SysFont('malgungothic', 30), True, color, None, 650, 230, 0, 0)
        if self.state == 2:
            img = load_image("load_bg.png")
            img = pygame.transform.scale(img, (1300, 900))
            img_rect = img.get_rect(topleft=(0, 0))
            screen.blit(img, img_rect)

            pygame.draw.rect(screen, (193, 147, 117), (50, 50, 1200, 450))
            pygame.draw.rect(screen, (90, 54, 39), (50, 50, 1200, 450), 6)

            draw_text(screen, f"В игре вам предстоит развивать свою железнодорожную империю,", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 70, -1, 0)
            draw_text(screen, f"строя дороги, станции, порты, шахты и управляя поездами.", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 110, -1, 0)
            draw_text(screen, f"За каждое полезное действие начисляется опыт, цель игры - достичь 10 уровня.", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 150, -1, 0)
            draw_text(screen, f"Управление:", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 230, -1, 0)
            draw_text(screen, f"S - магазин", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 270, -1, 0)
            draw_text(screen, f"B - строительство", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 310, -1, 0)
            draw_text(screen, f"M - статистика", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 350, -1, 0)
            draw_text(screen, f"Escape - удаление объектов", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 390, -1, 0)
            draw_text(screen, f"Ctrl - перемещение по карте", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 70, 430, -1, 0)

            color = (0, 0, 0)
            if 570 <= mouse_pos[0] <= 730 and 445 <= mouse_pos[1] <= 495:
                color = (100, 255, 100)
            draw_text(screen, f"← назад", pygame.font.SysFont('malgungothic', 30), True, color, None, 650, 470, 0, 0)

class Game:
    def __init__(self, biomes=None, rails=None, buildings=None, trains=None,
                 resources=None,
                 storage_rails=None, storage_carriages=None, storage_buildings=None,
                 map='data\map_image.png', dx=0, dy=0,
                 resources_for_buildings=None,
                 buildings_on_biomes=None,
                 shop = Shop_Helper(), build = Build_Helper(), manager = Manager(), controller = Game_Controller(), load=Loading_Screen(), stats=Stats_Helper(),
                 required_exp=None, lvl=1, exp=0,
                 lvl_for_building=None):
        if required_exp is None:
            required_exp = [0, 100, 150, 200, 250, 300, 350, 400, 450, 500]
        if trains is None:
            trains = []
        if buildings is None:
            buildings = {}
        if rails is None:
            rails = {}
        if biomes is None:
            biomes = {}
        if storage_carriages is None:
            storage_carriages = {0: 1, 1: 0, 2: 0, 3: 0, 4: 0, 5: 1}
        if storage_rails is None:
            storage_rails = {0: 10, 1: 4, 2: 0, 3: 0}
        if storage_buildings is None:
            storage_buildings = {'coal_mine' : 0, 'iron_mine' : 0, 'sawmill' : 0, 'seaport' : 0, 'station' : 2, 'storage' : 0}
        if resources is None:
            resources = {'money': 100, 'iron': 0, 'coal': 0, 'wood': 0, 'crops': 0}
        if buildings_on_biomes is None:
            buildings_on_biomes = {'mountains': ['coal_mine', 'iron_mine'], 'forest': ['sawmill'], 'sea': ['seaport'],
                                   'plain': ['station', 'storage', 'rail']}
        if resources_for_buildings is None:
            resources_for_buildings = {'coal_mine': {'money': 20, 'wood': 10},
                                       'iron_mine': {'money': 20, 'wood': 5},
                                       'sawmill': {'money': 10},
                                       'seaport': {'money': 50, 'iron': 15, 'wood': 20},
                                       'station': {'money': 40, 'iron': 5, 'wood': 10},
                                       'storage' : {'money' : 50, 'wood' : 15},
                                       'rail_0': {'money': 5, 'iron': 2, 'wood': 2},
                                       'rail_1': {'money': 7, 'iron': 2, 'wood': 3},
                                       'rail_2': {'money': 10, 'iron': 5, 'wood': 5},
                                       'rail_3': {'money': 12, 'iron': 7, 'wood': 8},
                                       'car_0': {'money': 30, 'iron': 10, 'wood': 20},
                                       'car_1': {'money': 15, 'iron': 30, 'wood': 5},
                                       'car_2': {'money': 10, 'iron': 20, 'wood': 5},
                                       'car_3': {'money': 10, 'iron': 10, 'wood': 10},
                                       'car_4': {'money': 20, 'iron': 20, 'wood': 20},
                                       'car_5': {'money': 50, 'iron': 30, 'wood': 20},
                                       'coal' : {'money' : 3},
                                       'iron' : {'money' : 2},
                                       'wood' : {'money' : 2},
                                       'crops' : {'money' : 5}}
        if lvl_for_building is None:
            lvl_for_building = {'coal_mine': 3,
                                'iron_mine': 4,
                                'sawmill': 2,
                                'seaport': 7,
                                'station': 1,
                                'storage' : 2,
                                'rail_0': 1,
                                'rail_1': 1,
                                'rail_2': 2,
                                'rail_3': 2,
                                'car_0': 1,
                                'car_1': 4,
                                'car_2': 3,
                                'car_3': 2,
                                'car_4': 7,
                                'car_5': 1,
                                'coal' : 1,
                                'iron' : 1,
                                'wood' : 1,
                                'crops' : 1}
        self.biomes = biomes
        self.rails = rails
        self.buildings = buildings
        self.trains = trains
        self.resources = resources
        self.storage_rails = storage_rails
        self.storage_carriages = storage_carriages
        self.storage_buildings = storage_buildings
        self.resources_for_buildings = resources_for_buildings
        self.buildings_on_biomes = buildings_on_biomes
        self.shop = shop
        self.build = build
        self.manager = manager
        self.controller = controller
        self.load = load
        self.required_exp = required_exp
        self.lvl = lvl
        self.exp = exp
        self.lvl_for_building = lvl_for_building
        self.stats = stats

        im = Image.open(map)
        pixels = im.load()
        x, y = im.size
        self.map = pixels
        self.map_size = (x, y)

        self.dx = dx
        self.dy = dy


    def get_biome(self, pos):
        if not (0 <= pos[0] < self.map_size[0] and 0 <= pos[1] < self.map_size[1]):
            return "sea"
        r, g, b = self.map[pos[0], pos[1]]
        if (r == 0 and g == 162 and b == 232):
            return "sea"
        if (r == 181 and g == 230 and b == 29):
            return "plain"
        if (r == 34 and g == 177 and b == 76):
            return "forest"
        if (r == 195 and g == 195 and b == 195):
            return "mountains"
        return "ERROR"

    def process(self):
        for train in self.trains:
            train.process()
        if self.lvl <= 9 and self.exp >= self.required_exp[self.lvl]:
            self.exp -= self.required_exp[self.lvl]
            self.lvl += 1
            create_particles((650, 200))
            if self.lvl == 10:
                S = int(TIMER/1000) % 60
                M = int(TIMER/1000) // 60
                self.stats.params['game_completed_time'] = f"{M} мин {S} сек"
        all_sprites.update()

    def draw(self, screen):
        screen.fill((0,0,0))

        ''' draw shop '''
        if game.shop.shop_mode:
            game.shop.draw(screen)
            all_sprites.draw(screen)
            return

        ''' draw stats '''
        if game.stats.stats_mode:
            game.stats.draw(screen)
            all_sprites.draw(screen)
            return

        ''' draw biomes '''
        for x in range(13):
            for y in range(9):
                img = load_image(f'biome_{self.get_biome((x+self.dx, y+self.dy))}.png')
                img = pygame.transform.scale(img, (100, 100))
                img_rect = img.get_rect(center=(50 + 100*x, 50 + 100*y))
                screen.blit(img, img_rect)

        ''' draw rails '''
        for rail in game.rails:
            img = load_image(f'rail_{game.rails[rail].type}_{game.rails[rail].state}.png', -1)
            img = pygame.transform.rotate(img, -90 * game.rails[rail].rotation)
            img = pygame.transform.scale(img, (100, 100))
            img_rect = img.get_rect(center=(50 + (rail[0]-self.dx) * 100, 50 + (rail[1]-self.dy) * 100))
            screen.blit(img, img_rect)

        ''' draw buildings '''
        for b in game.buildings:
            name = "iron_mine"
            if type(game.buildings[b]) == Coal_Mine:
                name = "coal_mine"
            if type(game.buildings[b]) == Iron_Mine:
                name = "iron_mine"
            if type(game.buildings[b]) == Sawmill:
                name = "sawmill"
            if type(game.buildings[b]) == Seaport:
                name = "seaport"
            if type(game.buildings[b]) == Station:
                name = "station"
            if type(game.buildings[b]) == Storage:
                name = "storage"
            img = load_image(f'building_{name}.png')
            img = pygame.transform.scale(img, (100, 100))
            img_rect = img.get_rect(center=(50 + (b[0] - self.dx) * 100, 50 + (b[1] - self.dy) * 100))
            screen.blit(img, img_rect)

        ''' draw trains '''
        for train in self.trains:
            for carriage in train.carriages:
                img = load_image(f'carriage_{carriage.type}.png')
                img = pygame.transform.scale(img, (100, 100))
                img_rect = img.get_rect(center=(50 + (carriage.pos[0] - self.dx) * 100, 50 + (carriage.pos[1] - self.dy) * 100))
                screen.blit(img, img_rect)

                name = ""
                if carriage.type == 0:
                    name = "passenger"
                if carriage.type == 1:
                    name = "iron"
                if carriage.type == 2:
                    name = "coal"
                if carriage.type == 3:
                    name = "wood"
                if carriage.type == 4:
                    name = "crops"
                if name != "":
                    img = load_image(f'icon_{name}.png')
                    img = pygame.transform.scale(img, (30, 30))
                    img_rect = img.get_rect(center=(20 + (carriage.pos[0] - self.dx) * 100, 80 + (carriage.pos[1] - self.dy) * 100))
                    screen.blit(img, img_rect)

                    pygame.draw.rect(screen, (0,150,100), (40 + (carriage.pos[0] - self.dx) * 100, 70 + (carriage.pos[1] - self.dy) * 100, 55, 20))
                    pygame.draw.rect(screen, (0, 255, 100), (40 + (carriage.pos[0] - self.dx) * 100, 70 + (carriage.pos[1] - self.dy) * 100, int(55 * carriage.full / carriage.capacity), 20))
                    pygame.draw.rect(screen, (0,0,0), (40 + (carriage.pos[0] - self.dx) * 100, 70 + (carriage.pos[1] - self.dy) * 100, 55, 20), 1)

                    font = pygame.font.SysFont('malgungothic', 15)
                    text = font.render(f"{carriage.full}/{carriage.capacity}", True, (0, 0, 0))
                    place = text.get_rect(topleft=(45 + (carriage.pos[0] - self.dx) * 100, 68 + (carriage.pos[1] - self.dy) * 100))
                    screen.blit(text, place)
                    if carriage.type == 0:
                        img = load_image(f'icon_crops.png')
                        img = pygame.transform.scale(img, (30, 30))
                        img_rect = img.get_rect(center=(20 + (carriage.pos[0] - self.dx) * 100, 20 + (carriage.pos[1] - self.dy) * 100))
                        screen.blit(img, img_rect)

                        pygame.draw.rect(screen, (0, 150, 100), (
                        40 + (carriage.pos[0] - self.dx) * 100, 10 + (carriage.pos[1] - self.dy) * 100, 55, 20))
                        pygame.draw.rect(screen, (0, 255, 100), (
                        40 + (carriage.pos[0] - self.dx) * 100, 10 + (carriage.pos[1] - self.dy) * 100,
                        int(55 * carriage.food / carriage.food_capacity), 20))
                        pygame.draw.rect(screen, (0, 0, 0), (
                        40 + (carriage.pos[0] - self.dx) * 100, 10 + (carriage.pos[1] - self.dy) * 100, 55, 20), 1)

                        font = pygame.font.SysFont('malgungothic', 15)
                        text = font.render(f"{carriage.food}/{carriage.food_capacity}", True, (0, 0, 0))
                        place = text.get_rect(
                            topleft=(45 + (carriage.pos[0] - self.dx) * 100, 8 + (carriage.pos[1] - self.dy) * 100))
                        screen.blit(text, place)
                else:
                    img = load_image(f'icon_furnace.png', -1)
                    img = pygame.transform.scale(img, (30, 30))
                    img_rect = img.get_rect(
                        center=(20 + (carriage.pos[0] - self.dx) * 100, 80 + (carriage.pos[1] - self.dy) * 100))
                    screen.blit(img, img_rect)

                    pygame.draw.rect(screen, (0, 150, 100), (
                    40 + (carriage.pos[0] - self.dx) * 100, 70 + (carriage.pos[1] - self.dy) * 100, 55, 20))
                    pygame.draw.rect(screen, (0, 255, 100), (
                    40 + (carriage.pos[0] - self.dx) * 100, 70 + (carriage.pos[1] - self.dy) * 100,
                    int(55 * train.coal / train.coal_capacity), 20))
                    pygame.draw.rect(screen, (0, 0, 0), (
                    40 + (carriage.pos[0] - self.dx) * 100, 70 + (carriage.pos[1] - self.dy) * 100, 55, 20), 1)

                    font = pygame.font.SysFont('malgungothic', 15)
                    text = font.render(f"{train.coal}/{train.coal_capacity}", True, (0, 0, 0))
                    place = text.get_rect(
                        topleft=(45 + (carriage.pos[0] - self.dx) * 100, 68 + (carriage.pos[1] - self.dy) * 100))
                    screen.blit(text, place)

        ''' draw icons and lvl'''
        pygame.draw.rect(screen, (193, 147, 117), (25, 10, 330, 390))
        pygame.draw.rect(screen, (90, 54, 39), (25, 10, 330, 390), 6)
        i = 0
        for resource in game.resources:
            i += 1
            img = load_image(f'icon_{resource}.png', -1)
            img = pygame.transform.scale(img, (54, 54))
            img_rect = img.get_rect(center=(61, 46 + 57*(i-1)))
            screen.blit(img, img_rect)
            draw_text(screen, f"x{game.resources[resource]}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 100, 43 + 57 * (i - 1), -1, 0)
        symb = "∞"
        if self.lvl <= 9:
            symb = str(self.required_exp[self.lvl])
        draw_text(screen, f"Уровень: {self.lvl}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 40, 330, -1, 0)
        draw_text(screen, f"Опыт: {self.exp}/{symb}", pygame.font.SysFont('malgungothic', 30), True, (0, 0, 0), None, 40, 370, -1, 0)

        ''' draw build mode '''
        game.build.draw(screen)

        ''' draw game manager '''
        game.manager.draw(screen)

        ''' draw particles '''
        all_sprites.draw(screen)



class Coal_Mine:
    def __init__(self, cooldown=0, frequency=500):
        self.cooldown = cooldown
        self.frequency = frequency
    def collect_coal(self):
        if (TIMER - self.cooldown < self.frequency):
            return None
        self.cooldown = TIMER
        return 1

class Iron_Mine:
    def __init__(self, cooldown=0, frequency=500):
        self.cooldown = cooldown
        self.frequency = frequency
    def collect_iron(self):
        if (TIMER - self.cooldown < self.frequency):
            return None
        self.cooldown = TIMER
        return 1

class Sawmill:
    def __init__(self, cooldown=0, frequency=500):
        self.cooldown = cooldown
        self.frequency = frequency
    def collect_wood(self):
        if (TIMER - self.cooldown < self.frequency):
            return None
        self.cooldown = TIMER
        return 1

class Seaport:
    def __init__(self, cooldown=0, frequency=500):
        self.cooldown = cooldown
        self.frequency = frequency
    def collect_crops(self):
        if (TIMER - self.cooldown < self.frequency):
            return None
        self.cooldown = TIMER
        return 1

class Passenger:
    def __init__(self, destination="", ticket_cost=10):
        self.destination = destination
        self.ticket_cost = ticket_cost

class Station:
    def __init__(self, cooldown=0, frequency=500):
        self.cooldown = cooldown
        self.frequency = frequency
        self.name = random.choice(["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань", "Нижний Новгород", "Челябинск", "Самара", "Уфа", "Ростов-на-Дону", "Омск", "Волгоград"])
    def collect_passenger(self):
        possible_stations = [game.buildings[b].name for b in game.buildings if type(game.buildings[b]) == Station and game.buildings[b].name != self.name]
        if (TIMER - self.cooldown < self.frequency or len(possible_stations)==0):
            return None
        passenger = Passenger(destination = random.choice(possible_stations), ticket_cost = random.randint(5, 15))
        return passenger

class Storage:
    def __init__(self, cooldown=0, frequency=500):
        self.cooldown = cooldown
        self.frequency = frequency
    def collect(self):
        if (TIMER - self.cooldown < self.frequency):
            return None
        return 1




pygame.init()
size = (1300, 900)
screen = pygame.display.set_mode(size)
TICK = pygame.USEREVENT + 1
FPS = 200
TICK_SPEED = int(1000 / FPS)
pygame.time.set_timer(TICK, TICK_SPEED)
TIMER = 0

game = Game()


pygame.mixer.init()
pygame.mixer.music.load(f"music/tomas.mp3" )
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(loops=-1)

'''
for i in range(10):
    game.rails[(i,5)] = Rail(type=0, rotation=0, pos=(i,5))
game.rails[(10,5)] = Rail(type=1, rotation=0, pos=(10,5))
game.rails[(10,6)] = Rail(type=0, rotation=1, pos=(10,6))
game.rails[(10,7)] = Rail(type=0, rotation=1, pos=(10,7))
game.rails[(10,8)] = Rail(type=1, rotation=1, pos=(10,8))
for i in range(10):
    game.rails[(i, 8)] = Rail(type=0, pos=(i, 8))

game.rails[(-1, 8)] = Rail(type=1, rotation=2, pos=(-1,8))
game.rails[(-1,7)] = Rail(type=0, rotation=1, pos=(-1,7))
game.rails[(-1,6)] = Rail(type=0, rotation=1, pos=(-1,6))
game.rails[(-1,5)] = Rail(type=1, rotation=3, pos=(-1,5))

game.buildings[(1,6)] = Station()
game.buildings[(9,4)] = Station()
game.buildings[(6,9)] = Station()
game.buildings[(5,7)] = Storage()
game.buildings[(7,6)] = Iron_Mine()
game.buildings[(11,7)] = Coal_Mine()
game.buildings[(2,9)] = Sawmill()
game.buildings[(-2,6)] = Seaport()


game.trains[0].engine = True
#game.trains.append(Train(carriages=[Carriage(type=5, pos=(9,8), rot=2)]))
'''

all_sprites = pygame.sprite.Group()
screen_rect = (0, 0, 1300, 900)

def create_particles(position):
    particle_count = 40
    numbers = range(-100, 100)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))

class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png", -1)]
    for scale in (30, 40, 50):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        GRAVITY = 200
        self.gravity = GRAVITY

    def update(self):
        self.velocity[1] += self.gravity * 1/FPS
        self.rect.x += self.velocity[0] * 1/FPS * 5
        self.rect.y += self.velocity[1] * 1/FPS * 5
        if not self.rect.colliderect(screen_rect):
            self.kill()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            exit()
        if game.load.state == 4:
            running = False
        if event.type == TICK:
            TIMER += TICK_SPEED
        game.load.process_event(event)
    screen.fill((255,255,255))
    game.load.draw(screen)
    pygame.display.update()



running = True
while running:
    for event in pygame.event.get():
        # keys = pygame.key.get_pressed()
        # event_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEMOTION:
            game.shop.process_event(event)
            game.build.process_event(event)
            game.stats.process_event(event)
            game.manager.process_event(event)

            #print(game.trains[0].carriages[0].pos)
            #print(game.resources)
            #print([el.destination for el in game.trains[0].carriages[5].passengers])

        if event.type == TICK:
            TIMER += TICK_SPEED
            game.controller.process_event(TICK_SPEED)
            game.process()
            #print(f"$ {game.resources['money']}")
            #print(game.trains[0].coal, game.trains[0].food)
    game.draw(screen)
    game.controller.draw(screen)
    pygame.display.update()