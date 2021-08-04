# Welcome to Zala's Manual
## Notice: This repository (Zala) is archived, with no future plans. 
___

Welcome to Zala!
Zala is a general-purpose, fast, and lightweight programming langauge with unique syntax.

Start with a basic program:

```

print("Hello World!");

```
This prints out "Hello World" to the console, similar to python.

You can also assign variables.
```
myvar is 7;
```
Notice how we don't use the `=` sign, but use `is` instead. This syntax may look odd but it's a unique alternative for using `==` in `if` statements.

Speaking of if statements, here is an example of an if statement being used:
```
if 10 > 5 {
  print("10 is greater than 5!");
} else {
  print("10 is not greater than 5!");
}
```
You see, Zala has a unique attribute where an entire program can be on one line. It achieves that by completely ignoring any form of whitespace in your code. This is why `;`s are required in all single statement, but can be ignored in block statements such as `if`

This example prints "10 is greater than 5!" if 10 is greater than 5, else it will print "10 is not greater than 5!"

While statements have the same attributes as `if` but are also quite different. For one, they do not have an `else` function.
```
while 10 > 5 {
  if 10 < 5 {
    break;
  }
}
```
They can also be stopped even though the statement is still true. It is possible to loop indefinitely with `while True`.

You can loop for a limited amount with `loop` and `iterate`.
```
loop 5 {
  print("Hi!");
}
```
```
iterate range(1, 5) with x {
  print(x);
}
```
Now, these functions may seem similar, but they are not. `loop` does not store any information to a variables and executes much faster than `iterate`. Meanwhile, `iterate` can iterate any iterables such as a list or a dictionary. It also stores variable information.

`loop 5` is highly suggested over `iterate range(0, 5)` because it operates much quicker. If you need to get the current loop number, you'll need to use `iterate`.

Now let's get into the spicy stuff, Classes and Functions!
```
class myClass {
  myvar is 2;
  def myfunc() {
    return 2;
  }
  class myOtherClass { myvar is 2; }
}
```
Classes, when created, are a bit similar to objects but are also different. You cannot create objects, but you can edit class attributes by assigning variables which can be accessed in your 
program. 
Objects are similar to classes. How they work is that they clone the class without providing refrence to it. This means that all attributes of the class are editable.
```
class customobj {
  attr is void;
  def init(obj) {
    obj.attr is 5;
    return obj;
  }
  def run(obj) {
    print(obj.attr);
  }
}
```
There are currently no methods to modify how your class works. Things such as initialization must be called directly by the user. (special methods comming soon).
```
myobj is customobj()
myobj.init();
myobj.run();

#You could also do this
customobj.run(myobj);
```
**Dont do these**:
```
#big nono
myobj is customobj().init();
```
This is not supported for now. You'll need to load a init method after. This is because `customobj` has not been copied properly.

You can also import other files and load them as a class. Then you can access attributes.
```
import myClass

print(myClass.myfunc());
```
Some Zala Py-Extenstions allow you to import classes from the web. Zala's built-in package manager lets you import code snippets directly from the web.
```
import pakrat

pakrat.import("hello_world");
hello_world.hello
```
While useful, it is not suboptimal and is reliant on a internet connection. Future Pakrat implementations will expand to installing larger and optimized Zala code. 

That's it for the Manual. There are features I may have missed, and some other things. There are built-in libs written in python, so if you would like refrence to them, please check `src/lib/README.md`
