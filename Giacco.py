import telebot
import pickle

class user:
    def __init__(self, nome, id, level):
        self.nome = nome
        self.id = id
        self.level = level
        self.xp = 0

