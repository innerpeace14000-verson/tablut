from PyQt6.QtCore import QRect, Qt
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen
from PyQt6.QtWidgets import QWidget
from tablut_model import COL_LETTERS, GRID_SIZE

DEFAULT_BOARD_SIZE = 540
MARGIN_SIDE = 50
MARGIN_TOP = 25
MARGIN_BOTTOM = 45
COORD_FONT_SIZE = 11
FRAME_BORDER_WIDTH = 8
FRAME_OFFSET = 6
COORD_LABEL_GAP = 15
PIECE_RADIUS_RATIO = 0.38

class TablutBoard(QWidget):

    def __init__(self, model):
        super().__init__()
        self.model = model

        # fixe la taille minimale du widget
        self.setMinimumSize(
            DEFAULT_BOARD_SIZE + 2 * MARGIN_SIDE,
            DEFAULT_BOARD_SIZE + MARGIN_TOP + MARGIN_BOTTOM,
        )

    def paintEvent(self, event):
        # crée un objet de dessin (QPainter) rattaché au widget
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        widget_w = self.width()
        widget_h = self.height()

        avail_w = widget_w - (2 * MARGIN_SIDE)
        avail_h = widget_h - MARGIN_TOP - MARGIN_BOTTOM
        board_area_size = min(avail_w, avail_h)

        offset_x = MARGIN_SIDE + (avail_w - board_area_size) / 2
        offset_y = MARGIN_TOP + (avail_h - board_area_size) / 2

        # Cadre extérieur
        painter.setPen(QPen(QColor("#2C1608"), FRAME_BORDER_WIDTH))
        painter.setBrush(QBrush(QColor("#7D4E2D")))
        painter.drawRect(
            QRect(
                int(round(offset_x - FRAME_OFFSET)),
                int(round(offset_y - FRAME_OFFSET)),
                int(round(board_area_size + 2 * FRAME_OFFSET)),
                int(round(board_area_size + 2 * FRAME_OFFSET)),
            )
        )

        cell_size = board_area_size / GRID_SIZE

        # Coordonnées
        painter.setFont(QFont("Arial", COORD_FONT_SIZE, QFont.Weight.Bold))
        painter.setPen(QPen(QColor("#2C1810")))

        for i in range(GRID_SIZE):
            row_label = str(GRID_SIZE - i)
            y_start = round(offset_y + i * cell_size)
            y_end = round(offset_y + (i + 1) * cell_size)
            
            painter.drawText(
                QRect(0, y_start, int(round(offset_x - COORD_LABEL_GAP)), y_end - y_start),
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter,
                row_label,
            )

            col_label = COL_LETTERS[i]
            x_start = round(offset_x + i * cell_size)
            x_end = round(offset_x + (i + 1) * cell_size)
            painter.drawText(
                QRect(x_start, int(round(offset_y + board_area_size + 6)), x_end - x_start, 30),
                Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignTop,
                col_label,
            )

        # Grille
        light_wood_brush = QBrush(QColor("#FCEECB"))
        special_wood_brush = QBrush(QColor("#DFBC8A"))

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x1 = round(offset_x + c * cell_size)
                x2 = round(offset_x + (c + 1) * cell_size)
                y1 = round(offset_y + r * cell_size)
                y2 = round(offset_y + (r + 1) * cell_size)
                rect = QRect(x1, y1, x2 - x1, y2 - y1)

                if (r, c) == (4, 4) or (r in (0, 8) and c in (0, 8)):
                    painter.setBrush(special_wood_brush)
                else:
                    painter.setBrush(light_wood_brush)

                painter.setPen(QPen(QColor("#B8976C"), 1))
                painter.drawRect(rect)

                if (r, c) == (4, 4):
                    painter.setPen(QPen(QColor("#7A5230"), 1, Qt.PenStyle.DashLine))
                    painter.drawRect(rect.adjusted(4, 4, -4, -4))
                    painter.setFont(QFont("Arial", int(round((x2 - x1) * 0.35)), QFont.Weight.Bold))
                    painter.setPen(QPen(QColor("#5C3A21"), 1))
                    painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "☩")
                elif r in (0, 8) and c in (0, 8):
                    painter.setPen(QPen(QColor("#7A5230"), 1, Qt.PenStyle.SolidLine))
                    painter.drawRect(rect.adjusted(4, 4, -4, -4))
                    painter.drawLine(x1 + 5, y1 + 5, x2 - 5, y2 - 5)
                    painter.drawLine(x1 + 5, y2 - 5, x2 - 5, y1 + 5)

        # Pièces (depuis l'état du Modèle)
        piece_radius = int(cell_size * PIECE_RADIUS_RATIO)
        
        for (r, c), piece_type in self.model.state.items():
            cx = int(round(offset_x + c * cell_size + cell_size / 2))
            cy = int(round(offset_y + r * cell_size + cell_size / 2))

            if piece_type == 'BLACK':
                painter.setBrush(QBrush(QColor("#2C221E")))
                painter.setPen(QPen(QColor("#1A1310"), 2))
                painter.drawEllipse(cx - piece_radius, cy - piece_radius, piece_radius * 2, piece_radius * 2)
            elif piece_type == 'WHITE':
                painter.setBrush(QBrush(QColor("#F5E6CC")))
                painter.setPen(QPen(QColor("#8C6239"), 2))
                painter.drawEllipse(cx - piece_radius, cy - piece_radius, piece_radius * 2, piece_radius * 2)
            elif piece_type == 'KING':
                painter.setBrush(QBrush(QColor("#D4AF37")))
                painter.setPen(QPen(QColor("#5C3A21"), 2))
                painter.drawEllipse(cx - piece_radius, cy - piece_radius, piece_radius * 2, piece_radius * 2)
                painter.setFont(QFont("Arial", int(round(piece_radius * 0.9)), QFont.Weight.Bold))
                painter.setPen(QPen(QColor("#2C1810"), 1))
                painter.drawText(QRect(cx - piece_radius, cy - piece_radius, piece_radius * 2, piece_radius * 2), Qt.AlignmentFlag.AlignCenter, "♔")