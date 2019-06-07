from django.shortcuts import render
import json
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.http import HttpResponseRedirect
from string import punctuation, digits
from snowballstemmer import stemmer

from .models import Movie

import pydgraph

# Create a client stub.
def create_client_stub():
    return pydgraph.DgraphClientStub('YOUR_DGRAPH_IP_AND_PORT (127.0.0.1:9080)')
    # FILL IT

# Create a client.
def create_client(client_stub):
    return pydgraph.DgraphClient(client_stub)


def close_client_stub(client_stub):
    client_stub.close()


def index(request):
    movies = Movie.objects.all()

    context = {
        'movies': movies,
    }
    return render(request, 'imdbapp/index.html', context)


@login_required
def task1(request):
    client_stub = create_client_stub()
    client = create_client(client_stub)

    query = """query all($a: string) {all(func: eq(name@., $a))
      {
          name@.
          starring {
            performance.actor {
              expand(_all_)
            }
          }
          ~director.film {
            expand(_all_)
          }
      }
    }"""
    variables = {'$a': "X-Men 2"}

    res = client.txn(read_only=True).query(query, variables=variables)
    ppl = json.loads(res.json)
    movies = ppl['all']

    movie = movies[0]["name@."]
    director = movies[0]["~director.film"][0]["name@en"]
    starring = list()

    for s in movies[0]["starring"]:
        starring.append(s["performance.actor"][0]["name@en"])

    context = {
        'movie': movie,
        'director': director,
        'starring': starring,
    }

    close_client_stub(client_stub)
    return render(request, 'imdbapp/task1.html', context)


@login_required
def task2(request):
    client_stub = create_client_stub()
    client = create_client(client_stub)

    query = """{
  var(func: has(initial_release_date)) @groupby(genre) {
      a as min(initial_release_date)
  }

  byGenre(func: uid(a), orderdesc: val(a)) {
    name@en
    avg_release_year : val(a)
  }
}"""

    res = client.txn(read_only=True).query(query)

    ppl = json.loads(res.json)
    genres_json = ppl['byGenre']

    genres = dict()

    for genre in genres_json:
        genres[genre["name@en"]] = str(genre["avg_release_year"]).split("-")[0]

    context = {
        'genres': genres,
    }

    close_client_stub(client_stub)
    return render(request, 'imdbapp/task2.html', context)


@login_required
def task3(request):
    client_stub = create_client_stub()
    client = create_client(client_stub)
    query = """query all($user: string)
	{
		all(func: anyofterms(name@., $user)) @cascade
		{
			name@.
			actor.film {
				performance.film {
					name@.
				}
			}
		}
	}"""

    user = request.user
    variables = {'$user': user.first_name + " " + user.last_name}

    res = client.txn(read_only=True).query(query, variables=variables)
    ppl = json.loads(res.json)
    all_json = ppl['all']

    actor_dict = dict()

    for one in all_json:
        movies = list()
        for film in one["actor.film"]:
            movies.append(film["performance.film"][0]["name@."])
        actor_dict[one["name@."]] = movies

    context = {
        'actor_dict': actor_dict,
    }

    close_client_stub(client_stub)
    return render(request, 'imdbapp/task3.html', context)


@login_required
def task4(request):
    client_stub = create_client_stub()
    client = create_client(client_stub)
    query = """{
  var(func: alloftext(name@., "Bryan Singer"))
  {
    director.film {
      starring @groupby(performance.actor) {
        a as count(uid)
      }
    }
  }

  byActor(func: uid(a), orderdesc: val(a), first: 15) {
    name@en
    film_num : val(a)
  }
}"""
    res = client.txn(read_only=True).query(query)
    ppl = json.loads(res.json)
    actors = ppl['byActor']

    actors_dict = dict()

    for actor in actors:
        actors_dict[actor["name@en"]] = actor["film_num"]

    context = {
        'actors_dict': actors_dict,
    }

    close_client_stub(client_stub)
    return render(request, 'imdbapp/task4.html', context)


@login_required
def task5(request):
    metin = """
        Ey Türk gençliği!

        Birinci vazifen, Türk istiklâlini, Türk Cumhuriyetini, ilelebet, muhafaza ve müdafaa etmektir. 

        Mevcudiyetinin ve istikbalinin yegâne temeli budur. Bu temel, senin, en kıymetli hazinendir. 

        İstikbalde dahi, seni, bu hazineden, mahrum etmek isteyecek, dahilî ve haricî, bedhahların olacaktır.

        Bir gün, istiklâl ve cumhuriyeti müdafaa mecburiyetine düşersen, vazifeye atılmak için, içinde bulunacağın vaziyetin imkân ve şerâitini düşünmeyeceksin!

        Bu imkân ve şerâit, çok nâmüsait bir mahiyette tezahür edebilir. 

        İstiklâl ve cumhuriyetine kastedecek düşmanlar, bütün dünyada emsali görülmemiş bir galibiyetin mümessili olabilirler.

        Cebren ve hile ile aziz vatanın, bütün kaleleri zaptedilmiş, bütün tersanelerine girilmiş, bütün orduları dağıtılmış ve memleketin her köşesi bilfiil işgal edilmiş olabilir.

        Bütün bu şerâitten daha elîm ve daha vahim olmak üzere, memleketin dahilinde, iktidara sahip olanlar gaflet ve dalâlet ve hattâ hıyanet içinde bulunabilirler.

        Hattâ bu iktidar sahipleri şahsî menfaatlerini, müstevlilerin siyasi emelleriyle tevhit edebilirler. 

        Millet, fakr-u-zaruret içinde harap ve bîtap düşmüş olabilir.

        Ey Türk istikbalinin evlâdı! İşte, bu ahval ve şerâit içinde dahi, vazifen; Türk İstiklâl ve cumhuriyetini kurtarmaktır!

        Muhtaç olduğun kudret, damarlarındaki asîl kanda, mevcuttur!
    """

    cevirici = str.maketrans('', '', punctuation)
    metin = metin.translate(cevirici)
    cevirici = str.maketrans('', '', digits)
    metin = metin.translate(cevirici)
    metin = metin.lower()

    kokbul1 = stemmer('turkish')

    client_stub = create_client_stub()
    client = create_client(client_stub)
    query = """query all($words: string = "ey türk gençlik b") 
    {
      all(func: anyoftext(name@., $words)) @filter(has(starring))
      {
        name@.
        }
    }"""

    variables = {'$words': " ".join(kokbul1.stemWords(metin.split()))}
    res = client.txn(read_only=True).query(query, variables=variables)
    ppl = json.loads(res.json)
    all = ppl['all']
    movies = list()

    for mov in all:
            movies.append(mov["name@."])

    context = {
        'movies': movies,
    }

    close_client_stub(client_stub)
    return render(request, 'imdbapp/task5.html', context)


@login_required
def task6(request):
    client_stub = create_client_stub()
    client = create_client(client_stub)
    query = """{
  movie as var(func: has(name@.)) @filter(regexp(name@en, /^.*man.*$/i) and not regexp(name@en, /^.*woman.*$/i)) @cascade {
    starring @groupby(performance.actor) {
      id as count(uid)
    }
  }

  byStar(func: uid(id), orderdesc: val(id), first: 10) @cascade {
    name@.
    actor.film {
      performance.film @filter(not uid(movie)) {
         name@.
      }
    }
    film_num : val(id)
  }
}"""
    res = client.txn(read_only=True).query(query)
    ppl = json.loads(res.json)
    stars = ppl['byStar']
    stars_dict = dict()

    for star in stars:
        movies = list()
        for film in star["actor.film"]:
            movies.append(film["performance.film"][0]["name@."])
        stars_dict[star["name@."]] = movies

    context = {
        'stars_dict': stars_dict,
    }

    close_client_stub(client_stub)
    return render(request, 'imdbapp/task6.html', context)


@login_required
def task7(request):
    client_stub = create_client_stub()
    client = create_client(client_stub)

    query = """ {
		var(func: has(initial_release_date)) @groupby(genre) {
			a as count(uid)
		}
		byGenre(func: uid(a), orderdesc: val(a)) {
			name@en
		}
	}"""

    res = client.txn(read_only=True).query(query)
    ppl = json.loads(res.json)
    genres_json = ppl['byGenre']
    genres = list()

    for g in genres_json:
        genres.append(g["name@en"])

    if request.method == 'POST':
        genre = request.POST.get('genres', None)

        query = """query all($genre: string) {
			all(func: eq(name@., $genre)) @cascade
			{
				name@.
				~genre @filter(lt(initial_release_date, "2013")) {
					name@.
				}
			}
    	}"""

        variables = {'$genre': genre}
        res = client.txn(read_only=True).query(query, variables=variables)
        ppl = json.loads(res.json)
        all = ppl['all']
        movies = list()
        category = all[0]["name@."]
		
        for mov in all[0]["~genre"]:
        	movies.append(mov["name@."])
			
        context = {
            'movies': movies,
            'genres': genres,
            'category': category,
        }
    else:
        context = {
            'genres': genres,
        }

    close_client_stub(client_stub)
    return render(request, 'imdbapp/task7.html', context)

def query_data(client, var_genre, var_year, var_director, var_star):
    query = """query all($genre: string, $director: string, $star: string, $year: int, $next_year: int) {   
    var(func: eq(name@., $genre)) @cascade
    {
        name@.
        GENRE as ~genre
    }
        
    YEAR as var(func: ge(initial_release_date, $year)) @filter(lt(initial_release_date, $next_year)) @cascade
        
    var(func: eq(name@., $director)) @cascade {
        name@.
        DIRECTOR as director.film
    }
    
    var(func: eq(name@., $star)) @cascade {
        name@.
        actor.film {
        STAR as performance.film
        }
    }
    
    all(func: has(name@.)) @filter(uid(GENRE) and uid(STAR) and uid(YEAR) and uid(DIRECTOR)) {
        name@.
        initial_release_date
        genre {
        name@.
        }
        starring {
        performance.actor {
            name@.
        }
        }
    }
    }"""
    variables = {
        '$genre': var_genre,
        '$year': var_year,
        '$next_year': str(int(var_year) + 1),
        '$director': var_director,
        '$star': var_star,
    }
    res = client.txn(read_only=True).query(query, variables=variables)
    ppl = json.loads(res.json)
    return ppl["all"]

@login_required
def task8(request):
    client_stub = create_client_stub()
    client = create_client(client_stub)

    if request.method == 'POST':
        genre = request.POST.get('genre', None)
        year = request.POST.get('year', None)
        director = request.POST.get('director', None)
        star = request.POST.get('star', None)

        genres_json = query_data(client, genre, year, director, star)
            
        context = {
            'movies': json.dumps(genres_json, sort_keys=True, indent=4, separators=(',', ': ')),
        }
    else:
        context = {
            'movies': None,
        }

    close_client_stub(client_stub)
    return render(request, 'imdbapp/task8.html', context)

@login_required
def profile(request):
    user = request.user
    auth0user = user.social_auth.get(provider='auth0')
    userdata = {
        'user_id': auth0user.uid,
        'name': user.first_name,
        'picture': auth0user.extra_data['picture']
    }

    return render(request, 'imdbapp/profile.html', {
        'auth0User': auth0user,
        'userdata': json.dumps(userdata, indent=4)
    })


def logout(request):
    django_logout(request)
    domain = 'dev-uu11qs8p.auth0.com'
    client_id = 'NeKNCgWz77crLY17j3fh4KKbYii3D8kj'
    # After logout return to the url
    return_to = 'YOUR_AUTH0_ALLOWED_LOGOUT_URL (127.0.0.1:8000)'
    # FILL IT
    
    return HttpResponseRedirect(f'https://{domain}/v2/logout?client_id={client_id}&returnTo={return_to}')
