import sys
from typing import *

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox

from functions import *

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.show()

        self.pushButton_model.clicked.connect(self.modeling_button_clicked)
        self.pushButton_graph_lambda.clicked.connect(
            self.graph_generator_intensity_button_clicked)
        self.pushButton_graph_mu.clicked.connect(
            self.graph_processor_intensity_button_clicked)
        self.pushButton_graph_workload.clicked.connect(
            self.graph_workload_button_clicked)

    def graph_generator_intensity_button_clicked(self):
        num_requests = self.input_num_requests.value()
        view_generator_intensity(
            start=1,
            end=30,
            N=num_requests,
        )

    def graph_processor_intensity_button_clicked(self):
        num_requests = self.input_num_requests.value()
        view_processor_intensity(
            start=1,
            end=10,
            N=num_requests,
        )

    def graph_workload_button_clicked(self):
        num_requests = self.input_num_requests.value()
        view_workload(
            start=0.01,
            end=1.0,
            N=num_requests,
        )

    def modeling_button_clicked(self):
        try:
            round_to = 3
            num_requests = self.input_num_requests.value()
            result = modelling(
                num_requests=num_requests,
                generator_intensity=self.input_intens_generator.value(),
                generator_range=0,
                processor_intensity=self.input_intens_processor.value(),
                processor_range=0,
            )

            workload_theory = float(self.input_intens_generator.value(
            ))/float(self.input_intens_processor.value())

            self.res_theor_zagr.setText(str(round(workload_theory, round_to)))

            workload_fact = result['workload']
            self.res_fact_zagr.setText(str(round(workload_fact, round_to)))
            self.res_exp_modelling_time.setText(
                str(round(result['time'], round_to)))
            self.res_exp_mean_time_in_queue.setText(
                str(round(result['mean_time_in_queue'], round_to)))

        except Exception as e:
            error_msg = QMessageBox()
            error_msg.setText('Ошибка!\n' + repr(e))
            error_msg.show()
            error_msg.exec()


if __name__ == "__main__":
    app = QApplication([])
    application = MainWindow()
    application.show()

    sys.exit(app.exec())
