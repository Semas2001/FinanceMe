import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
previous_prediction = None
previous_input_data = None


def generate_prediction(total_revenue, file_dates):
    global previous_prediction, previous_input_data
    if previous_input_data is not None and total_revenue == previous_input_data[0] and file_dates == \
            previous_input_data[1]:
        return previous_prediction
    start_date = file_dates[0]
    x = [(datetime.strptime(date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days for date in file_dates]
    x = np.array(x).reshape(-1, 1)
    y = np.array(total_revenue)
    model = LinearRegression()
    model.fit(x, y)
    last_date = datetime.strptime(file_dates[-1], "%Y-%m-%d")
    next_date_1 = last_date + timedelta(days=1)
    next_date_2 = last_date + timedelta(days=2)
    predicted_revenues = model.predict([[x[-1][0] + 1], [x[-1][0] + 2]])
    for date, revenue in zip([next_date_1, next_date_2], predicted_revenues):
        file_dates.append(date.strftime("%Y-%m-%d"))
        total_revenue.append(revenue)
    previous_prediction = total_revenue, file_dates
    previous_input_data = (total_revenue.copy(), file_dates.copy())

    return total_revenue, file_dates

def delete_generated_data(total_revenue, file_dates):
    del total_revenue[-2:]
    del file_dates[-2:]

    return total_revenue, file_dates

