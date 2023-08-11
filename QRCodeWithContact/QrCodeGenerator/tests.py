def get_gps_url(latitude, longitude):
    base_url = "https://www.openstreetmap.org/?mlat={}&mlon={}&zoom=14"
    return base_url.format(latitude, longitude)


def main():
    latitude = 22.9563  # Replace with your desired latitude
    longitude = 72.6125  # Replace with your desired longitude

    gps_url = get_gps_url(latitude, longitude)

    print("OpenStreetMap URL:", gps_url)


if __name__ == "__main__":
    main()
