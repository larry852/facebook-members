import bot
import json
from datetime import datetime


def login_facebook(username='lady.cris.16@hotmail.com', password='asu1053608972cp'):
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


def get_members(id_group='5347104545'):
    start = datetime.now()
    members = []
    old_information = []
    old_images = []
    active = True
    limit = 50
    filename = 'members-{}.json'.format(datetime.now())

    bot.init()
    bot.load_page('https://www.facebook.com/groups/{}/members/'.format(id_group))

    while active:
        active = bot.scrolling_down_facebook(limit, '_60ri')
        limit += 50

        information = bot.get_elements_class_name('_60ri')
        new_information = [item for item in information if item not in old_information]
        old_information = information

        images = bot.get_elements_class_name('_s0')
        new_images = [item for item in images if item not in old_images]
        old_images = images

        for index, element in enumerate(new_information):
            data = bot.get_child_tag_name(element, 'a')
            ajaxify = data.get_attribute('ajaxify')
            if ajaxify:
                id = ajaxify.split('&')[1].replace('member_id=', '')
                member = {
                    'id': id,
                    'name': data.text,
                    'image': new_images[index].get_attribute('src'),
                    'url': 'https://www.facebook.com/{}'.format(id)
                }
                if member not in members:
                    members.append(member)
                    save_member(filename, member)
        print("{} Members - {}".format(len(members), str(datetime.now() - start).split('.')[0]))
    format_file_json(filename)


def save_member(filename, member):
    with open(filename, 'a', encoding='utf8') as outfile:
        json.dump([member], outfile, sort_keys=True, indent=4, ensure_ascii=False)


def format_file_json(filename):
    with open(filename) as file:
        data = json.loads(file.read().replace('\n][', ','))
    with open(filename, 'w', encoding='utf8') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    login_facebook()
    get_members()
    bot.close()
    # format_file_json('')
