class VehicleListPage:
    def __init__(self, page):
        self.page = page

    def navigate(self, base_url):
        self.page.goto(base_url)

    def get_vehicle_count(self):
        return self.page.locator("tbody tr").count()

    def book_vehicle(self, vehicle_id):
        self.page.click(f"#book-btn-{vehicle_id}")


class BookingPage:
    def __init__(self, page):
        self.page = page

    def fill_form(self, name, age, is_premium, start_date, end_date):
        self.page.fill("#customer_name", name)
        self.page.fill("#customer_age", str(age))
        if is_premium:
            self.page.check("#is_premium")
        self.page.fill("#start_date", start_date)
        self.page.fill("#end_date", end_date)

    def submit(self):
        self.page.click("#submit-booking")

    def get_error_message(self):
        return self.page.locator("#error-message").inner_text()
