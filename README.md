# tensorflow-calc

A normal calculator...implemented in Tensorflow for no good reason.

Step 0: Set up a virtual environment

```
pip install virtualenv   # if you don't have virtualenv already
virtualenv venv
source venv/bin/activate
```

Step 1: Install tensorflow

Choose the right `pip install` for your platform (CPU-only, Python 2.7): https://www.tensorflow.org/versions/r0.9/get_started/os_setup.html#pip-installation

Step 2: Run the program.  `python main.py` for a calculator CLI or `python main.py test` to evaluate a few test expressions.

Step 3: After you've evaluated some expressions, run tensorboard on the logs to visualize your tensor graph.

`tensorboard --logdir logs/`

Then go to http://localhost:6006/#graphs to view them.

![](http://i.imgur.com/6aPY95J.png)

![](http://i.imgur.com/nZNpm5O.png)

wow
