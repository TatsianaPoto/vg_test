import csv
from datetime import datetime

def validate_install_date(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def validate_country(country):
    # Здесь можно добавить проверку на наличие двухбуквенного кода страны в стандарте ISO 3166
    # В данном примере просто проверим, что country состоит из 2 символов
    return len(country) == 2

def validate_campaign_id(campaign_id):
    return campaign_id.isdigit()

def validate_campaign_name(campaign_name):
    return len(campaign_name) > 0 and len(campaign_name) <= 255

def validate_installs(installs):
    return installs.isdigit() and int(installs) >= 0

def validate_row(row):
    errors = []

    if not validate_install_date(row['install_date']):
        errors.append('Invalid install_date format: {}'.format(row['install_date']))

    if not validate_country(row['country']):
        errors.append('Invalid country code: {}'.format(row['country']))

    if not validate_campaign_id(row['campaign_id']):
        errors.append('Invalid campaign_id: {}'.format(row['campaign_id']))

    if not validate_campaign_name(row['campaign_name']):
        errors.append('Invalid campaign_name: {}'.format(row['campaign_name']))

    if not validate_installs(row['installs']):
        errors.append('Invalid installs value: {}'.format(row['installs']))

    return errors

def validate_csv(input_file, output_file):
    with open(input_file, 'r', newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        all_errors = []

        for row_num, row in enumerate(reader, start=1):
            errors = validate_row(row)
            if errors:
                all_errors.append({'row_num': row_num, 'errors': errors})

    if all_errors:
        with open(output_file, 'w', newline='') as error_file:
            writer = csv.DictWriter(error_file, fieldnames=['row_num', 'errors'])
            writer.writeheader()
            writer.writerows(all_errors)
        print('Validation completed. Errors have been saved to {}.'.format(output_file))
    else:
        print('Validation completed. No errors found.')

if __name__ == '__main__':
    input_file = 'test.csv'
    output_file = 'validation_errors.csv'
    validate_csv(input_file, output_file)
