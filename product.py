from datetime import date


class product:
    def __init__(self, main_category, category, sub_category, sku, name, price):
        self.main_category = main_category
        self.category = category
        self.sub_category = sub_category
        self.sku = sku
        self.name = name
        self.price = price
        self.date = date.today()

    def __repr__(self):
        return "{} - {} - {} |{}({}): $ {}".format(
            self.main_category,
            self.category,
            self.sub_category,
            self.name,
            self.sku,
            self.price,
        )
