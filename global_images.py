from settings import *
import pygame
import os
side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "misc/images/board.jpeg"))
                                  .convert_alpha(), (1600, 65))
tree_image = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "misc/images/scroll.png"))
                                    .convert_alpha(), (10 * BLOCKSIZE, 13 * BLOCKSIZE))
unit_menu_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "misc/images/board.jpeg"))
                                       .convert_alpha(), (180, 250))
star_img = pygame.image.load(os.path.join("game_assets", "misc/images/star.png")).convert_alpha()

Conscript_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/conscrit.png")).convert_alpha(), (75, 75))
LineInfantry_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/infanterie_anglaise.png")).convert_alpha(), (75, 75))
Grenadier_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/grenadier.png")).convert_alpha(), (75, 75))
YoungGuard_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/jeune_garde.png")).convert_alpha(), (75, 75))
MedGuard_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/med_guard.png")).convert_alpha(), (75, 75))
OldGuard_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/vielle_garde/shooting/6.png")).convert_alpha(), (75, 75))
Chasseur_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/tirailleur.png")).convert_alpha(), (75, 75))
Flanqueur_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/tirailleur.png")).convert_alpha(), (75, 75))
GuardChasseur_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/voltigeur/shooting/6.png")).convert_alpha(), (65, 65))
Volitgeur_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/voltigeur/shooting/6.png")).convert_alpha(), (65, 65))
GuardVoltigeur_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/tirailleur.png")).convert_alpha(), (75, 75))

buy_unit = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/jeune_garde.png")).convert_alpha(), (75, 75))
buy_old_gard = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/viellegarde.png")).convert_alpha(), (75, 75))
buy_conscript = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/conscrit.png")).convert_alpha(), (75, 75))
buy_canon = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "misc/images/canon.png")).convert_alpha(), (75, 75))

bayonet = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "infantry/images/bayonet.png")).convert_alpha(), (50, 50))

special = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "misc/images/up.png")).convert_alpha(),
                                 (50, 50))
tree = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "misc/images/star.png")).convert_alpha(),
                                 (50, 50))
tree_land = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "misc/images/rock.png")).convert_alpha(),
                                 (65, 65))
scope = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "infantry/images/scope.png"))
                               .convert_alpha(), (50, 50))
rifle = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "infantry/images/rifle.png"))
                               .convert_alpha(), (50, 50))
money_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "misc/images/money.png")).convert_alpha(), (50, 50))
clock_img = pygame.transform.scale(
    pygame.image.load(os.path.join("game_assets", "misc/images/clock.png")).convert_alpha(), (50, 50))

close = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "misc/images/cross.png"))
                               .convert_alpha(), (50, 50))

cross = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "misc/images/cross_move.png"))
                               .convert_alpha(), (50, 50))