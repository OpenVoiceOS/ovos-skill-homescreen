/*
    SPDX-FileCopyrightText: 2023 Aditya Mehra <aix.m@outlook.com>
    SPDX-License-Identifier: Apache-2.0
*/

import QtQuick.Layouts 1.15
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Window 2.15
import org.kde.kirigami 2.19 as Kirigami
import Qt5Compat.GraphicalEffects
import Mycroft 1.0 as Mycroft

Control {
    id: appEntryDelegate
    leftInset: 1
    rightInset: 1
    topInset: 1
    bottomInset: 1
    padding: 12

    background: Rectangle {
        id: delBackground
        color: Qt.darker(Kirigami.Theme.backgroundColor, 2)
        radius: 6
    }

    contentItem: Column {

        Item {
            width: parent.width
            height: parent.height / 2

            Image {
                width: parent.width < parent.height ? parent.width : parent.height
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.verticalCenter: parent.verticalCenter
                height: width
                source: model.thumbnail
            }
        }

        Label {
            width: parent.width
            height: parent.height / 2
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignVCenter
            color: Kirigami.Theme.textColor
            text: model.name
            wrapMode: Text.Wrap
            font.capitalization: Font.Capitalize
            font.pixelSize: 22
            elide: Text.ElideRight
        }
    }

    MouseArea {
        anchors.fill: parent

        onClicked: (mouse)=> {
            delBackground.color = Qt.rgba(Kirigami.Theme.highlightColor.r, Kirigami.Theme.highlightColor.g, Kirigami.Theme.highlightColor.b, 0.8)
            delBackground.color = Qt.darker(Kirigami.Theme.backgroundColor, 2)
            appBarRoot.close()
            Mycroft.SoundEffects.playClickedSound(Qt.resolvedUrl("sounds/clicked.wav"))
            Mycroft.MycroftController.sendRequest(model.action, {})
        }
    }
}
