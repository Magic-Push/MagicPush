import csv
from magicpush.helpers.stripe_billing import StripeBilling


# generate coupon codes return as csv file
def generate_coupon_codes(coupon, quantity):
    coupon_codes = []
    for i in range(quantity):
        coupon_codes.append(StripeBilling().add_coupon_code(coupon).code)

    # turn into csv file
    with open('output.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # Write each string as a row in the CSV file
        for row in coupon_codes:
            # Split the string into a list based on commas
            writer.writerow(row.split(','))

