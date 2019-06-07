# IMDB-App

@ZeoAgency IMDB App Challenge with Django, Dgraph and Auth0

## Auth0
- [Auth0 Tutorial](https://auth0.com/blog/django-tutorial-building-and-securing-web-applications/)
- [Dgraph Tutorial](https://docs.dgraph.io/)

## Requirements.txt
    Django~=2.0.6
    python-jose
    social-auth-app-django
    pydgraph
    nltk
    snowballstemmer

## Initial Requirements
- Complete Auth0 and Dgraph tutorial
- Understand Auth0 and Dgraph
- Add the script to your auth0 rules of dashboard (Auth0 Tutorial Link includes this)
```
function (user, context, callback) {
  // role should only be set to verified users.
  if (!user.email || !user.email_verified) {
    return callback(null, user, context);
  }

  user.app_metadata = user.app_metadata || {};

  // set the 'admin' role to the following user
  const adminEmail = '<YOUR-OWN-EMAIL-ADDRESS>';
  user.app_metadata.role = user.email === adminEmail ? 'admin' : 'user';

  auth0.users.updateAppMetadata(user.user_id, user.app_metadata).then(() => {
    context.idToken['https://django-webapp/role'] = user.app_metadata.role;
    callback(null, user, context);
  }).catch((err) => {
    callback(err);
  });
}
```
- Constuct your Dgraph IMDB Database ([Load IMDB Database To Dgraph](https://tour.dgraph.io/moredata/1/))
- Find **# FILL IT** comments in code and change some informations with yours

## Setup Repo
```
git clone https://github.com/muhammet-mucahit/IMDB-App.git
cd IMDB-App
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Tasks

- [x] Task 0. Login, signup, admin panel and email verification with Auth0.

- [x] Task 1. (Basic Details Query) List the details of cast and director of the film called "X-Men 2".

- [x] Task 2. (Group by and Aggregate) List all genre values ​​in the system and list the average of years they were released.

- [x] Task 3. (Get Details from App and Query) List actors and movies which have the same name as the logged-in user's name or surname.

- [x] Task 4. (Basic Query + Full Text + Aggregation of Strings) Find the films directed by "Bryan Singer" and make full text search to list the most important actors in the films.

- [x] Task 5. (Python Text Operation + Query) Clear the suffixes of words in the "Atatürk’ün Gençliğe Hitabesi" by using NLTK and Turkish Stemming. Then list all movie names that contain these words, even if they are additional.

- [x] Task 6. (Complex Query + Regex + Extra Iteration) List the names of the actors who played the most in the films which include "man" in their names but not "woman" and the list the other films in which they acted.

- [x] Task 7. (Getting Input from User to Run Basic Query) List films made before 2013 related to any genre value that user will provide.

- [x] Task 8. (Advanced Query Builder to Run Basic Queries)

## Screenshots

![Dgraph](https://github.com/muhammet-mucahit/IMDB-App/blob/master/Images/dgraph.png)

![Home Without Login](https://github.com/muhammet-mucahit/IMDB-App/blob/master/Images/home_without_login.png)

![Login](https://github.com/muhammet-mucahit/IMDB-App/blob/master/Images/login.png)

![Home With Login](https://github.com/muhammet-mucahit/IMDB-App/blob/master/Images/home_with_login.png)

![Profile](https://github.com/muhammet-mucahit/IMDB-App/blob/master/Images/profile.png)

![Admin](https://github.com/muhammet-mucahit/IMDB-App/blob/master/Images/admin.png)