
import QtQuick 1.1

Rectangle {
    width: 360
    height: 360
    Text {
        anchors.centerIn: parent
        text: "Hello World"
    }

    Rectangle {
        id: base
        width: 200
        height: 200

        Rectangle {
            id: navbar

            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            height: 20

            color: "green"

            MouseArea {
                id: mouseRegion
                anchors.fill: parent;
                property variant clickPos: "1,1"

                onPressed: {
                    clickPos  = Qt.point(mouse.x,mouse.y)
                }

                onPositionChanged: {
                    var delta = Qt.point(mouse.x-clickPos.x, mouse.y-clickPos.y)
                    base.pos = Qt.point(base.pos.x+delta.x,
                                        base.pos.y+delta.y)
                }
            }
        }

        Rectangle {
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: navbar.bottom

            color: "red"
        }
    }
}
