BGELive
=======

A callback-based component framework built the Blender Game Engine's Python api.


## Why use BGELive?

The Blender Game Engine has a very powerful python api, allowing the programmer to do nearly anything they might want to with the game engine, and is surprisingly flexible, allowing for a wide range of coding styles. This power and flexibility, however, comes at the cost of complexity: The engine provides little in the way of flow control, and writing simple, reuseable code can be complicated. In addition, keeping track of states in the game engine can become complicated in real-world use cases.

### Why components?

There not enough room for a full advocacy of component systems here, but [this article] (http://www.raywenderlich.com/24878/introduction-to-component-based-architecture-in-games) provides a good explanation, although it is somewhat dismissive of object-oriented programming, which can complement a component system nicely. BGELive uses an approach similar to the second one in the article.

Simply put, component systems allow you to easily reuse code between a variety of game objects without worrying about complex object inheritance trees.

### BGELive's approach: Why callbacks?

While an entity componet system has it's strengths, as described by the aforementioned article, it is designed to be run from the engine level of a game, and while this could be mimiced by the Blender Game Engine, it ignores the existing design, in which each object has it's own script.

BGELive uses callbacks, run by each object during the logic phase. These callbacks can be swapped in and out at will, allowing for a virtually endless number of states in a game object. For example, a player object can have an enemy collision callback, which is temporarily removed after the player is hit, making them invincible. Meanwhile, a control callback will continue to run without being aware that the player has been hit. Callbacks can be any callable object: including a standard function, an object with a `__call__` function, or a [closure] (http://www.shutupandship.com/2012/01/python-closures-explained.html), allowing each callback to store variables; In the previous example, the enemy hit callback could have stored the player's health.

Callbacks also allow for function nesting. This can be useful for fun things like having a callback that counts down before running another function. This function chaining it the backbone of BGELive.

### An example

For this example, we will write a simple object that takes damage on colliding with an object, and then turns invincible for one second before returning to normal.

In the game engine, this might typically be accomplished like this, assuming that there is a timer named `timer`:

```python
class player(KX_GameObject):
  def __init__(self):
    self.health = 100:
  
  def run(self):
    if self['timer'] > 1.0 and len( self.sensors['Collision'].hitObjectList > 0 ):
      self.health -= 1
      self['timer'] = 0
```
          
Using BGELive, one might write it like this:

```python
from live.gameobject import Live_GameObject
class player(Live_GameObject):
  def __init__(self):
    self.logic_components.set( collide() )
    
def collide():
  health = 100
  def collide_callback(self, id):
    if len( self.sensors['Collision'].hitObjectList > 0 ):
      from live.components import timed
      self.logic_components.set( suspend(1), id )
```

### But that's more code!
While this may seem like more code at first, it does several things that are useful in longer programs:

1. __It's reuseable:__ Not only is the collision code a reusable function, but it uses the suspend component from the availible library to pause the function without concerning the coder with the specifics.

2. __Variables are contained by the relevant compenent:__ While the example may be a bit contrived, this can help prevent the object from getting cluttered with attributes that are only rarely used, and only concern a single function. The suspend component works in this way


### But I like the way the Blender Game Engine works now!
That's fair, and you don't have to use BGELive if you don't want to. However, BGELive expands on the Blender Game Engine in other ways too, adding new features to KX_GameObject, such as new options for the applyMovement and applyRotation methods, and a new applyScale method, and more will be added in the future. Best of all, since BGELive is built on top of the current api, you can take advantage of these without changing your coding style.

## Installation
Installation is easy:

1. Download the zip file from the sidebar on the left

2. Drop the `live` folder into you project's script folder

3. __That's it__

## Basic Usage

You can start by using the following template to convert a KX\_GameObject into a Live\_GameObject 

```python
from bge import logic

from live import Live_GameObject

class YOUR_OBJECT_NAME (Live_GameObject):
  def __init__(self, obj):
  	super().__init__(obj)

def run():
  obj = logic.getCurrentController().owner
  if type(obj) == KX_GameObject:
    obj = YOUR_OBJECT_NAME( obj )
	obj.run()
```

### Core Features
#### Setting an object's components
```python
# Add a compenent to your object:
self.logic_components.set( MY_COMPONENT )

#You can save an id reference to an object by assigning the return value from the function to a variable:
id = self.logic_components.set( MY_COMPONENT )
# Or you can set one manually:
self.logic_components.set( MY_COMPONENT, id='a component' )
```

#### Structure of a component
```python
# A component callback, at its simplest, if a function that takes two arguments—
# the object to which the compenent is attached, and an id that references the component (we will get to uses for this later):
def MY_COMPONENT(obj, id):
  pass
  
# If you want to give the component additional arguments, you can use a callable object, instead:
class MY_CLASS_COMPONENT():
  def __init__(self, MY_ARGUMENT):
    self.MY_VARIABLE = MY_ARGUMENT
  def __call__(self, obj, id):
    # do something with self.MY_VARIABLE
# You can—of course—change this variable:
  ...
  def __call__(self, obj, id)
    self.MY_VARIABLE += 1
# Make sure you pass in an instance of the object to logic_callbacks in order to make sure it's __call__ed correctly:
self.logic_components.set( MY_CLASS_COMPONENT( MY_ARGUMENT ) )
    
# You can also use other methods of saving variables to your component. I'm fond of closures:
def MY_CLOSURE( MY_ARGUMENT1, MY_ARGUMENT2 ):
  def MY_COMPONENT(obj, id):
    # do something with MY_ARGUMENT1
    nonlocal MY_ARGUMENT2
    MY_ARGUMENT2 += 1
  return MY_COMPONENT
# Similar to the above, you'll need to pass in the inner function by calling the other one:
self.logic_components.set( MY_CLOSURE( MY_ARGUMENT1, MY_ARGUMENT2 ) )
```

#### Removing components from a object
```python
# Now we get to the primary use for callback ids, removing components.
# Doing so is simple:
self.logic_components.remove(id)

# This can be done from outside of a component, or within:
def self_removing_component(obj, id);
	obj.logic_components.remove(id)
```

#### Retrieving components from an object
```python
# Id's can also be used to retrieve a callback from an object:
component = self.logic_components.get(id)

# This could be useful if you want to interrupt a component briefly:
def interrupting_closure(fun):
	def interrupting_component(obj, id):
		obj.logic_components.set(fun, id=id)
...
self.logic_components.add( interupting_closure( self.logic_components.get(ID) ), id=ID)
```

#### Pausing components at scene level
```python
# Compenents can be paused at scene level by adding a list of states to pause in via the 'pause_when' arugment when setting an argument:
self.logic_components.set( MY_COMPONENT, pause_when = ['scene_pause', 'cutscene'] )

# The pause state can then be set in the scene dictionary:
logic.getCurrentScene['pause_state'] = 'cutscene'

# By using multiple states, you could have diffent components pause in different circumstances.
# During a cutscene, for example, you might want to have your player no longer accept movement input, but still
# follow cutscene scripts. Meanwhile, both components should pause when the player hits the pause button:
self.logic_components.set( controls, pause_when = ['scene_pause', 'cutscene'] )
self.logic_components.set( cutscene_script, pause_when = ['scene_pause'] )

```

### Other Features of Live_GameObject

In addition to logic components, Live\_GameObject expands upon the existing feature set of KX\_GameObject.

#### Tranforms
##### applyMovement() and applyRotation per_second
```python
# Both of these method been given the keyword argument per_second, allowing them to transform the objects in 
# blender_units and radians per second, respecively, instead of per frame:
self.applyMovement([1,1,0], per_frame=True)
self.applyRotatation([0,0,pi], per_frame=True)
```
##### applyRotation() units
```python
# You can now specify whether to use degrees or radians for applyRotation():
self.applyRotation([0,0,180], units="degrees")
self.applyRotatation([0,0,pi], units="radians")
```
##### applyScale()
```python
# A new applyScale() method has been added. Arguments are the same as for applyMovement():
self.applyScale([1,1,1], True, per_frame=True)
