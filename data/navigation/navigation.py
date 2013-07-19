# This Python file uses the following encoding: utf-8

from collections import namedtuple

MenuItem = namedtuple('HeaderItem',['href','name'])

#header menu - the top menu, it's allmost everywhere on the site
HeaderMenu = (MenuItem ('/home', 'home'),
			  MenuItem ('/experimental','experimental'),

	)
HeaderParameters = dict(title = "Stoicism 2.0",
                         HeaderMenu = HeaderMenu,
                         username = 'Anonymous'
                     )

#The homepage displays the concepts
Concepts = (MenuItem('/concepts/overview.html','overview'),
			MenuItem('/concepts/stoicism.html', 'stoicism'),
			MenuItem('/concepts/gamification.html', 'gamification'),
			MenuItem('/concepts/iching.html', 'iching')

	)