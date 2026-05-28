import QtQuick

Canvas {
    id: chart

    property var values: [20, 35, 28, 44, 38, 52, 47, 60, 42, 24]
    property color lineColor: "#38BDF8"
    property color fillColor: "#22FFFFFF"
    property real lineWidth: 1

    width: 70
    height: 36

    onValuesChanged: requestPaint()
    onLineColorChanged: requestPaint()
    onFillColorChanged: requestPaint()
    onWidthChanged: requestPaint()
    onHeightChanged: requestPaint()

    function clamp(value, minValue, maxValue) {
        return Math.max(minValue, Math.min(maxValue, value))
    }

    function getPoints() {
        const padding = 2
        const chartWidth = width - padding * 2
        const chartHeight = height - padding * 2 // Changed from -padding to leave space at top/bottom

        let points = []

        // 1. Find current min and max values from array
        let currentMin = Math.min(...values)
        let currentMax = Math.max(...values)

        // 2. Add offset (safety margin) so chart doesn't touch extreme edges
        // If CPU varies between 2% and 8%, chart will be scaled on this interval, not 0-100%
        let minBound = Math.max(0, currentMin - 2) // Don't go below 0%
        let maxBound = Math.min(100, currentMax + 2) // Don't go above 100%

        // Prevent division by zero if all values are identical (e.g., CPU is constant at 5%)
        if (minBound === maxBound) {
            minBound = Math.max(0, minBound - 5)
            maxBound = Math.min(100, maxBound + 5)
        }

        const stepX = chartWidth / (values.length - 1)
        const valueRange = maxBound - minBound

        for (let i = 0; i < values.length; i++) {
            const value = clamp(values[i], 0, 100)

            // 3. Scale value based on the dynamically determined interval
            const normalizedValue = (value - minBound) / valueRange

            points.push({
                x: padding + i * stepX,
                // Invert Y axis (in QML, 0 is top, chartHeight is bottom)
                y: padding + chartHeight - (normalizedValue * chartHeight)
            })
        }

        return points
    }

    function addSmoothCurve(ctx, points) {
        for (let i = 0; i < points.length - 1; i++) {
            const current = points[i]
            const next = points[i + 1]
            const controlX = (current.x + next.x) / 2

            ctx.bezierCurveTo(
                controlX, current.y,
                controlX, next.y,
                next.x, next.y
            )
        }
    }

    onPaint: {
        const ctx = getContext("2d")
        ctx.clearRect(0, 0, width, height)

        if (!values || values.length < 2) {
            return
        }

        const padding = 2
        const axisY = height - padding
        const points = getPoints()

        // Fill area under curve
        ctx.beginPath()
        ctx.moveTo(points[0].x, points[0].y)

        addSmoothCurve(ctx, points)

        ctx.lineTo(points[points.length - 1].x, axisY)
        ctx.lineTo(points[0].x, axisY)
        ctx.closePath()

        ctx.fillStyle = fillColor
        ctx.fill()

        // Line on top
        ctx.beginPath()
        ctx.moveTo(points[0].x, points[0].y)

        addSmoothCurve(ctx, points)

        ctx.strokeStyle = lineColor
        ctx.lineWidth = lineWidth
        ctx.lineJoin = "miter"
        ctx.lineCap = "butt"
        ctx.stroke()
    }
}