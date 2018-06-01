import QtQuick 2.3
import QtQuick.Controls 1.2
import QtQuick.Controls.Styles 1.2

import QtSensors 5.3

import DataReader 1.0

ApplicationWindow {
    title: "Accelerate Bubble"
    id: mainWindow
    width: 320
    height: 480
    visible: true

    ListModel {
        id: modyModel
        ListElement {
            obrazky: [
                ListElement {
                    soubor: "food0.png"
                },
                ListElement {
                    soubor: "candy0.png"
                },
                ListElement {
                    soubor: "food1.png"
                },
                ListElement {
                    soubor: "candy1.png"
                },
                ListElement {
                    soubor: "food2.png"
                },
                ListElement {
                    soubor: "candy2.png"
                },
                ListElement {
                    soubor: "food3.png"
                },
                ListElement {
                    soubor: "candy3.png"
                },
                ListElement {
                    soubor: "food4.png"
                },
                ListElement {
                    soubor: "food5.png"
                }
            ]
        }
    }

    ListModel {
        id: zvirataModel
        ListElement {
            name: "Slon"
            soubor: "elephant.png"
        }
        ListElement {
            name: "Opice"
            soubor: "monkey.png"
        }
        ListElement {
            name: "Koza"
            soubor: "goat.png"
        }
        ListElement {
            name: "Lev"
            soubor: "lion.png"
        }
        ListElement {
            name: "Ovce"
            soubor: "sheep.png"
        }
        ListElement {
            name: "Žirafa"
            soubor: "giraffe.png"
        }
        ListElement {
            name: "Bizon"
            soubor: "bison.png"
        }
        ListElement {
            name: "Darth Vader"
            soubor: "vader.png"
        }
    }


    ListModel {
        id: zbraneModel
        ListElement {
            soubor: "elephant_weapon.png"
        }
        ListElement {
            soubor: "monkey_weapon.png"
        }
        ListElement {
            soubor: "goat_weapon.png"
        }
        ListElement {
            soubor: "lion_weapon.png"
        }
        ListElement {
            soubor: "sheep_weapon.png"
        }
        ListElement {
            soubor: "giraffe_weapon.png"
        }
        ListElement {
            soubor: "bison_weapon.png"
        }
        ListElement {
            soubor: "vader_weapon.png"
        }
    }

    DataReader {
        id: dataReader
        onServerMissing: {
            vyberButton.ready = false
        }
        onServerReady: {
            vyberButton.ready = true
        }
    }

    menuBar: MenuBar {
        Menu {
            title: qsTr("Game")
            MenuItem {
                text: qsTr("Bonus")
                onTriggered: dataReader.sendPacket("bonus")
            }

            MenuItem {
                text: qsTr("Win")
                onTriggered: dataReader.sendPacket("win")
            }

            MenuItem {
                text: qsTr("Reset")
                onTriggered: dataReader.sendPacket("reset")
            }

            MenuItem {
                text: qsTr("Špatná IP obrazovky")
                onTriggered: nastaveniIP.visible = true
            }

            MenuItem {
                text: qsTr("Exit")
                onTriggered: Qt.quit();
            }
        }
    }

    Image {
        anchors.fill: parent
        source: "mainbg.jpg"
        fillMode: Image.PreserveAspectCrop
        Rectangle {
            anchors.fill: parent
            color: "white"
            opacity: 0.5
        }
    }

    Rectangle {
        id: nastaveniIP
        anchors.fill: parent
        visible: false
        z: 2
        onVisibleChanged: ipField.text = ""
        Text {
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.margins: parent.width /32
            id: ipText
            text: "IP nebo hostname:"
            font.pixelSize: parent.width / 16
        }

        TextField {
            id: ipField
            anchors.margins: parent.width / 32
            height: parent.width / 8
            anchors.top: ipText.bottom
            anchors.left: parent.left
            anchors.right: parent.right
        }
        Button {
            anchors.margins: ipField.anchors.margins
            anchors.top: ipField.bottom
            anchors.left: parent.left
            width: ipField.width / 3
            height: ipField.height
            text: "Storno"
            onClicked: parent.visible = false
        }
        Button {
            anchors.margins: ipField.anchors.margins
            anchors.top: ipField.bottom
            anchors.right: parent.right
            width: ipField.width / 3
            height: ipField.height
            text: "OK"
            onClicked: {
                dataReader.setHost(ipField.text)
                parent.visible = false
            }
        }
    }

    Rectangle {
        id: vyber
        color: "transparent"
        anchors.fill: parent
        Behavior on x {
            NumberAnimation {
                duration: 100
            }
        }
        function hide() {
            x = -content.width
        }
        function show() {
            uvod.hide()
            x = 0
        }

        Text {
            id: vyberText
            height: 0
        }

        ListView {
            id: seznamModu
            anchors.top: vyberText.bottom
            anchors.left:parent.left
            anchors.bottom: vyberButton.top
            anchors.margins: 4
            width: parent.width / 3
            clip: true
            spacing: 8
            model: modyModel
            snapMode: ListView.SnapOneItem
            delegate:
                PathView {
                    id: nestedView
                    width: parent.width
                    height: width
                    clip: true
                    interactive: false
                    model: obrazky
                    pathItemCount: 2
                    path: Path {
                                startX: -0.5*width; startY: height/2
                                PathQuad { x: 1.5*width; y: height/2; controlX: 0.5*width; controlY: height/2}
                            }
                    snapMode: ListView.SnapOneItem
                    Timer {
                        interval: 2500
                        repeat: true
                        running: true
                        onTriggered: {
                            nestedView.currentIndex++
                            if (nestedView.currentIndex >= nestedView.count)
                                nestedView.currentIndex = 0
                        }
                    }



                    delegate: Image {
                        id: nabidkaObrazek
                        source: soubor
                        width: nestedView.width
                        height: width
                        fillMode: Image.PreserveAspectFit
                    }
                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                        }
                    }
                }

        }

        Rectangle {
            id: odd1
            width: parent.width / 160
            anchors.left: seznamModu.right
            anchors.top: parent.top
            anchors.bottom: vyberButton.top
            anchors.topMargin: parent.height / 32
            anchors.bottomMargin: parent.height / 32
        }

        ListView {
            id: seznamZvirat
            spacing: 10
            model: zvirataModel
            clip:true
            anchors.top: vyberText.bottom
            anchors.bottom: vyberButton.top
            anchors.left: odd1.right
            anchors.margins: 4
            width: parent.width / 3

            delegate: Rectangle {
                Image {
                    anchors.fill: parent
                    anchors.margins: 4
                    id: zvireKsicht
                    source: soubor
                    Timer {
                        running: true
                        onTriggered: {
                            interval = Math.random() * 5000
                            running = true
                            zvireKsichtKlepat.start() * 5000
                        }
                        repeat: false
                        interval: Math.random()
                    }

                    SequentialAnimation {
                        id: zvireKsichtKlepat
                        PropertyAnimation {
                            target: zvireKsicht
                            properties: "rotation"
                            to: 23
                            duration: 100
                        }
                        PropertyAnimation {
                            target: zvireKsicht
                            properties: "rotation"
                            to: -23
                            duration: 100
                        }
                        PropertyAnimation {
                            target: zvireKsicht
                            properties: "rotation"
                            to: 0
                            duration: 100
                        }
                    }
                    SequentialAnimation {
                        id: zvireKsichtTocit
                        PropertyAnimation {
                            target: zvireKsicht
                            properties: "rotation"
                            to: 180
                            duration: 60
                        }
                        PropertyAnimation {
                            target: zvireKsicht
                            properties: "rotation"
                            to: 360
                            duration: 60
                        }
                    }
                }

                color: "transparent"
                width: parent.width
                height: width
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        zvireKsichtTocit.start()
                        dataReader.sendPacket("ksicht:"+soubor)
                    }
                }
            }
        }

        Rectangle {
            id: odd2
            width: parent.width / 160
            anchors.left: seznamZvirat.right
            anchors.top: parent.top
            anchors.bottom: vyberButton.top
            anchors.topMargin: parent.height / 32
            anchors.bottomMargin: parent.height / 32
        }

        ListView {
            id: seznamZbrani
            spacing: 10
            model: zbraneModel
            clip:true
            anchors.top: vyberText.bottom
            anchors.bottom: vyberButton.top
            anchors.left: odd2.right
            anchors.right: parent.right
            anchors.margins: 4

            delegate: Rectangle {
                Image {
                    anchors.fill: parent
                    anchors.margins: 4
                    id: zbranObrazek
                    source: soubor
                    scale: 2
                    transform: Translate { x: -(parent.width/2) }
                }

                color: "transparent"
                width: parent.width
                height: width
                MouseArea {
                    anchors.fill: parent
                    onClicked: {
                        dataReader.sendPacket("zbran:"+soubor)
                    }
                }
            }
        }

        Rectangle {
            id: shadow
            anchors.fill: parent
            color: "#444444"
            opacity: vyberButton.ready ? 0 : 0.8
        }

        Rectangle {
            property bool ready: false

            id: vyberButton
            color: ready ? "green" : "red"
            height: parent.height / 10
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.margins: 4
            radius: 10
            z: 2

            Text {
                id: vyberButtonText
                anchors.centerIn: parent
                text: parent.ready ? "START" : "Navazuji spojení s obrazovkou"
                font.pointSize: parent.ready ? (parent.width * 0.07) : (parent.width * 0.03)
            }
            MouseArea {
                anchors.fill: parent
                property int cnt: 0
                onClicked: {
                    dataReader.sendPacket("fight")
                    dataReader.startFight()
                }
            }
        }
    }
}
