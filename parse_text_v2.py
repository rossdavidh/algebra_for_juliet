import sys
import random
from create_algebra_problems import create_algebra_problem_one_variable

PUZZLE_INTRO = '''
<html>
<head>
<meta content="text/html;charset=utf-8" http-equiv="Content-Type">
<meta content="utf-8" http-equiv="encoding">
<style>

#fill_in_blanks td {
    height: 1em;
}

#fill_in_blanks tr:nth-child(even) { /* numbers under the characters */
    white-space: pre;
    color: #ccc;
}

#fill_in_blanks tr:nth-child(odd) td { /* where the characters will be put */
    border-bottom-style: solid;
    font-weight: 100;
    font-size: 200%;
}

#fill_in_blanks table {
    width: 55%; /* if you change this change ul margin-left to be the same */
    float: left;
    table-layout: fixed;
}

#fill_in_blanks ul {
    margin-left: 55%;
    /* Change this to whatever the width of your left column is*/
}

</style>
<script src="https://unpkg.com/vue"></script>

</head>
<body>

<div id="fill_in_blanks">
<table>
'''

PUZZLE_MIDTRO_1 = '''
</table>

<ul>
'''

PUZZLE_MIDTRO_2 = '''
</ul>
</div>

<script>
var app5 = new Vue({
  el: '#fill_in_blanks',
  data: {
'''

PUZZLE_OUTRO = '''
  }
})

</script>
</body>
</html>
'''

def convert_file_to_text_string(file_path):
    input_file  = open(file_path, 'r')
    text_string = ''
    for new_line in input_file:
        if len(new_line) > 21:
            print('keep your lines short, so we can print them out puzzle-fied!')
            print(new_line)
            sys.exit()
        else:
            next_line   = new_line.lower().strip()
            if len(next_line) > 0:
                text_string += next_line 
                text_string += '\n'
    input_file.close()
    return text_string

def count_char_frequencies(text_string):
    freqs = {}
    for char in text_string:
        if char not in freqs:
            freqs[char] = 1
        else:
            freqs[char] += 1
    return freqs

def create_puzzle_output(text_string,encoder):
    new_text_string = ''
    line_of_blanks  = '<tr >'
    line_of_cipher  = '<tr>'
    for char in text_string:
        if (char == '\n'):
            new_text_string += line_of_blanks
            new_text_string += '</tr>'
            new_text_string += char #eol
            new_text_string += line_of_cipher
            new_text_string += '</tr>'
            new_text_string += char #eol
            line_of_blanks = '<tr >'
            line_of_cipher = '<tr>'
        else:
            line_of_blanks += '<td>{{ n'+str(encoder[char])+' }}</td>'
            line_of_cipher += '<td>'+str(encoder[char])+'</td>'
    return new_text_string

def create_data_ul_string(nbr_for_char):
    new_data_string = ''
    new_ul_string   = ''
    nbrs            = []
    for char in nbr_for_char:
        nbrs.append(nbr_for_char[char])
    nbrs            = sorted(nbrs)
    for nbr in nbrs:
        new_ul_string   += '<li>'+str(nbr)+'<input v-model="n'+str(nbr)+'"></li>\n'
        new_data_string += "    n"+str(nbr)+": ' ',\n"
    new_data_string = new_data_string[:-2] #chop off last comma
    return new_data_string,new_ul_string

def create_puzzle_file(text_string,nbr_for_char,ip_text_filepath):
    puzzle_string         = create_puzzle_output(text_string,nbr_for_char)
    data_string,ul_string = create_data_ul_string(nbr_for_char)
    file_text             = PUZZLE_INTRO
    file_text            += puzzle_string
    file_text            += PUZZLE_MIDTRO_1
    file_text            += ul_string
    file_text            += PUZZLE_MIDTRO_2
    file_text            += data_string
    file_text            += PUZZLE_OUTRO
    puzzle_filename = sys.argv[1].split('.')[0] + '_puzzle.html'
    puzzle_file     = open(puzzle_filename,'w')
    puzzle_file.write(file_text)
    puzzle_file.close()
    return puzzle_filename

def create_worksheet_file(nbr_for_char,ip_text_filepath):
    worksheet_string         = ''
    nbr_chars_processed      = 0
    power_of_one_levels      = ['one','two','three','four','five'] #not numbers, in case we get more descriptive later
    power_of_two_levels      = ['power_two_squared_only','power_two_one_squared_term','power_two_two_squared_terms']
    for char in sorted(nbr_for_char.keys()):
        nbr_chars_processed += 1
        if char == ' ':
            char_to_print = '_'
        elif char == '\n':
            continue #no algebra problem for the eol character
        else:
            char_to_print    = char
        if (char_to_print in ['_','e','t','a','o','n']):
            level_for_this_char = random.choice(power_of_two_levels)
        else:
            level_for_this_char = random.choice(power_of_one_levels)
        next_problem_string = create_algebra_problem_one_variable(char_to_print,nbr_for_char[char],level_for_this_char)
        worksheet_string    += next_problem_string
        worksheet_string    += '\n\n'
    worksheet_string_filename = sys.argv[1].split('.')[0] + '_worksheet.txt'
    worksheet_string_file = open(worksheet_string_filename,'w')
    worksheet_string_file.write(worksheet_string)
    worksheet_string_file.close()
    return worksheet_string_filename

if __name__ == "__main__":
    #first we analyze the text file that will be the solution
    if len(sys.argv) < 1:
        print('you need to provide the text file location')
        sys.exit()
    text_string              = convert_file_to_text_string(sys.argv[1])
    char_counts              = count_char_frequencies(text_string)
    cc_by_c                  = [(k, char_counts[k]) for k in sorted(char_counts, key=char_counts.get)]
    #now we decide what number to substitute for each character in the puzzle
    nbr_for_char             = {}
    nbrs_to_choose_from      = list(range(1,99))
    random.shuffle(nbrs_to_choose_from)
    for char,next_nbr_to_assign in zip(cc_by_c,nbrs_to_choose_from):
        nbr_for_char[char[0]] = next_nbr_to_assign
    #create the puzzle string as a txt file with the same name
    puzzle_filename          = create_puzzle_file(text_string,nbr_for_char,sys.argv[1])
    print('created puzzle ',puzzle_filename)
    #now we need to make the worksheet to use in solving the puzzle 
    worksheet_filename       = create_worksheet_file(nbr_for_char,sys.argv[1])
    print('created worksheet ',worksheet_filename)
