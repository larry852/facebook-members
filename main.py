import bot
import json
from datetime import datetime


def login_facebook(username, password):
    bot.init()
    initial_url = 'https://www.facebook.com/'
    login_user_element_xpath = '//*[@id="email"]'
    login_pass_element_xpath = '//*[@id="pass"]'
    bot.load_page(initial_url)
    element_user = bot.get_element_xpath(login_user_element_xpath)
    element_password = bot.get_element_xpath(login_pass_element_xpath)
    bot.set_text_input(element_user, username)
    bot.set_text_input(element_password, password)
    bot.submit_form(element_password)


def get_members(id_group):
    start = datetime.now()
    count_members = 0
    filename = 'members/members[{}][{}].json'.format(id_group, str(datetime.now()).split('.')[0].replace(' ', '_'))

    bot.init()
    bot.load_page('https://www.facebook.com/groups/{}/members/'.format(id_group))

    while bot.scrolling_down_facebook('_60ri'):
        information = bot.get_elements_class_name('_60ri')
        for index, element in enumerate(information):
            data = bot.get_child_tag_name(element, 'a')
            ajaxify = data.get_attribute('ajaxify')
            if ajaxify:
                id = ajaxify.split('&')[1].replace('member_id=', '')
                member = {
                    'id': id,
                    'name': data.text,
                    'url': 'https://www.facebook.com/{}'.format(id)
                }
                save_member(filename, member)
                count_members += 1
            bot.remove_element(element.find_element_by_xpath('./../../../../..'))
        print("{} Members [{}]".format(count_members, str(datetime.now() - start).split('.')[0]))
    format_file_json(filename)


def save_member(filename, member):
    with open(filename, 'a') as outfile:
        json.dump([member], outfile)


def format_file_json(filename):
    with open(filename) as file:
        data = json.loads(file.read().replace('][', ','))
        unique_members = {each['id']: each for each in data}.values()
    with open(filename, 'w', encoding='utf8') as outfile:
        json.dump(list(unique_members), outfile, sort_keys=True, indent=4, ensure_ascii=False)
        print("[{}] Total members".format(len(unique_members)))


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-u", "--username", dest="username", help="username facebook login", required=True)
    parser.add_argument("-p", "--password", dest="password", help="password facebook login", required=True)
    parser.add_argument("-g", "--group", dest="group", help="id group facebook", required=True)
    args = parser.parse_args()

    login_facebook(args.username, args.password)
    get_members(args.group)
    bot.close()
