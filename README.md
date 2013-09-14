things_indifferent
==================

Things indifferent web project. A web constructor of courses with a little bit stoicism. This is my first project in web-development, so don't be too rigorous about that, pls.

The supported features:
+ user registration
+ simple blog system with comments. (User can create posts but can't delete anything)
+ simple to-do system. User can add new tasks, freeze them, finish (then some experience is gained) or fail. Privacy is allowed.

Everything is written from the basement, and im very gratefull to Steve Huffmon (and his course:https://www.udacity.com/course/cs253).
So it means that it's a not serious project but a prototype of future full version. Stay with me.

Shortcomings:
- bad structure of code, some classes should be reorganised
- the user's input is not safe (though all they can do is to not close  b and i tags - the only two tags are allowed)
- the site is vulnerable to cross-site scripting

Thanks
- the background image is under GPL v2 from kde-look.org.
- Sass bootstrap http://alademann.github.io/sass-bootstrap/
  I included it in the presented code
- Steve Huffman

Use google app engine to run this project.
1) Download Google App Engine SDK
2) copy this folder to GAE folder
3) write in console: python ./dev_appserver.py things_indifferent/
4) open http://localhost:8080/ in your browser


