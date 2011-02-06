from decimal import *
getcontext().prec = 8

class Vector:
	__slots__ = ['x', 'y']
	__hash__ = None

	def __init__(self, x=0, y=0):
		self.x = decimal(x)
		self.y = decimal(y)

	def __copy__(self):
		return self.__class__(self.x, self.y)

	copy = __copy__

	def __repr__(self):
		return 'Vector(%.2f, %.2f)' % (self.x, self.y)

	def __eq__(self, other):
		if isinstance(other, Vector):
			return self.x == other.x and self.y == other.y
		else:
			assert hasattr(other, '__len__') and len(other) == 2
			return self.x == other[0] and self.y == other[1]

	def __ne__(self, other):
		return not self.__eq__(other)

	def __nonzero__(self):
		return self.x != 0 or self.y != 0

	def __len__(self):
		return 2

	def __getitem__(self, key):
		return (self.x, self.y)[key]

	def __setitem__(self, key, value):
		l = [self.x, self.y]
		l[key] = value
		self.x, self.y = l

	def __iter__(self):
		return iter((self.x, self.y))

	def __getattr__(self, name):
		try:
			return tuple([(self.x, self.y)['xy'.index(c)] \
						  for c in name])
		except ValueError:
			raise AttributeError, name

	'''
	def __setattr__(self, name, value):
		if len(name) == 1:
			object.__setattr__(self, name, value)
		else:
			try:
				l = [self.x, self.y]
				for c, v in map(None, name, value):
					l['xy'.index(c)] = v
				self.x, self.y = l
			except ValueError:
				raise AttributeError, name
	'''

	def __add__(self, other):
		if isinstance(other, Vector):
			# Vector + Vector -> Vector
			# Vector + Point -> Point
			# Point + Point -> Vector
			if self.__class__ is other.__class__:
				_class = Vector
			else:
				_class = Point2
			return _class(self.x + other.x,
						  self.y + other.y)
		else:
			assert hasattr(other, '__len__') and len(other) == 2
			return Vector(self.x + other[0],
						   self.y + other[1])
	__radd__ = __add__

	def __iadd__(self, other):
		if isinstance(other, Vector):
			self.x += other.x
			self.y += other.y
		else:
			self.x += other[0]
			self.y += other[1]
		return self

	def __sub__(self, other):
		if isinstance(other, Vector):
			# Vector - Vector -> Vector
			# Vector - Point -> Point
			# Point - Point -> Vector
			if self.__class__ is other.__class__:
				_class = Vector
			else:
				_class = Point2
			return _class(self.x - other.x,
						  self.y - other.y)
		else:
			assert hasattr(other, '__len__') and len(other) == 2
			return Vector(self.x - other[0],
						   self.y - other[1])

   
	def __rsub__(self, other):
		if isinstance(other, Vector):
			return Vector(other.x - self.x,
						   other.y - self.y)
		else:
			assert hasattr(other, '__len__') and len(other) == 2
			return Vector(other.x - self[0],
						   other.y - self[1])

	def __mul__(self, other):
		assert type(other) in (int, long, float)
		return Vector(self.x * other,
					   self.y * other)

	__rmul__ = __mul__

	def __imul__(self, other):
		assert type(other) in (int, long, float)
		self.x *= other
		self.y *= other
		return self

	def __div__(self, other):
		assert type(other) in (int, long, float)
		return Vector(operator.div(self.x, other),
					   operator.div(self.y, other))


	def __rdiv__(self, other):
		assert type(other) in (int, long, float)
		return Vector(operator.div(other, self.x),
					   operator.div(other, self.y))

	def __floordiv__(self, other):
		assert type(other) in (int, long, float)
		return Vector(operator.floordiv(self.x, other),
					   operator.floordiv(self.y, other))


	def __rfloordiv__(self, other):
		assert type(other) in (int, long, float)
		return Vector(operator.floordiv(other, self.x),
					   operator.floordiv(other, self.y))

	def __truediv__(self, other):
		assert type(other) in (int, long, float)
		return Vector(operator.truediv(self.x, other),
					   operator.truediv(self.y, other))


	def __rtruediv__(self, other):
		assert type(other) in (int, long, float)
		return Vector(operator.truediv(other, self.x),
					   operator.truediv(other, self.y))
	
	def __neg__(self):
		return Vector(-self.x,
						-self.y)

	__pos__ = __copy__
	
	def __abs__(self):
		return math.sqrt(self.x ** 2 + \
						 self.y ** 2)

	magnitude = __abs__

	def magnitude_squared(self):
		return self.x ** 2 + \
			   self.y ** 2

	def normalize(self):
		d = self.magnitude()
		if d:
			self.x /= d
			self.y /= d
		return self

	def normalized(self):
		d = self.magnitude()
		if d:
			return Vector(self.x / d, 
						   self.y / d)
		return self.copy()

	def dot(self, other):
		assert isinstance(other, Vector)
		return self.x * other.x + \
			   self.y * other.y

	def cross(self):
		return Vector(self.y, -self.x)

	def reflect(self, normal):
		# assume normal is normalized
		assert isinstance(normal, Vector)
		d = 2 * (self.x * normal.x + self.y * normal.y)
		return Vector(self.x - d * normal.x, self.y - d * normal.y)

