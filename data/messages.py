from collections import namedtuple

Messages = namedtuple('Messages', ('read_rules', 'rules', 'give_request', 'where_was_found_out',
                                   'profile_link', 'work_hours', 'scam_experience',
                                   'request_info', 'request_was_sent', 'new_request', 'request_accepted',
                                   'admin_request_accepted', 'request_rejected', 'admin_request_rejected'))

answers = Messages(read_rules='Привет, {}! Перед подачей заявки ознакомься с правилами проекта',
                   rules='Воркеры...',
                   give_request='Для подачи заявки нажмите на кнопку ниже',
                   where_was_found_out='Откуда вы о нас узнали?',
                   profile_link='Отправьте ссылку на ваш профиль в LOLZTEAM',
                   work_hours='Сколько часов в день вы готовы уделять?',
                   scam_experience='Каков ваш опыт в сфере скама? Расскажите поподробней.',
                   request_info='Откуда узнали: {from_where}\nПрофиль LOLZTEAM: {profile_link}\n'
                                'Сколько часов готов уделять: {work_hours}\nОпыт: {experience}',
                   request_was_sent='Ваша заявка успешно отправлена. В ближайшее время её рассмотрят.',
                   new_request='Новая заявка (User ID: {})!\n',
                   request_accepted='Поздравляем, Ваша заявка успешно принята!',
                   admin_request_accepted='Заявка (User ID: {}) успешно принята!',
                   request_rejected='Увы, Ваша заявка была отклонена!',
                   admin_request_rejected='Заявка (User ID: {}) отклонена!'
                   )
