BGELive
=======

A callback-based component framework built the Blender Game Engine's Python api.


# Why use BGELive?

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
class player():
  def __init__(self):
    self.health = 100:
  
  def run(self):
    if self['timer'] > 1.0 and len( self.sensors['Collision'].hitObjectList > 0 ):
      self.health -= 1
      self['timer'] = 0
```
          
Using BGELive, one might write it like this:

```python
class player():
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
