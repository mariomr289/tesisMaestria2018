#include <QApplication>
#include <QtQml>
#include <QQmlApplicationEngine>

#include "datareader.h"

int main(int argc, char *argv[])
{
    QApplication app(argc, argv);
    qmlRegisterType<DataReader>("DataReader", 1, 0, "DataReader");

    QQmlApplicationEngine engine;
//    new DataReader(&app);
    engine.load(QUrl(QStringLiteral("qrc:/main.qml")));

    return app.exec();
}
