import random
#класс Player, имеет в себе функции которые может делать игрок и атрибуты игрока
class Player:
    def __init__(self,name):
        self.name = name
        self.balance = 2000000000
        self.position = 0
        self.properties = []
        self.jail = False
        self.is_playing = True
    def dice_roll(self):
        return random.randint(1,6), random.randint(1,6)
    #если игрок проходит через старт получает деньги, 20 это количество полей
    def move(self, roll):
        self.position += sum(roll)
        if self.position >= 20:
            self.position -= 20
            self.balance += 500000
        return self.position
    def __str__(self):
        return self.name
#класс Активов, на самом деле включает в себе аттрибуты всех полей 
class Asset:
    def __init__(self,name,color,type,price_sale,price_for_passing):
        self.name = name 
        self.color = color
        self.type = type
        self.price_sale = price_sale
        self.price_for_passing = price_for_passing
    def __str__(self):
        return self.name 
#класс самой игровой карты, добавляет в класс активов игровые поля, тут 20 полей в два раза меньше чем в оригинальной игре    
class Board:
    def __init__(self):
        self.spaces = [
            Asset("СТАРТ", "none", "start", 0, 0),
            Asset("Tassay", "синий", "property", 55000000, 2000000),
            Asset("Asu","синий","property", 45000000, 1500000),
            Asset("НАЛОГ #1", "none", "tax",0, 5000000),
            Asset("BonAqua", "синий", "property", 70000000, 6000000),
            Asset("ШАНС #1","none","chance",0, 0),
            Asset("Magnum", "желтый", "property", 90000000, 9000000),
            Asset("Galmart", "желтый", "property", 85000000, 8500000),
            Asset("Зарплата", "none", "salary", 0, 0),
            Asset("Small", "желтый", "property", 80000000, 8000000),
            Asset("Скамейка", "none", "bench", 0, 0),
            Asset("Technodom","зеленый", "property", 120000000, 12000000),
            Asset("Налог #2", "none", "tax", 0, 5000000),
            Asset("Sulpak", "зеленый", "property", 100000000, 10000000),
            Asset("Mechta", "зеленый", "property", 105000000, 10500000),
            Asset("Тюрьма", "none", "jail", 0, 0),
            Asset("H&M", "красный", "property", 130000000, 13000000),
            Asset("ШАНС #2", "none", "chance", 0,0),
            Asset("Bershka", "красный", "property", 1350000000, 13500000),
            Asset("Zara", "красный", "property", 140000000, 14000000)
        ]
#класс самой игры, тут нужные аттрибуты для игры как количество игроков и купленные собственности, так же иницализация карты и регистрация игроков 
class Game:
    def __init__(self, number):
        self.num_players = number
        self.players = []
        self.purchased = {}
        self.board = Board()
    def player_registration(self):
        for i in range(self.num_players):
            name = input(f"Как вас зовут игрок #{i+1}:")
            self.players.append(Player(name))
#функция для запуска игры 

def play_game():
    number =int(input("Сколько игроков будет играть в игру:"))
    #Проверяем чтоб в игру играли минимум два игрока
    if number >= 2:
        game = Game(number)
    else:
        print("в Игру могут играть как миним два игрока, попробуйте еще раз.")
        play_game()
    #Регистрируем игроков 
    game.player_registration()
    while True:
        print("-----------------------------------")
        #Проверяем перед каждой итерацией; если игрок в тюрьме он пропускает ход и освобажадется из тюрьмы 
        for player in game.players:
            if player.jail == True:
                player.jail = False
                continue
            print("-----------------------------------")
            #процесс игры, игрок кидает кубики и ходит на нужное поле
            print(f"Ходит игрок -> {player.name}")
            input("нажмите Enter чтобы бросить кубики")
            roll = player.dice_roll()
            print(f"у {player.name} выпало {roll[0]} и {roll[1]}")
            asset = player.move(roll)
            print (f"{player.name} теперь находится на поле '{game.board.spaces[asset]}'")
            #если игрок попал на поле с собственностью он может ее купить
            if game.board.spaces[asset].type == "property":
                if asset not in game.purchased:
                    decision = input(f"{player.name} желаете приоберсти {game.board.spaces[asset]} цвета {game.board.spaces[asset].color} за {game.board.spaces[asset].price_sale} тенге? (+/-)")
                    if decision == "+":
                        player.properties.append(asset)
                        game.purchased[asset] = player
                        player.balance -= game.board.spaces[asset].price_sale
                        print(f"{player.name} приборел {game.board.spaces[asset]}")
                    else:
                        print("Вы отказались приборетать этот участок, играем дальше")
                else:
                    if player == game.purchased[asset]:
                        print("Это ваша собственность")
                    else:
                        #если это поле не наше, то мы платим налог владельцу
                        rent = game.board.spaces[asset].price_for_passing
                        #если у игрока есть поля всех цвето то ему платят в три раза больше
                        #тут я захардкодил, не успел придумать что то лучше чем проверять по полям
                        if game.board.spaces[asset].color == "синий":
                            # 1 2 4 
                            if 1 and 2 and 4 in game.purchased[asset].properties: 
                                rent *= 3
                        elif game.board.spaces[asset].color == "желтый":
                            # 6 7 9
                            if 6 and 7 and 9 in game.purchased[asset].properties: 
                                rent *= 3
                        elif game.board.spaces[asset].color == "зеленый":
                            # 11 13 14
                            if 11 and 13 and 14 in game.purchased[asset].properties: 
                                rent *= 3
                        elif game.board.spaces[asset].color == "красный":       
                            # 16 18 19
                            if 16 and 18 and 19 in game.purchased[asset].properties: 
                                rent *= 3
                        player.balance -= rent                 
                        game.purchased[asset].balance += rent
                        print(f"Игрок {player} заплатил {rent} тенге игроку -> {game.purchased[asset]}")   
            #поле налогов, игрок платит налог
            elif game.board.spaces[asset].type == "tax":
                tax = game.board.spaces[asset].price_for_passing
                player.balance -= tax
                print(f"Игрок {player.name} заплатил налог в сумме {tax} тенге")
            #тут поле шанс; рандомно может выпасть отправление в тюрьму или в начало карты, можно добавить больше 
            elif game.board.spaces[asset].type == "chance":
                print("Вы попали на поле шанс")
                rand = random.randint(1,2)
                if rand == 1:
                    player.position = 0
                    player.balance += 500000
                    print("Вам попалась карта - СТАРТ")
                    print("Вы отправляетесь на поле СТАРТ, ваш баланс пополнен на 500000 тенге")
                else:
                    player.position = 15
                    player.jail = True
                    print("Вам попалась карта - Тюрьма")
                    print("Вы отправляетесь в Тюрьму и пропускаете ход")
            #зарплата, поле где пополняется баланс
            elif game.board.spaces[asset].type == "salary":
                player.balance += 1000000
                print("Вам поступила зарплата, ваш баланс пополнен на 1000000 тенге")
            #тюрьма, игрок пропускает ход
            elif game.board.spaces[asset].type == "jail":
                player.jail = True
                print("Вы в Тюрьме, пропускаете ход")
            #если игрок находится в поле старт получает деньги
            elif game.board.spaces[asset].type == "start":
                player.balance += 500000
                print ("Вы на поле старт, баланс пополнен на 500000 тенге")
            #изначально было поле вокзала, вокзал примерно такой же как и другие поля с собственностью, изменил на скамейку как тюрьма но не пропускаешь ход
            elif game.board.spaces[asset].type == "bench":
                print("Присядьте и отдохните")
            #в конце проверяем баланс и количество участников            
            print(f"Ваш баланс {player.balance}")
            if player.balance < 0:
                print("к сожалению вы проиграли")
                game.players.remove(player)
            if len(game.players) == 1:
                print(f"{game.players[0]} вы победили!!! поздравляем!!!")
                return     
