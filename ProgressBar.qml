import QtQuick 1.1

Rectangle {
    id: progressbar
    objectName: 'progressbar'

    width: 14
    height: 100

    signal progressValueChanged(real value)

    property color firstColor: "#ffffff"
    property color middleColor: "#ffffff"
    property color secondColor: "#00ff00"

    property real value: 0

    onValueChanged: {
        progressbar.progressValueChanged(value)

        if(value > 1) value = 1
        if(value < 0) value = 0

        gsv.position = value
    }

    gradient: Gradient {
        GradientStop {
            position: 0
            color: progressbar.secondColor
        }

        GradientStop {
            id: gsv
            position: 0
            color: progressbar.middleColor
        }

        GradientStop {
            position: 1
            color: progressbar.firstColor
        }
    }
}
