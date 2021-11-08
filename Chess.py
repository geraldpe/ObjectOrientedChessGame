#coding:utf-8

"""
author : Gerald Pellegrino
date of creation : 02/10/2021
"""

import gameEngine as ge
from movements import *

CASE_DIMS = 63
possible_movements = []

"""---------------------------------------Classes des pieces----------------------------------------------------"""

class Tower(ge.Character):
    def __init__(self, container, color, coordinates, tag):
        self.clicked = False
        self.color = color
        self.possible_movements = []
        self.tag=tag
        self.rook = False
        ge.Character.__init__(self, container=container,
                                name=color+"_tower",
                                img_link="graphics/{}_tower.png".format(color),
                                coordinates=coordinates,
                                bheight=63,
                                bwidth=63,
                                tag=tag)
    
    def possibleMovements(self, in_game_piece_list, color):
        trajectoires = towerPossibleMovements((int(self.coordinates[0]/63), int(self.coordinates[1]/63)))
        return cutPiecePath(in_game_piece_list=in_game_piece_list, trajectoires=trajectoires, piece=self)

class Pawn(ge.Character):
    def __init__(self, container, color, coordinates, tag):
        self.clicked = False
        self.color = color
        self.possible_movements = []
        self.tag=tag
        self.turn = 1
        ge.Character.__init__(self, 
                                container=container,
                                name=tag,
                                img_link="graphics/{}_pawn.png".format(color),
                                coordinates=coordinates,
                                bheight=63,
                                bwidth=63,
                                tag=tag)              
        
    def possibleMovements(self, in_game_piece_list, color, player_color):
        def canEat(in_game_piece_list, color, player_color):
            diago_possibilities = []
            if color == self.color and self.color == player_color:
                diagonales = [[self.coordinates[0]+CASE_DIMS, self.coordinates[1]-CASE_DIMS], 
                                [self.coordinates[0]-CASE_DIMS, self.coordinates[1]-CASE_DIMS]]
            else:
                diagonales = [[self.coordinates[0]+CASE_DIMS, self.coordinates[1]+CASE_DIMS], 
                                [self.coordinates[0]-CASE_DIMS, self.coordinates[1]+CASE_DIMS]]
            for piece in in_game_piece_list:
                if list(piece.coordinates) in diagonales and piece.color != self.color:
                    diago_possibilities.append((piece.coordinates[0]//63, piece.coordinates[1]//63))
            return diago_possibilities
        #def trajectoires

        if color == self.color and self.turn == 1 and self.color == player_color:
            trajectoires = [[self.coordinates[0], self.coordinates[1]-CASE_DIMS], [self.coordinates[0], self.coordinates[1]-2*CASE_DIMS]]
        elif color == self.color and self.color == player_color:
            trajectoires = [[self.coordinates[0], self.coordinates[1]-CASE_DIMS]]
        elif color == self.color and self.turn == 1 and self.color != player_color:
            trajectoires = [[self.coordinates[0], self.coordinates[1]+CASE_DIMS], [self.coordinates[0], self.coordinates[1]+2*CASE_DIMS]]
        else:
            trajectoires = [[self.coordinates[0], self.coordinates[1]+CASE_DIMS]]
        for route in trajectoires:
            for piece in in_game_piece_list:
                if list((piece.coordinates[0], piece.coordinates[1])) == route:
                    index = trajectoires.index(route)
                    if index == 0:
                        diag_possibilities = canEat(in_game_piece_list, color, player_color)
                        return diag_possibilities
                    else:
                        #trajectoires = trajectoires[0]
                        return [(trajectoires[0][0]//63, trajectoires[0][1]//63)] + canEat(in_game_piece_list, color, player_color)

        return [(route[0]//63, route[1]//63) for route in trajectoires] + canEat(in_game_piece_list, color, player_color)
    
    def move(self, coordinates):
        deplacement_X = coordinates[0] - self.coordinates[0]
        deplacement_Y = coordinates[1] - self.coordinates[1]
        tag = self.container.gettags(self.tag)[0]
        self.container.move(tag, deplacement_X, deplacement_Y)
        self.clicked = False
        self.coordinates = coordinates
        self.turn += 1

    def getTrajectoiresPawn(self, in_game_piece_list, color, player_color):
        diago_possibilities = []
        if color == self.color and self.color == player_color:
            diagonales = [[self.coordinates[0]+CASE_DIMS, self.coordinates[1]-CASE_DIMS], 
                            [self.coordinates[0]-CASE_DIMS, self.coordinates[1]-CASE_DIMS]]
        else:
            diagonales = [[self.coordinates[0]+CASE_DIMS, self.coordinates[1]+CASE_DIMS], 
                            [self.coordinates[0]-CASE_DIMS, self.coordinates[1]+CASE_DIMS]]
        for piece in in_game_piece_list:
            if list(piece.coordinates) in diagonales and piece.color != self.color:
                diago_possibilities.append((piece.coordinates[0]//63, piece.coordinates[1]//63))
        return diago_possibilities

    def isAtOppositeSide(self):
        if self.color == "black" and self.coordinates[1] == 7:
            return True
        elif self.coordinates[1] == 0:
            return True
        return False


class Queen(ge.Character):
    def __init__(self, container, color, coordinates, tag):
        self.clicked = False
        self.color = color
        self.possible_movements = []
        self.tag=tag
        ge.Character.__init__(self, 
                                container=container,
                                name=color+"_queen",
                                img_link="graphics/{}_queen.png".format(color),
                                coordinates=coordinates,
                                bheight=63,
                                bwidth=63,
                                tag=tag)

    def possibleMovements(self, in_game_piece_list, color):
        trajectoires = queenPossibleMovements((int(self.coordinates[0]/63), int(self.coordinates[1]/63)))
        return cutPiecePath(in_game_piece_list=in_game_piece_list, trajectoires=trajectoires, piece=self)
        
class King(ge.Character):
    def __init__(self, container, color, coordinates, tag):
        self.clicked = False
        self.color = color
        self.possible_movements = []
        self.tag=tag
        self.rook = False
        ge.Character.__init__(self, 
                                container=container,
                                name=color+"_king",
                                img_link="graphics/{}_king.png".format(color),
                                coordinates=coordinates,
                                bheight=63,
                                bwidth=63,
                                tag=tag)
    
    def possibleMovements(self, in_game_piece_list, color):
        trajectoires = kingPossibleMovements((int(self.coordinates[0]/63), int(self.coordinates[1]/63)))
        self.sideDetectionForRook(in_game_piece_list)
        return cutPiecePathShort(in_game_piece_list=in_game_piece_list, trajectoires=trajectoires, player_color=color)

    def isInDanger(self, in_game_piece_list, player_color):
        enemy_pieces = [enemy for enemy in in_game_piece_list if enemy.color != self.color]
        attack_matrix = [   [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]]
        for enemy in enemy_pieces:
            if 'pawn' not in enemy.name:
                enemy_possible_movements = enemy.possibleMovements(in_game_piece_list, enemy.color)
            else:
                enemy_possible_movements = enemy.possibleMovements(in_game_piece_list, enemy.color, player_color)
            for position in enemy_possible_movements:
                attack_matrix[position[0]][position[1]] = 1
        
        if attack_matrix[self.coordinates[0]//63][self.coordinates[1]//63] == 1:
            print(self.name, " in danger")
            return attack_matrix
        return True
    
    def sideDetectionForRook(self, in_game_piece_list):
        #find color towers positions
        same_color_towers = [tower for tower in in_game_piece_list if tower.name == "{}_tower".format(self.color)]
        #are squares between king and tower empty ?

        #return (bool, bool) ind0 == big rook ind1 == lil rook. the bool tells if you can do it or not

class Fool(ge.Character):
    def __init__(self, container, color, coordinates, tag):
        self.clicked = False
        self.color = color
        self.possible_movements = []
        self.tag=tag
        ge.Character.__init__(self, 
                                container=container,
                                name=color+"_fool",
                                img_link="graphics/{}_fool.png".format(color),
                                coordinates=coordinates,
                                bheight=63,
                                bwidth=63,
                                tag=tag)
    
    def possibleMovements(self, in_game_piece_list, color):
        trajectoires = foolPossibleMovements((self.coordinates[0]//63, self.coordinates[1]//63))
        return cutPiecePath(in_game_piece_list=in_game_piece_list, trajectoires=trajectoires, piece=self)
       
class Horse(ge.Character):
    def __init__(self, container, color, coordinates, tag):
        self.clicked = False
        self.color = color
        self.possible_movements = []
        self.tag=tag
        ge.Character.__init__(self, 
                                container=container,
                                name=color+"_horse",
                                img_link="graphics/{}_horse.png".format(color),
                                coordinates=coordinates,
                                bheight=63,
                                bwidth=63,
                                tag=tag)
    
    def possibleMovements(self, in_game_piece_list, color):
        trajectoires = horsePossibleMovements((int(self.coordinates[0]/63), int(self.coordinates[1]/63)))
        return cutPiecePathShort(in_game_piece_list=in_game_piece_list, trajectoires=trajectoires, player_color=color)

"""---------------------------------fonction d'initialisation--------------------------------------------------"""

def initiateGame(container: object, color: str="white"):
    if color == "black":
        y_black = 7*CASE_DIMS
        y_white = 0
        y_white_pawn = y_white + CASE_DIMS
        y_black_pawn = y_black - CASE_DIMS  
    else:
        y_black = 0
        y_white = 7*CASE_DIMS
        y_white_pawn = y_white - CASE_DIMS
        y_black_pawn = y_black + CASE_DIMS
    #place pawns
    in_game_piece_list = []
    for i in range(8):
        in_game_piece_list.append(Pawn(container, "white", (i*CASE_DIMS,y_white_pawn), "white_pawn_{}".format(i)))
        in_game_piece_list.append(Pawn(container, "black", (i*CASE_DIMS,y_black_pawn), "black_pawn_{}".format(i)))
        
    #initiate black pieces
    
    in_game_piece_list.append(Tower(container, "black", (0, y_black), "black_tower_1"))
    in_game_piece_list.append(Tower(container, "black", (7*CASE_DIMS, y_black), "black_tower_2"))

    in_game_piece_list.append(Horse(container, "black", (CASE_DIMS, y_black), "black_horse_1"))
    in_game_piece_list.append(Horse(container, "black", (6*CASE_DIMS, y_black), "black_horse_2"))

    in_game_piece_list.append(Fool(container, "black", (2*CASE_DIMS, y_black), "black_fool_1"))
    in_game_piece_list.append(Fool(container, "black", (5*CASE_DIMS, y_black), "black_fool_2"))

    in_game_piece_list.append(Queen(container, "black", (4*CASE_DIMS, y_black), "black_queen"))
    in_game_piece_list.append(King(container, "black", (3*CASE_DIMS, y_black), "black_king"))

    #initiate white pieces
    in_game_piece_list.append(Tower(container, "white", (0, y_white), "white_tower_1"))
    in_game_piece_list.append(Tower(container, "white", (7*CASE_DIMS, y_white), "white_tower_2"))

    in_game_piece_list.append(Horse(container, "white", (CASE_DIMS, y_white), "white_horse_1"))
    in_game_piece_list.append(Horse(container, "white", (6*CASE_DIMS, y_white), "white_horse_2"))

    in_game_piece_list.append(Fool(container, "white", (2*CASE_DIMS, y_white), "white_fool_1"))
    in_game_piece_list.append(Fool(container, "white", (5*CASE_DIMS, y_white), "white_fool_2"))

    in_game_piece_list.append(Queen(container, "white", (4*CASE_DIMS, y_white), "white_queen"))
    in_game_piece_list.append(King(container, "white", (3*CASE_DIMS, y_white), "white_king"))

    return in_game_piece_list

"""---------------------------------initialisation de la classe Game (principale)------------------------------"""
class Game(ge.Window):

    def __init__(self):
        ge.Window.__init__(self, size="800x504", name="chess game", bg="#FFD4AB")
        self.turn = 1
        self.state = "white_turn" #white_turn, black_turn, eating_state
        self.player_color = "white"
        self.lastpiecemove = [None, 0, 0]
        self.addBackgroundImage("graphics/chess_board_brown.png", bwidth=504)
        self.in_game_pieces_list = initiateGame(self.backgroundCanv, self.player_color)
        self.backgroundCanv.pack()
        self.backgroundCanv.bind("<Button-1>", self.manageClick)
        
    def manageClick(self, event):
        global possible_movements

        def click(event, color):
            for piece in self.in_game_pieces_list:
                if piece.clicked:
                    for position in piece.possible_movements:
                        if position[0]*63 <= event.x <= position[0]*63+CASE_DIMS and position[1]*63 <= event.y <= position[1]*63+CASE_DIMS:
                            piece.move((position[0]*63, position[1]*63))
                            piece.container.delete("dot")
                            self.lastpiecemove = [piece, piece.coordinates[0], piece.coordinates[1]]
                            self.eating()
                            self.turn += 1
                            for piece in self.in_game_pieces_list:
                                if "pawn" in piece.name and piece.isAtOppositeSide():
                                    self.launchPieceSelector()
                            return "moved"
                if piece.coordinates[0] <= event.x <= piece.coordinates[0]+CASE_DIMS and piece.coordinates[1] <= event.y <= piece.coordinates[1]+63 and piece.color == color:
                    self.unclick()
                    possible_movements = self.seePossibleMovements(piece, color)
                    king = [king for king in self.in_game_pieces_list if ("king" in king.name and king.color == piece.color)][0]
                    possible_movements = formatLegalMove(piece, self.in_game_pieces_list, self.player_color, possible_movements, king)
                    print(piece.name, " Clicked")
                    piece.clicked = True
                    self.addDots(possible_movements)
                    piece.possible_movements = possible_movements
                    return

        #mouvement et selection de la pièce
        if "white" in self.state:
            moved = click(event, "white")
            if moved == "moved":
                self.state = "black_turn"

        else:
            moved = click(event, "black")
            if moved == "moved":
                self.state = "white_turn"
        self.handleCheck()

        return

    def addDots(self, possible_movements):
        global image
        image = ge.setimage("graphics/round_dot.png", int(round(CASE_DIMS/3)), int(round(CASE_DIMS/3)))
        for movement in possible_movements:
            self.backgroundCanv.create_image(movement[0]*63 + 63/2, movement[1]*63 + 63/2, anchor="center", image=image, tag="dot")

    def handleCheck(self):
        #detection d'un echec
        self.backgroundCanv.delete("check")

        king = [piece for piece in self.in_game_pieces_list if ("king" in piece.name and piece.color == "white")][0]
        attack_matrix = king.isInDanger(self.in_game_pieces_list, self.player_color)
        if type(attack_matrix) == bool:
            king = [piece for piece in self.in_game_pieces_list if ("king" in piece.name and piece.color == "black")][0]
            attack_matrix = king.isInDanger(self.in_game_pieces_list, self.player_color)

            if type(attack_matrix) != bool:
                king_position = self.findKingPosition("black")
                self.backgroundCanv.create_rectangle(king_position[0], king_position[1],
                                                    king_position[0]+CASE_DIMS, king_position[1]+CASE_DIMS,
                                                    fill="red", stipple="gray25", tag="check")
        else:
            king_position = self.findKingPosition("white")
            self.backgroundCanv.create_rectangle(king_position[0], king_position[1],
                                                    king_position[0]+CASE_DIMS, king_position[1]+CASE_DIMS,
                                                    fill="red", stipple="gray25", tag="check")
        self.eating()

    def eating(self):
        if self.lastpiecemove[0] != None:
            movement = self.lastpiecemove[1:]
            for piece in self.in_game_pieces_list:
                if piece.coordinates == tuple(movement) and piece != self.lastpiecemove[0]:
                    self.in_game_pieces_list.pop(self.in_game_pieces_list.index(piece))
                    self.backgroundCanv.delete(piece.tag)
                    break
    
    def seePossibleMovements(self, piece: ge.Character, color):
        if type(piece) != Pawn:
            return piece.possibleMovements(self.in_game_pieces_list, color)
        elif type(piece) == Pawn:
            return piece.possibleMovements(self.in_game_pieces_list, color, self.player_color)

    def unclick(self):
        for piece in self.in_game_pieces_list:
            piece.clicked = False

    def findKingPosition(self, color):
        for piece in self.in_game_pieces_list:
            if piece.name == "{}_king".format(color):
                return piece.coordinates
    
    def launchPieceSelector(self, piece):
        pass

"""------------------------------corps du jeu-------------------------------------------------------------------"""

def main():
    window = Game()
    window.window.mainloop()

if __name__ == "__main__":
    main()