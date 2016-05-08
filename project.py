from flask import Flask, render_template, request, redirect, url_for, flash, jsonify

app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, BaseMenuItem, Cuisine, RestaurantMenuItem

import RestaurantManager

import bleach


### Make a API Endpoints (for GET Requests)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
        restaurant = RestaurantManager.getRestaurant(restaurant_id)
        restaurantMenuItems = RestaurantManager.\
            getRestaurantMenuItems(restaurant_id=restaurant_id)
        return jsonify(RestaurantMenuItems=[i.serialize for i in restaurantMenuItems])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:restaurantMenuItem_id>/JSON')
def RestaurantMenuItemJSON(restaurant_id, restaurantMenuItem_id):
        restaurantMenuItem = RestaurantManager.\
            getRestaurantMenuItem(restaurantMenuItem_id)
        return jsonify(RestaurantMenuItem=restaurantMenuItem.serialize)


### Retrieve and post data

@app.route('/')
@app.route('/index/')
def restaurantManagerIndex():
        return render_template("index.html")

@app.route('/cuisines/')
def cuisines():
        cuisines = RestaurantManager.getCuisines()

        return render_template("Cuisines.html",
                               cuisines=cuisines)

@app.route('/cuisines/add/', methods=['GET', 'POST'])
def addCuisine():
        if request.method == 'POST':

            RestaurantManager.addCuisine(bleach.clean(request.form['name']))

            flash("Cuisine '" + name + "' added to the database!")

            return redirect(url_for('cuisines'))
        else:

            return render_template('AddCuisine.html')

@app.route('/cuisines/<int:cuisine_id>/')
def cuisine(cuisine_id):
        cuisine = RestaurantManager.getCuisine(cuisine_id)
        restaurants = RestaurantManager.getRestaurants(cuisine_id=cuisine_id)
        baseMenuItems = RestaurantManager.\
                        getBaseMenuItems(cuisine_id=cuisine_id)
        restaurantMenuItems = RestaurantManager.\
                              getRestaurantMenuItems(cuisine_id=cuisine_id)

        mostExpensiveBaseMenuItem = baseMenuItems[0]
        for item in baseMenuItems:
            if item.price > mostExpensiveBaseMenuItem.price:
                mostExpensiveBaseMenuItem = item

        mostExpensiveRestaurantMenuItem = restaurantMenuItems[0]
        for item in restaurantMenuItems:
            if item.price > mostExpensiveRestaurantMenuItem.price:
                mostExpensiveRestaurantMenuItem = item

        return render_template("Cuisine.html",
                               cuisine=cuisine,
                               mostExpensiveBaseMenuItem=mostExpensiveBaseMenuItem,
                               mostExpensiveRestaurantMenuItem=mostExpensiveRestaurantMenuItem,
                               restaurants=restaurants,
                               baseMenuItems=baseMenuItems,
                               restaurantMenuItems=restaurantMenuItems)

@app.route('/cuisines/<int:cuisine_id>/edit/')
def editCuisine(cuisine_id):
        return "edit cuisine " + str(cuisine_id)

@app.route('/cuisines/<int:cuisine_id>/delete/', methods=['GET', 'POST'])
def deleteCuisine(cuisine_id):
        cuisine = RestaurantManager.getCuisine(cuisine_id)

        if request.method == 'POST':

            redirect(url_for('cuisines'))
        else:
            return render_template("DeleteCuisine.html",
                                   cuisine=cuisine)

@app.route('/restaurants/')
def restaurants():
        restaurants = RestaurantManager.getRestaurants()
        
        return render_template("Restaurants.html",
                               restaurants=restaurants)

@app.route('/restaurants/add/', methods=['GET','POST'])
def addRestaurant():
        if request.method == 'POST':

            if request.form['cuisineID'] == 'custom':
                cuisineName = bleach.clean(request.form['customCuisine'])
                RestaurantManager.addCuisine(name=name)
                custCuisine = RestaurantManager.getCuisine(cuisineName)
                cuisine_id = custCuisine.id
            else:
                cuisine_id = request.form['cuisineID']

            RestaurantManager.addRestaurant(
                name=bleach.clean(request.form['name']),
                cuisine_id=cuisine_id
            )

            flash("restaurant '" + name + "' with cuisine '" + cuisineName +\
                "' added to the database!")

            return redirect(url_for('restaurants'))
        else:

            cuisines = RestaurantManager.getCuisines()
            return render_template('AddRestaurant.html', cuisines=cuisines)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurant(restaurant_id):
        restaurant = RestaurantManager.getRestaurant(restaurant_id)
        restaurantMenuItems = RestaurantManager.\
                              getRestaurantMenuItems(restaurant_id=restaurant_id)

        # get some stats about the restaurant
        print restaurantMenuItems
        numMenuItems = len(restaurantMenuItems)

        mostExpensiveItem = restaurantMenuItems[0]

        for item in restaurantMenuItems:
            if item.price > mostExpensiveItem.price:
                mostExpensiveItem = item

        return render_template('Restaurant.html', 
                               restaurant=restaurant, 
                               numMenuItems=numMenuItems,
                               mostExpensiveItem=mostExpensiveItem)

@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
        restaurant = RestaurantManager.getRestaurant(restaurant_id)
        cuisines = RestaurantManager.getCuisines()
        
        if request.method == 'POST':

            oldName = restaurant.name
            oldCuisineID = restauran.cuisine_id
            newName = None
            newCuisineID = None
            
            if request.form['name']:
                newName = bleach.clean(request.form['name'])
                
            if request.form['cuisineID'] != 2:
                newCuisineID = request.form['cuisineID']

            RestaurantManager.updateRestaurant(restaurant.id,
                name=newName, newCuisineID=newCuisineID)

            if newName is not None:
                flash("changed restaurant " + str(restaurant.id) + "'s name "+\
                    "from '" + oldName + "' to '" + newName + "'")

            if newCuisineID is not None:
                flash("changed restaurant " + str(restaurantMenuitem.id) + \
                    "'s cuisine from '"+ oldCuisineID + "' to '" + \
                    newCuisineID + "'")
            
            return redirect(url_for('restaurantMenu',
                                    restaurant_id=restaurant_id))
        else:

            return render_template('EditRestaurant.html',
                                   restaurant=restaurant,
                                   cuisines=cuisines)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
        restaurant = RestaurantManager.getRestaurant(restaurant_id)

        if request.method == 'POST':

            # delete restaurant

            flash("restaurant " + str(restaurant.id) + " (" + restaurant.name+\
                ") deleted from the database.")
            
            return redirect(url_for('restaurants'))
        else:   
            
            return render_template('DeleteRestaurant.html',
                                   restaurant=restaurant)

@app.route('/cuisines/<int:cuisine_id>/add/', methods=['GET','POST'])
def addBaseMenuItem(cuisine_id):
        cuisine = RestaurantManager.getCuisine(cuisine_id)

        if request.method == 'POST':

            return redirect(url_for('cuisine', cuisine_id=cuisine.id))
        else:
            return render_template('AddBaseMenuItem.html',
                                   cuisine=cuisine)

@app.route('/cuisines/<int:cuisine_id>/<int:baseMenuItem_id>/')
def baseMenuItem(cuisine_id, baseMenuItem_id):
        baseMenuItem = RestaurantManager.getBaseMenuItem(baseMenuItem_id)
        cuisine = RestaurantManager.getCuisine(baseMenuItem.cuisine_id)
        restaurantMenuItems = RestaurantManager.\
                              getRestaurantMenuItems(baseMenuItem_id=baseMenuItem.id)
        timesOrdered = 0

        return render_template("BaseMenuItem.html",
                                baseMenuItem=baseMenuItem,
                                restaurantMenuItems=restaurantMenuItems,
                                cuisine=cuisine,
                                timesOrdered=timesOrdered)

@app.route('/cuisines/<int:cuisine_id>/<int:baseMenuItem_id>/edit/',
           methods=['POST','GET'])
def editBaseMenuItem(cuisine_id, baseMenuItem_id):
        baseMenuItem = RestaurantManager.\
                       getBaseMenuItem(baseMenuItem_id=baseMenuItem_id)

        if request.method == 'POST':

            return redirect(url_for('baseMenuItem',
                                    cuisine_id=cuisine_id,
                                    baseMenuItem_id=baseMenuItem_id))
        else:
            return render_template("EditBaseMenuItem.html",
                                   baseMenuItem=baseMenuItem,
                                   cuisine_id=cuisine_id)

@app.route('/cuisines/<int:cuisine_id>/<int:baseMenuItem_id>/delete/',
           methods=['GET','POST'])
def deleteBaseMenuItem(cuisine_id, baseMenuItem_id):
        baseMenuItem = RestaurantManager.\
                       getBaseMenuItem(baseMenuItem_id=baseMenuItem_id)

        if request.method == 'POST':

            return redirect(url_for('cuisine',cuisine_id=cuisine_id))
        else:

            return render_template("DeleteBaseMenuItem.html",
                                   baseMenuItem=baseMenuItem,
                                   cuisine_id=cuisine_id)

@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurantMenu(restaurant_id):
        restaurant = RestaurantManager.getRestaurant(restaurant_id)
        restaurantMenuItems = RestaurantManager.\
            getRestaurantMenuItems(restaurant_id=restaurant_id)

        return render_template('RestaurantMenu.html',
                               restaurant=restaurant,
                               items=restaurantMenuItems)

@app.route('/restaurants/<int:restaurant_id>/menu/add/',
           methods=['GET','POST'])
def addRestaurantMenuItem(restaurant_id):
        restaurant = RestaurantManager.getRestaurant(restaurant_id)
        baseMenuItems = RestaurantManager.getBaseMenuItems()
        #### update this! 
        if request.method == 'POST':

            RestaurantManager.addRestaurantMenuItem(
                name=bleach.clean(request.form['name']),
                restaurant_id=restaurant_id,
                description=bleach.clean(request.form['description']),
                price=bleach.clean(request.form['price'])
            )

            flash("menu item '" + name + "' added to the menu!")

            return redirect(url_for('restaurantMenu',
                                    restaurant_id=restaurant_id))
        else:

            return render_template('AddRestaurantMenuItem.html',
                                   restaurant=restaurant,
                                   baseMenuItems=baseMenuItems)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:restaurantMenuItem_id>/')
def restaurantMenuItem(restaurant_id, restaurantMenuItem_id):
        restaurantMenuItem = RestaurantManager.\
                             getRestaurantMenuItem(restaurantMenuItem_id)

        restaurant = RestaurantManager.getRestaurant(restaurant_id)
        restaurantCuisineObj = RestaurantManager.getCuisine(restaurant.cuisine_id)
        restaurantCuisine = restaurantCuisineObj.name

        baseMenuItem = RestaurantManager.\
                       getBaseMenuItem(restaurantMenuItem.baseMenuItem_id)
        baseMenuItemCuisineObj = RestaurantManager.\
                                 getCuisine(baseMenuItem.cuisine_id)
        baseMenuItemCuisine = baseMenuItemCuisineObj.name

        timesOrdered = 0

        return render_template("RestaurantMenuItem.html",
                               restaurantMenuItem=restaurantMenuItem,
                               restaurant=restaurant,
                               restaurantCuisine=restaurantCuisine,
                               baseMenuItem=baseMenuItem,
                               baseMenuItemCuisine=baseMenuItemCuisine,
                               timesOrdered=timesOrdered)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:restaurantMenuItem_id>/edit/',
           methods=['GET','POST'])
def editRestaurantMenuItem(restaurant_id, restaurantMenuItem_id):

        restaurantMenuItem = RestaurantManager.\
            getRestaurantMenuItem(restaurantMenuItem_id)
        
        if request.method == 'POST':

            oldName = restaurantMenuItem.name
            oldDescription = restaurantMenuItem.description
            oldPrice = restaurantMenuItem.price
            newName = None
            newDescription = None
            newPrice = None
            
            if request.form['name']:
                newName = bleach.clean(request.form['name'])
                
            if request.form['description']:
                newDescription = bleach.clean(request.form['description'])
                
            if request.form['price']:
                newPrice = bleach.clean(request.form['price'])

            RestaurantManager.updateRestaurantMenuItem(restaurantMenuItem.id,
                name=newName, newDescription=newDescription, newPrice=newPrice)

            if newName is not None:
                flash("changed restaurant menu item " + str(restaurantMenuitem.id) + \
                    "'s name from '" + oldName + "' to '" + newName + "'")

            if newDescription is not None:
                flash("changed restaurant menu item " + str(restaurantMenuitem.id) + \
                    "'s description from '"+ oldDescription + "' to '" + \
                    newDescription + "'")

            if newPrice is not None:
                flash("changed restaurant menu item " + str(restaurantMenuitem.id) + \
                    "'s price changed from '" + oldPrice + "' to '" + \
                    newPrice + "'")
            
            return redirect(url_for('restaurantMenu',
                                    restaurant_id=restaurant_id))
        else:

            return render_template('EditRestaurantMenuItem.html',
                                   restaurant_id=restaurant_id,
                                   restaurantMenuItem=restaurantMenuItem)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:restaurantMenuItem_id>/delete/',
           methods=['GET','POST'])
def deleteRestaurantMenuItem(restaurant_id, restaurantMenuItem_id):

        restaurantMenuItem = RestaurantManager.\
                             getRestaurantMenuItem(restaurantMenuItem_id)

        if request.method == 'POST':

            """update this
            session = session.getRestaurantDBSession()

            itemToDelete = session.query(RestaurantMenuItem).\
                           filter_by(id=RestaurantMenuItem_id).one()
            session.delete(itemToDelete)
            session.commit()
            session.close()
            flash("menu item " + str(itemToDelete.id) + " (" + \
                  itemToDelete.name + ") deleted from the menu and database")
            """
            return redirect(url_for('restaurantMenu',
                                    restaurant_id=restaurant_id))
        else:
            return render_template('DeleteRestaurantMenuItem.html',
                                   restaurant_id=restaurant_id,
                                   restaurantMenuItem=restaurantMenuItem)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
