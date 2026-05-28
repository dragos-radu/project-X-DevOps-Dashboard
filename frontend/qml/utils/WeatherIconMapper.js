.pragma library

function iconForCode(code) {
    switch (Number(code)) {
    case 0:
    case 1:
        return "assets/weather/clear.svg"
    case 2:
        return "assets/weather/partly-cloudy.svg"
    case 3:
        return "assets/weather/cloudy.svg"
    case 45:
    case 48:
        return "assets/weather/fog.svg"
    case 51:
    case 53:
    case 55:
        return "assets/weather/drizzle.svg"
    case 56:
    case 57:
    case 66:
    case 67:
        return "assets/weather/freezing-rain.svg"
    case 61:
    case 63:
    case 65:
        return "assets/weather/rain.svg"
    case 71:
    case 73:
    case 75:
    case 85:
    case 86:
        return "assets/weather/snow.svg"
    case 77:
        return "assets/weather/snow-grains.svg"
    case 80:
    case 81:
    case 82:
        return "assets/weather/showers.svg"
    case 95:
    case 96:
    case 99:
        return "assets/weather/thunderstorm.svg"
    default:
        return "assets/weather/unknown.svg"
    }
}
