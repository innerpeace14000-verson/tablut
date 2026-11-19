# Le Tablut se joue sur un plateau carré de 9 sur 9 cases
GRID_SIZE = 9

# Les lettres pour repérer les colonnes
# Les chiffres pour repérer les lignes
COL_LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

# Les Suédois (blancs)
# 9 pièces au total.
# Le Roi placé au centre (Konakis) et ses 8 soldats positionnés en croix juste autour de lui

# Les Moscovites  (noirs)
# 16 pièces placées sur les bordures et les périphéries du plateau 
INITIAL_STATE = {
    # Le Roi (au centre e5)
    (4, 4): 'KING',
    # Défenseurs blancs (8 pions)
    (4, 3): 'WHITE', (4, 5): 'WHITE', (3, 4): 'WHITE', (5, 4): 'WHITE',
    (2, 4): 'WHITE', (6, 4): 'WHITE', (4, 2): 'WHITE', (4, 6): 'WHITE',
    # Attaquants noirs (16 pions)
    (0, 3): 'BLACK', (0, 4): 'BLACK', (0, 5): 'BLACK', (1, 4): 'BLACK',  # Nord
    (8, 3): 'BLACK', (8, 4): 'BLACK', (8, 5): 'BLACK', (7, 4): 'BLACK',  # Sud
    (5, 0): 'BLACK', (4, 0): 'BLACK', (3, 0): 'BLACK', (4, 1): 'BLACK',  # Ouest
    (5, 8): 'BLACK', (4, 8): 'BLACK', (3, 8): 'BLACK', (4, 7): 'BLACK',  # Est
}


class TablutModel:

    def __init__(self):
        # copie superficielle (shallow copy) d'un dictionnaire.
        self.state = INITIAL_STATE.copy()

    def get_piece(self, row, col):
        return self.state.get((row, col))

    def is_empty(self, row, col):
        return (row, col) not in self.state

    def reset(self):
        # copie superficielle (shallow copy) d'un dictionnaire.
        self.state = INITIAL_STATE.copy()