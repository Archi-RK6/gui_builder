from pyparsing import *

rus_alphas = 'ёйцукенгшщзхъфывапролджэячсмитьбюЁЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'

bool_var = Word('0' + '1')
word_num = Word(nums + alphas + '@')
variable = Word(nums + alphas + '_')
rus_eng_word_num = Word(alphas + rus_alphas + ' ' + nums)
link = Word(alphanums + '-' + '+' + '=' + '/' + '.' + '_' + '#' + ':' + '&' + '?' + '%')
text = Word(printables + rus_alphas + ' ')
menu_link = Word(alphanums + '-' + '+' + '=' + '.' + '_' + '#' + ':' + '&' + '?' + '%')

parse_section = '[' + variable + ']' + '//' + rus_eng_word_num
parse_text_box = variable + '=' + word_num + '//' + rus_eng_word_num
parse_box = variable + '=' + '[' + bool_var + ']' + '{0|1}' + '//' + rus_eng_word_num
parse_file_selection = variable + '=' + '[file]' + '//' + rus_eng_word_num
parse_link = '[' + link + ']' + '//' + rus_eng_word_num
parse_text = '//' + OneOrMore(text)
aini_file_name = menu_link + '=' + '[' + variable + ']' + '//' + rus_eng_word_num

num_of_section = -1


def parsing(s):
    try:
        test = parse_section.parseString(s).asList()
        patern_id = 1
    except ParseException:
        try:
            test = parse_text_box.parseString(s).asList()
            patern_id = 2
        except ParseException:
            try:
                test = parse_box.parseString(s).asList()
                patern_id = 3
            except ParseException:
                try:
                    test = parse_file_selection.parseString(s).asList()
                    patern_id = 4
                except ParseException:
                    try:
                        test = parse_link.parseString(s).asList()
                        patern_id = 5
                    except ParseException:
                        try:
                            test = parse_text.parseString(s).asList()
                            patern_id = 6
                        except ParseException:
                            print('The string is not parsed:' + s + '')
                            quit()
    return [patern_id, test]


def html_start(title, html_file_name):
    folder = 'output\\'
    f = open(folder + html_file_name + '.html', 'w', encoding='utf-8')
    f.write('<!DOCTYPE html>\n<html>\n<head>\n<meta name="viewport" content="width=device-width, '
            'initial-scale=1">\n<style>\nbody {font-family: Arial;}\n\n.tab {\n\toverflow: hidden;\n\tborder: 1px '
            'solid #ccc;\n\tbackground-color: #f1f1f1;\n}\n\n.tab button, .clickable {\n\tfloat: left;\nborder: '
            'none;\n\toutline: none;\n\tcursor: pointer;\n\tpadding: 14px 16px;\n\ttransition: 0.3s;\n\tfont-size: '
            '17px;\n}\n\n.tab button:hover, .clickable:hover {\n\tbackground-color: #ddd;\n}\n\n.tab '
            'button.active {\n\tbackground-color: #ccc;\n}\n\n.tabcontent {\n\tdisplay: none;\n\tpadding: 6px '
            '12px;\n\tborder: 1px solid #ccc;\n\tborder-top: none;\n}\n</style>\n<title>' + title +
            '</title>\n</head>\n<body>\n \n<div class="tab">\n')
    return f


def section_to_html(parsed_line):
    if len(parsed_line) != 5:
        section = parsed_line[1]
    else:
        section = parsed_line[4]
    global num_of_section
    num_of_section += 1
    id = "'section_" + str(num_of_section) + "'"
    if num_of_section == 0:
        return '\t<button class="tablinks" onclick="tabs(event,' + id + ')" id="defaultOpen">' + section + '</button>\n'
    else:
        return '\t<button class="tablinks" onclick="tabs(event,' + id + ')">' + section + '</button>\n'


def textbox_to_html(parsed_line, file_name):
    html_code = []
    if len(parsed_line) != 5:
        textbox = parsed_line[0]
        html_code.append('\t\tif request.POST["' + parsed_line[0] + '"]:\n\t\t\t' + parsed_line[0] + ' = request.POST["'
                         + parsed_line[0] + '"]\n\t\t\tnew_data = \'\'\n\t\t\tinput = open(\'/home/app/web/input/'
                         + file_name + '\', \'r\', encoding=\'utf-8\')\n\t\t\tinput_f = File(input)\n\t\t\told_data = '
                                       'input_f.readlines()\n\t\t\tfor l in old_data:\n\t\t\t\tif l.find(\'\\n' +
                         parsed_line[0] + '=\') != -1:\n\t\t\t\t\tl = \'' + parsed_line[0] + '=\' + ' + parsed_line[0] +
                         ' + \'//' + parsed_line[0] + '\\n\'\n\t\t\t\tnew_data = new_data + str(l)\n\t\t\toutput = '
                                                      'open(\'/home/app/web/input/' + file_name +
                         '\', \'w\', encoding=\'utf-8\')\n\t\t\toutput_f = File(output)\n\t\t\toutput_f.write('
                         'new_data)\n\t\t\tinput_f.close()\n\t\t\tinput.close()\n\t\t\toutput_f.close('
                         ')\n\t\t\toutput.close()\n\n')
    else:
        textbox = parsed_line[4]
        html_code.append('\t\tif request.POST["' + parsed_line[0] + '"]:\n\t\t\t' + parsed_line[0] + ' = request.POST["'
                         + parsed_line[0] + '"]\n\t\t\tnew_data = \'\'\n\t\t\tinput = open(\'/home/app/web/input/'
                         + file_name + '\', \'r\', encoding=\'utf-8\')\n\t\t\tinput_f = File(input)\n\t\t\told_data = '
                                       'input_f.readlines()\n\t\t\tfor l in old_data:\n\t\t\t\tif l.find(\'//' +
                         parsed_line[4] + '\\n\') != -1:\n\t\t\t\t\tl = \'' + parsed_line[0] + '=\' + ' + parsed_line[0]
                         + ' + \'//' + parsed_line[4] + '\\n\'\n\t\t\t\tnew_data = new_data + str(l)\n\t\t\toutput = '
                                                        'open(\'/home/app/web/input/' + file_name +
                         '\', \'w\', encoding=\'utf-8\')\n\t\t\toutput_f = File(output)\n\t\t\toutput_f.write('
                         'new_data)\n\t\t\tinput_f.close()\n\t\t\tinput.close()\n\t\t\toutput_f.close('
                         ')\n\t\t\toutput.close()\n\n')
    print(parsed_line)

    if parsed_line[2] == '@' + parsed_line[0] + '@':
        value = ''
    else:
        value = parsed_line[2]
    html_code.append('\t<p><b>' + textbox + '</b><br>\n\t<input type="text" name="' + parsed_line[0] + '" value="'
                     + value + '"></p>\n')

    return html_code


def box_to_html(parsed_line, file_name):
    html_code = []
    if len(parsed_line) != 8:
        box = parsed_line[0]
        html_code.append('\t\tif "' + parsed_line[0] + '" in request.POST:\n\t\t\t' + parsed_line[0] +
                         ' = \'1\'\n\t\telse:\n\t\t\t' + parsed_line[0] +
                         ' = \'0\'\n\t\tnew_data = \'\'\n\t\tinput = open(\'/home/app/web/input/' + file_name +
                         '\', \'r\', encoding=\'utf-8\')\n\t\tinput_f = File(input)\n\t\told_data = '
                         'input_f.readlines()\n\t\tfor l in old_data:\n\t\t\tif l.find(\'\\n' + parsed_line[0] +
                         '=\') != -1:\n\t\t\t\tl = \'' + parsed_line[0] + '=[\' + ' + parsed_line[0] + ' + \']{0|1}//' +
                         parsed_line[0] + '\\n\'\n\t\t\tnew_data = new_data + str(l)\n\t\toutput = open('
                                          '\'/home/app/web/input/' + file_name + '\', \'w\', '
                                                                                 'encoding=\'utf-8\')\n\t\toutput_f = '
                                                                                 'File(output)\n\t\toutput_f.write('
                                                                                 'new_data)\n\t\tinput_f.close('
                                                                                 ')\n\t\tinput.close('
                                                                                 ')\n\t\toutput_f.close('
                                                                                 ')\n\t\toutput.close()\n\n')
    else:
        box = parsed_line[7]
        html_code.append('\t\tif "' + parsed_line[0] + '" in request.POST:\n\t\t\t' + parsed_line[0] +
                         ' = \'1\'\n\t\telse:\n\t\t\t' + parsed_line[0] + '= \'0\'\n\t\tnew_data = \'\'\n\t\tinput = '
                                                                          'open(\'/home/app/web/input/' + file_name +
                         '\', \'r\', encoding=\'utf-8\')\n\t\tinput_f = File(input)\n\t\told_data = '
                         'input_f.readlines()\n\t\tfor l in old_data:\n\t\t\tif l.find(\'//' + parsed_line[7] +
                         '\\n\') != -1:\n\t\t\t\tl = \'' + parsed_line[0] + '=[\' + ' + parsed_line[0] + ' + \']{0|1}//'
                         + parsed_line[7] + '\\n\'\n\t\t\tnew_data = new_data + str(l)\n\t\toutput = open('
                                            '\'/home/app/web/input/' + file_name + '\', \'w\', '
                                                                                   'encoding=\'utf-8\')\n\t\toutput_f '
                                                                                   '= File('
                                                                                   'output)\n\t\toutput_f.write('
                                                                                   'new_data)\n\t\tinput_f.close('
                                                                                   ')\n\t\tinput.close('
                                                                                   ')\n\t\toutput_f.close('
                                                                                   ')\n\t\toutput.close()\n\n')
    if parsed_line[3] == '1':
        html_code.append('\t<p><input type="checkbox" name="' + parsed_line[0] + '" value="' + parsed_line[0]
                         + '" checked>' + box + '</p>\n')
    else:
        html_code.append('\t<p><input type="checkbox" name="' + parsed_line[0] + '" value="' + parsed_line[0] + '">'
                         + box + '</p>\n')
    return html_code


def file_selection_to_html(parsed_line):
    html_code = []
    if len(parsed_line) != 5:
        file_selection = parsed_line[0]
    else:
        file_selection = parsed_line[4]
    html_code.append('\t\tif "' + parsed_line[0] + '" in request.FILES:\n\t\t\t' + parsed_line[0] + ' = request.FILES["'
                     + parsed_line[0] + '"]\n\t\t\tfs = FileSystemStorage()\n\t\t\tfilename = fs.save(' + parsed_line[0]
                     + '.name, ' + parsed_line[0] + ')\n\t\t\tfile_url = fs.url(filename)\n\n')
    html_code.append('\t<p><b>' + file_selection + '</b><br>\n\t<input type="file" name="'
                     + parsed_line[0] + '"></p>\n')
    return html_code


def link_to_html(parsed_line):
    if len(parsed_line) != 5:
        link_title = parsed_line[1]
    else:
        link_title = parsed_line[4]
    return '\t<p><a href="' + parsed_line[1] + '">' + link_title + '</a></p>\n'


def text_to_html(parsed_line):
    return '\t<p>' + parsed_line[1] + '</p>\n'


def html_finish(f):
    f.write('<p><input class="clickable" type="submit"></p>\n</form>\n<br>\n<br>\n<br>\n<button class="clickable" '
            'onclick="document.location=\'/\'">Назад</button>\n\n'
            '<script>\nfunction tabs(evt, tab_id) {\n\tvar i, tabcontent, tablinks;\n\ttabcontent = '
            'document.getElementsByClassName("tabcontent");\n\tfor (i = 0; i < tabcontent.length; i++) '
            '{\n\t\ttabcontent[i].style.display = "none";\n\t}\n\ttablinks = '
            'document.getElementsByClassName("tablinks");\n\tfor (i = 0; i < '
            'tablinks.length; i++) {\n\t\ttablinks[i].className = tablinks[i].className.replace(" active", '
            '"");\n\t}\n\tdocument.getElementById(tab_id).style.display = "block";\n\tevt.currentTarget.className += " '
            'active";\n}\n\ndocument.getElementById("defaultOpen").click();\n</script>\n\n</body>\n</html>')
    f.close()


def aini_to_html(file_name, title):
    sections_list = []
    elements_list = []
    list_of_variables = []

    input_f = open('input/' + file_name, encoding='utf-8')
    f = html_start(title, file_name)

    for line in input_f:
        id_and_line = parsing(line)
        patern_id = id_and_line[0]
        parsed_line = id_and_line[1]
        print(parsed_line)
        if patern_id <= 3:
            match patern_id:
                case 1:
                    html_code = section_to_html(parsed_line)
                    sections_list.append(html_code)
                case 2:
                    html_code = textbox_to_html(parsed_line, file_name)
                    if len(elements_list) == num_of_section + 1:
                        elements_list[num_of_section] += html_code[1]
                    else:
                        elements_list.append(html_code[1])
                    list_of_variables.append(html_code[0])
                case 3:
                    html_code = box_to_html(parsed_line, file_name)
                    if len(elements_list) == num_of_section + 1:
                        elements_list[num_of_section] += html_code[1]
                    else:
                        elements_list.append(html_code[1])
                    list_of_variables.append(html_code[0])
        else:
            match patern_id:
                case 4:
                    html_code = file_selection_to_html(parsed_line)
                    if len(elements_list) == num_of_section + 1:
                        elements_list[num_of_section] += html_code[1]
                    else:
                        elements_list.append(html_code[1])
                    list_of_variables.append(html_code[0])
                case 5:
                    html_code = link_to_html(parsed_line)
                    if len(elements_list) == num_of_section + 1:
                        elements_list[num_of_section] += html_code
                    else:
                        elements_list.append(html_code)
                case 6:
                    html_code = text_to_html(parsed_line)
                    if len(elements_list) == num_of_section + 1:
                        elements_list[num_of_section] += html_code
                    else:
                        elements_list.append(html_code)

    for section in sections_list:
        f.write(section)
    f.write('</div>\n\n')

    i = 0
    f.write('<form method="post" enctype="multipart/form-data">\n\n{% csrf_token %}\n')
    for element in elements_list:
        id = 'section_' + str(i)
        f.write('<div id="' + id + '" class="tabcontent">\n' + element + '</div>\n\n')
        i += 1
    html_finish(f)
    return list_of_variables


def main():
    input_f = open(r'input\config', encoding='utf-8')
    f_menu = open(r'output\menu.html', 'w', encoding='utf-8')
    f_urls = open(r'output\txt_for_urls.txt', 'w', encoding='utf-8')
    f_views = open(r'output\txt_for_views.txt', 'w', encoding='utf-8')
    list_of_functions = 'from upload.views import menu'

    f_urls.write('#Ниже представлен код, который должен быть вставлен в файл urls.py в список urlpatterns\n\n\tpath('
                 '"", menu, name="menu"),\n')
    f_views.write(
        '#Ниже представлен код, который должен быть вставлен в файл views.py\n\n\ndef menu(request):\n\treturn render('
        'request, "menu.html")\n\n')
    f_menu.write(
        '<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<style>\nbody {font-family: '
        'Arial;}\n\n.tab {\n\toverflow: hidden;\n\tborder: 1px solid #ccc;\n\tbackground-color: #f1f1f1;\n}\n\n.tab '
        'button {\n\toverflow: hidden;\n\tborder: 1px solid #ccc;\n\tbackground-color: #ddd;\n\tfloat: '
        'left;\n\tborder: none;\n\toutline: none;\n\tcursor: pointer;\n\tpadding: 14px 16px;\n\ttransition: '
        '0.3s;\n\tfont-size: '
        '17px;\n\tdisplay: block;\n\twidth: 100%;\n}\n\n.tab button:hover {\n\tbackground-color: '
        '#808080;\n}\n\n</style>\n<title>menu</title>\n</head>\n<body>\n<h1>Здравствуйте! Выберите один из '
        'предложенных вариантов.</h1>\n<div class="tab">\n')

    for line in input_f:
        global num_of_section
        num_of_section = -1

        try:
            config = aini_file_name.parseString(line).asList()
        except ParseException:
            print('The string is not parsed:')
            print(line)
            quit()

        f_menu.write('\t<button onclick="document.location=\'/' + config[0] + '/\'">' + config[6] + '</button>\n')
        f_urls.write('\tpath("' + config[0] + '/", ' + config[3] + ', name="' + config[3] + '"),\n')
        list_of_functions = list_of_functions + ', ' + config[3]
        list_of_variables = aini_to_html(config[3], config[6], )
        f_views.write('\ndef ' + config[3] + '(request):\n\tif request.method == "POST":\n')
        for variable in list_of_variables:
            f_views.write(variable)
        f_views.write('\t\treturn render(request, "' + config[3] + '.html")\n\treturn render(request, "' + config[
            3] + '.html")\n\n')

    f_menu.write('</div>\n</body>\n</html>\n')
    f_urls.write('\n#Также вставьте следующую строку в файл urls.py до списка urlpatterns\n' + list_of_functions)

    input_f.close()
    f_menu.close()
    f_urls.close()
    f_views.close()


if __name__ == '__main__':
    main()
