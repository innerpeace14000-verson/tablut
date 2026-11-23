from PyQt6.QtCore import QRect, Qt, QPointF
from PyQt6.QtGui import QBrush, QColor, QFont, QPainter, QPen, QPolygonF
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

PIECE_BORDER_WIDTH = 2
PIECE_INNER_RING_RATIO = 0.76
PIECE_SYMBOL_SCALE_RATIO = 0.36
PIECE_MIN_DETAIL_RADIUS = 10

WHITE_PIECE_FILL = "#EFE3C8"
WHITE_PIECE_BORDER = "#4A2E16"
WHITE_PIECE_DETAIL = "#7A4B24"

BLACK_PIECE_FILL = "#3B2414"
BLACK_PIECE_BORDER = "#1C0F07"
BLACK_PIECE_DETAIL = "#D8B98A"

KING_RADIUS_RATIO = 0.41
KING_PIECE_FILL = WHITE_PIECE_FILL
KING_PIECE_BORDER = WHITE_PIECE_BORDER
KING_PIECE_DETAIL = WHITE_PIECE_DETAIL
KING_RADIUS_RATIO = KING_RADIUS_RATIO

class TablutBoard(QWidget):

    def __init__(self, model):
        super().__init__()
        self.model = model

        # fixe la taille minimale du widget
        self.setMinimumSize(
            DEFAULT_BOARD_SIZE + 2 * MARGIN_SIDE,
            DEFAULT_BOARD_SIZE + MARGIN_TOP + MARGIN_BOTTOM,
        )

    def _draw_king_piece(
        self,
        painter: QPainter,
        center_x: float,
        center_y: float,
        king_radius: float,
    ) -> None:
        diameter = int(round(king_radius * 2))
        left = int(round(center_x - king_radius))
        top = int(round(center_y - king_radius))

        painter.setBrush(QBrush(QColor(WHITE_PIECE_FILL)))
        painter.setPen(QPen(QColor(WHITE_PIECE_BORDER), PIECE_BORDER_WIDTH))
        painter.drawEllipse(left, top, diameter, diameter)

        painter.setFont(QFont("Arial", int(round(king_radius * 0.9)), QFont.Weight.Bold))
        painter.setPen(QPen(QColor(WHITE_PIECE_DETAIL), 1))
        painter.drawText(
            QRect(left, top, diameter, diameter),
            Qt.AlignmentFlag.AlignCenter,
            "♔",
        )    
    
    def _draw_standard_piece(
    self,
    painter: QPainter,
    center_x: float,
    center_y: float,
    radius: float,
    is_white: bool,
    ) -> None:
        if is_white:
            fill_color = QColor(WHITE_PIECE_FILL)
            border_color = QColor(WHITE_PIECE_BORDER)
            detail_color = QColor(WHITE_PIECE_DETAIL)
        else:
            fill_color = QColor(BLACK_PIECE_FILL)
            border_color = QColor(BLACK_PIECE_BORDER)
            detail_color = QColor(BLACK_PIECE_DETAIL)

        # Disque principal du pion
        painter.setPen(QPen(border_color, PIECE_BORDER_WIDTH))
        painter.setBrush(QBrush(fill_color))
        painter.drawEllipse(QPointF(center_x, center_y), radius, radius)

        # Anneau intérieur et motif géométrique gravé si la taille le permet
        if radius >= PIECE_MIN_DETAIL_RADIUS:
            ring_radius = radius * PIECE_INNER_RING_RATIO
            painter.setPen(QPen(detail_color, 1.2))
            painter.setBrush(Qt.BrushStyle.NoBrush)
            painter.drawEllipse(QPointF(center_x, center_y), ring_radius, ring_radius)

            # Losange / motif central gravé mis à l'échelle du rayon
            sym_size = radius * PIECE_SYMBOL_SCALE_RATIO
            diamond = QPolygonF(
                [
                    QPointF(center_x, center_y - sym_size),
                    QPointF(center_x + sym_size, center_y),
                    QPointF(center_x, center_y + sym_size),
                    QPointF(center_x - sym_size, center_y),
                ]
            )
            painter.setBrush(QBrush(detail_color))
            painter.drawPolygon(diamond)

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
                center_x = offset_x + (c + 0.5) * cell_size
                center_y = offset_y + (r + 0.5) * cell_size
                piece_radius = cell_size * PIECE_RADIUS_RATIO
                self._draw_standard_piece(
                    painter=painter,
                    center_x=center_x,
                    center_y=center_y,
                    radius=piece_radius,
                    is_white=False,
                )
 
            elif piece_type == 'WHITE':
                center_x = offset_x + (c + 0.5) * cell_size
                center_y = offset_y + (r + 0.5) * cell_size
                piece_radius = cell_size * PIECE_RADIUS_RATIO
                self._draw_standard_piece(
                    painter=painter,
                    center_x=center_x,
                    center_y=center_y,
                    radius=piece_radius,
                    is_white=True,
                )
      
            elif piece_type == 'KING':
                center_x = offset_x + (c + 0.5) * cell_size
                center_y = offset_y + (r + 0.5) * cell_size
                king_radius = cell_size * KING_RADIUS_RATIO

                self._draw_king_piece(
                    painter=painter,
                    center_x=center_x,
                    center_y=center_y,
                    king_radius=king_radius,
                )
  