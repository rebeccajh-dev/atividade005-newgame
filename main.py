"""
Main module for the components.
This module handles the initialization of the components loop and the rendering process.
"""
import pygame as pg

from components.game import Game

if __name__ == '__main__':
    pg.init()
    game = Game()
    game.run()