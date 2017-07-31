from .rect import Rect

class Builder(object):
	"""
	The Builder takes the GUI layout as a tree and
	will produce a vertex array understandable by openGL
	"""
	def __init__(self, params):
		self.window_parameters = params

	def computeLayoutRects(self, layout_elements, layout_tree):
		"""
		Given a layout tree of elements, returns the corresponding array of
		rects where the GUI elements have to be drawn (absolute position).
		The given elements have a parenting relation described by the tree,
		and a relative positionning.
		"""

		# Each data chunk is ordered this way :
		# X,	Y,    Z,	R,	G,	B,	A
		global layout
		layout_rects = []

		print(layout_elements, layout_tree)

		def _aux(subtree, node_index, rect):
			global layout
			node_element = layout_elements[node_index]

			layout_rects.append(rect)

			# Recursively apply it to the children
			for child_index, node_index in enumerate(subtree):
				c_rect = node_element.child_rects[child_index].fitRect(rect)
				_aux(layout_tree[node_index], node_index, c_rect)

		_aux(layout_tree[0], 0, Rect(0, 0,
								int(self.window_parameters["resolution"][0]),
								int(self.window_parameters["resolution"][1])))

		return layout_rects

	def _relativeToAbsolute(self, element, rect):
		"""
		Given a GUI element, break it down to vertices
		and build an array of absolute coordonates out of it.
		"""
		absolute_coord = []
		prim_list = element.getBlueprintPrimitives()
		color_list = element.getColors()
		for p in prim_list:
			c = color_list[p.getColorId()]
			for v in p.getVerticies():
				# Each vertex transforms with respect to its limiting attributes
				X = v.x * rect.w + rect.x
				Y = v.y * rect.h + rect.y

				cv = [X, Y, 0.0, c.R/255.0, c.G/255.0, c.B/255.0, 1.0]
				absolute_coord += cv

		return absolute_coord