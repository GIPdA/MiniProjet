import QtQuick 1.1

Rectangle {

	property color onColor: '#16c000'
	property color offColor: '#666666'

	signal checked (bool check)

	color: offColor

	MouseArea {
		id: sensor_ma
		anchors.fill: parent

		onClicked: {
			if(parent.color == parent.offColor)
			{
				parent.checked(true)
				parent.color = parent.onColor
			}
			else
			{
				parent.checked(false)
				parent.color = parent.offColor
			}
		}
	}

}