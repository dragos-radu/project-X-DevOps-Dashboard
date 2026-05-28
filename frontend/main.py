import os
import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from controllers.system_metrics_controller import SystemMetricsController
from controllers.local_system_info_controller import LocalSystemInfoController
from controllers.weather_controller import WeatherController
from controllers.calendar_controller import CalendarController
from controllers.news_controller import NewsController


os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")


def main():
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()

    system_metrics = SystemMetricsController()
    local_system_info = LocalSystemInfoController()
    weather = WeatherController()
    calendar = CalendarController()
    news = NewsController()

    engine.rootContext().setContextProperty("systemMetrics", system_metrics)
    engine.rootContext().setContextProperty("localSystemInfo", local_system_info)
    engine.rootContext().setContextProperty("weatherController", weather)
    engine.rootContext().setContextProperty("calendarController", calendar)
    engine.rootContext().setContextProperty("newsController", news)

    engine.load("qml/Main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
