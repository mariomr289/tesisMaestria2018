TEMPLATE = app

QT += qml quick widgets sensors svg xml network

SOURCES += main.cpp \
    datareader.cpp

RESOURCES += qml.qrc \
             ../graphics/graphics.qrc

# Additional import path used to resolve QML modules in Qt Creator's code model
QML_IMPORT_PATH =

# Default rules for deployment.
include(deployment.pri)

OTHER_FILES += \
    android/AndroidManifest.xml

HEADERS += \
    datareader.h
