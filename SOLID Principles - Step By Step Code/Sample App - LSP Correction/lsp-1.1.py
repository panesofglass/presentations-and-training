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

# Here's a better implementation that doesn't violate LSP:

class IShape(object):
  def __init__(self):
    raise NotImplementedError
  def area(self):
    """
    Calculates the area of the shape.

    Limit the interface to this lone function.
    Subclasses can add additional properties, as necessary.
    """
    raise NotImplementedError

class Rectangle(IShape):
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
    """
    Calculates the area of the rectangle.

    >>> r = Rectangle()
    >>> r.height = 4
    >>> r.width = 5
    >>> r.area()
    20
    """
    return height * width

class Square(IShape):
  def __init__(self):
    self._length = None

  @property
  def length(self):
    return self._length

  @length.setter
  def length(self, h):
    self._length = h

  def area(self):
    """
    Calculates the area of the square.

    >>> s = Square()
    >>> s.length = 5
    >>> s.area()
    25
    """
    return length**2

if __name__ == "__main__":
  import doctest
  doctest.testmod()
