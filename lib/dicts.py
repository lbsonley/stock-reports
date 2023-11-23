from lib.utils import get_dates

dates = get_dates()

returns_labels_by_period = {
    "1wk": "1 Week ∆",
    "1q": "1 Quarter ∆",
    "1y": "52 Week ∆",
    "5y": "5 Year ∆",
}

chart_interval_labels_by_period = {
    "1wk": "30m",
    "1q": "Daily",
    "1y": "Weekly",
    "5y": "Monthly",
}

chart_intervals_by_period = {
    "1wk": "30m",
    "1q": "1d",
    "1y": "1wk",
    "5y": "1mo",
}

start_dates_by_period = {
    "1wk": dates["last_monday"],
    "1q": dates["last_quarter"],
    "1y": dates["last_year"],
    "5y": dates["last_5_year"],
}
