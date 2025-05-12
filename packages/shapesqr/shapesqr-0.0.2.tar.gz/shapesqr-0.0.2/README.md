# Shape Square Calculation Library #

## What is this? ##
The test task which should calculate square of circle by its radius and triangle by its sides.

## Quick Guide ##
Set up the library

```
pip install shapesqr
```

Then import ShapeFabric from the library and pass into its constructor a tuple, containing one or three integers or floats.

```
from shapesqr import ShapeFabric


circle = ShapeFabric().get_shape((1.0,))

triangle = ShapeFabric().get_shape((4, 3, 5))
```


----------


### Using ###


Using the library is as simple and convenient as possible:

```
    from shapesqr import ShapeFabric


    circle = ShapeFabric().get_shape((1.0,))
    circle.get_shape_type()  # "circle"
    
    circle.calculate_square()
    status, result = shape.get_calculated_result()  # 1 - for OK, -1 - for NOK, 0 - default
```


----------


## Developer ##
My site: [link](https://github.com/DmitriyReztsov) 