import requests
import config
import datetime


def get_available_relevant_date_times():
    available_dates = []
    for i in range(config.next_months + 1):
        month = (datetime.datetime.now().month + i) % 12
        year = datetime.datetime.now().year + (datetime.datetime.now().month + i) // 12
        print(f"Checking availability for {year}/{month}")
        url = (
            f"https://widget-api.formitable.com/api/availability/{config.restaurant_id}/month"
            f"/{month}/{year}/{config.number_of_guests}/en"
        )
        response = requests.get(url)
        for availability_date in response.json():
            if availability_date["status"] == 0:
                # status 0 means available
                # status 1 means closed
                # status 2 means date is in the past
                # status 3 means fully booked
                available_dates.append(
                    datetime.datetime.strptime(
                        availability_date["dayString"], "%Y-%m-%d"
                    )
                )

    print("Available dates:")
    for date in available_dates:
        print(date.strftime("%Y-%m-%d"))

    # Select the available dates that match the filters
    filtered_dates = []
    for date in available_dates:
        if date.weekday() in config.days_of_the_week:
            filtered_dates.append(date)

    print("Filtered dates:")
    for date in filtered_dates:
        print(date.strftime("%Y-%m-%d"))

    # gather data for each of the filtered dates
    available_date_times = []
    for date in filtered_dates:
        url = (
            f"https://widget-api.formitable.com/api/availability/{config.restaurant_id}/day"
            f"/{date.strftime('%Y-%m-%d')}/{config.number_of_guests}/en"
        )
        response = requests.get(url)
        for availability_time in response.json():
            if availability_time["status"] == "AVAILABLE":
                available_date_times.append(
                    datetime.datetime(
                        date.year,
                        date.month,
                        date.day,
                        int(availability_time["timeString"][:2]),
                        int(availability_time["timeString"][3:]),
                    )
                )

    print("Available date times:")
    for date_time in available_date_times:
        print(date_time.strftime("%Y-%m-%d %H:%M"))

    # Select the available date times that match the filters
    filtered_date_times = []
    for date_time in available_date_times:
        if config.from_hour <= date_time.hour < config.to_hour:
            filtered_date_times.append(date_time)

    print("Filtered date times:")
    for date_time in filtered_date_times:
        print(date_time.strftime("%Y-%m-%d %H:%M"))

    return filtered_date_times


def load_already_notified_date_times():
    date_times = []
    with open("already_notified_datetimes.txt") as f:
        for line in f:
            date_times.append(
                datetime.datetime.strptime(line.strip(), "%Y-%m-%d %H:%M")
            )
    return date_times


def save_notified_date_times(date_times):
    with open("already_notified_datetimes.txt", "a") as f:
        for date_time in date_times:
            f.write(date_time.strftime("%Y-%m-%d %H:%M") + "\n")


def notify(date_times):
    for date_time in date_times:
        print(f"Notify: {date_time}")


def main():
    available_date_times = get_available_relevant_date_times()
    already_notified_date_times = load_already_notified_date_times()
    datetime_to_notify = [
        date_time
        for date_time in available_date_times
        if date_time not in already_notified_date_times
    ]
    notify(datetime_to_notify)
    save_notified_date_times(datetime_to_notify)


if __name__ == "__main__":
    main()
