#coding:utf-8

"""
calculer les coordonnées de chaque position possibles sur une trajectoire et couper la trajectoire au moment où
les coordonnées coincident avec d'autres pièces
"""
def towerPossibleMovements(coordinates: tuple) -> list:
    #generation des trajectoires
    trajectoires = [[], [], [], []]
    microPosition = ["", ""]
    i = 1
    while i <= 8:
        microPosition = list(coordinates) #reinitialisation de microPosition
        
        microPosition[0] = coordinates[0] + i
        if (0 <= microPosition[0] < 8) and (0 <= microPosition[1] < 8):
            trajectoires[0].append(microPosition)

        microPosition = list(coordinates) #same

        microPosition[0] = coordinates[0] - i
        if (0 <= microPosition[0] < 8) and (0 <= microPosition[1] < 8):
            trajectoires[1].append(microPosition)
        
        microPosition = list(coordinates) #same
        
        microPosition[1] = coordinates[1] + i
        if (0 <= microPosition[0] < 8) and (0 <= microPosition[1] < 8):
            trajectoires[2].append(microPosition)

        microPosition = list(coordinates) #same

        microPosition[1] = coordinates[1] - i
        if (0 <= microPosition[0] < 8) and (0 <= microPosition[1] < 8):
            trajectoires[3].append(microPosition)
        i += 1
    return trajectoires

def foolPossibleMovements(coordinates: tuple):
    trajectoires = [[], [], [], []]
    microPosition = ["", ""]
    i = 1
    while i <= 8:
        microPosition = list(coordinates) #reinitialisation de microPosition
        
        microPosition[0] = coordinates[0] + i
        microPosition[1] = coordinates[1] + i
        if (0 <= microPosition[0] < 8) and (0 <= microPosition[1] < 8):
            trajectoires[0].append(microPosition)

        microPosition = list(coordinates) #same

        microPosition[0] = coordinates[0] - i
        microPosition[1] = coordinates[1] - i
        if (0 <= microPosition[0] < 8) and (0 <= microPosition[1] < 8):
            trajectoires[1].append(microPosition)
        
        microPosition = list(coordinates) #same
        
        microPosition[1] = coordinates[1] - i
        microPosition[0] = coordinates[0] + i
        if (0 <= microPosition[0] < 8) and (0 <= microPosition[1] < 8):
            trajectoires[2].append(microPosition)

        microPosition = list(coordinates) #same

        microPosition[1] = coordinates[1] + i
        microPosition[0] = coordinates[0] - i
        if (0 <= microPosition[0] < 8) and (0 <= microPosition[1] < 8):
            trajectoires[3].append(microPosition)
        i += 1
    return trajectoires

def queenPossibleMovements(coordinates: tuple):
    trajectoires = foolPossibleMovements(coordinates)
    trajectoires += towerPossibleMovements(coordinates)
    return trajectoires

def kingPossibleMovements(coordinates: tuple):
    before = queenPossibleMovements(coordinates)
    trajectoires = []
    for route in before:
        trajectoires += [route[:1]]
    
    return trajectoires

def horsePossibleMovements(coordinates: tuple):
    before = [[[coordinates[0]+2, coordinates[1]+1]],
            [[coordinates[0]+2, coordinates[1]-1]],
            [[coordinates[0]-2, coordinates[1]+1]],
            [[coordinates[0]-2, coordinates[1]-1]],
            [[coordinates[0]+1, coordinates[1]+2]],
            [[coordinates[0]-1, coordinates[1]+2]],
            [[coordinates[0]+1, coordinates[1]-2]],
            [[coordinates[0]-1, coordinates[1]-2]]]
    trajectoires = []
    for index in range(len(before)):
        if 0 <= before[index][0][0] < 8 and 0 <= before[index][0][1] < 8:
            trajectoires += [before[index]]

    return trajectoires

def cutPiecePath(in_game_piece_list, trajectoires, piece):
    possiblemovements = []
    in_game_piece_list_position = [list((piece_.coordinates[0]//63, piece_.coordinates[1]//63)) for piece_ in in_game_piece_list]
    for trajet in trajectoires:
        cut = False
        for position in trajet:
            if position in in_game_piece_list_position:
                found_piece = getPieceByCoordinates(coordinates=in_game_piece_list_position[in_game_piece_list_position.index(position)],
                                                    in_game_piece_list=in_game_piece_list)
                if found_piece.color == piece.color:
                    possiblemovements += trajet[:trajet.index(position)]
                    cut = True
                    break
                else:
                    possiblemovements += trajet[:trajet.index(position)+1]
                    cut = True
                    break
        if not cut:
            possiblemovements += trajet

    return possiblemovements

def getPieceByCoordinates(coordinates, in_game_piece_list):
    i = 0
    running = True
    coordinates = (coordinates[0]*63, coordinates[1]*63)
    while running and i < len(in_game_piece_list):
        if coordinates == in_game_piece_list[i].coordinates:
            return in_game_piece_list[i]
        i += 1
    return False

def cutPiecePathShort(in_game_piece_list, trajectoires, player_color):
    possiblemovements = []
    trajets = [trajet[0] for trajet in trajectoires if trajet != []]
    in_game_piece_coordinates = [list((int(round(piece.coordinates[0]/63)), int(round(piece.coordinates[1]/63)))) for piece in in_game_piece_list]

    for trajet in trajets:
        if trajet in in_game_piece_coordinates:
            for piece in in_game_piece_list:
                if list((int(round(piece.coordinates[0]/63)), int(round(piece.coordinates[1]/63)))) == trajet and player_color != piece.color:
                    possiblemovements.append(trajet)
        else:
            possiblemovements.append(trajet)

    return possiblemovements

def formatLegalMove(piece, in_game_piece_list, player_color, possible_movements, king):
    backup = in_game_piece_list[in_game_piece_list.index(piece)].coordinates
    index_list = []
    backup2 = False
    for movement in possible_movements:
        if type(backup2) != bool:
            in_game_piece_list.append(backup2)
        in_game_piece_list[in_game_piece_list.index(piece)].coordinates = (movement[0]*63, movement[1]*63)
        for piece_ in in_game_piece_list:
            if piece_.coordinates == (movement[0]*63, movement[1]*63) and piece_ != piece:
                backup2 = piece_
                in_game_piece_list.pop(in_game_piece_list.index(piece_))
                break
        if type(king.isInDanger(in_game_piece_list, player_color)) != bool:
            index_list.append(movement)
    if type(backup2) != bool:
        in_game_piece_list.append(backup2)
    while index_list != []:
        possible_movements.pop(possible_movements.index(index_list[0]))
        if index_list != []:
            index_list.pop(0)
    
    in_game_piece_list[in_game_piece_list.index(piece)].coordinates = backup
    return possible_movements


if __name__ == "__main__":
    pass