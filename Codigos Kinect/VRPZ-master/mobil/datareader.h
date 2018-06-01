#ifndef DATAREADER_H
#define DATAREADER_H

#include <QObject>

class QUdpSocket;
class QRotationSensor;
class QTimer;
class DataReader : public QObject
{
    Q_OBJECT
public:
    explicit DataReader(QObject *parent = 0);

signals:
    void serverReady();
    void serverMissing();
    void serverBusy();

public slots:
    void checkServer();
    void sendPacket(const QString &data);
    void readPacket();
    void startFight();
    void setHost(const QString &name);
private slots:
    void newReading();
    void timeout();
private:
    QUdpSocket *m_sock;
    QRotationSensor *m_rotation;
    QTimer *m_timer;
};

#endif // DATAREADER_H
