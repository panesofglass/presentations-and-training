"""
Liscov Substitution Principle

Derived classes must be substitutable for their base classes.

The LSV deals with abstractions related to polymorphism and inheritance,
as well as coupling. In particular, the LSV states that the consumer
of your abstraction should be able to use any concrete implementations
with the expectation that they will behave similarly. In other words,
if I ask you for a parser, you shouldn't start spitting out text to the
console when other implementations only return a parsed representation.

In Python, abstract base classes really aren't necessary since we can
rely on duck typing. In that light, I've merely refactored the types
to not inherit from a base class. In other languages, we would have gone
back and created abstract base classes for letter vs. tabloid reports.

We finally begin to really get into the ideas of coupling. Coupling is
necessary to write software. If nothing knows about anything else, then
you will have a difficult time writing anything useful.

"""

class Rectangle(object):
  """
  Represents a rectangle.

  >>> r = Rectangle()
  >>> r.height = 4
  >>> r.area()
  Traceback (most recent call last):
      ...
  TypeError: unsupported operand type(s) for *: 'int' and 'NoneType'
  >>> r.width = 5
  >>> r.area()
  20
  """
  def __init__(self):
    self._height = None
    self._width = None

  @property
  def height(self):
    return self._height

  @height.setter
  def height(self, h):
    self._height = h

  @property
  def width(self):
    return self._width

  @width.setter
  def width(self, w):
    self._width = w

  def area(self):
    return height * width

class Square(Rectangle):
  """
  Represents a square as a subclass of rectangle.

  >>> s = Square()
  >>> s.height = 4
  >>> s.area()
  16
  >>> s.width = 5
  >>> s.area()
  25
  """
  @property
  def height(self):
    return self._height

  @height.setter
  def height(self, h):
    self._height = h
    self._width = h

  @property
  def width(self):
    return self._width

  @width.setter
  def width(self, w):
    self._width = w
    self._height = w

# The tests pass, but if I set height and width, I'm expecting the same thing,
# especially if the Square I have is a Rectangle when I'm using it.

if __name__ == "__main__":
  import doctest
  doctest.testmod()
