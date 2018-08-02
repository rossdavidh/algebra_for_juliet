from __future__ import division
import os
import unittest

from create_algebra_problems import *
from parse_text_v2 import *

class TestPrintableLetter(unittest.TestCase):

    def test_ordinary_letters(self):
        ol = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for letter in ol:
            assert(printable(letter) == letter)

    def test_numerals(self):
        numerals = ['[one]','[two]','[three]','[four]','[five]','[six]','[seven]','[eight]','[nine]']
        for numeral in range(0,9):
            assert(printable(str(numeral+1)) == numerals[numeral])

    def test_punctuation(self):
        pl = '_\',?"!.();-:[]/'
        for punct in pl:
            assert(printable(punct)[0] == '[')
            assert(printable(punct)[-1] == ']')

class TestProblemStringPostProcessing(unittest.TestCase):

    def test_one(self):
        pts = '1l + 3 = 5'
        assert(problem_string_postproc(pts,'l','l') == '1L + 3 = 5')

    def test_two(self):
        pts = '3[period] + 8[apostrophe] = 4'
        pts = problem_string_postproc(pts,'.','[period]')
        pts = problem_string_postproc(pts,"'",'[apostrophe]')
        assert(pts == '3*[period] + 8*[apostrophe] = 4')

    def test_three(self):
        pts = '5x + -2 = 7'
        assert(problem_string_postproc(pts,'x','x') == '5x - 2 = 7')

class TestCreateAlgebraProblemFunctions(unittest.TestCase):

    def test_determine_sign(self):
        sum_so_far = 0
        for i in range(0,1000):
            sum_so_far += determine_sign(1)
        assert(-90 < sum_so_far < 90)

    def test_create_algebra_problem_one_variable_type_one(self):
        for i in range(0,10):
            answer    = random.randrange(1,9,1)
            a,b,c,d,e = generate_components_one_var(answer,'one')
            assert((a*answer) + b == c)

    def test_create_algebra_problem_one_variable_type_two(self):
        for i in range(0,10):
            answer    = random.randrange(1,9,1)
            a,b,c,d,e = generate_components_one_var(answer,'two')
            assert(((a*answer)/b) == c)

    def test_create_algebra_problem_one_variable_type_three(self):
        for i in range(0,10):
            answer    = random.randrange(1,9,1)
            a,b,c,d,e = generate_components_one_var(answer,'three')
            assert((a*answer) + b + (c*answer) == d)

    def test_create_algebra_problem_one_variable_type_four(self):
        for i in range(0,10):
            answer    = random.randrange(1,9,1)
            a,b,c,d,e = generate_components_one_var(answer,'four')
            assert(a*((b*answer) + c) == d)

    def test_create_algebra_problem_one_variable_type_five(self):
        for i in range(0,10):
            answer    = random.randrange(1,9,1)
            a,b,c,d,e = generate_components_one_var(answer,'five')
            assert((a*answer) + b == (c*answer) + d)

    def test_create_algebra_problem_one_variable_type_power_two_squared_only(self):
        for i in range(0,10):
            answer    = random.randrange(1,9,1)
            a,b,c,d,e = generate_components_one_var(answer,'power_two_squared_only')
            assert((a*answer*answer) + b == c)

    def test_create_algebra_problem_one_variable_type_power_two_one_squared_term(self):
        for i in range(0,10):
            answer    = random.randrange(1,9,1)
            a,b,c,d,e = generate_components_one_var(answer,'power_two_one_squared_term')
            assert((a*answer*answer) + (b*answer) + c == (d*answer) + e)

    def test_create_algebra_problem_one_variable_type_power_two_two_squared_terms(self):
        for i in range(0,10):
            answer    = random.randrange(1,9,1)
            a,b,c,d,e = generate_components_one_var(answer,'power_two_two_squared_terms')
            assert((a*answer*answer) + (b*answer) == (c*answer*answer) + (d*answer) + e)

    def test_create_algebra_problem_two_variables_type_one(self):
        for i in range(0,10):
            answer1   = random.randrange(1,9,1)
            answer2   = random.randrange(1,9,1)
            a,b,c,d,e,f = generate_components_two_vars(answer1,answer2,'one')
            assert((a*answer1) + (b*answer2) == c)
            assert((d*answer1) + (e*answer2) == f)

    def test_problem_text_one_var(self):
        a = 2
        b = 3
        c = 4
        d = 5
        e = 6
        letter = 'x'
        problem_text = problem_text_one_var(a,b,c,d,e,letter,'one') #ax + b = c
        assert(problem_text == '2x + 3 = 4    x = ___?')
        problem_text = problem_text_one_var(a,b,c,d,e,letter,'two') #ax/b = c
        assert(problem_text == '2x/3 = 4    x = ___?')
        problem_text = problem_text_one_var(a,b,c,d,e,letter,'three') #ax + b + cx = d
        assert(problem_text == '2x + 3 + 4x = 5    x = ___?')
        problem_text = problem_text_one_var(a,b,c,d,e,letter,'four') #a(bx + c) = d
        assert(problem_text == '2(3x + 4) = 5    x = ___?')
        problem_text = problem_text_one_var(a,b,c,d,e,letter,'five') # ax + b = cx + d
        assert(problem_text == '2x + 3 = 4x + 5    x = ___?')
        problem_text = problem_text_one_var(a,b,c,d,e,letter,'power_two_squared_only') # ax^2 + b = c
        assert(problem_text == '2x^2 + 3 = 4    x = ___?')
        problem_text = problem_text_one_var(a,b,c,d,e,letter,'power_two_one_squared_term') # ax^2 + bx + c = dx + e
        assert(problem_text == '2x^2 + 3x + 4 = 5x + 6    x = ___?')
        problem_text = problem_text_one_var(a,b,c,d,e,letter,'power_two_two_squared_terms') # ax^2 + bx = cx^2 + dx + e
        assert(problem_text == '2x^2 + 3x = 4x^2 + 5x + 6    x = ___?')

    def test_problem_text_one_var_punctuation(self):
        for punct in ["'",',','"','!',',',';','-','(',')']:
            for problem_type in ['one','two','three','four','five','power_two_squared_only','power_two_one_squared_term']:
                problem_text = problem_text_one_var(2,3,4,5,6,punct,problem_type)
                if punct == '?':
                    assert(problem_text.count(punct) == 2)
                elif punct in [')','('] and problem_type == 'four':
                    assert(problem_text.count(punct) == 2)
                else:
                    assert(problem_text.count(punct) == 1)

    def test_create_algebra_problem_two_variables_type_one(self):
        for i in range(0,10):
            answer1     = random.randrange(1,9,1)
            answer2     = random.randrange(1,9,1)
            a,b,c,d,e,f = generate_components_two_vars(answer1,answer2,'one') #ax + by = c, dx + ey = f
            assert((a*answer1)+(b*answer2) == c)
            assert((d*answer1)+(e*answer2) == f)
        
        
class TestParseTextFunctions(unittest.TestCase):

    def test_convert_file_to_text_string(self):
        long_string_of_text = "on a branch\nfloating downriver\na cricket, singing\n"
        temp_test_file = open('./temp_test_file.txt','w')
        temp_test_file.write(long_string_of_text)
        temp_test_file.close()
        new_long_string = convert_file_to_text_string('./temp_test_file.txt')
        assert(long_string_of_text == new_long_string)
        os.remove('./temp_test_file.txt')

    def test_convert_file_to_text_string_2(self):
        #this time it has capital letters, and no ending eol
        long_string_of_text = "An ancient pond!\nWith a sound\nfrom the water\nOf the frog\nas it plunges in."
        temp_test_file = open('./temp_test_file.txt','w')
        temp_test_file.write(long_string_of_text)
        temp_test_file.close()
        target_string = "an ancient pond!\nwith a sound\nfrom the water\nof the frog\nas it plunges in.\n"
        new_long_string = convert_file_to_text_string('./temp_test_file.txt')
        assert(target_string == new_long_string)
        os.remove('./temp_test_file.txt')

    def test_convert_file_to_text_string_3(self):
        #this time trailing space which should be removed
        long_string_of_text = "On a withered branch\nA crow is sitting \nThis autumn eve.\n "
        temp_test_file = open('./temp_test_file.txt','w')
        temp_test_file.write(long_string_of_text)
        temp_test_file.close()
        target_string = "on a withered branch\na crow is sitting\nthis autumn eve.\n"
        new_long_string = convert_file_to_text_string('./temp_test_file.txt')
        assert(target_string == new_long_string)
        os.remove('./temp_test_file.txt')

    def test_count_char_frequencies(self):
        text_string = 'a bb ccc dddd  '
        letter_freqs = count_char_frequencies(text_string)
        assert(len(letter_freqs) == 5)
        assert(letter_freqs['a'] == 1)
        assert(letter_freqs['b'] == 2)
        assert(letter_freqs['c'] == 3)
        assert(letter_freqs['d'] == 4)
        assert(letter_freqs[' '] == 5)

if __name__ == '__main__':
    unittest.main()
