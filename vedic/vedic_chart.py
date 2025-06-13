import argparse
from datetime import datetime

try:
    import swisseph as swe
except ImportError as e:
    raise SystemExit("This script requires the 'swisseph' package. Install it via pip: pip install pyswisseph")

def compute_chart(date_str, lat, lon):
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M")
    jd = swe.julday(date.year, date.month, date.day, date.hour + date.minute / 60.0)

    planets = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE,
        'Ketu': swe.TRUE_NODE,
    }

    positions = {}
    for name, planet in planets.items():
        lon, lat0, dist = swe.calc_ut(jd, planet)
        positions[name] = lon
    return positions

def main():
    parser = argparse.ArgumentParser(description='Basic Vedic astrology chart calculator')
    parser.add_argument('datetime', help='Date and time in YYYY-MM-DD HH:MM format (UTC)')
    parser.add_argument('latitude', type=float, help='Latitude of birthplace')
    parser.add_argument('longitude', type=float, help='Longitude of birthplace')
    args = parser.parse_args()
    positions = compute_chart(args.datetime, args.latitude, args.longitude)
    for body, lon in positions.items():
        print(f"{body}: {lon:.2f} degrees")

if __name__ == '__main__':
    main()
