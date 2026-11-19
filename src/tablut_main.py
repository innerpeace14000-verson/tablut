import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

from tablut_model import TablutModel
from tablut_view import TablutBoard

# -----------------------------------
# MainWindow
# -----------------------------------
class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tablut")

        # Instanciation du Modèle
        self.model = TablutModel()

        # Instanciation de la Vue en lui passant le modèle
        self.board_widget = TablutBoard(self.model)

        # On crée donc un QWidget générique qui va servir 
        # de conteneur principal à l'intérieur de la fenêtre.
        # main_widget joue le rôle d'intermédiaire (un simple conteneur vide) entre la MainWindow et le layout 
        # qui porte self.board_widget.
        main_widget = QWidget()

        # On crée un gestionnaire de mise en page vertical.
        layout = QVBoxLayout()

        # On ajoute la vue dans le layout
        layout.addWidget(self.board_widget)

        # On associe le layout au conteneur
        main_widget.setLayout(layout)

        # On place main_widget dans la zone centrale de la MainWindow
        self.setCentralWidget(main_widget)



# -----------------------------------
# MAIN ENTRY POINT
# -----------------------------------
if __name__ == "__main__":
    # gestion de la boucle d'événements (Event Loop)
    # initialisation du système
    # instance unique
    app = QApplication(sys.argv)

    # fenêtre principale de l'application graphique
    window = MainWindow()
    window.resize(680, 680)
    window.show()

    # démarre la boucle d'événements principale (event loop) de
    # l'application PyQt
    sys.exit(app.exec())