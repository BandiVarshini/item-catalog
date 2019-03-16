<p align="left">
By-: B.Varshni
</p>

### item-catalog
*************************************************************************************************************************************
> It is the item catalog project in UACITY FULL STACK.

### Abstract-:
*************************************************************************************************************************************
> Our Agenda is in this project we have categories like novel(Parent) and book(child). By using CRUD operations(Edit, Delete, Update, Retreve) we modify the data. Currently OAuth2 implemented for Google Accounts. OAuth2 provides authentication for CRUD operations. 
### Python files-:
*************************************************************************************************************************************
 - I have one main file ----------> `novel.py` 
 - One database file ------------->`novel_database.py`
 - One novel information file ---->`novelinfo.py` 
### How to run python files
*************************************************************************************************************************************
 - pyhon novel.py
 - python novel_database.py
 - python novelinfo.py
### Install Libraries
*************************************************************************************************************************************
 - pip install Flask 
 - pip install SQLalchemy
 - pip install requests
 - pip install psycopg2
 - pip install OAuth2client
### Softwares for item-catalog
*************************************************************************************************************************************
 - `python3` - It is a general-purpose interpreted, interactive, object-oriented, and high-level programming language.
 - `Git-Bash` - Git is a distributed version-control system for tracking changes in source code.
 - `Virtual-Box` - Oracle VM VirtualBox is a free and open-source hosted hypervisor.
 - `Vagrant` - It is an open-source softwarw product for building and maintaining portable virtual software development environmeants.
 - `DB browser` - Unlike client–server database management systems, the SQLite engine has no standalone processes with which the application program communicates. 
 - `Any Editor` - Like (Sublime text, Notepad, Notepad++, Visual Studio) I'm using Sublime text.
### Download Links

 | Softwares | Links |
 | ------------ | ----- |
 | Python3 | [https://www.python.org/downloads/] |
 | Git-Bash | [https://git-scm.com/downloads] |
 | Virtual-Box | [https://www.virtualbox.org/wiki/Downloads] |
 | Vagrant | [https://www.vagrantup.com/downloads.html] |
 | DB browser | [https://sqlitebrowser.org/dl/] |
 | Sublime text | [https://www.sublimetext.com/3] |
### Requirements for item-catalog
*************************************************************************************************************************************
 -> `python3` - It is a general-purpose interpreted, interactive, object-oriented, and high-level programming language.
 -> `HTML` - Hypertext Markup Language is the standard markup language for creating web pages and web applications. (we save files with `.html`).
 ->`CSS` - Cascading Style Sheets (it is used for styling the web pages).
 -> `BOOTSTRAP` - It contains HTML and CSS-based design templates for typography, forms, buttons, navigation and other interface components, as well as optional JavaScript extensions.(It is FRONT-END-FRAMEWORK)
 -> `JavaScript(JS)` - is a lightweight, interpreted or JIT compiled programming language with first-class functions. Most well-known as the scripting language for Web pages, many non-browser environments also use it, such as node.js and Apache CouchDB.
 -> `OAuth` - (Open Authorization) is an open standard for token-based authentication and authorization on the Internet.
 ->`Flask` - Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries (except for some basics standard libraries such as bottom.
 ->`SQLalchemy` -  SQLAlchemy's philosophy is that relational databases behave less like object collections as the scale gets larger and performance starts being a concern, while object collections behave less like tables and rows as more abstraction is designed into them.

### Process for login through Google authentication
*************************************************************************************************************************************
> Open Browser and go to [console.developers.google.com](https://console.developers.google.com/)
> Create a new project based on your UDACITY-PROJECT-NAME.
> Then click on Credentials, to create a new credentials, and after that there wiil be a dialogue box showing.
> Click on OAuth client ID, then you will see a option format for application type.
> Select on `Web-application`, and then click on create button.
> Fill the given columns with appropriate `HTTP` URL's.
> After filling the columns with appropriate details
> Download the `JSON` file, renamed it as `client_secrets.json`
> After complition of this process. You used this in your project.

### JSON Endpoints
*************************************************************************************************************************************
`localhost:5000/novel/JSON`

`localhost:5000/novel/<int:novel_id>/main/<int:book_id>/JSON`
	
`localhost:5000/novel/<int:book_id>/main/JSON`