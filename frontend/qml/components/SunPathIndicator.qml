import QtQuick

Item {
    id: root

    property string sunriseTime: "05:42"
    property string sunsetTime: "20:48"
    property date currentDateTime: new Date()

    readonly property bool isDaytime: isCurrentTimeDaytime()
    readonly property real phaseProgress: currentPhaseProgress()
    readonly property real markerProgress: phaseProgress
    readonly property string leftTimeText: isDaytime ? sunriseTime : sunsetTime
    readonly property string rightTimeText: isDaytime ? sunsetTime : sunriseTime

    implicitWidth: 128
    implicitHeight: 30

    function minutesForTime(value) {
        const parts = value.split(":")
        if (parts.length !== 2) {
            return 0
        }

        const hours = parseInt(parts[0], 10)
        const minutes = parseInt(parts[1], 10)
        if (isNaN(hours) || isNaN(minutes)) {
            return 0
        }

        return hours * 60 + minutes
    }

    function currentMinutes() {
        return currentDateTime.getHours() * 60 + currentDateTime.getMinutes()
    }

    function isCurrentTimeDaytime() {
        const sunrise = minutesForTime(sunriseTime)
        const sunset = minutesForTime(sunsetTime)
        const now = currentMinutes()

        return sunset > sunrise && now >= sunrise && now <= sunset
    }

    function currentPhaseProgress() {
        const sunrise = minutesForTime(sunriseTime)
        const sunset = minutesForTime(sunsetTime)
        const now = currentMinutes()

        if (sunset <= sunrise) {
            return 0
        }

        if (isCurrentTimeDaytime()) {
            return Math.max(0, Math.min(1, (now - sunrise) / (sunset - sunrise)))
        }

        const nightDuration = (24 * 60 - sunset) + sunrise
        const nightElapsed = now > sunset ? now - sunset : (24 * 60 - sunset) + now
        return Math.max(0, Math.min(1, nightElapsed / nightDuration))
    }

    function pointOnArc(progress, night) {
        const left = 8
        const right = width - 8
        const baseY = height - 8
        const peakY = night ? 12 : 5
        const x = left + (right - left) * progress
        const curve = Math.sin(Math.PI * progress)
        const y = baseY - (baseY - peakY) * curve

        return Qt.point(x, y)
    }

    Canvas {
        id: arcCanvas

        anchors.fill: parent

        onPaint: {
            const ctx = getContext("2d")
            const left = 8
            const right = width - 8
            const dayBaseY = height - 8
            const dayPeakY = 5
            const nightBaseY = dayBaseY
            const nightPeakY = 12

            ctx.clearRect(0, 0, width, height)

            ctx.lineWidth = 1
            ctx.strokeStyle = "rgba(248, 249, 250, 0.12)"
            ctx.beginPath()
            ctx.moveTo(left, height - 6)
            ctx.lineTo(right, height - 6)
            ctx.stroke()

            const dayGradient = ctx.createLinearGradient(left, 0, right, 0)
            dayGradient.addColorStop(0, "rgba(250, 204, 21, 0.12)")
            dayGradient.addColorStop(0.5, "rgba(250, 204, 21, 0.38)")
            dayGradient.addColorStop(1, "rgba(250, 204, 21, 0.12)")

            ctx.lineWidth = 1.1
            ctx.strokeStyle = dayGradient
            ctx.beginPath()
            ctx.moveTo(left, dayBaseY)
            ctx.quadraticCurveTo(width / 2, dayPeakY, right, dayBaseY)
            ctx.stroke()

            ctx.lineWidth = 1.1
            ctx.strokeStyle = "rgba(148, 163, 184, 0.16)"
            ctx.beginPath()
            ctx.moveTo(left, nightBaseY)
            ctx.quadraticCurveTo(width / 2, nightPeakY, right, nightBaseY)
            ctx.stroke()

            ctx.fillStyle = "rgba(248, 249, 250, 0.34)"
            ctx.beginPath()
            ctx.arc(left, dayBaseY, 2, 0, Math.PI * 2)
            ctx.fill()

            ctx.beginPath()
            ctx.arc(right, dayBaseY, 2, 0, Math.PI * 2)
            ctx.fill()

            ctx.lineWidth = 2.2
            ctx.strokeStyle = root.isDaytime ? "rgba(250, 204, 21, 0.78)" : "rgba(203, 213, 225, 0.46)"
            ctx.beginPath()

            const steps = 24
            if (root.isDaytime) {
                ctx.moveTo(left, dayBaseY)
                for (let i = 1; i <= steps; i++) {
                    const stepProgress = root.markerProgress * i / steps
                    const point = root.pointOnArc(stepProgress, false)
                    ctx.lineTo(point.x, point.y)
                }
            } else {
                ctx.moveTo(left, nightBaseY)
                for (let j = 1; j <= steps; j++) {
                    const stepProgress = root.phaseProgress * j / steps
                    const nightPoint = root.pointOnArc(stepProgress, true)
                    ctx.lineTo(nightPoint.x, nightPoint.y)
                }
            }

            ctx.stroke()
        }
    }

    Item {
        id: marker

        readonly property point arcPoint: root.pointOnArc(root.markerProgress, !root.isDaytime)

        width: root.isDaytime ? 12 : 14
        height: root.isDaytime ? 12 : 14
        x: arcPoint.x - width / 2
        y: arcPoint.y - height / 2

        Behavior on x {
            NumberAnimation {
                duration: 180
                easing.type: Easing.OutCubic
            }
        }

        Behavior on y {
            NumberAnimation {
                duration: 180
                easing.type: Easing.OutCubic
            }
        }

        Rectangle {
            visible: root.isDaytime
            anchors.centerIn: parent
            width: parent.width + 16
            height: parent.height + 16
            radius: width / 2
            color: "#FACC15"
            opacity: 0.10
        }

        Rectangle {
            visible: root.isDaytime
            anchors.centerIn: parent
            width: parent.width + 8
            height: parent.height + 8
            radius: width / 2
            color: "#FACC15"
            opacity: 0.18
        }

        Rectangle {
            visible: root.isDaytime
            anchors.fill: parent
            radius: width / 2
            color: "#FACC15"
            opacity: 0.98
        }

        Rectangle {
            visible: root.isDaytime
            anchors.centerIn: parent
            width: parent.width * 0.38
            height: parent.height * 0.38
            radius: width / 2
            color: "#FFF7AD"
            opacity: 0.9
        }

        Rectangle {
            visible: !root.isDaytime
            anchors.centerIn: parent
            width: parent.width + 10
            height: parent.height + 10
            radius: width / 2
            color: "#CBD5E1"
            opacity: 0.08
        }

        Rectangle {
            visible: !root.isDaytime
            anchors.fill: parent
            radius: width / 2
            color: "#CBD5E1"
            opacity: 0.76
        }

        Rectangle {
            visible: !root.isDaytime
            width: parent.width
            height: parent.height
            radius: width / 2
            color: "#071426"
            x: 4
            y: -1
        }
    }

    Timer {
        interval: 60000
        running: true
        repeat: true

        onTriggered: root.currentDateTime = new Date()
    }

    onCurrentDateTimeChanged: arcCanvas.requestPaint()
    onSunriseTimeChanged: arcCanvas.requestPaint()
    onSunsetTimeChanged: arcCanvas.requestPaint()
    onWidthChanged: arcCanvas.requestPaint()
    onHeightChanged: arcCanvas.requestPaint()

    Component.onCompleted: arcCanvas.requestPaint()
}
