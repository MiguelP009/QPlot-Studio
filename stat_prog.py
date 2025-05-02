import sys
import os
import re
import json
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QListWidget, QComboBox, QMessageBox,
    QSplitter, QTextEdit, QListWidgetItem, QFileDialog, QMenu, QAction
)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator

DATA_FILE = "questions.json"

class DiagramApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Créateur de Diagrammes - Questionnaire")
        self.setGeometry(100, 100, 1200, 800)

        self.responses = {}
        self.saved_questions = {}
        self.load_saved_questions()

        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout()

        # Menu latéral
        self.project_list = QListWidget()
        self.project_list.itemClicked.connect(self.load_project_question)
        self.project_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.project_list.customContextMenuRequested.connect(self.open_context_menu)

        # Panel principal avec Splitter
        central_splitter = QSplitter(Qt.Vertical)

        top_panel = QWidget()
        top_layout = QVBoxLayout()

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Entrez la question")
        top_layout.addWidget(QLabel("Question :"))
        top_layout.addWidget(self.question_input)

        answer_layout = QHBoxLayout()
        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Réponse")
        self.count_input = QLineEdit()
        self.count_input.setPlaceholderText("Nombre")
        add_button = QPushButton("Ajouter")
        add_button.clicked.connect(self.add_response)

        answer_layout.addWidget(self.answer_input)
        answer_layout.addWidget(self.count_input)
        answer_layout.addWidget(add_button)
        top_layout.addLayout(answer_layout)

        self.response_list = QListWidget()
        top_layout.addWidget(self.response_list)

        question_action_layout = QHBoxLayout()
        add_project_button = QPushButton("Ajouter au projet")
        add_project_button.clicked.connect(self.save_question_to_project)
        new_question_button = QPushButton("Nouvelle question")
        new_question_button.clicked.connect(self.reset_fields)
        question_action_layout.addWidget(add_project_button)
        question_action_layout.addWidget(new_question_button)
        top_layout.addLayout(question_action_layout)

        top_panel.setLayout(top_layout)

        # Partie graphique
        bottom_panel = QWidget()
        bottom_layout = QVBoxLayout()

        chart_layout = QHBoxLayout()
        self.chart_selector = QComboBox()
        self.chart_selector.addItems(["Barres", "Camembert", "Histogramme", "Ligne"])
        chart_layout.addWidget(QLabel("Type de diagramme :"))
        chart_layout.addWidget(self.chart_selector)

        self.plot_button = QPushButton("Afficher")
        self.plot_button.clicked.connect(self.plot_chart)
        chart_layout.addWidget(self.plot_button)

        self.save_button = QPushButton("Enregistrer")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_chart)
        chart_layout.addWidget(self.save_button)

        bottom_layout.addLayout(chart_layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        bottom_layout.addWidget(self.canvas)

        bottom_panel.setLayout(bottom_layout)

        # Splitter pour redimensionner dynamiquement
        central_splitter.addWidget(top_panel)
        central_splitter.addWidget(bottom_panel)
        central_splitter.setSizes([400, 400])

        main_layout.addWidget(self.project_list, 1)
        main_layout.addWidget(central_splitter, 4)
        self.setLayout(main_layout)
        self.setStyleSheet(self.load_qss())

        self.refresh_project_list()

    def add_response(self):
        answer = self.answer_input.text().strip()
        count_text = self.count_input.text().strip()
        if not answer or not count_text:
            QMessageBox.warning(self, "Champs manquants", "Veuillez remplir tous les champs.")
            return

        try:
            count = int(count_text)
        except ValueError:
            QMessageBox.critical(self, "Erreur", "Le nombre doit être un entier.")
            return

        self.responses[answer] = count
        self.response_list.addItem(f"{answer} : {count}")
        self.answer_input.clear()
        self.count_input.clear()

    def plot_chart(self):
        question = self.question_input.text().strip()
        if not question or not self.responses:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une question et des réponses.")
            return

        self.figure.clear()
        ax = self.figure.add_subplot(111)

        labels = list(self.responses.keys())
        values = list(self.responses.values())
        chart = self.chart_selector.currentText()

        if chart == "Barres":
            ax.bar(labels, values, color='lightblue')
            ax.set_ylabel("Nombre de personnes")
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.tick_params(axis='x', rotation=45)
        elif chart == "Camembert":
            ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=140)
            ax.axis('equal')
        elif chart == "Histogramme":
            ax.hist(values, bins=range(min(values), max(values)+2), color='orange', edgecolor='black')
            ax.set_xlabel("Valeurs")
            ax.set_ylabel("Fréquence")
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        elif chart == "Ligne":
            ax.plot(labels, values, marker='o', color='green')
            ax.set_ylabel("Nombre de personnes")
            ax.yaxis.set_major_locator(MaxNLocator(integer=True))
            ax.tick_params(axis='x', rotation=45)

        ax.set_title(question)
        self.canvas.draw()
        self.save_button.setEnabled(True)

    def save_chart(self):
        question = self.question_input.text().strip()
        chart_type = self.chart_selector.currentText().lower()
        if not question:
            QMessageBox.warning(self, "Erreur", "Veuillez entrer une question.")
            return

        filename = re.sub(r'[^\w\s-]', '', question).strip().replace(' ', '_')[:50]
        full_name = f"{filename}_{chart_type}.png"

        try:
            self.figure.savefig(full_name)
            QMessageBox.information(self, "Succès", f"Diagramme enregistré sous : {full_name}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur d'enregistrement : {str(e)}")

    def save_question_to_project(self):
        question = self.question_input.text().strip()
        if not question or not self.responses:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir une question et ses réponses.")
            return

        self.saved_questions[question] = self.responses.copy()
        self.save_to_file()
        self.refresh_project_list()
        QMessageBox.information(self, "Ajouté", f"Question ajoutée au projet : {question}")

    def load_project_question(self, item: QListWidgetItem):
        question = item.text()
        self.question_input.setText(question)
        self.responses = self.saved_questions.get(question, {})
        self.response_list.clear()
        for k, v in self.responses.items():
            self.response_list.addItem(f"{k} : {v}")

    def refresh_project_list(self):
        self.project_list.clear()
        for q in self.saved_questions.keys():
            self.project_list.addItem(q)

    def reset_fields(self):
        self.question_input.clear()
        self.answer_input.clear()
        self.count_input.clear()
        self.response_list.clear()
        self.responses = {}
        self.save_button.setEnabled(False)
        self.canvas.figure.clear()
        self.canvas.draw()

    def open_context_menu(self, position: QPoint):
        item = self.project_list.itemAt(position)
        if item:
            menu = QMenu()
            delete_action = QAction("Supprimer", self)
            delete_action.triggered.connect(lambda: self.delete_question(item))
            menu.addAction(delete_action)
            menu.exec_(self.project_list.viewport().mapToGlobal(position))

    def delete_question(self, item: QListWidgetItem):
        question = item.text()
        reply = QMessageBox.question(self, "Supprimer", f"Supprimer la question : '{question}' ?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            if question in self.saved_questions:
                del self.saved_questions[question]
                self.save_to_file()
                self.refresh_project_list()
                self.reset_fields()

    def save_to_file(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.saved_questions, f, indent=2, ensure_ascii=False)

    def load_saved_questions(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.saved_questions = json.load(f)
            except Exception:
                self.saved_questions = {}

    def load_qss(self):
        return """
            QWidget {
                font-family: 'Segoe UI';
                font-size: 13px;
                background-color: #2b2b2b;
                color: #f0f0f0;
            }
            QLineEdit, QComboBox, QListWidget, QPushButton {
                padding: 6px;
                border: 1px solid #555;
                border-radius: 4px;
                background-color: #3c3c3c;
            }
            QPushButton:hover {
                background-color: #505050;
            }
            QListWidget::item:selected {
                background-color: #007acc;
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DiagramApp()
    window.show()
    sys.exit(app.exec_())
