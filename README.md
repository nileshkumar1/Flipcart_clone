#FleaMarket
# Django E-commerce Flipkart Clone
## Project Summary
#This is the [LIVE DEMO](https://mubinattar.pythonanywhere.com/) of the project.


This project deals with developing a Virtual website 'E-commerce Website'. It provides the user with a list of the various products available for purchase in the store. For the convenience of online shopping, a shopping cart is provided to the user.

---
E-commerce website built with Django. It has following functionality:
- user registration
- add / change user billing address
- add / remove item from cart
- change the default billing address during the checkout process
- apply a promotion code during the checkout process
- pay for a order using Stripe
- list all proceeded orders
- request a refund for a order

The purpose of this project was to learn Django Framework.

----


## Setup

To get this project up and running you should start by having Python and Django installed on your computer. It's advised you create a virtual environment to store your projects dependencies separately. You can install virtualenv with

```
pip install virtualenv
```

Clone or download this repository and open it in your editor of choice. In a terminal (mac/linux) or windows terminal, run the following command in the base directory of this project

```
virtualenv env
```

That will create a new folder `env` in your project directory. Next activate it with this command on mac/linux:

```
source env/bin/active
```

Then install the project dependencies with

```
pip install -r requirements.txt
```

Now you can run the project with this command

```
python manage.py runserver
```

**Note** if you want payments to work you will need to enter your own Stripe API keys into the `.env` file in the settings files.

