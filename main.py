import bot
import json


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


def get_members(id_group='5347104545', limit=None):
    members = []
    bot.init()
    bot.load_page('https://www.facebook.com/groups/{}/members/'.format(id_group))
    bot.scrolling_down_facebook(limit, '_60ri')

    information = bot.get_elements_class_name('_60ri')
    images = bot.get_elements_class_name('_s0')

    for index, element in enumerate(information):
        data = bot.get_child_tag_name(element, 'a')
        ajaxify = data.get_attribute('ajaxify')
        if ajaxify:
            id = ajaxify.split('&')[1].replace('member_id=', '')
            member = {
                'id': id,
                'name': data.text,
                'image': images[index].get_attribute('src'),
                'url': 'https://www.facebook.com/{}'.format(id)
            }
            members.append(member)
    return members


def save_members(data):
    with open('members.json', 'w') as outfile:
        json.dump(data, outfile)


if __name__ == '__main__':
    login_facebook()
    members = get_members()
    save_members(members)
    bot.close()
