import click
from faker import Faker

fake = Faker()


@click.command()
@click.option('--filename', '-f')
@click.option('--person', '-p', type=bool)
@click.option('--date', '-d', type=bool)
@click.option('--money', '-m', type=bool)
@click.option('--email', '-e', type=bool)
@click.option('--phone', '-ph', type=bool)
@click.option('--creditcard', '-c', type=bool)
def generate_message(filename=None, person=None, date=None, money=None, email=None, phone=None, creditcard=None):
    """
    Generate random text message into json format and save to file.
    Optionally, include specific information into the text. If not given, these info will be randomly added.
    :param filename:
    :param person:
    :param date:
    :param money:
    :param email:
    :param phone:
    :param credit_card:
    :return:
    """
    filename = filename or "test.json"
    text = ""
    if person or (person is None and fake.random_element([True, False])):
        text = text + str(fake.name()) + ', '
    if date or (date is None and fake.random_element([True, False])):
        text = text + str(fake.date()) + ', '
    if money or (money is None and fake.random_element([True, False])):
        text = text + '$' + str(fake.random_number()) + ', '
    if email or (email is None and fake.random_element([True, False])):
        text = text + str(fake.ascii_email()) + ', '
    if phone or (phone is None and fake.random_element([True, False])):
        text = text + str(fake.phone_number()) + ', '
    if creditcard or (creditcard is None and fake.random_element([True, False])):
        text = text + str(fake.credit_card_number()) + ', '
    json_message = '{{"message" : "{text}"}}'.format(text=text)

    with open('examples/'+filename, 'w') as f:
        f.write(json_message)

    click.echo("Generated message and saved to file {filename}:\n {json_message}".
               format(filename=filename, json_message=json_message))
    return


if __name__ == "__main__":
    generate_message()
