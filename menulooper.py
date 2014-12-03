#!/usr/bin/python

import re

"""
An exception with a descriptive name
"""
class DefaultChoiceError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)


class MenuLooper:
  """
  A class that provides convenient commandline/console menus
  """
  def __init__(self, params=None, runloop=True):
    self.option_cnt = 0
    self.optionArray = {}

    """
    An array of choices to display.
    TODO: at some point this should also accept a dictionary and
    ensure the order remains consistent
    """
    try:
      self.choices = params['choices']
    except KeyError:
      print "NO MENU CHOICES GIVEN!"
      return None

    """
    A string of any specific key options. With the callback handler
    the designer can specify special handling based on a particular
    choice.  In future versions they'll be able to provide an 
    additional handler for the options keys.
    """
    try:
      self.options = params['options']
    except KeyError:
      self.options = "q or Q to quit"

    """
    Top Message
    """
    try:
      self.msg = params['msg']
      self.curmsg = self.msg
    except KeyError:
      self.msg = "Choose from List"
      self.curmsg = self.msg

    """
    Bottom Prompt.
    """
    try:
      self.prompt = params['prompt']
    except KeyError:
      self.prompt = ''

    """
    Message to use for most errors.
    """
    try:
      self.errormsg = params['errormsg']
    except KeyError:
      self.errormsg = 'Please Choose from The Options Provided'

    """
    An alternate top message in the event that the user chooses
    more than one selection and justone is set
    """
    try:
      self.justonemsg = params['justonemsg']
    except KeyError:
      self.justonemsg = 'Please Choose Only One Item from The Options Provided'

    """
    A handler to fire when the choices have been processed by the menu
    code.  This is currently two way code.  If the handler returns True
    the loop will rerun.  If it returns False it exits.
    """
    try:
      self.handler = params['callback']
    except KeyError:
      pass

    """
    A default value provided for user convenience.
    """
    try:
      self.verify_default(params['default'])
    except KeyError:
      self.default = None

    """
    Currently the class only provides numeric choice keys.  In future
    editions it will be able to provide alpha and string choices
    """
    try:
      self.menutype = params['menutype']
    except KeyError:
      self.menutype = 'numeric'

    """
    Allows the user to make only one choice.  Helpful for yes no or 
    true false prompts.
    """
    try:
      self.justone = params['justone']
    except KeyError:
      self.justone = False

    """
    An param that will allow the developer to delay running the
    loop until required otherwise it runs when the constructor fires.
    """
    if runloop is True:
      self.run_loop()

  def run_loop(self):
    """
    The primary menu loop. Runs based on rules set in init defaults
    or input parameters from calling code.
    """
    looper = True
    self.menu = self.make_numeric_menu()

    while looper is True:
      print
      print self.curmsg

      ans = raw_input(self.menu)

      if ans is '' and self.default:
        for (k, v) in self.optionArray.iteritems():
          if v == self.default:
            self.userChoices = k

      else:
        self.userChoices = self.split_choices(ans)

        for choice in self.userChoices:
          if choice in ['q','Q','quit','exit']:
            looper = False
            break

      if self.test_answer(self.userChoices) is True:
        try:
          looper = self.handler(self.userChoices, self.optionArray)
        except Exception as e:
          return self.userChoices

  def test_answer(self, choices):
    """
    Basic input checks.
    """
    error = False

    if self.test_choice_length(choices) is True:
      return

    if self.menutype is 'numeric':
      for choice in choices:
        if choice not in self.optionArray:
          error = True

    self.error = error
    if error is True:
      self.curmsg = self.errormsg
      return False
    else:
      self.curmsg = self.msg
      return True

  def test_choice_length(self, choices):
    """
    Length checks and the place to catch min max numbers of inputs.
    """
    if self.justone is True:
      if len(choices) > 1:
        self.curmsg = self.justonemsg
        return True
    if len(choices) > len(self.choices):
      self.userChoices = range(1,len(self.choices) + 1)
      return False
    return False


  def make_numeric_menu(self):
    """
    Build a numeric selection list and create an internal dictionary
    that lets us correlate the entries.
    """
    cnt = 1
    menu = []
    self.menu = {}

    for choice in self.choices:
      cntStr = str(cnt)
      chStr = str(choice)
      menu.append("\t{}.\t{}".format(cntStr, chStr))
      self.optionArray[cntStr] = chStr
      cnt += 1

    try:
      menu.append("{} {} Default [{}]: ".format(self.options , self.prompt,
        self.default))
    except Exception:
      menu.append("{} {}: ".format(self.options , self.prompt))

    menuOut = '\n'.join(menu)
    menuOut = menuOut.rstrip('\n')
    return menuOut


  def set_default(self, value=None):
    """
    A default value setter.  Defaults may change based on context of
    the calling program.
    """
    if value is not None:
      self.default = value


  def set_prompt(self, prompt=None):
    """
    Bottom line setter.
    """
    if prompt is not None:
      self.prompt = prompt


  def set_error_prompt(self, eprompt=None):
    """
    Message to display when an input violation occurs. Can
    be set from the external code. 
    """
    if eprompt is not None:
      self.errormsg = eprompt


  def verify_default(self, default):
    """
    Make sure that our input default value is also in the list of choices
    """
    if default not in self.choices:
      raise DefaultChoiceError("Default choice not included in list of choices")
    else:
      self.default = default


  @staticmethod
  def split_choices(choices):
    """
    A convenience method provided as a way to split the 
    choices into a useable string array using either whitespace or commas.
    """
    myLen = len(re.findall(',', choices))
    if myLen > 0:
      return [s.strip() for s in choices.split(',')]
    else:
      regx = re.compile('\s+')
      return [s.strip() for s in regx.split(choices)]

