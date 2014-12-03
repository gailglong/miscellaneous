import menulooper
import pathbuilder
import os

def rm_elements(elements, ary):
    for ii in elements:
        x.remove_path(ary[ii])
    return False

def i_elements(elements, ary):
    x.insert_path(int(elements[0]), '/foo/bar/snafu')
    return False

def mv_elements_down(elements, ary):
    x.move_down(ary[elements[0]])
    return False

def mv_elements_up(elements, ary):
    x.move_up(ary[elements[0]])
    return False

x = pathbuilder.PathBuilder(os.getenv('PATH'))
print str(x.get_current_path_array())
"""
y = menulooper.MenuLooper(
        {
            'choices' : x.get_current_path_array(),
            'msg' : 'Choose element to move up one',
            'justone' : True,
            'callback' : mv_elements_up
        }
    )
"""
x.add_dot()
print
print str(x.get_current_path_array())
