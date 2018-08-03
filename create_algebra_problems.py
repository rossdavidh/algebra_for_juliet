from __future__ import division
import random

numerals = {'1':'[one]','2':'[two]','3':'[three]','4':'[four]','5':'[five]','6':'[six]','7':'[seven]','8':'[eight]','9':'[nine]'}

def determine_sign(nbr):
    if (random.random() < 0.5):
        return (-1 * nbr)
    else:
        return nbr

def create_algebra_problem_one_variable(letter, answer,problem_type = 'one'):
    assert(type(letter) is str)
    assert(type(answer) is int)

    a,b,c,d,e      = generate_components_one_var(answer,problem_type)
    problem_string = problem_text_one_var(a,b,c,d,e,letter,problem_type)
    return problem_string

def create_algebra_problem_two_variables(letter1,letter2,answer1,answer2,problem_type = 'one'):
    assert(type(letter1) is str)
    assert(type(letter2) is str)
    assert(type(answer1) is int)
    assert(type(answer2) is int)

    a,b,c,d,e,f    = generate_components_two_vars(answer1,answer2,problem_type)
    problem_string = problem_text_two_vars(a,b,c,d,e,f,letter1,letter2,problem_type)
    return problem_string

def generate_components_one_var(answer,problem_type):
    assert(type(answer) is int)

    a     = determine_sign(random.randrange(1,9,1))
    b     = determine_sign(random.randrange(1,9,1))
    c     = determine_sign(random.randrange(1,9,1)) #sometimes overwritten
    d     = 0 #sometimes not used
    e     = 0 #sometimes not used
    if (problem_type == 'one'): #ax + b = c
        c = (a * answer) + b
    elif (problem_type == 'two'): #ax/b = c
        c = a * answer / b
    elif (problem_type == 'three'): #ax + b + cx = d
        if a == (-1*c):
            a = -1 * a  #done to avoid x terms cancelling out
        d = (a * answer) + b + (c * answer)
    elif (problem_type == 'four'): #a(bx + c) = d
        d = a * ((b * answer) + c)
    elif (problem_type == 'five'): # ax + b = cx + d
        if a == c:
            a = -1 * a #done to avoid x terms cancelling out
        d = ((a-c)*answer) + b
    elif (problem_type == 'power_two_squared_only'): # ax^2 + b = c
        c = (a*answer*answer) + b
    elif (problem_type == 'power_two_one_squared_term'): # ax^2 + bx + c = dx + e
        d = determine_sign(random.randrange(1,9,1))
        e = (a*answer*answer) + ((b - d)*answer) + c
    elif (problem_type == 'power_two_two_squared_terms'): #ax^2 + bx = cx^2 + dx + e
        d = determine_sign(random.randrange(1,9,1))
        e = ((a-c)*answer*answer) + ((b-d)*answer)
    else:
        raise ValueException('Unknown problem type: '+str(problem_type))
    return a,b,c,d,e 

def generate_components_two_vars(answer1,answer2,problem_type):
    assert(type(answer1) is int)
    assert(type(answer2) is int)

    a     = determine_sign(random.randrange(1,9,1))
    b     = determine_sign(random.randrange(1,9,1))
    c     = 0
    d     = determine_sign(random.randrange(1,9,1)) 
    e     = determine_sign(random.randrange(1,9,1)) 
    f     = 0

    if (problem_type == 'one'): #ax + by = c, dx + ey = f
        c = (a * answer1) + (b * answer2)
        f = (d * answer1) + (e * answer2)
    else:
        raise ValueException('Unknown problem type: '+str(problem_type))
    return a,b,c,d,e,f

def printable(letter):
    if letter == '_' or letter == ' ':
        printable_letter = '[space]'
    elif letter == '\'':
        printable_letter = '[apostrophe]'
    elif letter == ',':
        printable_letter = '[comma]'
    elif letter == '?':
        printable_letter = '[question mark]'
    elif letter == '"':
        printable_letter = '[quotation mark]'
    elif letter == '!':
        printable_letter = '[exclamation point]'
    elif letter == '.':
        printable_letter = '[period]'
    elif letter == '(':
        printable_letter = '[open parentheses]'
    elif letter == ')':
        printable_letter = '[close parentheses]'
    elif letter == ';':
        printable_letter = '[semicolon]'
    elif letter == '-':
        printable_letter = '[dash]'
    elif letter == ':':
        printable_letter = '[colon]'
    elif letter == '[':
        printable_letter = '[left bracket]'
    elif letter == ']':
        printable_letter = '[right bracket]'
    elif letter == '/':
        printable_letter = '[slash]'
    elif letter in numerals.keys():
        printable_letter = numerals[letter]
    else:
        printable_letter = letter
    return printable_letter

def problem_string_postproc(pts,letter,printable_letter):
    pts = pts.replace(" + -"," - ")
    if letter == "l":
        pts = pts.replace("l","L") # in some fonts l and 1 look too similar
    if printable_letter[0] == '[':
        pts = pts.replace(printable_letter,'*'+printable_letter) #e.g. 3[period] should become 3*[period]
    return pts


def problem_text_one_var(a,b,c,d,e,letter,problem_type):
    printable_letter  = printable(letter)
    if problem_type == 'one':
        pts = '{0}{4} + {2} = {3}    {1} = ___?'.format(a,letter,b,c,printable_letter)
    elif problem_type == 'two':
        c_rounded_off = '%.3f'%(c)
        while ('.' in c_rounded_off) and (c_rounded_off[-1] in ['0','.']):
            c_rounded_off = c_rounded_off[0:-1]
        if c_rounded_off[0] == '.':
            c_rounded_off = '0'+c_rounded_off 
        pts = '{0}{4}/{2} = {3}    {1} = ___?'.format(a,letter,b,c_rounded_off,printable_letter)
    elif problem_type == 'three':
        pts = '{0}{5} + {2} + {3}{5} = {4}    {1} = ___?'.format(a,letter,b,c,d,printable_letter)
    elif problem_type == 'four':
        pts = '{0}({1}{5} + {3}) = {4}    {2} = ___?'.format(a,b,letter,c,d,printable_letter)
    elif problem_type == 'five':
        pts = '{0}{5} + {2} = {3}{5} + {4}    {1} = ___?'.format(a,letter,b,c,d,printable_letter)
    elif problem_type == 'power_two_squared_only': #ax^2 + b = c
        pts = '{0}{4}^2 + {2} = {3}    {1} = ___?'.format(a,letter,b,c,printable_letter)
    elif problem_type == 'power_two_one_squared_term': #ax^2 + bx + c = dx + e
        pts = '{0}{6}^2 + {2}{6} + {3} = {4}{6} + {5}    {1} = ___?'.format(a,letter,b,c,d,e,printable_letter)
    else: #ax^2 + bx = cx^2 + dx + e
        pts = '{0}{6}^2 + {2}{6} = {3}{6}^2 + {4}{6} + {5}    {1} = ___?'.format(a,letter,b,c,d,e,printable_letter)
    return problem_string_postproc(pts,letter,printable_letter)

def problem_text_two_vars(a,b,c,d,e,f,letter1,letter2,problem_type):
    printable_letter1 = printable(letter1)
    printable_letter2 = printable(letter2)
    if problem_type == 'one': #ax + by = c, dx + ey = f
        pts  = '{0}{8} + {1}{9} = {2}    {6} = ___?\n'
        pts += '{3}{8} + {4}{9} = {5}    {7} = ___?'
        pts  = pts.format(a,b,c,d,e,f,letter1,letter2,printable_letter1,printable_letter2)
    else: #ax^2 + bx = cx^2 + dx + e
        pts = '{0}{6}^2 + {2}{6} = {3}{6}^2 + {4}{6} + {5}    {1} = ___?'.format(a,letter,b,c,d,e,printable_letter)
    pts = problem_string_postproc(pts,letter1,printable_letter1)
    pts = problem_string_postproc(pts,letter2,printable_letter2)
    return pts

