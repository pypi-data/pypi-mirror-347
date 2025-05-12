import datetime

class TimeUtils:
    @staticmethod
    def get_all_months_years():
        """Returns a list of all months and years from 0 to 9999."""
        months = []
        for year in range(10000):
            for month in range(1, 13):  # Months from 1 to 12
                months.append(f"{year}-{month:02d}")
        return months

    @staticmethod
    def get_all_seconds_minutes_hours():
        """Returns all seconds, minutes, hours, and milliseconds."""
        time_details = {
            'seconds': [i for i in range(60)],
            'minutes': [i for i in range(60)],
            'hours': [i for i in range(24)],
            'milliseconds': [i for i in range(1000)]
        }
        return time_details

    @staticmethod
    def get_full_datetime():
        """Returns full datetime information including all time units."""
        now = datetime.datetime.now()
        full_time = {
            'year': now.year,
            'month': now.month,
            'day': now.day,
            'hour': now.hour,
            'minute': now.minute,
            'second': now.second,
            'microsecond': now.microsecond
        }
        return full_time

    @staticmethod
    def limit_time(start, end, time_unit='second'):
        """Limits the time between start and end values for a given time unit."""
        time_units_in_seconds = {
            'second': 1,
            'minute': 60,
            'hour': 3600,
            'day': 86400,
            'month': 2592000,  # Approx 30 days
            'year': 31536000,  # Approx 365 days
        }

        if time_unit not in time_units_in_seconds:
            raise ValueError("Invalid time unit provided. Choose from: 'second', 'minute', 'hour', 'day', 'month', 'year'")

        # Convert start and end to seconds
        start_in_seconds = start * time_units_in_seconds[time_unit]
        end_in_seconds = end * time_units_in_seconds[time_unit]

        # Calculate the time difference
        time_difference = end_in_seconds - start_in_seconds
        return time_difference
