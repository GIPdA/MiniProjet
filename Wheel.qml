import QtQuick 1.1

Rectangle {
    id: wheel
    objectName: 'wheel'

    property color wheelColor: '#000000'
    property color wheelRayColor: '#919191'

    property int speed: 0

    function setSpeed(wheelSpeed) {
        anim.running = false;

        if(wheelSpeed < 0)
        {
            mainWheel.reverse = true
            speed = -wheelSpeed;
        }else
        {
            mainWheel.reverse = false
            speed = wheelSpeed;
        }

        if(wheelSpeed === 0)
            anim.running = false;
        else
            anim.running = true;
    }


    Rectangle {
        id: mainWheel
        x: 11
        y: 0
        width: 63
        height: 200
        radius: 5

        property bool reverse: false

        gradient: Gradient {
            GradientStop {
                position: 0
                color: wheel.wheelColor
            }

            GradientStop {
                id:topGrad
                position: 0.220
                color: wheel.wheelRayColor
            }

            GradientStop {
                position: 1
                color: wheel.wheelColor
            }
        }
        z: 5

        SequentialAnimation {
            id: anim
            running: false
            loops: Animation.Infinite

            NumberAnimation {
                target: topGrad
                property: "position"
                //to: 0.9
                to: mainWheel.reverse ? 0.1 : 0.9
                duration: wheel.speed*10
            }

            ParallelAnimation {

                NumberAnimation {
                    target: topGrad
                    property: "position"
                    //to: 0.999
                    to: mainWheel.reverse ? 0 : 0.99
                    duration: wheel.speed
                }

                PropertyAnimation { target: botGrad; property: "position"; to: mainWheel.reverse ? 0 : 1; duration: 0 }
                PropertyAnimation { target: topGrad;  property: "color"; to: wheel.wheelColor; duration: wheel.speed*2 }
                PropertyAnimation { target: botGrad; property: "color"; to: wheel.wheelRayColor; duration: wheel.speed*2 }
            }

            NumberAnimation {
                target: botGrad
                property: "position"
                //to: 0.1
                to: mainWheel.reverse ? 0.9 : 0.1
                duration: wheel.speed*10
            }

            ParallelAnimation {

                NumberAnimation {
                    target: botGrad
                    property: "position"
                    //to: 0
                    to: mainWheel.reverse ? 0.9999 : 0
                    duration: wheel.speed
                }

                PropertyAnimation { target: topGrad; property: "position"; to: mainWheel.reverse ? 1 : 0; duration: 0 }
                PropertyAnimation { target: botGrad;  property: "color"; to: wheel.wheelColor; duration: wheel.speed*2 }
                PropertyAnimation { target: topGrad; property: "color"; to: wheel.wheelRayColor; duration: wheel.speed*2 }
            }

        }
    }

    Rectangle {
        id: subWheel
        x: 3
        y: 0
        width: 71
        height: 200
        radius: 5
        z: 1

        gradient: Gradient {
            GradientStop {
                position: 0
                color: wheel.wheelColor
            }

            GradientStop {
                id: botGrad
                position: 0.30
                color: wheel.wheelRayColor
            }

            GradientStop {
                position: 1
                color: wheel.wheelColor
            }
        }
    }

    Rectangle {
        id: lwheel1sh
        x: 0
        y: 85
        width: 80
        height: 31
        color: "#b5b2b2"
        radius: 6
        z: 2
    }
}
