#include "datareader.h"

#include <QRotationSensor>
#include <QUdpSocket>
#include <QTimer>

#include <QDebug>

DataReader::DataReader(QObject *parent) :
    QObject(parent), m_sock(new QUdpSocket(this)), m_rotation(new QRotationSensor(this)), m_timer(new QTimer(this)) {
    m_rotation->setDataRate(5);
    setHost("147.229.179.75");
    connect(m_rotation, SIGNAL(readingChanged()), this, SLOT(newReading()));
    connect(m_timer, SIGNAL(timeout()), this, SLOT(timeout()));
}

void DataReader::checkServer() {
    if (m_sock->write("ping") <= 0) {
        emit serverMissing();
    }
    m_timer->setSingleShot(true);
    m_timer->start(3000);
}

void DataReader::timeout() {
    emit serverMissing();
    checkServer();
}

void DataReader::sendPacket(const QString &msg) {
    if (msg.length() > 0 && m_sock->write(msg.toLatin1()) <= 0)
        emit serverMissing();
}

void DataReader::setHost(const QString &name) {
    qDebug() << "setting host" << name;
    m_sock->deleteLater();
    m_sock = new QUdpSocket(this);
    connect(m_sock, SIGNAL(readyRead()), this, SLOT(readPacket()));
    m_sock->connectToHost(QHostAddress(name), 5005);
    m_sock->waitForConnected();
    checkServer();
}

void DataReader::readPacket() {
    m_timer->stop();
    while (m_sock->hasPendingDatagrams()) {
        QByteArray incomingData;
        incomingData.resize(m_sock->pendingDatagramSize());
        QHostAddress sender;
        quint16 senderPort;
        m_sock->readDatagram(incomingData.data(), incomingData.size(), &sender, &senderPort);
        if (incomingData == "ready")
            emit serverReady();
        else if (incomingData == "busy")
            emit serverBusy();
        else
            qDebug() << "Unrecognized  message, contents:" << incomingData;
    }
    checkServer();
}

void DataReader::startFight() {
    m_rotation->setActive(true);
}

void DataReader::newReading() {
    static int consecutiveFails = 0;
    int fail = m_sock->write(QString("%1;%2;%3").arg(m_rotation->reading()->x()).arg(m_rotation->reading()->y()).arg(m_rotation->reading()->z()).toLatin1());
    if (fail <= 0)
        consecutiveFails++;
    else
        consecutiveFails = 0;
    if (consecutiveFails == 100)
        emit serverMissing();
}
