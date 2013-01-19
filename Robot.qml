// import QtQuick 1.0 // to target S60 5th Edition or Maemo 5
import QtQuick 1.1

Rectangle {
    id: robot
    objectName: 'bot'
    width: 600
    height: 500


    transform: Rotation {
        id: robotRotation
        objectName: 'robotRotation'
        origin.x: robot.x + robot.width/2
        origin.y: robot.y + robot.height/2
        angle: 0
    }



    Wheel {
        id: leftWheel
        objectName: 'leftWheel'
        x: 92
        y: 150
        z: 5
    }

    Wheel {
        id: rightWheel
        objectName: 'rightWheel'
        x: 431
        y: 150
        z: 5
    }


    Rectangle {
        id: rwheel1sh
        x: 388
        y: 235
        width: 78
        height: 31
        color: "#b5b2b2"
        radius: 6
        z: 1
    }



    Rectangle {
        id: rectangle1
        x: 200
        y: 151
        width: 200
        height: 200
        color: "#5e5b66"
        z: 4

        Rectangle {
            id: rectangle2
            x: 6
            y: 7
            width: 18
            height: 18
            color: "#ffffff"
            radius: 200
        }

        Rectangle {
            id: rectangle3
            x: 175
            y: 7
            width: 18
            height: 18
            color: "#ffffff"
            radius: 200
        }

        Rectangle {
            id: rectangle5
            x: 6
            y: 176
            width: 18
            height: 18
            color: "#ffffff"
            radius: 200
        }

        Rectangle {
            id: rectangle6
            x: 175
            y: 176
            width: 18
            height: 18
            color: "#ffffff"
            radius: 200
        }
    }



    Sensor {
        id: sens_fm
        objectName: 'sens_fm'
        x: 276
        y: 51
        width: 26
        height: 12
        offColor: "#666666"
        onColor: "#16c000"
        radius: 200
        z: 1
    }

    Sensor {
        id: sens_fr2
        objectName: 'sens_fr2'
        x: 413
        y: 109
        width: 26
        height: 12
        offColor: "#666666"
        onColor: "#16c000"
        radius: 200
        z: 2
        rotation: 48
    }

    Sensor {
        id: sens_fr1
        objectName: 'sens_fr1'
        x: 357
        y: 69
        width: 26
        height: 12
        offColor: "#666666"
        onColor: "#16c000"
        radius: 200
        z: 1
        rotation: 28
    }

    Sensor {
        id: sens_fl2
        objectName: 'sens_fl2'
        x: 142
        y: 108
        width: 26
        height: 14
        offColor: "#666666"
        onColor: "#16c000"
        radius: 200
        rotation: -45
        z: 1
    }

    Sensor {
        id: sens_fl1
        objectName: 'sens_fl1'
        x: 199
        y: 67
        width: 26
        height: 14
        offColor: "#666666"
        onColor: "#16c000"
        radius: 200
        z: 2
        rotation: -20
    }


    Sensor {
        id: sens_rr1
        objectName: 'sens_rr1'
        x: 382
        y: 406
        width: 26
        height: 12
        offColor: "#666666"
        onColor: "#16c000"
        radius: 200
        z: 2
        rotation: -38
    }

    Sensor {
        id: sens_rl1
        objectName: 'sens_rl1'
        x: 171
        y: 407
        width: 26
        height: 12
        offColor: "#666666"
        onColor: "#16c000"
        radius: 200
        rotation: 35
        z: 2
    }



    Rectangle {
        id: rectangle7
        x: 184
        y: 151
        width: 45
        height: 200
        color: "#4d4b53"
        z: 1
    }

    Rectangle {
        id: rectangle12
        x: 154
        y: 235
        width: 45
        height: 31
        color: "#b5b2b2"
        radius: 114
        z: 4
    }



    Rectangle {
        id: body
        x: 94
        y: 51
        width: 389
        height: 400
        color: "#09015a"
        radius: 200
        z: 0
    }

    Rectangle {
        id: body1
        x: 118
        y: 63
        width: 348
        height: 376
        color: "#8d8d8d"
        radius: 200
        z: 0
    }

    Rectangle {
        id: body2
        x: 113
        y: 67
        width: 344
        height: 371
        color: "#dbd8d8"
        radius: 200
        z: 0

        Text {
            id: text1
            x: 105
            y: 9
            width: 144
            height: 57
            color: "#474141"
            text: qsTr("Wulka ™")
            font.family: "Noteworthy"
            horizontalAlignment: Text.AlignHCenter
            font.pixelSize: 32
        }

        Text {
            id: text2
            x: 148
            y: 36
            width: 144
            height: 57
            color: "#474141"
            text: qsTr("Bot")
            font.pixelSize: 26
            font.family: "Noteworthy"
            horizontalAlignment: Text.AlignHCenter
        }
    }



    Rectangle {
        id: rearDirWheel
        z: 6


        transform: Rotation {
            id: robotDirWheelRotation
            objectName: 'robotDirWheelRotation'
            origin.x: rectangle11.x+rectangle11.width/2
            origin.y: rectangle11.y+rectangle11.height/2
            angle: 0
        }

        Rectangle {
            id: rectangle8
            x: 272
            y: 393
            width: 30
            height: 97
            radius: 5
            gradient: Gradient {
                GradientStop {
                    position: 0
                    color: "#272525"
                }

                GradientStop {
                    position: 0.210
                    color: "#585757"
                }

                GradientStop {
                    position: 1
                    color: "#000000"
                }
            }
            z: 4
        }

        Rectangle {
            id: rwheel3sh
            x: 245
            y: 429
            width: 85
            height: 25
            color: "#b5b2b2"
            radius: 6
            z: 1
        }

        Rectangle {
            id: rectangle9
            x: 254
            y: 367
            width: 16
            height: 97
            color: "#4f4a4a"
            z: 4
        }

        Rectangle {
            id: rectangle10
            x: 304
            y: 367
            width: 16
            height: 97
            color: "#4f4a4a"
            z: 4
        }

        Rectangle {
            id: rectangle11
            x: 245
            y: 351
            width: 83
            height: 83
            color: "#6b6666"
            radius: 200
        }
    }



    MouseArea {
        id: sfm_ma
        objectName: 'sfm_ma'
        x: 268
        y: 0
        width: 40
        height: 51

        hoverEnabled: true
        onPositionChanged: {
            sfm_value.value = (height - mouse.y) / height
        }
        onExited: {
            sfm_value.value = 0
        }
    }

    MouseArea {
        id: sfr1_ma
        objectName: 'sfr1_ma'
        x: 360
        y: -25
        width: 69
        height: 100
        rotation: 25

        hoverEnabled: true
        onPositionChanged: {
            sfr1_value.value = (height - mouse.y) / height
        }
        onExited: {
            sfr1_value.value = 0
        }
    }

    MouseArea {
        id: sfr2_ma
        objectName: 'sfr2_ma'
        x: 456
        y: -16
        width: 60
        height: 150
        rotation: 45

        hoverEnabled: true
        onPositionChanged: {
            sfr2_value.value = (height - mouse.y) / height
        }
        onExited: {
            sfr2_value.value = 0
        }
    }

    MouseArea {
        id: sfl1_ma
        objectName: 'sfl1_ma'
        x: 153
        y: -28
        width: 69
        height: 100
        rotation: -25

        hoverEnabled: true
        onPositionChanged: {
            sfl1_value.value = (height - mouse.y) / height
        }
        onExited: {
            sfl1_value.value = 0
        }
    }

    MouseArea {
        id: sfl2_ma
        objectName: 'sfl2_ma'
        x: 65
        y: -18
        width: 60
        height: 150
        rotation: -45

        hoverEnabled: true
        onPositionChanged: {
            sfl2_value.value = (height - mouse.y) / height
        }
        onExited: {
            sfl2_value.value = 0
        }
    }

    MouseArea {
        id: srr1_ma
        objectName: 'srr1_ma'
        x: 393
        y: 410
        width: 69
        height: 100
        rotation: -35

        hoverEnabled: true
        onPositionChanged: {
            srr1_value.value = 1-(height - mouse.y) / height
        }
        onExited: {
            srr1_value.value = 0
        }
    }

    MouseArea {
        id: srl1_ma
        objectName: 'srl1_ma'
        x: 116
        y: 410
        width: 69
        height: 100
        rotation: 35

        hoverEnabled: true
        onPositionChanged: {
            srl1_value.value = 1-(height - mouse.y) / height
        }
        onExited: {
            srl1_value.value = 0
        }
    }



    ProgressBar {
        id: sfm_value
        objectName: 'sfm_value'
        x: 282
        y: 2
        width: 14
        height: 51
        value: 0
        firstColor: "#ffffff"
        middleColor: "#ffffff"
        secondColor: "#00ff00"
        rotation: 180
    }

    ProgressBar {
        id: sfl2_value
        objectName: 'sfl2_value'
        x: 91
        y: -18
        width: 14
        height: 150
        value: 0
        firstColor: "#ffffff"
        middleColor: "#ffffff"
        secondColor: "#00ff00"
        rotation: -45+180
    }

    ProgressBar {
        id: sfl1_value
        objectName: 'sfl1_value'
        x: 182
        y: -27
        width: 14
        height: 100
        value: 0
        firstColor: "#ffffff"
        middleColor: "#ffffff"
        secondColor: "#00ff00"
        rotation: -25+180
    }

    ProgressBar {
        id: sfr1_value
        objectName: 'sfr1_value'
        x: 386
        y: -24
        width: 14
        height: 100
        value: 0
        firstColor: "#ffffff"
        middleColor: "#ffffff"
        secondColor: "#00ff00"
        rotation: 25+180
    }

    ProgressBar {
        id: sfr2_value
        objectName: 'sfr2_value'
        x: 475
        y: -15
        width: 14
        height: 150
        value: 0

        firstColor: "#ffffff"
        middleColor: "#ffffff"
        secondColor: "#00ff00"

        rotation: 45+180
    }


    ProgressBar {
        id: srr1_value
        objectName: 'srr1_value'
        x: 419
        y: 406
        width: 14
        height: 100
        value: 0

        firstColor: "#ffffff"
        middleColor: "#ffffff"
        secondColor: "#00ff00"

        rotation: -35
    }

    ProgressBar {
        id: srl1_value
        objectName: 'srl1_value'
        x: 146
        y: 408
        width: 14
        height: 100
        value: 0

        firstColor: "#ffffff"
        middleColor: "#ffffff"
        secondColor: "#00ff00"

        rotation: 35
    }




}
